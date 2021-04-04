import os
from json.decoder import JSONDecodeError
from typing import List, Dict

from starlette.endpoints import HTTPEndpoint
from starlette.requests import Request
from starlette.responses import Response, RedirectResponse, FileResponse

from mock.modals import Response as SwaVanResponse, Header
from mock.servers.rest.helper import rule_matcher, proxy_request
from mock.servers.rest.modal import SwaVanHttpResponse, RuleStatus
from shared.helper import response_modifier, filter_by_code


class SwaVanRestEndpoint(HTTPEndpoint):
    __server = "swavan"

    async def get(self, request: Request):
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
            _responses: List[SwaVanResponse] = _endpoint['responses']
            for _response in _responses:
                _matched_rules = rule_matcher(_response.rules, _header, _query, _body)
                _and_rules = _response.connector.lower() == "and" and all(_matched_rules)
                _or_rules = _response.connector.lower() == "or" and any(_matched_rules)

                _and_or_rule_matched = RuleStatus.Matched if _and_rules or _or_rules else RuleStatus.Unmatched

                _code_rule_matched = filter_by_code(
                    _response.filter_by,
                    query=_query,
                    headers=_header,
                    body=_body,
                    rule_status=_and_or_rule_matched) if _response.filter_by else _and_or_rule_matched

                if _code_rule_matched == RuleStatus.Matched:
                    if _response.redirect and _response.modifier:
                        __response = await SwaVanRestEndpoint.proxy_request(
                            _response,
                            _header,
                            method,
                            _query,
                            _body, request.cookies)
                    elif _response.redirect:
                        __response = await SwaVanRestEndpoint.redirect_response(_response)
                    elif _response.content_path:
                        __response = await SwaVanRestEndpoint.file_response(_response)
                    else:
                        __response = await SwaVanRestEndpoint.make_response(_response)
                    break
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
    async def redirect_response(cls, _response: SwaVanResponse) -> Response:
        return RedirectResponse(_response.redirect, _response.status)

    @classmethod
    async def file_response(cls, _response: SwaVanResponse) -> Response:
        __path = os.path.join(_response.content_path)
        return FileResponse(path=__path, status_code=_response.status, headers=cls.header(_response.headers))

    @classmethod
    async def proxy_request(cls, _response: SwaVanResponse,
                            request_header: Dict,
                            method_name: str,
                            queries: Dict,
                            body: Dict,
                            cookies: Dict
                            ) -> Response:
        _mock_header = cls.header(_response.headers)
        _original_header = request_header
        _headers = {**_mock_header, **_original_header}
        proxy_response = proxy_request(_response.redirect, method_name, queries, body, _headers, cookies)
        if proxy_response:
            altered: SwaVanHttpResponse = response_modifier(_response.modifier, proxy_response)
            if altered:
                modified_response = Response(
                    content=altered.body,
                    status_code=altered.status,
                    headers=altered.headers)
                modified_response.headers["content-length"] = "{}".format(len(altered.body))
                return modified_response
        return Response(content=proxy_response.text, status_code=proxy_response.status_code)
