import os
import time
import random
import json
from google.cloud import storage, bigquery  # , pubsub_v1
from google.oauth2 import service_account
from io import BytesIO
import requests
from PIL import Image, ImageDraw

name_project = 'xtreamly-ai'
name_bucket = 'reports'
name_database = 'startups'
auth_file = os.path.join(f'gcp-account.json')
credentials = None
if os.path.isfile(auth_file):
    credentials = service_account.Credentials.from_service_account_file(
        auth_file)
client_storage = storage.Client(credentials=credentials, project=name_project)
client_bigquery = bigquery.Client(credentials=credentials, project=name_project)
client_bq = client_bigquery

def _upload_blob_json(content, name_bucket, loc):
    bucket = client_storage.bucket(name_bucket)
    blob = bucket.blob(loc)
    blob.upload_from_string(data=json.dumps(content), content_type='application/json')

def _upload_blob_pdf(pdf, name_bucket, blob_name):
    byte_string = pdf.output(dest="S")
    stream = BytesIO(byte_string)
    stream.seek(0)
    bucket = client_storage.bucket(name_bucket)
    blob = bucket.blob(blob_name)
    blob.upload_from_file(stream, content_type='application/pdf')

def _upload_blob_img(image_url, name_bucket, blob_name):
    response = requests.get(image_url)
    image_content = response.content
    bucket = client_storage.bucket(name_bucket)
    blob = bucket.blob(blob_name)
    blob.upload_from_string(data=image_content, content_type='image/png')

def _read_blob_json(name_bucket, loc):
    bucket = client_storage.bucket(name_bucket)
    blob = bucket.blob(loc)
    file_content = blob.download_as_string()
    json_content = json.loads(file_content)
    return json_content

def _read_blob_img(name_bucket, blob_name):
    bucket = client_storage.bucket(name_bucket)
    blob = bucket.blob(blob_name)
    image_data = blob.download_as_bytes()
    image = Image.open(BytesIO(image_data))
    return image


# =============================================================================
# from google.cloud import bigquery
# from google.auth import default
# auth_file = os.path.join(f'gcp-account.json')
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = auth_file
# 
# credentials, project = default()
# print("Authenticated project:", project)
# print("Credentials:", credentials.service_account_email if hasattr(credentials, "service_account_email") else "Not a service account")
# client_bq = bigquery.Client(project='ai-agents-project-431615')
# 
# query = "SELECT 1 AS test_column"
# query_job = client_bq.query(query)
# =============================================================================