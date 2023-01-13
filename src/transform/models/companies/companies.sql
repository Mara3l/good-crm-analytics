with companies as (
       select
              id,
              created_date,
              to_json("item") as item_json
       from
              input_stage.airtable_crm_companies
),
final as (
       select
              id,
              CAST(
                     json_extract_path_text(item_json, 'Name') as VARCHAR
              ) as name,
              CAST(
                     json_extract_path_text(item_json, 'Type') as VARCHAR
              ) as type,
              CAST(
                     json_extract_path_text(item_json, 'Address') as VARCHAR
              ) as address,
              CAST(
                     json_extract_path_text(item_json, 'Employees') as NUMERIC
              ) as employees,
              CAST(
                     json_extract_path_text(item_json, 'Description') as VARCHAR
              ) as description,
              CAST(
                     json_extract_path_text(item_json, 'Contacts', '0') as VARCHAR
              ) as contact_id
       from
              companies
)
select
       *
from
       final