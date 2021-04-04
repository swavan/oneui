import json
from dataclasses import asdict
from typing import List, Dict, Union

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QToolButton, QApplication
from requests import Response

from mock.servers.rest.modal import SwaVanHttpResponse, SwaVanHttp, SwaVanHttpRequest, RuleStatus
from mock.services.endpoint import EndpointService


def string_func_wrapper(code: str, func_name):
    return f'''
{code}
try:
    {func_name}()
except Exception as e:
    print(e)
    '''


def mutable_response(response: Response) -> SwaVanHttpResponse:
    return SwaVanHttpResponse(
        status=response.status_code,
        body=response.content,
        headers=dict(zip(response.headers.keys(), response.headers.values())),
    )


def response_modifier(function_body, response: Response) -> Union[SwaVanHttpResponse, None]:
    _custom = code_to_text(function_body)
    if 'def swavan_response() -> None:' in _custom:
        _mutable_response = mutable_response(response=response)
        _func_literal = string_func_wrapper(_custom, 'swavan_response')
        exec(_func_literal, {"swavan": SwaVanHttp(response=_mutable_response)}, {"Dict": Dict, 'json': json})
        return _mutable_response
    return None


def filter_by_code(function_body, query: Dict, headers: Dict, body: any, rule_status: RuleStatus) -> RuleStatus:
    _request = SwaVanHttpRequest(body=body, headers=headers, query=query)
    _custom = code_to_text(function_body)
    if 'def swavan_rule() -> None:' in _custom:
        _func_literal = string_func_wrapper(_custom, 'swavan_rule')
        _swavan = {"swavan": SwaVanHttp(request=_request, rule_status=rule_status),"RuleStatus": RuleStatus}
        try:
            exec(_func_literal, _swavan, {
                "SwaVanHttp": SwaVanHttp,
                "Dict": Dict,
                "json": json,
                "bool": bool,
                "RuleStatus": RuleStatus})
        finally:
            pass
        if isinstance(_swavan, dict) and "swavan" in _swavan:
            __swavan: SwaVanHttp = _swavan.get("swavan")
            return __swavan.rule_status
        return RuleStatus.Unmatched


def text_to_code(text: str) -> List[int]:
    return [ord(code) for code in text]


def code_to_text(codes: List[int]) -> str:
    return "".join([chr(code) for code in codes])


def convert_to_function(code: str):
    return eval(code)


def custom_callable(codes: List[int]):
    _code_text = code_to_text(codes)
    return convert_to_function(_code_text)


def add_or_button(button: QToolButton):
    if button.text().lower() == "and":
        button.setText("or")
        button.setIcon(QIcon("assets/images/icons/or.ico"))
    elif button.text().lower() == "or":
        button.setText("and")
        button.setIcon(QIcon("assets/images/icons/and.ico"))


def copy_endpoint(endpoint_ids: List[str]):
    _endpoints = EndpointService.load_by_ids(endpoint_ids)
    QApplication.clipboard().setText(json.dumps([asdict(endpoint) for endpoint in _endpoints]))


def do_nothing():
    pass
