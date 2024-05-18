import discord
import os
from discord.ext import commands

from config import settings

import awake

class MyBot(commands.Bot):
    def __init__(self, intents: discord.Intents = discord.Intents.default()) -> None:
        super().__init__(command_prefix="/", intents=intents)
        self.guild: discord.Guild = ... # setup_hookで初期化する

    
    async def setup_hook(self):
        guild = discord.Object(settings.GUILD_ID)
        # cogsフォルダ内のすべての.pyファイルを取得
        cog_files = [f[:-3] for f in os.listdir('./cogs') if f.endswith('.py')]
        
        # Cogを読み込む
        for cog in cog_files:
            await self.load_extension(f"cogs.{cog}")
            
        appcommand_list = await self.tree.sync(guild=guild)
        
        print(
            "Available App Commands",
            "-"*10,
            *appcommand_list,
            "-"*10,
            sep="\n"
            )


#Discordオブジェクトの生成
bot = MyBot(intents=discord.Intents.all())

# Botの起動とDiscordサーバーへの接続
bot.run(settings.TOKEN)
