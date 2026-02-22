from abc import ABC, abstractmethod

from src.rabbitmq.tasks.CertificateSchema import AbstractCertificateSchema


class AbstractCertificate(ABC):
    @staticmethod
    @abstractmethod
    def render(data: AbstractCertificateSchema):
        pass