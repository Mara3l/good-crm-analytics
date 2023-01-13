from dataclasses import dataclass


@dataclass
class AirtableCredentials:
    api_key: str
    base_id: str
