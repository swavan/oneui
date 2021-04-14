import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Dict


class HttpMethod(Enum):
    Post = 'post'
    Put = 'put'
    Delete = 'Delete'
    Get = 'get'
    Option = 'option'
    Patch = 'patch'


@dataclass
class Header:
    id: str = str(uuid.uuid4())
    key: str = ""
    value: str = ""
    created_at: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @classmethod
    def from_dict(cls, header: Dict): return cls(
        id=header.get("id") or str(uuid.uuid4()),
        key=header.get("key", ""),
        value=header.get("value", ""),
        created_at=header.get("created_at"))


@dataclass
class Rule:
    id: str = str(uuid.uuid4())
    filter_by: str = ""
    field: str = ""
    operator: str = ""
    value: str = ""
    created_at: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @classmethod
    def from_dict(cls, rule: Dict):
        return cls(
            id=rule.get("id") or str(uuid.uuid4()),
            filter_by=rule.get("filter_by", ""),
            field=rule.get("field", ""),
            operator=rule.get("operator", ""),
            value=rule.get("value", ""),
            created_at=rule.get("created_at"))


@dataclass
class Response:
    id: str = str(uuid.uuid4())
    status: int = 200
    content: str = ""
    content_path: str = ""
    redirect: List[int] = field(default_factory=list)
    is_modifier_active: bool = False
    modifier: List[int] = field(default_factory=list)
    is_active: bool = True
    headers: List[Header] = field(default_factory=list)
    rules: List[Rule] = field(default_factory=list)
    connector: str = "and"
    note: str = ""
    filter_by: List[int] = field(default_factory=list)
    created_at: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @classmethod
    def from_dict(cls, response: Dict):
        return cls(
            id=response.get("id") or str(uuid.uuid4()),
            status=int(response.get("status") or 200),
            content=response.get("content", ""),
            content_path=response.get("content_path", ""),
            redirect=response.get("redirect", ""),
            is_modifier_active=response.get("is_modifier_active", False),
            modifier=response.get("modifier", []),
            headers=[Header.from_dict(header) for header in response.get("headers", [])],
            rules=[Rule.from_dict(rule) for rule in response.get("rules", [])],
            connector=response.get("connector", "and"),
            note=response.get("note", ""),
            filter_by=response.get("filter_by", []),
            created_at=response.get("created_at"))


@dataclass
class Endpoint:
    id: str = str(uuid.uuid4())
    pid: str = str(uuid.uuid4())
    http_method: str = ""
    url: str = ""
    delay: int = 0
    is_active: bool = True
    responses: List[Response] = field(default_factory=list)
    created_at: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @classmethod
    def from_dict(cls, endpoint: Dict):
        return cls(
            id=endpoint.get("id") or str(uuid.uuid4()),
            pid=endpoint.get("pid"),
            http_method=endpoint.get("http_method", "Get"),
            url=endpoint.get("url", ""),
            delay=int(endpoint.get("delay", 0)),
            is_active=endpoint.get("is_active", True),
            responses=[Response.from_dict(response) for response in endpoint.get("responses", [])],
            created_at=endpoint.get("created_at"))


@dataclass
class Mock:
    id: str = str(uuid.uuid4())
    name: str = ""
    port: str = "4001"
    prefix: str = ""
    delay: int = 0
    enable_https: bool = False
    ssl_key_file_url: str = ""
    ssl_cert_file_url: str = ""
    use_default_cert: bool = True
    enable_cross_origin: bool = False
    cross_origin_allowed_headers: List[Header] = field(default_factory=list)
    enable_proxy: bool = False
    proxy_http_url: str = ""
    proxy_https_url: str = ""
    proxy_http_env: str = ""
    proxy_https_env: str = ""
    endpoints: List[Endpoint] = field(default_factory=list)
    created_at: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S%f")
    viewed_at: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S%f")

    @classmethod
    def from_dict(cls, mock: Dict):
        return cls(
            id=mock.get("id", uuid.uuid4()),
            name=mock.get("name", "localhost"),
            port=mock.get("port", "4001"),
            prefix=mock.get("prefix", ""),
            delay=int(mock.get("delay", 0)),
            enable_https=mock.get("enable_https", False),
            ssl_key_file_url=mock.get("ssl_key_file_url", ""),
            ssl_cert_file_url=mock.get("ssl_cert_file_url", ""),
            use_default_cert=mock.get("use_default_cert", True),
            enable_cross_origin=mock.get("enable_cross_origin", False),
            enable_proxy=mock.get("enable_proxy", False),
            proxy_http_url=mock.get("proxy_http_url", ""),
            proxy_https_url=mock.get("proxy_https_url", ""),
            proxy_http_env=mock.get("proxy_http_env", ""),
            proxy_https_env=mock.get("proxy_http_env", ""),
            cross_origin_allowed_headers=[
                Header.from_dict(_header) for _header in mock.get("cross_origin_allowed_headers", [])],
            endpoints=[Endpoint.from_dict(_endpoint) for _endpoint in mock.get("endpoints", [])],
            created_at=mock.get("created_at"),
            viewed_at=mock.get("viewed_at"))
