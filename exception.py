from discord.app_commands.errors import AppCommandError

class BaseCookieException(AppCommandError):
    """Cookie Exception"""
    pass

class GenshinCookieException(BaseCookieException):
    """등록되지 않은 쿠키"""
    pass

class GenshinInvalidCookies(BaseCookieException):
    """유효하지 않는 쿠키"""
    pass