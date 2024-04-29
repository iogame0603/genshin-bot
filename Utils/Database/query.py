import pymysql

import os
from dotenv import load_dotenv

from Types.cookie_type import Cookie
from Utils.util import RSA_CRYPTO, Logging

from typing import Union

load_dotenv()

HOST = os.getenv("DB_HOST")
PORT = int(os.getenv("DB_PORT"))
ID = os.getenv("DB_ID")
PW = os.getenv("DB_PW")
DATABASE = os.getenv("DB_NAME")

PUBLIC_KEY = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAuPuuyo3veWCTuFxT1ZV6
JTOwHvkqEx9WGKKeBBQmf9lFEEbw9K0DE6Km+q6gha5gmcprONhMjIbRmmbmgeZ3
rDM6kVsK8PblpgHSR3ZKfvi2hqK6gPOuAfucrH8Xzn3f2K52FSb3rPoImYSjsKlN
e+0tIDv8cYL1PXY+TH2s2vTXOIVKqSrPyMzukfS73W/OlDc3zcyD82YqDR9mMXYx
t70bdwHD6orMHsp+1xH80afE/6Zmqg7EbhuT7rGIw6u2DOIDXyxd8UVxMqPJ9RoS
wyR02lGqGrUd4byBn1QZPhF2+vfgxCuu8E5O0xc53fr+RnJ4GKGAue0DqhoOh/2k
YQIDAQAB
-----END PUBLIC KEY-----"""

def __connect_database(func):
    def connect_database(*args, **kwargs):
        import exception as exc

        conn = None
        cursor = None
        try:
            conn = pymysql.connect(host=HOST, port=PORT, user=ID, password=PW, database=DATABASE, charset="utf8")
            cursor = conn.cursor()

            result = func(cursor, *args, **kwargs)

            conn.commit()

            database_close(cursor, conn)

            return result
        except pymysql.Error as se:
            Logging.LOGGER.exception(f"database 작업 중 에러 발생")
            database_close(cursor, conn)
            raise exc.DataBaseException()
        except Exception as e:
            Logging.LOGGER.exception(f"에러 발생")
            database_close(cursor, conn)
            raise exc.DataBaseException()

    return connect_database


def database_close(cursor, conn):
    if cursor:
        cursor.close()
    if conn:
        conn.close()

        
@__connect_database
def select_cookies(cursor, user_id: int):
    query = f"SELECT {Cookie.LTUID_V2}, {Cookie.LTMID_V2}, {Cookie.LTOKEN_V2} FROM USER_INFO WHERE USER_ID = %s"
    cursor.execute(query, (user_id,))
    return cursor.fetchone()

@__connect_database
def insert_cookies(cursor, user_id: int, ltuid_v2: str, ltmid_v2: str, ltoken_v2: str):
    query = "INSERT INTO USER_INFO VALUES (%s, %s, %s, %s)"

    ltmid_v2 = RSA_CRYPTO.encrypt_msg(PUBLIC_KEY, ltmid_v2)
    ltoken_v2 = RSA_CRYPTO.encrypt_msg(PUBLIC_KEY, ltoken_v2)

    cursor.execute(query, (user_id, ltuid_v2, ltmid_v2, ltoken_v2))

@__connect_database
def update_cookies(cursor, user_id: int, cookie_type: Cookie, cookie: Union[int, str]):
    query = f"UPDATE USER_INFO SET {cookie_type.upper()} = %s WHERE USER_ID = %s"

    if cookie_type != Cookie.LTUID_V2:
        cookie = RSA_CRYPTO.encrypt_msg(PUBLIC_KEY, cookie)

    cursor.execute(query, (cookie, user_id,))

@__connect_database
def delete_cookies(cursor, user_id: int):
    query = "DELETE FROM USER_INFO WHERE USER_ID = %s"
    cursor.execute(query, (user_id,))

@__connect_database
def select_users(cursor):
    query = "SELECT USER_ID FROM USER_INFO"
    cursor.execute(query)
    return cursor.fetchall()