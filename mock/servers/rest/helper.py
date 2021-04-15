import errno
import socket
from dataclasses import asdict
from typing import Dict, List, Any

from requests import Response, request, HTTPError
from uncurl import parse_context

from mock.modals import Rule, Endpoint
from mock.servers.rest.modal import RequestModal
from shared.comparable import SwaVanComparable
from shared.recorder import SwaVanLogRecorder


def match_header(_rule: Rule, _headers: Dict):
    return SwaVanComparable.action(
        _rule.operator,
        _headers.get(_rule.field),
        _rule.value)


def match_query(_rule: Rule, _query: Dict):
    return SwaVanComparable.action(
        _rule.operator,
        _query.get(_rule.field),
        _rule.value)


def match_body(_rule: Rule, _data) -> bool:
    _operator, _value = None, None
    _fields = _rule.field.split(".")
    try:
        for field in _fields:
            if isinstance(_data, list) and len(_data) > 0:
                _data = _data[int(field)]
            elif isinstance(_data, dict):
                _data = _data.get(field, None)
            _operator, _value = _rule.operator, _rule.value
        return SwaVanComparable.action(_rule.operator, _data, _rule.value)
    except Exception as err:
        SwaVanLogRecorder.send_log(f"Error occurred while comparing with body: {err}")
        return False


def route_collector(prefix: str, endpoints: List[Endpoint]) -> dict:
    _endpoints = {}
    for endpoint in endpoints:
        if endpoint.is_active:
            _url_to_method = _endpoints.get(endpoint.url, {})
            _method_to_response = _url_to_method.get(endpoint.http_method, {
                'responses': [],
                'delay': endpoint.delay})

            _method_to_response["responses"].extend(endpoint.responses)
            _method_to_response["responses"] = list(filter(lambda x: x.is_active, _method_to_response["responses"]))
            _url_to_method.update({endpoint.http_method.lower(): _method_to_response})

            _endpoint = {f"{prefix.lower()}{endpoint.url}": _url_to_method}
            _endpoints.update(_endpoint)
    return _endpoints


def is_and(x):
    return x == "&&"


def is_or(x):
    return x == "||"


def is_query(x):
    return x.lower() == "query"


def is_header(x):
    return x.lower() == "header"


def is_body(x):
    return x.lower() == "body"


def rule_matcher(_rules: List[Rule], headers: Dict, queries: Dict, body: Any) -> List[bool]:
    def __query_match(x): return is_query(x.filter_by) and match_query(x, queries)

    def __header_match(x): return is_header(x.filter_by) and match_header(x, headers)

    def __body_match(x): return is_body(x.filter_by) and match_body(x, body)

    def __all_match(x): return __query_match(x) or __header_match(x) or __body_match(x)

    return [__all_match(_rule) for _rule in _rules]


def curl_handler(command: str) -> RequestModal:
    try:
        removed_unwanted = command.replace("\\", "")
        _request = parse_context(f"{removed_unwanted}")
        return RequestModal(
            method=_request.method,
            url=_request.url,
            data=_request.data or None,
            headers=dict(zip(_request.headers.keys(), _request.headers.values())),
            cookies=dict(zip(_request.cookies.keys(), _request.cookies.values())),
            verify=True,
            auth=_request.auth
        )
    except Exception as err:
        SwaVanLogRecorder.send_log(f"Unable to parse the cURL {err}")


def make_http_request(params: RequestModal) -> Response:
    _params = asdict(params)
    try:
        return request(**_params)
    except HTTPError as http_err:
        SwaVanLogRecorder.send_log(f'HTTP error occurred: {http_err}')
    except Exception as err:
        SwaVanLogRecorder.send_log(f'Other error occurred: {err}')


def port_is_busy(host: str, port: int) -> bool:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind((host, port))
        return False
    except socket.error as e:
        if e.errno == errno.EADDRINUSE:
            return True
        else:
            return False
    finally:
        s.close()
