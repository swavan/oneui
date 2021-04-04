from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Union


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
