from sqlalchemy import select
import asyncio
from pyodm import Node
from models import TaskModel, OptionsModel
from .parser import ODMParser
from database.engine import new_session
from database.tables import ProcessingTask


class ProcessingEngine:
    enabled = False


class ProcessingNode:
    pass


class MetashapeNode(ProcessingNode):
    pass


class ODMNode(ProcessingNode):
    def __init__(self, host: str = "localhost", port: int = 3000, token: str = ""):
        self.host = host
        self.port = port
        self.token = token

        self.parser = ODMParser()
        self._node = Node(self.host, self.port, self.token)

    async def create_task(self, files_list: list, name: str, options: dict, webhook: str = ""):
        print(f"Запуск обработки {name} с параметрами: {options}")
        async with new_session() as session:
            processing_task = await asyncio.to_thread(
                self._node.create_task, files=files_list, name=name, webhook=webhook, options=options
            )
            task = ProcessingTask(uuid=processing_task.uuid, name=name)
            session.add(task)
            await session.commit()
            return processing_task.uuid

    async def restart_task(self, uuid: str):
        task = await asyncio.to_thread(self._node.get_task, uuid)
        result = task.restart()
        if result:
            print(f"Задача {uuid} перезапущена")
            return result
        else:
            raise Exception("Ошибка перезапуска задачи")

    async def remove_task(self, uuid: str):
        task = await asyncio.to_thread(self._node.get_task, uuid)
        result = task.remove()
        if result:
            print(f"Задача {uuid} удалена")
            return result
        else:
            raise Exception("Ошибка удаления задачи")

    async def cancel_task(self, uuid: str):
        task = await asyncio.to_thread(self._node.get_task, uuid)

        if task.status.name == "COMPLETED":
            raise Exception("Нельзя отменить завершенную задачу")

        result = task.cancel()
        if result:
            print(f"Задача {uuid} отменена")
            return result
        else:
            raise Exception("Ошибка отмены задачи")

    async def task_info(self, uuid: str):
        task = await asyncio.to_thread(self._node.get_task, uuid)
        info = task.info()

        return TaskModel(
            uuid=info.uuid,
            name=info.name,
            created=info.date_created,
            status=info.status.name,
            progress=info.progress,
            last_error=info.last_error,
            options=info.options,
        )

    async def get_task_options(self, uuid: str):
        info = await self.task_info(uuid)
        return OptionsModel(uuid=uuid, options={option['name']: option['value'] for option in info.options})

    async def tasks_info(self):
        async with new_session() as session:
            tasks = await session.execute(select(ProcessingTask))
            tasks_info = []
            for task in tasks.scalars():
                task_info = await self.task_info(task.uuid)
                tasks_info.append(task_info)

            return tasks_info

    async def get_options(self):
        return await self.parser.get_options(self._node)


class MetashapeEngine(ProcessingEngine):
    enabled = False
    node = MetashapeNode()


class ODMEngine(ProcessingEngine):
    enabled = True
    node = ODMNode()

    @staticmethod
    async def run(name: str, files_list: list, options: dict):
        """Запуск задачи
        :param name: Название задачи
        :param files_list: Список файлов для обработки
        :param options: Параметры обработки
        :return: UUID задачи
        """
        return await ODMEngine.node.create_task(files_list, name=name, options=options)

    @staticmethod
    async def task_info(uuid: str):
        """Информация о задаче
        :param uuid: UUID задачи
        :return: Информация о задаче
        """
        return await ODMEngine.node.task_info(uuid)

    @staticmethod
    async def tasks_info() -> list[TaskModel]:
        """Список задач
        :return: Список задач
        """
        return await ODMEngine.node.tasks_info()

    @staticmethod
    async def get_task_options(uuid: str) -> OptionsModel:
        """Получение опций задачи
        :param uuid: UUID задачи
        :return: Опции задачи
        """
        return await ODMEngine.node.get_task_options(uuid)

    @staticmethod
    async def restart_task(uuid: str) -> bool:
        """Перезапуск задачи
        :param uuid: UUID задачи
        :return: True в случае успеха, иначе False
        """
        return await ODMEngine.node.restart_task(uuid)

    @staticmethod
    async def remove_task(uuid: str) -> bool:
        """Удаление задачи и файлов обработки
        :param uuid: UUID задачи
        :return: True в случае успеха, иначе False
        """
        return await ODMEngine.node.remove_task(uuid)

    @staticmethod
    async def cancel_task(uuid: str) -> bool:
        """Отмена обработки задачи
        :param uuid: UUID задачи
        :return: True в случае успеха, иначе False
        """
        return await ODMEngine.node.cancel_task(uuid)

    @staticmethod
    async def get_options():
        """
        Получение списка доступных опций
        :return: Список опций
        """
        return await ODMEngine.node.get_options()


class Processing:
    """
    Обработка данных

    Поддерживаемые движки:
    - ODMEngine
    - MetashapeEngine

    По умолчанию используется ODMEngine
    """

    default_engine = ODMEngine
    engines = [
        ODMEngine,
        MetashapeEngine,
    ]
