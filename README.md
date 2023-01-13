Hello and welcome to the Sales Analytics repository! 🚀🚀🚀

## Load Analytics to Your GoodData Trial

If you want replicate the whole analytics from the article, you can easily do that by the following command. Before you run it, please do the steps described in the following sections:

👉 [Setup virtual environment](#setup-virtual-environment)

👉 [Install dependencies](#install-dependencies)

👉 [Environment Variables](#environment-variables)

```bash
$ python ./src/store_and_load_analytics.py load <workspace-id> 
```

**Important note:** You should create a workspace in GoodData Trial before you run the `store_and_load_analytics.py` script, see [Create a Workspace](https://www.gooddata.com/developers/cloud-native/doc/cloud/getting-started/create-workspace/?utm_medium=blogpost&utm_source=medium.com&utm_campaign=gooddata_airtable_022023&utm_content=autor_patrik).

# Setup virtual environment

```bash
# Create virtual env
python -m virtualenv venv
# Activate virtual env
source venv/bin/activate
#You should see a `(venv)` appear at the beginning of your terminal prompt indicating that you are working inside the `virtualenv`.
# Deactivate virtual env once you are done
deactivate
```

# Install dependencies

```bash
$ pip install -r requirements.txt
```

# Environment Variables

## Extract

If you want to replicate the Airtable Sales CRM from the article, visit [this link](https://airtable.com/shrbAw7acN2xUJLtW) and click **Copy base**. Once you have it, you can setup environment variables: 

```bash
export EXTRACT_AIRTABLE_API_KEY='<AIRTABLE-API-KEY>'
```

You can create Airtable API KEY [here](https://airtable.com/create/tokens).

```bash
export EXTRACT_AIRTABLE_BASE_ID='<AIRTABLE-BASE-ID>'
```

Example: `export EXTRACT_AIRTABLE_BASE_ID='appZj5ydFeMfC8f7p'`.

```bash
export EXTRACT_AIRTABLE_TABLES='["<AIRTABLE-TABLE>", "<AIRTABLE-TABLE>"]'
```

Example: `export EXTRACT_AIRTABLE_TABLES='["tblwMVmNNV3HhJtww", "tblwIZrCQ0bJmFtBB", "tblvM4lMGVdBqAFLH"]'`.

**Important note:** you should define `EXTRACT_AIRTABLE_TABLES` in the order you see it in the UI: `deals`, `companies`, `contacts`.

## Load & Transform

If you do not have database, please create one on [bit.io](bit.io) (or somewhere else) and setup the following environment variables:

```bash
export LOAD_DATABASE_HOST='<DATABASE_HOST>'
export LOAD_DATABASE_PORT='<DATABASE_PORT>'
export LOAD_DATABASE_USERNAME='<DATABASE_USERNAME>'
export LOAD_DATABASE_PASSWORD='<DATABASE_PASSWORD>'
export LOAD_DATABASE_NAME='<DATABASE_NAME>'
```

```bash
export LOAD_DATABASE_SCHEMA='input_stage'
```

Please use this exact variable; otherwise, it will not work.

```bash
export LOAD_DATABASE_SCHEMA='["airtable_crm_deals", "airtable_crm_companies", "airtable_crm_contacts"]'
```

Please use this exact variable; otherwise, it will not work.

## Analytics

```bash
export ANALYTICS_GOODDATA_HOST='<GOODDATA_HOST>'
```

You can register [here](https://www.gooddata.com/trial/?utm_medium=blogpost&utm_source=medium.com&utm_campaign=gooddata_airtable_022023&utm_content=autor_patrik).

```bash
export ANALYTICS_GOODDATA_TOKEN='<GOODDATA_TOKEN>'
```

You can create GoodData token on the following URL: `<your-gooddata-account>/settings`.

```bash
export ANALYTICS_GOODDATA_DATASOURCE_ID='<GOODDATA_DATASOURCE_ID>'
```

You can connect a data source (in this case PostgreSQL from the previous step) on the following URL: `<your-gooddata-account>/data-sources`.

# Troubleshooting

If you jumped into an issue, please feel free to [report it](https://github.com/patrikbraborec/good-crm-analytics/issues/new). Also, you can write me on [GoodData Community Slack](https://www.gooddata.com/slack/).

# Local Run

## Run Extract & Load

```bash
$ python ./src/main.py
```

## Run Transform

```bash
$ cd transform
$ dbt deps
$ dbt run
$ dbt test
```

## Run Analytics

```bash
$ python ./src/extract_load.py
```
