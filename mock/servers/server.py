from typing import List

from PyQt6.QtCore import QThread

from mock.modals import Mock
from mock.servers.config import SwaVanMockTask, ServerTypes
from mock.servers.rest.helper import port_is_busy
from mock.servers.rest.service import SwaVanRestMockServer


class SwaVanMockWorker(QThread):
    _task: SwaVanMockTask = None

    def run(self):
        if self._task:
            self._task.start()

    def stop_execution(self):
        if self._task:
            self._task.stop()
        self.exit(0)

    def assign(self, task: SwaVanMockTask):
        self._task = task

    def task(self) -> SwaVanMockTask:
        return self._task


class SwaVanMockServerService:
    _workers: List[SwaVanMockWorker] = []

    @classmethod
    def is_running(cls, _id: str):
        return any([_worker.task().id == _id for _worker in cls._workers])

    @classmethod
    def stop(cls, _id: str):
        for i, _worker in enumerate(cls._workers):
            if _worker.task().id == _id:
                _worker.stop_execution()
                cls._workers.pop(i)
                break

    @classmethod
    def stop_all(cls, _id: str):
        for i, _worker in enumerate(cls._workers):
            _worker.stop_execution()
            cls._workers.pop(i)

    @classmethod
    def start(cls, _mock: Mock, _type: ServerTypes):
        if not port_is_busy("localhost", int(_mock.port)):
            worker = SwaVanMockWorker()
            position = len(cls._workers)
            if _type == ServerTypes.REST:
                _task = SwaVanRestMockServer(_mock)
                worker.assign(_task)

            cls._workers.append(worker)
            cls._workers[position].start()
