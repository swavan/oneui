import os

from uvicorn import Config, Server

from mock.modals import Mock
from mock.servers.config import SwaVanMockTask
from mock.servers.rest.app import SwaVanHttp


class SwaVanRestMockServer(SwaVanMockTask):

    def __init__(self, _mock: Mock):
        self._id = _mock.id
        self._mock = _mock
        _headers = [('server', 'swavan')]
        _config = Config(app=SwaVanHttp(_mock).app,
                         host="localhost",
                         headers=_headers,
                         port=int(_mock.port))
        if _mock.enable_https:
            if _mock.use_default_cert:
                cwd = os.path.dirname(os.path.realpath(__file__))
                _config.ssl_keyfile = os.path.join(cwd, "certs/swavan.key")
                _config.ssl_certfile = os.path.join(cwd, "certs/swavan.crt")
            else:
                _config.ssl_keyfile = _mock.ssl_key_file_url
                _config.ssl_certfile = _mock.ssl_cert_file_url
        self._core_server = Server(config=_config)

    def start(self):
        if self._core_server:
            self._core_server.run()

    def stop(self):
        self._core_server.should_exit = True

    def set_id(self, _id: str):
        self._id = _id

    def set_mock(self, _mock: Mock):
        self._mock = _mock

    @property
    def id(self) -> str:
        return self._mock.id
