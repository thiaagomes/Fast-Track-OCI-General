import io
import json
import logging
from urllib.parse import quote

import pymysql
from fdk import response


DB_HOST = "IP_PRIVADO"
DB_PORT = 3306
DB_USER = "COLOQUE_USUARIO_AQUI"
DB_PASSWORD = "COLOQUE_A_SENHA_AQUI"
DB_NAME = "fast_track_db"

OBJECT_STORAGE_ENDPOINT = "https://objectstorage.sa-saopaulo-1.oraclecloud.com"


def extract_object_metadata(body):
    if "data" in body and "additionalDetails" in body["data"]:
        data = body.get("data", {})
        details = data.get("additionalDetails", {})

        namespace = details.get("namespace", "idi1o0a010nx")
        bucket_name = details.get("bucketName", "bucket-fast-track")
        object_name = data.get("resourceName", "arquivo-sem-nome.txt")
        event_time = body.get("eventTime", "")

        encoded_object_name = quote(object_name, safe="")
        object_url = (
            f"{OBJECT_STORAGE_ENDPOINT}/n/{namespace}"
            f"/b/{bucket_name}/o/{encoded_object_name}"
        )

        return bucket_name, object_name, object_url, event_time

    bucket_name = body.get("bucket_name", "bucket-fast-track")
    object_name = body.get("object_name", "arquivo-sem-nome.txt")
    object_url = body.get("object_url", "")
    event_time = body.get("event_time", "")

    return bucket_name, object_name, object_url, event_time


def handler(ctx, data: io.BytesIO = None):
    logging.getLogger().info("Starting function execution")

    try:
        body = json.loads(data.getvalue()) if data and data.getvalue() else {}

        bucket_name, object_name, object_url, event_time = extract_object_metadata(body)

        connection = pymysql.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            connect_timeout=10,
        )

        with connection:
            with connection.cursor() as cursor:
                sql = """
                    INSERT INTO bucket_files (
                        bucket_name,
                        object_name,
                        object_url,
                        event_time
                    ) VALUES (%s, %s, %s, %s)
                """

                cursor.execute(
                    sql,
                    (
                        bucket_name,
                        object_name,
                        object_url,
                        event_time,
                    ),
                )

            connection.commit()

        result = {
            "status": "success",
            "message": "Object metadata inserted into MySQL",
            "bucket_name": bucket_name,
            "object_name": object_name,
            "object_url": object_url,
            "event_time": event_time,
        }

        return response.Response(
            ctx,
            response_data=json.dumps(result),
            headers={"Content-Type": "application/json"},
        )

    except Exception as ex:
        logging.getLogger().error("Error inserting object metadata: " + str(ex))

        return response.Response(
            ctx,
            response_data=json.dumps(
                {
                    "status": "error",
                    "message": str(ex),
                }
            ),
            headers={"Content-Type": "application/json"},
            status_code=500,
        )