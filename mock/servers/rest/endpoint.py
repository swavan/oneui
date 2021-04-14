import os
import time
from json.decoder import JSONDecodeError
from typing import List, Dict, Union

import requests.exceptions
import validators
from starlette.endpoints import HTTPEndpoint
from starlette.requests import Request
from starlette.responses import Response, RedirectResponse, FileResponse
from validators import ValidationFailure

from mock.modals import Response as SwaVanResponse, Header
from mock.servers.rest.helper import rule_matcher, make_http_request, curl_handler
from mock.servers.rest.modal import SwaVanHttpResponse, RuleStatus, RequestModal
from shared.helper import response_modifier, filter_by_code, code_to_text
from shared.recorder import SwaVanLogRecorder


class SwaVanRestEndpoint(HTTPEndpoint):
    __server = "swavan"

    async def get(self, request: Request):
        SwaVanLogRecorder.send_log(f"Get request made")
        return await self.handler(request, "get")

    async def post(self, request):
        return await self.handler(request, "post")

    async def put(self, request):
        return await self.handler(request, "put")

    async def delete(self, request):
        return await self.handler(request, "delete")

    async def patch(self, request):
        return await self.handler(request, "patch")

    async def handler(self, request: Request, method: str) -> Response:
        _ = self.__server
        __response = Response(status_code=404)
        _endpoint_method_data = request.app.state.mock.get(request.url.path)
        _header = dict(zip(request.headers.keys(), request.headers.values()))
        _query = dict(zip(request.query_params.keys(), request.query_params.values()))
        _body = {}
        __raw_body = await request.body()
        try:
            _form = await request.form()
            _keys = _form.keys()
            _values = _form.values()
            _body = dict(zip(_keys, _values))
        finally:
            pass

        try:
            _body = await request.json()
        except JSONDecodeError:
            pass

        if _endpoint_method_data:
            _endpoint: Dict = _endpoint_method_data.get(method, {'responses': [], 'delay': 0})
            _responses: List[SwaVanResponse] = _endpoint.get('responses', '')
            for _response in _responses:
                _matched_rules = rule_matcher(_response.rules, _header, _query, _body)
                _and_rules = _response.connector.lower() == "and" and all(_matched_rules)
                _or_rules = _response.connector.lower() == "or" and any(_matched_rules)
                _have_rules = len(_response.rules) != 0
                _and_or_rules_and_has_rules = _and_rules or _or_rules or not _have_rules
                _and_or_rule_matched = RuleStatus.Matched if _and_or_rules_and_has_rules else RuleStatus.Unmatched
                _code_rule_matched = filter_by_code(
                    _response.filter_by,
                    query=_query,
                    headers=_header,
                    body=_body,
                    rule_status=_and_or_rule_matched) if _response.filter_by else _and_or_rule_matched
                if _code_rule_matched == RuleStatus.Matched:
                    if _response.redirect:
                        try:
                            __response_data = await SwaVanRestEndpoint.proxy_request(
                                _response,
                                method,
                                request.app.state.proxies)
                            if __response_data:
                                __response = __response_data
                        except requests.exceptions.ConnectionError as err:
                            __response.status_code = 500
                            __response.body = b"Unable to redirect request, please check the log message"
                            SwaVanLogRecorder.send_log(f"Unable to redirect request {err}")
                    elif _response.content_path:
                        __response = await SwaVanRestEndpoint.file_response(_response)
                    else:
                        __response = await SwaVanRestEndpoint.make_response(_response)
                    break
            sleeping_period = _endpoint.get('delay') or request.app.state.delay or 0
            time.sleep(sleeping_period)

        return __response

    @classmethod
    def header(cls, __headers: List[Header]) -> Dict:
        _header_keys = list(map(lambda x: x.key, __headers))
        _header_values = list(map(lambda x: x.value, __headers))
        return dict(zip(_header_keys, _header_values))

    @classmethod
    async def make_response(cls, _response: SwaVanResponse) -> Response:
        return Response(content=_response.content, status_code=_response.status, headers=cls.header(_response.headers))

    @classmethod
    async def redirect_response(cls, _redirect: str) -> Response:
        return RedirectResponse(url=_redirect)

    @classmethod
    async def file_response(cls, _response: SwaVanResponse) -> Response:
        __path = os.path.join(_response.content_path)

        return FileResponse(path=__path, status_code=_response.status, headers=cls.header(_response.headers))

    @classmethod
    async def proxy_request(cls, _response: SwaVanResponse, method_name: str, proxies: Dict) -> Union[Response, None]:
        _mock_header = cls.header(_response.headers)
        _redirect = code_to_text(_response.redirect)
        _response_handler = None
        try:
            if validators.url(_redirect):
                if not _response.is_modifier_active:
                    return await cls.redirect_response(_redirect)

                _response_handler = make_http_request(RequestModal(
                    url=_redirect,
                    method=method_name,
                    proxies=proxies))
        except ValidationFailure as _:
            pass

        if _redirect.startswith("curl "):
            _request_modal = curl_handler(_redirect)
            _request_modal.proxies = proxies
            _response_handler = make_http_request(_request_modal)

        if _response.is_modifier_active and _response_handler:
            altered: SwaVanHttpResponse = response_modifier(_response.modifier, _response_handler)
            if altered:
                modified_response = Response(
                    content=altered.body,
                    headers=_mock_header,
                    status_code=altered.status)
                modified_response.headers["content-length"] = "{}".format(len(altered.body))
                return modified_response
        return Response(
            content=_response_handler.content,
            headers=_mock_header,
            status_code=_response_handler.status_code)
