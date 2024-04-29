import genshin
from Utils.Database.query import select_cookies
from typing import Dict, Any
from Types.cookie_type import Cookie
from Utils.util import RSA_CRYPTO
import os
from dotenv import load_dotenv
import exception as exc

load_dotenv()
__PRIVATE_KEY = os.getenv("RSA_PRIVATE_KEY")

def get_cookies(user_id: int) -> Dict[Cookie, Any]:
    cookies = select_cookies(user_id)
    if cookies == None:
        raise exc.GenshinCookieException
    return {
                Cookie.LTUID_V2.value: cookies[0],
                Cookie.LTMID_V2.value: RSA_CRYPTO.decrypt_msg(__PRIVATE_KEY, cookies[1]),
                Cookie.LTOKEN_V2.value: RSA_CRYPTO.decrypt_msg(__PRIVATE_KEY, cookies[2]),
            }

def get_genshin_client(user_id: int) -> genshin.Client:
    cookies = get_cookies(user_id)
    if cookies == None:
        raise exc.GenshinCookieException
    client = genshin.Client(lang="ko-kr")
    client.set_cookies(cookies=cookies)
    return client