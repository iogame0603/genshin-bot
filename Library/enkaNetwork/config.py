class Config:
    LANG = ""
    LANG_LIST = ["ar", "de", "en", "es", "fr", "id", "it", "ja", "ko", "pt", "ru", "th", "tr", "uk", "vi", "ch-CN", "zh-TW"]

    ENKA_PROTOCOL = "https"
    ENKA_API_URL = "enka.network"
    ASSET_PROTOCOL = "https"

    class PATH:
        ASSET_GITHUB_PATH = "raw.githubusercontent.com/EnkaNetwork/API-docs/master/store/"
        ASSET_GITLAB_PATH = "gitlab.com/Dimbreath/AnimeGameData/-/raw/main/ExcelBinOutput/"
        ASSET_GITLAB_TEXTMAP_PATH = "gitlab.com/Dimbreath/AnimeGameData/-/raw/main/TextMap/"
        ASSET_FILE_PATH = "Library/enkaNetwork/assets/"

    class GITHUB_ASSET:
        CHARACTER = "characters.json"
        NAME_CARDS = "namecards.json"
        LOC = "loc.json"
        PFPS = "pfps.json"

    class GITLAB_ASSET:
        SKILL = "AvatarSkillExcelConfigData.json"
        TEXTMAP_KR = "TextMapKR.json"