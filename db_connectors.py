from contextlib import contextmanager
from dataclasses import dataclass
from functools import cached_property
from typing import Generator, List
import pandas as pd
import sqlalchemy
from sqlalchemy import inspect, text, create_engine
import mysql.connector
from prompt_formatters import TableColumn, Table


@dataclass
class PostgresConnector:
    """Postgres connection."""

    user: str
    password: str
    dbname: str
    host: str
    port: int

    @cached_property
    def pg_uri(self) -> str:
        """Get Postgres URI."""
        uri = (
            f"postgresql://"
            f"{self.user}:{self.password}@{self.host}:{self.port}/{self.dbname}"
        )
        # ensure we can actually connect to this postgres uri
        engine = sqlalchemy.create_engine(uri)
        conn = engine.connect()

        # assuming the above connection is successful, we can now close the connection
        conn.close()
        engine.dispose()

        return uri

    @contextmanager
    def connect(self) -> Generator[sqlalchemy.engine.base.Connection, None, None]:
        """Yield a connection to a Postgres db.

        Example:
        .. code-block:: python
            postgres = PostgresConnector(
                user=USER, password=PASSWORD, dbname=DBNAME, host=HOST, port=PORT
            )
            with postgres.connect() as conn:
                conn.execute(sql)
        """
        try:
            engine = sqlalchemy.create_engine(self.pg_uri)
            conn = engine.connect()
            yield conn
        finally:
            conn.close()
            engine.dispose()

    def run_sql_as_df(self, sql: str) -> pd.DataFrame:
        """Run SQL statement."""
        with self.connect() as conn:
            return pd.read_sql(sql, conn)

    def get_tables(self) -> List[str]:
        """Get all tables in the database."""
        engine = sqlalchemy.create_engine(self.pg_uri)
        inspection = inspect(engine)
        table_names = inspection.get_table_names()
        #table_names = engine.table_names()
        engine.dispose()
        return table_names

    def get_schema(self, table: str) -> Table:
        """Return Table."""
        with self.connect() as conn:
            columns = []
            sql = f"""
                SELECT column_name, data_type
                FROM information_schema.columns
                WHERE table_name = '{table}';
            """
            schema = conn.execute(text(sql)).fetchall()
            for col, type_ in schema:
                columns.append(TableColumn(name=col, dtype=type_))
            return Table(name=table, columns=columns)

@dataclass
class SQLiteConnector:
    """SQLite connection."""

    database_path: str

    @cached_property
    def sqlite_uri(self) -> str:
        """Get SQLite URI."""
        uri = f"sqlite:///{self.database_path}"
        # ensure we can actually connect to this SQLite uri
        engine = sqlalchemy.create_engine(uri)
        conn = engine.connect()

        # assuming the above connection is successful, we can now close the connection
        conn.close()
        engine.dispose()

        return uri

    @contextmanager
    def connect(self) -> Generator[sqlalchemy.engine.base.Connection, None, None]:
        """Yield a connection to a SQLite database.

        Example:
        .. code-block:: python
            sqlite = SQLiteConnector(database_path=DB_PATH)
            with sqlite.connect() as conn:
                conn.execute(sql)
        """
        try:
            engine = sqlalchemy.create_engine(self.sqlite_uri)
            conn = engine.connect()
            yield conn
        finally:
            conn.close()
            engine.dispose()

    def get_tables(self) -> List[str]:
        """Get all tables in the database."""
        engine = sqlalchemy.create_engine(self.sqlite_uri)
        table_names = engine.table_names()
        engine.dispose()
        return table_names

    def run_sql_as_df(self, sql: str) -> pd.DataFrame:
        """Run SQL statement."""
        with self.connect() as conn:
            return pd.read_sql(sql, conn)

    def get_schema(self, table: str) -> Table:
        """Return Table."""
        with self.connect() as conn:
            columns = []
            sql = f"PRAGMA table_info({table});"
            schema = conn.execute(sql).fetchall()
            for row in schema:
                col = row[1]
                type_ = row[2]
                columns.append(TableColumn(name=col, dtype=type_))
            return Table(name=table, columns=columns)
        
@dataclass
class MysqlConnector:
    """MySQL connection."""

    user: str
    password: str
    dbname: str  
    host: str
    port : int

    @contextmanager
    def connect(self) -> Generator[mysql.connector.connection.MySQLConnection, None, None]:
        """Yield a connection to a MySQL database."""
        try:
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.dbname,
                port=self.port
            )
            yield connection
        finally:
            connection.close()

    def get_tables(self) -> List[str]:
        """Get all tables in the database."""
        with self.connect() as connection:
            cursor = connection.cursor()
            cursor.execute("SHOW TABLES")
            table_names = [table[0] for table in cursor]
            cursor.close()

        return table_names

    def get_schema(self, table: str) -> Table:
        """Return Table."""
        with self.connect() as conn:
            columns = []
            cursor = conn.cursor(dictionary=True)
            cursor.execute(f"DESCRIBE {table}")
            schema = cursor.fetchall()
            for row in schema:
                col = row["Field"]
                type_ = row["Type"]
                columns.append(TableColumn(name=col, dtype=type_))
            cursor.close()

        return Table(name=table, columns=columns)