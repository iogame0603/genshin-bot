import genshin
from Utils.Database.query import select_cookies
from typing import Dict, Any
from Types.cookie_type import CookieTypeLiteral, CookieType
from Utils.util import RSA_CRYPTO
import os
from dotenv import load_dotenv

load_dotenv()
__PRIVATE_KEY = os.getenv("RSA_PRIVATE_KEY")

def get_cookies(user_id: int) -> Dict[CookieTypeLiteral, Any]:
    cookies = select_cookies(user_id)
    return None if cookies == None else {
                                            CookieType.LTUID_V2: cookies[0],
                                            CookieType.LTMID_V2: RSA_CRYPTO.decrypt_msg(__PRIVATE_KEY, cookies[1]),
                                            CookieType.LTOKEN_V2: RSA_CRYPTO.decrypt_msg(__PRIVATE_KEY, cookies[2]),
                                        }

def get_genshin_client(user_id: int) -> genshin.Client:
    cookies = get_cookies(user_id)
    if cookies == None:
        return None
    client = genshin.Client(lang="ko-kr")
    client.set_cookies(cookies=cookies)
    return client