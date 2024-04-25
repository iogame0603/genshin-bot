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

        cafe_imagge_url = "https://cafeptthumb-phinf.pstatic.net/MjAyNDA0MDFfMTkx/MDAxNzExOTgwMDQwMDMw.7kqHm2gxDYXT37Rvc0U64fBALzmfyVEDBnfbyLPFNF0g.xL4EF9pycJMPnMgIjY35nu6rY24SFPWkU0S5TW5uwpUg.PNG/%25EB%2584%25A4%25EC%259D%25B4%25EB%25B2%2584.png?type=f150_150_mask"
        
        p: Pagination = Pagination(interaction, title="원신 공식카페 공지", data=noticeList, offset=5, image_url=cafe_imagge_url, defer=True)
        await p.embed_pagination()

def get_notice():
    """원신 공식카페의 공지 가져오기\n
    return List[게시글 이름, 게시글 url]"""

    url = "https://cafe.naver.com/MyCafeIntro.nhn?clubid=29893655"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
               "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
               "Accept-Encoding": "gzip, deflate, br, zstd"}
    req = requests.get(url=url, headers=headers)
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