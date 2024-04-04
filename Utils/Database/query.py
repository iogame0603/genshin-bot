import sqlite3

from Types.cookie_type import Cookie
from dotenv import load_dotenv
from Utils.util import RSA_CRYPTO, Logging

load_dotenv()

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
        conn = None
        cursor = None
        try:
            conn = sqlite3.connect("databases/user_info.db")
            cursor = conn.cursor()

            result = func(cursor, *args, **kwargs)

            conn.commit()

            cursor.close()
            conn.close()

            return result
        except sqlite3.Error as se:
            database_close(cursor, conn)
            Logging.LOGGER.error(f"database 작업 중 에러 발생")
        except Exception as e:
            database_close(cursor, conn)
            Logging.LOGGER.error(f"database 작업 중 에러 발생")
    return connect_database


def database_close(cursor, conn):
    if cursor:
        cursor.close()
    if conn:
        conn.close()

        
@__connect_database
def __create_cookie_info_table(cursor: sqlite3.Cursor):
    query = """CREATE TABLE USER_INFO(
        USER_ID INT PRIMARY KEY,
        LTUID_V2 STR,
        LTMID_V2 STR,
        LTOKEN_V2 STR
    )"""
    cursor.execute(query)

@__connect_database
def select_cookies(cursor: sqlite3.Cursor, user_id: int):
    query = f"SELECT {Cookie.LTUID_V2}, {Cookie.LTMID_V2}, {Cookie.LTOKEN_V2} FROM USER_INFO WHERE USER_ID = ?"
    cursor.execute(query, (user_id,))
    return cursor.fetchone()

@__connect_database
def insert_cookies(cursor: sqlite3.Cursor, user_id: int, ltuid_v2: str, ltmid_v2: str, ltoken_v2: str):
    query = f"INSERT INTO USER_INFO VALUES (?, ?, ?, ?)"

    ltmid_v2 = RSA_CRYPTO.encrypt_msg(PUBLIC_KEY, ltmid_v2)
    ltoken_v2 = RSA_CRYPTO.encrypt_msg(PUBLIC_KEY, ltoken_v2)

    cursor.execute(query, (user_id, ltuid_v2, ltmid_v2, ltoken_v2))

@__connect_database
def update_cookies(cursor: sqlite3.Cursor, user_id: int, cookie_type: Cookie, cookie: str):
    query = f"UPDATE USER_INFO SET {cookie_type.upper()} = ? WHERE USER_ID = ?"

    if cookie != "":
        cookie = RSA_CRYPTO.encrypt_msg(PUBLIC_KEY, cookie)

    cursor.execute(query, (cookie, user_id,))

@__connect_database
def delete_cookies(cursor: sqlite3.Cursor, user_id: int):
    query = "DELETE FROM USER_INFO WHERE USER_ID = ?"
    cursor.execute(query, (user_id,))

@__connect_database
def select_users(cursor: sqlite3.Cursor):
    query = "SELECT USER_ID FROM USER_INFO"
    cursor.execute(query)
    return cursor.fetchall()