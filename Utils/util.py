## rsa util
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

class RSA_CRYPTO:
    """암호화 관련 Util"""
    def __create_keys(self):
        key = RSA.generate(2048)
        private_key = key.export_key()
        public_key = key.public_key().export_key()

        print(private_key)

        print(public_key)

    # 암호화
    @classmethod
    def encrypt_msg(cls, public_key, message):
        rsa_key = RSA.import_key(public_key)
        cipher = PKCS1_OAEP.new(rsa_key)
        encrypted_message = cipher.encrypt(message.encode())
        return encrypted_message

    # 복호화
    @classmethod
    def decrypt_msg(cls, private_key, encrypted_message):
        rsa_key = RSA.import_key(private_key)
        cipher = PKCS1_OAEP.new(rsa_key)
        decrypted_message = cipher.decrypt(encrypted_message).decode()
        return decrypted_message


## discord pagination util
import discord
from typing import List, Any, Union
import math

class PaginationBtn(discord.ui.View):
    def __init__(self, author: Union[discord.Member, discord.User], title: str, data: List[List[Any]], offset: int, image_url: str, defer: bool) -> None:
        self.author = author

        self.title = title
        self.data = data
        self.offset = offset
        self.image_url = image_url
        self.defer = defer

        self.current_page = 1
        self.max_page = math.ceil(len(data[0]) / offset)

        super().__init__(timeout=10)

    def __get_embed_page_data(self) -> discord.Embed:
        title_data = self.data[0]
        description_data = self.data[1]

        start = self.offset * (self.current_page - 1)
        end = self.current_page * self.offset

        embed_data = [title_data[start:end], description_data[start:end]]

        embed = discord.Embed(title=self.title)
        embed.set_thumbnail(url=self.image_url)
        embed.clear_fields()
        for o in range(self.offset):
            embed.add_field(name=embed_data[0][o], value=embed_data[1][o], inline=False)
        embed.set_footer(text=f"{self.current_page} / {self.max_page}")

        return embed

    def __btn_control(self):
        if self.current_page == 1:
            self.children[0].disabled = True
        if self.current_page != 1:
            self.children[0].disabled = False
        if self.max_page == self.current_page:
            self.children[1].disabled = True
        if self.max_page != self.current_page:
            self.children[1].disabled = False

        return self

    @discord.ui.button(emoji="⬅️", custom_id="prev_btn", disabled=True)
    async def prev_btn(self, interaction: discord.Interaction, btn: discord.ui.Button):
        self.current_page -= 1
        await interaction.response.edit_message(embed=self.__get_embed_page_data(), view=self.__btn_control())

    @discord.ui.button(emoji="➡️", custom_id="next_btn", disabled=False)
    async def next_btn(self, interaction: discord.Interaction, btn: discord.ui.Button):
        self.current_page += 1
        await interaction.response.edit_message(embed=self.__get_embed_page_data(), view=self.__btn_control())

    async def interaction_check(self, interaction: discord.Interaction[discord.Client]) -> bool:
        return interaction.user.id == self.author.id
    
    async def on_timeout(self):
        await self.message.edit(view=None)

class Pagination():
    """디스코드 페이징처리 관련 Util"""

    def __init__(self, interaction: discord.Interaction, title: str, data: List[List[Any]], offset: int, image_url: str = None, defer: bool = False):
        self.interaction = interaction

        self.title = title
        self.data = data
        self.offset = offset
        self.image_url = image_url
        self.defer = defer

        self.max_page = math.ceil(len(self.data[0]) / self.offset)

    async def embed_pagination(self):
        """title: :class:`str`
                임베드에서 사용할 title

            image_url: :class:`str`
                임베드에서 사용할 이미지 url

            data: :class:`List[List[Any]]`
                임베드에 들어갈 데이터 리스트\n
                0번째 index는 제목\n
                1번째 index는 설명

            offset: :class:`int`
                임베드에 표시될 데이터 개수
            defer: :class`bool`
                default: False\n
                await interaction.response.defer()을 사용했을 경우 True"""
        
        if len(self.data) > 2:
            raise ValueError("data의 길이는 2 이하로 들어와야합니다.")
        
        embed = discord.Embed(title=self.title)
        embed.set_thumbnail(url=self.image_url)
        for o in range(self.offset):
            embed.add_field(name=self.data[0][o], value=self.data[1][o], inline=False)
        embed.set_footer(text=f"1 / {self.max_page}")

        p_btn = PaginationBtn(author=self.interaction.user, title=self.title, data=self.data, offset=self.offset, image_url=self.image_url, defer=self.defer)

        if self.defer:
            p_btn.message = await self.interaction.followup.send(embed=embed, view=p_btn)
        else:
            p_btn.message = await self.interaction.response.send_message(embed=embed, view=p_btn)


## logging util
import logging
from datetime import datetime

class Logging:
    LOGGER = logging.getLogger(__name__)

    logging.basicConfig(
        filename=f"Log/{datetime.now().strftime('%Y%m%d')}.log",
        format="%(asctime)s [%(levelname)s]\t%(filename)s (line: %(lineno)d) --> %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        filemode="w",
        level=30
    )