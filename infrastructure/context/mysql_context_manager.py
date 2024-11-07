from pymysql import connect

from pymysql.err import OperationalError
import logging

logger = logging.getLogger(__name__)

class MysqlContextManager:
    def __init__(self, db_config: dict) -> None:
        self._conn = None
        self._cur = None
        self._db_config = db_config

    def __enter__(self):
        try:
            self._conn = connect(**self._db_config)
            self._cur = self._conn.cursor()
        except OperationalError as err:
            logger.error("Error connecting to a DB", exc_info=True)
            return None
        return self._cur
    

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            logging.error(f"Error occured while performing a request. type: {exc_type}, value: {exc_val}")

        if self._cur:
            if exc_type:
                self._conn.rollback()
                return False
            else:
                self._conn.commit()
            self._cur.close()
        return True
