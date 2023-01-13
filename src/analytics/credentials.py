from dataclasses import dataclass


@dataclass
class GoodDataCredentials:
    host: str
    token: str
    data_source_id: str