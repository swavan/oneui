import os
from typing import Dict, List

from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.routing import Route
from mock.modals import Mock
from mock.servers.rest.endpoint import SwaVanRestEndpoint
from mock.servers.rest.helper import route_collector


class SwaVanHttp:
    def __init__(self, mock: Mock):
        _endpoint_mapper = route_collector(mock.prefix, mock.endpoints)
        self.app = SwaVanHttp.setup(_endpoint_mapper, SwaVanHttp.middleware(mock))
        self.app.state.mock = _endpoint_mapper
        self.app.state.delay = mock.delay
        self.app.state.proxies = {}
        _proxy_http = os.environ.get(mock.proxy_http_env, "")
        _proxy_https = os.environ.get(mock.proxy_https_env, "")
        if mock.proxy_http_url and mock.proxy_http_url:
            _proxy_http = mock.proxy_http_url
            _proxy_https = mock.proxy_https_url
        if mock.enable_proxy:
            self.app.state.proxies.update({"http": _proxy_http, "https": _proxy_https})

    @classmethod
    def setup(cls, _endpoint_mapper: Dict, middleware: List[Middleware]) -> Starlette:
        routes = map(lambda url: SwaVanHttp.make_route(url, _endpoint_mapper.get(url)),
                     list(_endpoint_mapper.keys()))
        return Starlette(debug=False, routes=list(routes), middleware=middleware)

    @classmethod
    def make_route(cls, url, mapper) -> Route:
        return Route(
            path=url,
            endpoint=SwaVanRestEndpoint,
            methods=mapper.keys())

    @classmethod
    def middleware(cls, mock: Mock) -> List[Middleware]:
        _cross_origin_allowed_headers = dict(zip(list(map(lambda x: x.key.lower(), mock.cross_origin_allowed_headers)),
                                                 list(map(lambda x: x.value, mock.cross_origin_allowed_headers))))
        _middlewares = [
            Middleware(
                TrustedHostMiddleware,
                allowed_hosts=[_cross_origin_allowed_headers.get("access-control-allow-host", "*")]),
        ]
        if mock.enable_cross_origin:
            _middlewares.append(
                Middleware(
                    CORSMiddleware,
                    allow_methods=[_cross_origin_allowed_headers.get("access-control-allow-methods", "*")],
                    allow_headers=[_cross_origin_allowed_headers.get("access-control-allow-headers", "*")],
                    allow_origins=[_cross_origin_allowed_headers.get("access-control-allow-origin", "*")],
                    allow_credentials=[_cross_origin_allowed_headers.get("access-control-allow-credentials", False)],
                )
            )
        if mock.enable_https:
            _middlewares.append(Middleware(HTTPSRedirectMiddleware))
        return _middlewares
