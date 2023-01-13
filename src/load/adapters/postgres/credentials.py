from dataclasses import dataclass


@dataclass
class PostgresCredentials:
    host: str
    port: str
    user: str
    password: str
    database_name: str
    database_schema: str
