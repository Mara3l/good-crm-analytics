with contacts as (
    select
        id,
        created_date,
        to_json("item") as item_json
    from
        input_stage.airtable_crm_contacts
),
final as (
    select
        id,
        CAST(
            json_extract_path_text(item_json, 'Name') as VARCHAR
        ) as name
    from
        contacts
)
select
    *
from
    final