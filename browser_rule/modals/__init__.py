from dataclasses import dataclass
from enum import Enum
from typing import List


class SourceTypes(Enum):
    Server = 's'
    Url = 'u'
    Path = 'p'


class DataSourceTypes(Enum):
    Redirect = 'r'
    Mock = 'd'
    Block = 'b'


class BrowserRuleHttpMethod(Enum):
    All = 'al'
    Get = 'ge'
    Post = 'po'
    Put = 'pu'
    Delete = 'de'
    Patch = 'pa'


class BrowserRuleFilterBy(Enum):
    Query = 'q'
    Header = 'h'
    Body = 'b'


class BrowserRuleOperator(Enum):
    Equals = 'e'
    Contain = 'c'
    Wildcard = 'w'
    Prefix = 'p'
    Suffix = 's'


@dataclass
class BrowserRuleFilter:
    filter_by: BrowserRuleFilterBy
    key: str
    value: str


@dataclass
class BrowserRuleMockHeader:
    key: str
    value: str


@dataclass
class BrowserRuleMock:
    content: str
    link: str
    key: str
    status: str
    header: List[BrowserRuleMockHeader]
    action_perform: str


@dataclass
class BrowserRuleResponse:
    data_source_type: DataSourceTypes
    data: BrowserRuleMock
    http_method: BrowserRuleHttpMethod
    filters: List[BrowserRuleFilter]
    is_logic_enabled: bool
    cloud_store_permission: str
    tags: str
    delay: int


@dataclass
class BrowserRule:
    name: str
    description: str
    source_type: SourceTypes
    operator: BrowserRuleOperator
    source: str
    is_enabled: bool
    is_favorite: bool
    responses: List[BrowserRuleResponse]
