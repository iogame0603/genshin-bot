from discord.app_commands.errors import AppCommandError

class GenshinCookieException(AppCommandError):
    """등록되지 않은 쿠키"""
    pass

class GenshinInvalidCookies(AppCommandError):
    """유효하지 않는 쿠키"""
    pass