import requests
import json
import os
from datetime import datetime

PROJECT_ID = os.getenv("PROJECT_ID", "quiet-invention-417303")
DB_ID = os.getenv("DB_ID", "fs-test")
COLLECTION_ID = os.getenv("COLLECTION_ID", "collection_1")
DOC_ID = os.getenv("DOC_ID", "document_1")

def consultar_firestore(token):
    url = f'https://firestore.googleapis.com/v1/projects/{PROJECT_ID}/databases/{DB_ID}/documents/{COLLECTION_ID}/{DOC_ID}'
  
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        respuesta_json = response.json()
        return respuesta_json
    else:
        print(json.loads(response.text)['error']['message'])
        return None

def escribir_firestore(token, count_str):
    #url = f'https://firestore.googleapis.com/v1/projects/{PROJECT_ID}/databases/{DB_ID}/documents/{COLLECTION_ID}/{DOC_ID}?currentDocument.exists=true'
    url = f"https://firestore.googleapis.com/v1/projects/{PROJECT_ID}/databases/{DB_ID}/documents/{COLLECTION_ID}/{DOC_ID}?updateMask.fieldPaths=count_str"
  
    headers = {"Authorization": f"Bearer {token}", "Content-Type":"application/json"}
    #body = {"fields": fields}
    body = json.dumps({
    "fields": {
        "count_str": {
            "stringValue": str(count_str)
        }
    }})

    response = requests.patch(url, headers=headers, data=body)

    if response.status_code == 200:
        respuesta_json = response.json()
        return respuesta_json
    else:
        print(json.loads(response.text)['error']['message'])
        return None


def fs_read_write(token):
    # read
    time_read = datetime.now()
    resultado_read = consultar_firestore(token)
    fields = resultado_read['fields']

    # write
    count = int(fields['count_str']['stringValue'])
    resultado_write = escribir_firestore(token, count+1)

    # read again
    resultado_read2 = consultar_firestore(token)
    fields2 = resultado_read2['fields']
    count2 = int(fields2['count_str']['stringValue'])
    time_read2 = datetime.now()
    
    # print
    resultado = f'R({time_read}):{count} | U({time_read}):{count2}'
    print(resultado)
    return resultado


token = ''
response = fs_read_write(token)
