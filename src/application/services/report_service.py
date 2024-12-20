from dataclasses import dataclass
from infrastructure.providers.sql_provider import SQLProvider
from infrastructure.repositories.report_repository import ReportRepository
import logging


module_logger = logging.getLogger(__name__)


@dataclass
class ReportService:
    sql_provider: SQLProvider
    report_repository: ReportRepository

    report_dict = {
        "billboard_stats" : {
            "check_query_name": "check_bilboard_rent_report.sql",
            "procedure_name": "generate_billboard_stats_report",
            "report_table": "billboard_report",
            "query_name": "get_billboard_rent_report.sql",
            "translation": "Отчет по аренде билбордов"
        }
    }


    def create_report(self, name, year, month):
        check_query_name = self.report_dict.get(name).get("check_query_name")
        procedure_name = self.report_dict.get(name).get("procedure_name")
        report_table_base = self.report_dict.get(name).get("report_table")
        table_name = f"{report_table_base}_{year}_{month:02d}"
        check_query = self.sql_provider.get(check_query_name, table_name=table_name)
        exists = self.report_repository.check_exists(check_query)
        if exists:
            raise Exception("Отчет уже существует")
        else:
            self.report_repository.create_report(procedure_name, year, month)

    def view_report(self, name, year, month):
        check_query_name = self.report_dict.get(name).get("check_query_name")
        report_table_base = self.report_dict.get(name).get("report_table")
        table_name = f"{report_table_base}_{year}_{month:02d}"
        check_query = self.sql_provider.get(check_query_name, table_name=table_name)
        exists = self.report_repository.check_exists(check_query)
        if not exists:
            raise Exception("Отчета не существует")
        else:
            query_name = self.report_dict.get(name).get("query_name")
            query = self.sql_provider.get(query_name, table_name=table_name)
            return self.report_repository.get_report(query)
            