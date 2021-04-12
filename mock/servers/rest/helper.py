from typing import Dict, List, Any, Union
from urllib.parse import urlencode

import requests
from requests import Response

from mock.modals import Rule, Endpoint
from shared.comparable import SwaVanComparable


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


def match_body(_rule: Rule, _data):
    for field in _rule.field.split("."):
        if isinstance(_data, list) and len(_data) > 0:
            _data = _data[int(field)]
        elif isinstance(_data, dict):
            _data = _data.get(field, None)
        elif not isinstance(_data, dict):
            return SwaVanComparable.action(_rule.operator, _data, _rule.value)


def route_collector(endpoints: List[Endpoint]) -> dict:
    _endpoints = {}
    for endpoint in endpoints:
        if endpoint.is_active:
            _url_to_method = _endpoints.get(endpoint.url.lower(), {})
            _method_to_response = _url_to_method.get(endpoint.http_method,  {
                'responses': [],
                'delay':  endpoint.delay})

            _method_to_response["responses"].extend(endpoint.responses)

            _url_to_method.update({endpoint.http_method.lower(): _method_to_response})

            _endpoint = {endpoint.url.lower(): _url_to_method}
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


def proxy_request(
        url,
        method="",
        queries: Dict = {},
        body: Dict = None,
        headers: Dict = None,
        cookies: Dict = None,
        proxies: Dict = None) -> Union[Response, None]:
    _params = {
        'url': url,
        'proxies': proxies,
        'cookies': cookies,
        'headers': headers,
        'data': body,
        'params': {'q': urlencode(queries)}
    }
    if method == "get":
        return requests.get(**_params)
    if method == "post":
        return requests.post(**_params)
    if method == "delete":
        return requests.delete(**_params)
    if method == "put":
        return requests.put(**_params)
    if method == "patch":
        return requests.patch(**_params)
    return None
