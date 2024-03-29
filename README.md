# Esquemas

## bigquery
```json
[
  {
    "name": "name_str",
    "mode": "NULLABLE",
    "type": "STRING",
    "description": null,
    "fields": []
  },
  {
    "name": "date_dt",
    "mode": "NULLABLE",
    "type": "DATE",
    "description": null,
    "fields": []
  },
  {
    "name": "count_str",
    "mode": "NULLABLE",
    "type": "STRING",
    "description": null,
    "fields": []
  },
  {
    "name": "count_int",
    "mode": "NULLABLE",
    "type": "INTEGER",
    "description": null,
    "fields": []
  }
]
```
## firestore
```json
{
    "fields": {
        "count_int": {
            "integerValue": 0
        },
        "count_str": {
            "stringValue": "0"
        },
        "date_dt": {
            "stringValue": "2024 at 1:12:54.005 PM UTC-5"
        },
        "name_str": {
            "stringValue": "name"
        },
    }
}
```

# BASH

```bash
python3 -m virtualenv venv;
source venv/bin/activate;

pip install -r requirements.txt;

gcloud auth print-access-token;

python main.py;
```

- Test:

```bash
for i in {0..100};do python bq_main.py >> bq_responses.txt & sleep 0.5 ;done
for i in {0..100};do python fs_main.py >> fs_responses.txt & sleep 0.5 ;done
```

# Resultados

- Biguqery [rest](https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs/query?apix_params=%7B%22projectId%22%3A%22quiet-invention-417303%22%2C%22resource%22%3A%7B%22query%22%3A%22SELECT%20*%20FROM%20%60quiet-invention-417303.datatest_us.bq_table%60%20LIMIT%201000%22%2C%22useLegacySql%22%3Afalse%7D%7D)
-- 3.1s (read, update, read) 1s by one
-- De 100 solo hizo update en 4 y muchas salieron con error
- Firestore [rest](https://cloud.google.com/firestore/docs/reference/rest/v1/projects.databases.documents/patch?apix=true&apix_params=%7B%22name%22%3A%22projects%2Fquiet-invention-417303%2Fdatabases%2Ffs-test%2Fdocuments%2Fcollection_1%2Fdocument_1%22%2C%22mask.fieldPaths%22%3A%5B%22count_str%22%5D%2C%22resource%22%3A%7B%22fields%22%3A%7B%22count_str%22%3A%7B%22stringValue%22%3A%220%22%7D%7D%7D%7D) [overflow](https://stackoverflow.com/questions/59076188/using-the-firestore-rest-api-to-update-a-document-field)
-- 0.7s (read, update, read) 0.2s by one
-- 
