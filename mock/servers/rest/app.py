from typing import Dict, List

from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.routing import Route
from mock.modals import Mock
from mock.servers.rest.endpoint import SwaVanRestEndpoint
from mock.servers.rest.helper import route_collector


class SwaVanHttp:

    def __init__(self, mock: Mock):
        _endpoint_mapper = route_collector(mock.endpoints)
        self.app = SwaVanHttp.setup(_endpoint_mapper, SwaVanHttp.middleware(mock))
        self.app.state.mock = route_collector(mock.endpoints)

    @classmethod
    def setup(cls, _endpoint_mapper: Dict, middleware: List[Middleware]) -> Starlette:
        routes = map(lambda url: SwaVanHttp.make_route(url, _endpoint_mapper.get(url)),
                     list(_endpoint_mapper.keys()))
        return Starlette(debug=True, routes=list(routes), middleware=middleware)

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
            Middleware(TrustedHostMiddleware,
                       allowed_hosts=[_cross_origin_allowed_headers.get("access-control-allow-host", "*")]),
            Middleware(
                CORSMiddleware,
                allow_methods=[_cross_origin_allowed_headers.get("access-control-allow-methods", "*")],
                allow_headers=[_cross_origin_allowed_headers.get("access-control-allow-headers", "*")],
                allow_origins=[_cross_origin_allowed_headers.get("access-control-allow-origin", "*")],
                allow_credentials=[_cross_origin_allowed_headers.get("access-control-allow-credentials", False)]
            ),
        ]
        return _middlewares
