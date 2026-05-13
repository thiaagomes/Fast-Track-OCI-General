from flask import Flask, render_template_string
import pymysql


app = Flask(__name__)


DB_HOST = "IP_PRIVADO"
DB_PORT = 3306
DB_USER = "thiaagomes"
DB_PASSWORD = "COLOQUE_USUARIO_AQUI"
DB_NAME = "fast_track_db"


HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>OCI Fast Track - Processed Files</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f5f7fa;
            margin: 0;
            padding: 40px;
            color: #1f2937;
        }

        .container {
            max-width: 1200px;
            margin: auto;
            background: #ffffff;
            border-radius: 16px;
            padding: 32px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        }

        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 16px;
            margin-bottom: 24px;
        }

        h1 {
            margin: 0;
            font-size: 28px;
            color: #111827;
        }

        .subtitle {
            margin-top: 8px;
            color: #6b7280;
            font-size: 15px;
        }

        .badge {
            background: #eef2ff;
            color: #3730a3;
            padding: 10px 16px;
            border-radius: 999px;
            font-weight: bold;
            white-space: nowrap;
        }

        .flow {
            background: #f9fafb;
            border: 1px solid #e5e7eb;
            border-radius: 12px;
            padding: 16px;
            margin-bottom: 24px;
            color: #374151;
            font-size: 14px;
        }

        .actions {
            margin-bottom: 20px;
        }

        .button {
            display: inline-block;
            background: #111827;
            color: #ffffff;
            text-decoration: none;
            padding: 10px 16px;
            border-radius: 10px;
            font-weight: bold;
        }

        .button:hover {
            background: #374151;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            overflow: hidden;
            border-radius: 12px;
        }

        th {
            background: #111827;
            color: #ffffff;
            text-align: left;
            padding: 14px;
            font-size: 13px;
        }

        td {
            padding: 14px;
            border-bottom: 1px solid #e5e7eb;
            font-size: 13px;
            vertical-align: top;
        }

        tr:hover {
            background: #f9fafb;
        }

        a {
            color: #2563eb;
            text-decoration: none;
        }

        a:hover {
            text-decoration: underline;
        }

        .empty {
            text-align: center;
            padding: 40px;
            color: #6b7280;
            background: #f9fafb;
            border-radius: 12px;
        }

        .object-name {
            font-weight: bold;
            color: #111827;
        }

        .url-cell {
            max-width: 420px;
            word-break: break-all;
        }

        .footer {
            margin-top: 24px;
            color: #9ca3af;
            font-size: 12px;
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div>
                <h1>OCI Fast Track - Processed Files</h1>
                <div class="subtitle">
                    Files captured from Object Storage events and registered by OCI Functions into MySQL.
                </div>
            </div>
            <div class="badge">
                Total: {{ files|length }}
            </div>
        </div>

        <div class="flow">
            <strong>Flow:</strong>
            Object Storage Bucket → OCI Events → OCI Function → MySQL → VM Flask App
        </div>

        <div class="actions">
            <a class="button" href="/">Refresh files</a>
        </div>

        {% if files %}
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Bucket</th>
                    <th>Object Name</th>
                    <th>Object URL</th>
                    <th>Event Time</th>
                    <th>Created At</th>
                </tr>
            </thead>
            <tbody>
                {% for file in files %}
                <tr>
                    <td>{{ file.id }}</td>
                    <td>{{ file.bucket_name }}</td>
                    <td class="object-name">{{ file.object_name }}</td>
                    <td class="url-cell">
                        {% if file.object_url %}
                        <a href="{{ file.object_url }}" target="_blank">{{ file.object_url }}</a>
                        {% else %}
                        -
                        {% endif %}
                    </td>
                    <td>{{ file.event_time }}</td>
                    <td>{{ file.created_at }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
        {% else %}
        <div class="empty">
            No files found yet. Upload a file to the Object Storage bucket and refresh this page.
        </div>
        {% endif %}

        <div class="footer">
            Running on OCI Compute | Querying MySQL Database System
        </div>
    </div>
</body>
</html>
"""


def get_files():
    connection = pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor,
        connect_timeout=10,
    )

    with connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    id,
                    bucket_name,
                    object_name,
                    object_url,
                    event_time,
                    created_at
                FROM bucket_files
                ORDER BY id DESC
                """
            )
            return cursor.fetchall()


@app.route("/")
def index():
    files = get_files()
    return render_template_string(HTML_TEMPLATE, files=files)


@app.route("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)