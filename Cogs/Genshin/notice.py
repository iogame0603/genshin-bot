import discord
from discord import app_commands
from discord.ext import commands
import requests
from bs4 import BeautifulSoup
from urllib import parse

from Utils.util import Pagination

class Notice(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @app_commands.command(name="공지", description="원신 공식카페의 공지를 확인합니다.")
    async def notice(self, interaction: discord.Interaction):
        await interaction.response.defer()

        noticeList = get_notice()

        if noticeList[0] == None:
            await interaction.response.send_message(content=f"공지를 가져오는 중 에러가 발생했습니다. (code: {noticeList[1]})", ephemeral=True)
            return

        cafe_imagge_url = "https://cafeptthumb-phinf.pstatic.net/MjAyMzExMDhfMjg5/MDAxNjk5NDEwNzY2MTYz.ZxdWHM87UFZXRLccFndyEHeveO4JeKsT6Zg-y37UPOQg.ydetICo0M45KZ84wY9-wGL3Y8Xn3S8MUyjNOLLOtArcg.PNG/02%25E5%259C%2586%25E5%25BD%25A2%25E5%25A4%25B4%25E5%2583%258F%25E7%2594%25A8_%2528For_rounded_avatars%2529.png?type=f150_150_mask"
        
        p: Pagination = Pagination(interaction, title="원신 공식카페 공지", data=noticeList, offset=5, image_url=cafe_imagge_url, defer=True)
        await p.embed_pagination()

def get_notice():
    """원신 공식카페의 공지 가져오기\n
    return List[게시글 이름, 게시글 url]"""

    url = "https://cafe.naver.com/MyCafeIntro.nhn?clubid=29893655"
    req = requests.get(url=url)
    if req.status_code != 200:
        return [None, req.status_code]
    soup = BeautifulSoup(req.text, "html.parser")

    noticeUrlList = []
    noticeNameList = []

    soup_1 = soup.select(selector=".board-notice.type_main")
    for s in soup_1:
        a_tag = s.find_all("a", {"class", "article"})
        for a in a_tag:
            articleid = parse.parse_qs(parse.urlsplit(url=a["href"]).query)["articleid"][0]
            noticeUrlList.append(f"https://cafe.naver.com/genshin/{articleid}")

            noticeNameList.append(a.text.replace("\t", "").replace("\n", ""))

    return [noticeNameList, noticeUrlList]

async def setup(bot:commands.Bot):
    await bot.add_cog(Notice(bot))