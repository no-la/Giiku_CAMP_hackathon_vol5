import discord
from discord.ext import commands

import settings

import awake

class MyBot(commands.Bot):
    def __init__(self, intents: discord.Intents = discord.Intents.default()) -> None:
        super().__init__(command_prefix="/", intents=intents)
        self.guild: discord.Guild = ... # setup_hookで初期化する

    
    async def setup_hook(self):
        guild = discord.Object(settings.GUILD_ID)
        # Cogを読み込む
        for m in ["test_cog"]:
            await self.load_extension(f"cogs.{m}")
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
