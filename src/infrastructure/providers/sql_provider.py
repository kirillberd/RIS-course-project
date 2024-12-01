from pathlib import Path
from string import Template
from typing import Dict


class SQLProvider:
    def __init__(self, file_path: str | Path):
        self.sql_path = Path(file_path)
        if not self.sql_path.exists():
            raise FileNotFoundError(f"Directory {file_path} does not exist")
        if not self.sql_path.is_dir():
            raise NotADirectoryError(f"{file_path} is not a directory")
            
        self.scripts: Dict[str, Template] = {}
        self._load_sql_files()
    
    def _load_sql_files(self) -> None:
        for sql_file in self.sql_path.glob('*.sql'):
            sql = sql_file.read_text(encoding='utf-8')
            self.scripts[sql_file.name] = Template(sql)
    
    def get(self, file_name: str, **kwargs) -> str:
        if file_name not in self.scripts:
            raise KeyError(f"SQL file {file_name} not found in {self.sql_path}")
            
        return self.scripts[file_name].substitute(**kwargs)