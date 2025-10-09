from typing import TypeVar, Generic, List, Optional, Type
from datetime import datetime
from .base import BaseRepository
from ...services import logger

T = TypeVar("T")


class RepositoryLoggingDecorator(BaseRepository[T]):
    """
    ПАТТЕРН: DECORATOR (Декоратор)
    
    Динамически добавляет дополнительную функциональность (логирование) 
    к объекту репозитория без изменения его кода.
    
    Преимущества:
    - Добавляет функциональность прозрачно для клиента
    - Соблюдает принцип открытости/закрытости (Open/Closed Principle)
    - Можно комбинировать несколько декораторов
    - Не изменяет оригинальный класс
    """
    
    def __init__(self, repository: BaseRepository[T], log_operations: bool = True):
        """
        Args:
            repository: Оригинальный репозиторий, который декорируем
            log_operations: Флаг включения/выключения логирования
        """
        self._repository = repository
        self._log_operations = log_operations
        self._operation_count = 0
    
    def get_model(self) -> Type[T]:
        """Делегируем вызов оригинальному репозиторию"""
        return self._repository.get_model()
    
    async def get(self, id: int) -> Optional[T]:
        """Декорированный метод получения сущности по ID"""
        self._operation_count += 1
        
        if self._log_operations:
            model_name = self.get_model().__name__
            logger.info(f"[DECORATOR] Get operation #{self._operation_count}: {model_name} with id={id}")
        
        start_time = datetime.now()
        result = await self._repository.get(id)
        execution_time = (datetime.now() - start_time).total_seconds()
        
        if self._log_operations:
            status = "found" if result else "not found"
            logger.info(f"[DECORATOR] Get operation completed: {status} in {execution_time:.3f}s")
        
        return result
    
    async def list(self, limit: int = 100, offset: int = 0) -> List[T]:
        """Декорированный метод получения списка сущностей"""
        self._operation_count += 1
        
        if self._log_operations:
            model_name = self.get_model().__name__
            logger.info(f"[DECORATOR] List operation #{self._operation_count}: {model_name} (limit={limit}, offset={offset})")
        
        start_time = datetime.now()
        result = await self._repository.list(limit, offset)
        execution_time = (datetime.now() - start_time).total_seconds()
        
        if self._log_operations:
            logger.info(f"[DECORATOR] List operation completed: {len(result)} items in {execution_time:.3f}s")
        
        return result
    
    async def create(self, entity: T) -> T:
        """Декорированный метод создания сущности"""
        self._operation_count += 1
        
        if self._log_operations:
            model_name = self.get_model().__name__
            logger.info(f"[DECORATOR] Create operation #{self._operation_count}: {model_name}")
        
        start_time = datetime.now()
        result = await self._repository.create(entity)
        execution_time = (datetime.now() - start_time).total_seconds()
        
        if self._log_operations:
            entity_id = getattr(result, 'id', 'unknown')
            logger.info(f"[DECORATOR] Create operation completed: created id={entity_id} in {execution_time:.3f}s")
        
        return result
    
    async def update(self, id: int, entity: T) -> T:
        """Декорированный метод обновления сущности"""
        self._operation_count += 1
        
        if self._log_operations:
            model_name = self.get_model().__name__
            logger.info(f"[DECORATOR] Update operation #{self._operation_count}: {model_name} with id={id}")
        
        start_time = datetime.now()
        result = await self._repository.update(id, entity)
        execution_time = (datetime.now() - start_time).total_seconds()
        
        if self._log_operations:
            logger.info(f"[DECORATOR] Update operation completed in {execution_time:.3f}s")
        
        return result
    
    async def delete(self, entity_id: int):
        """Декорированный метод удаления сущности"""
        self._operation_count += 1
        
        if self._log_operations:
            model_name = self.get_model().__name__
            logger.info(f"[DECORATOR] Delete operation #{self._operation_count}: {model_name} with id={entity_id}")
        
        start_time = datetime.now()
        await self._repository.delete(entity_id)
        execution_time = (datetime.now() - start_time).total_seconds()
        
        if self._log_operations:
            logger.info(f"[DECORATOR] Delete operation completed in {execution_time:.3f}s")
    
    def get_statistics(self) -> dict:
        """Дополнительная функциональность декоратора - статистика операций"""
        return {
            "total_operations": self._operation_count,
            "logging_enabled": self._log_operations,
            "decorated_model": self.get_model().__name__
        }
    
    def enable_logging(self):
        """Включить логирование"""
        self._log_operations = True
        logger.info("[DECORATOR] Logging enabled")
    
    def disable_logging(self):
        """Выключить логирование"""
        self._log_operations = False
        logger.info("[DECORATOR] Logging disabled")
