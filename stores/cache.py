from typing import List, Dict, Tuple


class SwaVanCache:
    __running_environment_ids: List[str] = []
    __selected_environment_id: str = ""
    __proxy_cred: Dict = {}

    @classmethod
    def clear(cls):
        cls.__running_environment_ids = []
        cls.__selected_environment_id = ""

    @classmethod
    def get_selected_env(cls) -> str:
        return cls.__selected_environment_id

    @classmethod
    def set_selected_env(cls, _id: str) -> None:
        cls.__selected_environment_id = _id

    @classmethod
    def get_running_env_ids(cls) -> List[str]:
        return cls.__running_environment_ids

    @classmethod
    def set_running_env_ids(cls, _ids: List[str]) -> None:
        cls.__running_environment_ids.extend(_ids)

    @classmethod
    def set_running_env_id(cls, _id: str) -> None:
        cls.__running_environment_ids.append(_id)

    @classmethod
    def set_proxy_auth(cls, mock_id, username: str, password: str) -> None:
        cls.__proxy_cred.update({[mock_id]: (username, password,)})

    @classmethod
    def get_proxy_auth(cls, mock_id) -> Tuple:
        return cls.__proxy_cred.get(mock_id)
