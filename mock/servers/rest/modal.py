from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Union, Tuple


class RuleStatus(Enum):
    Matched = True
    Unmatched = False


@dataclass
class SwaVanHttpResponse:
    status: int
    body: Any
    headers: Dict


@dataclass
class SwaVanHttpRequest:
    body: Any
    headers: Dict
    query: Dict


@dataclass
class SwaVanHttp:
    response: Union[SwaVanHttpResponse, None] = None
    request: Union[SwaVanHttpRequest, None] = None
    rule_status: RuleStatus = RuleStatus.Unmatched


@dataclass
class RequestModal:
    method: str = 'get'
    url: str = ''
    data: Any = None
    headers: Dict = field(default_factory=dict)
    cookies: Dict = field(default_factory=dict)
    verify: Any = None
    auth: Tuple = field(default_factory=tuple)
    proxies: Dict = field(default_factory=dict)
