import os

from uvicorn import Config, Server

from mock.modals import Mock
from mock.servers.config import SwaVanMockTask
from mock.servers.rest.app import SwaVanHttp
from shared.recorder import SwaVanLogRecorder
from shared.widgets.builder import full_path


class SwaVanRestMockServer(SwaVanMockTask):

    def __init__(self, _mock: Mock):
        self._id = _mock.id
        self._mock = _mock
        _headers = [('server', 'swavan')]
        _config = Config(app=SwaVanHttp(_mock).app,
                         host="localhost",
                         headers=_headers,
                         port=int(_mock.port),
                         access_log=False)
        if _mock.enable_https:
            _key = full_path("data/__certs__/swavan.key")
            _crt = full_path("data/__certs__/swavan.crt")
            if _mock.use_default_cert:
                if os.path.isfile(_key) and os.path.isfile(_crt):
                    _config.ssl_keyfile = _key
                    _config.ssl_certfile = _crt
                    SwaVanLogRecorder.send_log(f"Using default cert")
            else:
                if os.path.isfile( _mock.ssl_key_file_url) and os.path.isfile( _mock.ssl_cert_file_url):
                    _config.ssl_keyfile = _mock.ssl_key_file_url
                    _config.ssl_certfile = _mock.ssl_cert_file_url
                    SwaVanLogRecorder.send_log(f"Using custom cert")
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
