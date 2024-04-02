from typing import Literal

class CookieType:
    LTUID_V2 = "ltuid_v2"
    LTMID_V2 = "ltmid_v2"
    LTOKEN_V2 = "ltoken_v2"

CookieTypeLiteral = Literal["ltuid_v2", "ltmid_v2", "ltoken_v2",]