from pydantic import BaseModel


class MysqlCMConfig(BaseModel):
    host: str
    user: str
    password: str
    database: str
    