import discord
from discord.ext import commands
import os
import datetime
import pytz
import aiohttp
import random

timezone = pytz.timezone('UTC')

UB_API_TOKEN = os.environ.get('CHOZATU_UB_API_TOKEN')
ub_api_url = 'https://unbelievaboat.com/api/v1/guilds/733707710784340100/users/'
header = {'Authorization': UB_API_TOKEN, 'Accept': 'application/json'}


def to_min(time_delta):
    seconds = time_delta.seconds
    return seconds // 60

class Voice_money(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member.bot:
            return
            
        # join
        # 新規で入る、入ったチャンネルがafkチャンネルではない
        if before.channel == None and not after.afk:
            await self.bot.voice_time_ch.send(f'{member.id} {datetime.datetime.now(tz=timezone)}')
            print('新規参加')
            return

        # 終了
        # 元のチャンネルがNoneではない
        if not before.channel == None:
            # 元のチャンネルがafkではない、afterがNone
            if not before.afk and after.channel == None:
                async for msg in self.bot.voice_time_ch.history():
                    if msg.content.startswith(str(member.id)):
                        await msg.delete()

                        splited = msg.content.split(' ', 1)
                        user_id = splited[0]
                        time = datetime.datetime.strptime(splited[1], '%Y-%m-%d %H:%M:%S.%f%z')
                        now = datetime.datetime.now(tz=timezone)
                        delta = now - time
                        min = to_min(delta)
                        print(min)

                        money = random.randint(self.bot.voice_money_min, self.bot.voice_money_max)

                        async with aiohttp.ClientSession(headers=header) as session:
                            await session.patch(url=f'{ub_api_url}{member.id}', json={'cash': (min // self.bot.voice_give_per) * money, 'reason': f'ボイスチャット報酬({min}分)'})

                        print('終了')
                        return

        # afkへ移動
        # 入ったチャンネルがafkチャンネル、joinではない
        if after.afk and not before.channel == None:
            async for msg in self.bot.voice_time_ch.history():
                if msg.content.startswith(str(member.id)):
                    await msg.delete()
                    splited = msg.content.split(' ', 1)
                    user_id = splited[0]
                    time = datetime.datetime.strptime(splited[1], '%Y-%m-%d %H:%M:%S.%f%z')
                    now = datetime.datetime.now(tz=timezone)
                    delta = now - time
                    min = to_min(delta)
                    print(min)

                    money = random.randint(self.bot.voice_money_min, self.bot.voice_money_max)

                    async with aiohttp.ClientSession(headers=header) as session:
                        await session.patch(url=f'{ub_api_url}{member.id}', json={'cash': (min // self.bot.voice_give_per) * money, 'reason': f'ボイスチャット報酬({min}分)'})

                    print('afkへ移動')
                    return

        # afk -> 通常
        # 元のチャンネルがNoneではない
        if not before.channel == None and not after.channel == None:
            # 元のチャンネルがafk、afterがafkではない
            if before.afk and not after.afk:
                await self.bot.voice_time_ch.send(f'{member.id} {datetime.datetime.now(tz=timezone)}')
                print('通常へ移動')
                return

        # afkへ参加(処理なし)
        if before.channel == None:
            if after.afk:
                print('afkへ参加')
                return


def setup(bot):
    return bot.add_cog(Voice_money(bot))
