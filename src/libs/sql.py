import json


def get_basic_table_sql(table_name: str) -> str:
    return f"CREATE TABLE {table_name}(" \
           f"id varchar not null primary key, " \
           f"created_date timestamp, " \
           f"item jsonb)"


def get_basic_table_sql_from_list(table_names: list) -> dict:
    dict_of_sql = {}
    for table_name in table_names:
        dict_of_sql[table_name] = get_basic_table_sql(table_name)
    return dict_of_sql


def get_insert_sql(table_name: str, item: dict) -> str:
    return f"INSERT INTO {table_name} " \
           f"(id, created_date, item) " \
           f"values ('{item['id']}', '{item['createdTime']}', '{json.dumps(item['fields'])}')"


def get_delete_table_sql_from_list(table_names: list) -> dict:
    dict_of_sql = {}
    for table_name in table_names:
        dict_of_sql[table_name] = f"delete from {table_name}"
    return dict_of_sql
