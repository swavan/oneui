from typing import List


class SwaVanCache:
    __running_environment_ids: List[str] = []
    __selected_environment_id: str = ""

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
