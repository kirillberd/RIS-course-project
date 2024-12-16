from dataclasses import dataclass
from infrastructure.providers.sql_provider import SQLProvider
from infrastructure.repositories.report_repository import ReportRepository
import logging


module_logger = logging.getLogger(__name__)


@dataclass
class ReportService:
    sql_provider: SQLProvider
    report_repository: ReportRepository

    def get_report(self, name, year, month):
        ...
