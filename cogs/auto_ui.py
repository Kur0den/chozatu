import discord
from discord.ext import commands
from discord_embed_extensions import make
import asyncio
import re

status_dict = {
    "offline": "オフライン",
    "online": "オンライン",
    "idle": "退席中",
    "dnd": "取り込み中",
    "do_not_disturb": "取り込み中"
}
class Autoui(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await self.bot.unei_ch.send(
            embed=make(
                title='ユーザ情報',
                description='この情報で表示されている時間情報はUTCを用いられています。\n日本(東京)時間への変換は `+9時間` してください。',
                author={"name": f'{member.name}(ID:{member.id})', "icon_url": member.avatar_url},
                fields=[
                    {"name": "アカウント作成日時", "value": member.created_at},
                    {"name": "サーバー参加日時", "value": member.joined_at},
                    {"name": "ステータス", "value": status_dict[str(member.status)]},
                    {"name": "ロール", "value": ', '.join([r.mention for r in member.roles])}
                ]
            ))

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        async for msg in self.bot.unei_ch.history(limit=50):
            if not msg.author.id == 804649928638595093:
                continue
            if len(msg.embeds) > 0:
                embed = msg.embeds[0]
                if not embed.title == 'ユーザ情報':
                    continue
                if embed.author.name.endswith(f'{str(member.id)})'):
                    await msg.edit(embed=make(
                        title=embed.title,
                        description='サーバー脱退済み',
                        author={"name": embed.author.name, "icon_url": embed.author.icon_url}
                    ))
                    return

def setup(bot):
    return bot.add_cog(Autoui(bot))
