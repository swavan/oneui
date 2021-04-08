import uuid
from dataclasses import asdict
from typing import List

from mock.modals import Endpoint, Response, Header
from stores import DataStoreService


class EndpointService:
    __filename = "endpoints.json"

    @classmethod
    def load_by_ids(cls, ids: List[str]) -> List[Endpoint]:
        return [endpoint for endpoint in cls.load() if endpoint.id in ids]

    @classmethod
    def toggle_state(cls, ids: List[str]) -> bool:
        endpoints = [endpoint for endpoint in cls.load() if endpoint.id in ids]
        for endpoint in endpoints:
            endpoint.is_active = not endpoint.is_active
        return cls.save_all(endpoints)

    @classmethod
    def load_by_parent(cls, _pid: str) -> List[Endpoint]:
        return [_row for _row in cls.load() if _row.pid == _pid]

    @classmethod
    def load(cls) -> List[Endpoint]:
        endpoints = []
        try:
            endpoints = [Endpoint.from_dict(endpoint) for endpoint in DataStoreService.load(cls.__filename)]
        except Exception as e:
            print(e)
        finally:
            return endpoints

    @classmethod
    def is_endpoint_duplicate(cls, url: str, method: str, id: str) -> bool:
        __endpoints = list(filter(lambda x: method.lower() == x.http_method.lower()
                                            and url.lower() == x.url.lower()
                                            and id != x.id, cls.load()))
        return len(__endpoints) > 0

    @classmethod
    def save_all(cls, _endpoints: List[Endpoint]) -> bool:
        is_saved = False
        try:
            DataStoreService.save_all([asdict(_endpoint) for _endpoint in _endpoints], cls.__filename)
            is_saved = True
        except Exception as e:
            print(e)
        finally:
            return is_saved

    @classmethod
    def save(cls, _endpoint: Endpoint) -> bool:
        is_saved = False
        try:
            DataStoreService.save(asdict(_endpoint), cls.__filename)
            is_saved = True
        except Exception as e:
            print(e)
        finally:
            return is_saved

    @classmethod
    def remove(cls, _endpoint_id: str) -> bool:
        is_deleted = False
        try:
            DataStoreService.remove(_endpoint_id, cls.__filename)
            is_deleted = True
        finally:
            return is_deleted

    @classmethod
    def remove_by_parent(cls, _mock_id: str) -> bool:
        is_deleted = False
        try:
            DataStoreService.remove_children(_mock_id, cls.__filename)
            is_deleted = True
        finally:
            return is_deleted

    @classmethod
    def reset(cls) -> Endpoint:
        return Endpoint(id=str(uuid.uuid4()), responses=[cls.response_reset()])

    @classmethod
    def response_reset(cls) -> Response:
        return Response(headers=[Header(key="Content-Type", value="application/json")], rules=[])

    @classmethod
    def default_swavan_response(cls) -> str:
        return '''# Do not delete "swavan_response" method
# You can access response, headers, body and status using swavan
# You can add additional header i.e. swavan.response.headers["app_name"] = "swavan"

def swavan_response() -> None:
    # Add your logic here    
    pass
'''

    @classmethod
    def default_swavan_rule(cls) -> str:
        return '''# Do not delete "swavan_rule" method
# You can access request's headers, body and query and matched using swavan module
# You can update the rule match status ( Please use the enum as provided in the example when setting swavan.rule_status )
# i.e. swavan.rule_status = RuleStatus.Matched if swavan.request.get("app_name") == "swavan" else RuleStatus.Unmatched

def swavan_rule() -> None:
    # Add your logic here   
    # swavan.rule_status = RuleStatus.Matched if swavan.request.get("app_name") == "swavan" else RuleStatus.Unmatched
    pass
'''
