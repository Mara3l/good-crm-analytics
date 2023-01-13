with deals as (
    select
        id,
        created_date,
        to_json("item") as item_json
    from
        input_stage.airtable_crm_deals
),
final as (
    select
        id,
        CAST(
            json_extract_path_text(item_json, 'Name') as VARCHAR
        ) as name,
        CAST(
            json_extract_path_text(item_json, 'Stage') as VARCHAR
        ) as stage,
        CAST(
            json_extract_path_text(item_json, 'Amount') as NUMERIC
        ) as amount,
        CAST(
            json_extract_path_text(item_json, 'Details') as VARCHAR
        ) as details,
        CAST(
            json_extract_path_text(item_json, 'Close Probability') as NUMERIC
        ) as close_probability,
        CAST(
            json_extract_path_text(
                item_json,
                'Accounts (listing this as Opportunities )',
                '0'
            ) as TEXT
        ) as account_id,
        CAST(
            json_extract_path_text(item_json, 'Open date') as DATE
        ) as open_date,
        CAST(
            json_extract_path_text(item_json, 'Close date') as DATE
        ) as close_date,
        CAST(
            json_extract_path_text(item_json, 'Last update') as DATE
        ) as last_update
    from
        deals
)
select
    *
from
    final