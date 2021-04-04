from dataclasses import asdict
from json.decoder import JSONDecodeError
from typing import List, Union

from mock.modals import Mock as MockModal, Header
from mock.services.endpoint import EndpointService
from stores import DataStoreService


class MockEnvironmentService:
    __filename = "mocks.json"

    @classmethod
    def last_seen(cls) -> Union[MockModal, None]:
        _mocks = cls.load()
        if len(_mocks) > 0:
            return sorted(_mocks, key=lambda x: x.viewed_at, reverse=False)[0]
        else:
            _mock = cls.default()
            DataStoreService.create([asdict(_mock)], cls.__filename)
            _mocks = cls.load()
            return _mocks[0]

    @classmethod
    def load_by_id(cls, _id: str) -> MockModal:
        try:
            for _mock in cls.load():
                if _mock.id == _id:
                    return _mock
        except IOError as _:
            return None

    @classmethod
    def load_by_ids(cls, _ids: List[str]) -> List[MockModal]:
        try:
            return [MockModal.from_dict(mock) for mock in DataStoreService.load(cls.__filename)
                    if mock.get("id") in _ids]
        except IOError as _:
            return []

    @classmethod
    def load(cls) -> List[MockModal]:
        try:
            return [MockModal.from_dict(mock) for mock in DataStoreService.load(cls.__filename)]
        except IOError as _:
            return []
        except JSONDecodeError as _:
            return []

    @classmethod
    def save(cls, _mock: MockModal) -> bool:
        is_saved = False
        try:
            DataStoreService.save(asdict(_mock), cls.__filename)
            is_saved = True
        except IOError as err:
            print("save: ", err)
        finally:
            return is_saved

    @classmethod
    def remove(cls, _id: str) -> bool:
        is_deleted = False
        try:
            DataStoreService.remove(_id, cls.__filename)
            is_deleted = EndpointService.remove_by_parent(_id)
        finally:
            return is_deleted

    @classmethod
    def default(cls, _mock: MockModal = None) -> MockModal:
        if _mock:
            return _mock
        else:
            return MockModal(
                name="localhost",
                port="4000",
                cross_origin_allowed_headers=cls.default_cross_origin_headers()
            )

    @classmethod
    def default_cross_origin_headers(cls, _mock: MockModal = None) -> List[Header]:
        return [Header(key="Content-Type", value="application/json"),
                Header(key="Access-Control-Allow-Origin", value="*"),
                Header(key="Access-Control-Allow-Methods", value="GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS"),
                Header(key="Access-Control-Allow-Headers",
                       value="Content-Type, Origin, Accept, Authorization, Content-Length, X-Requested-With")
                ]
