import requests
import json
import os
from datetime import datetime


PROJECT_ID = os.getenv("PROJECT_ID", "quiet-invention-417303")


def bq_send_query(token, consulta, proyecto=PROJECT_ID):
    url = f"https://bigquery.googleapis.com/bigquery/v2/projects/{PROJECT_ID}/queries"
    payload = {"query": consulta, "useLegacySql": False}

    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        respuesta_json = response.json()
        return respuesta_json
    else:
        print(json.loads(response.text)['error']['message'])
        return None


def bq_read_write(token):
    lectura = "SELECT * FROM `quiet-invention-417303.datatest_us.bq_table` LIMIT 1"
    resultado_read = bq_send_query(token, lectura)
    time_read = datetime.now()
    count = int(resultado_read['rows'][0]['f'][2]['v'])
    escritura = f"UPDATE `quiet-invention-417303.datatest_us.bq_table` SET count_str='{count+1}' WHERE count_str='{count}'"
    resultado_write = bq_send_query(token, escritura)
    resultado_read2 = bq_send_query(token, lectura)
    count2 = int(resultado_read2['rows'][0]['f'][2]['v'])
    time_read2 = datetime.now()
    resultado = f'R({time_read}):{count} | U({time_read}):{count2}'
    print(resultado)
    return resultado


token=""
bq_read_write(token)
