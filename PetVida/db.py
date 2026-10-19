import os
import pyodbc
from contextlib import contextmanager


def montar_connection_string():
    servidor = os.getenv("DB_SERVER", ".")
    banco = os.getenv("DB_NAME", "PetVida")
    driver = os.getenv("DB_DRIVER", "ODBC Driver 18 for SQL Server")
    usuario = os.getenv("DB_USER")
    senha = os.getenv("DB_PASSWORD")

    conn_str = (
        f"DRIVER={{{driver}}};"
        f"SERVER={servidor};"
        f"DATABASE={banco};"
        "TrustServerCertificate=yes;"
    )

    if usuario or senha:
        if not usuario or not senha:
            raise ValueError("Defina DB_USER e DB_PASSWORD juntos.")
        conn_str += f"UID={usuario};PWD={senha};"
    else:
        conn_str += "Trusted_Connection=yes;"

    return conn_str


def conectar():
    try:
        return pyodbc.connect(
            montar_connection_string(),
            autocommit=False
        )
    except pyodbc.OperationalError as erro:
        raise ConnectionError(
            "Não foi possível conectar ao SQL Server."
        ) from erro


def testar_conexao():
    conn = conectar()

    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT @@SERVERNAME, DB_NAME(), @@VERSION"
        )
        resultado = cursor.fetchone()

        return resultado[0], resultado[1], resultado[2]

    finally:
        conn.close()


@contextmanager
def transacao():
    conn = conectar()

    try:
        cursor = conn.cursor()
        yield cursor
        conn.commit()

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()
