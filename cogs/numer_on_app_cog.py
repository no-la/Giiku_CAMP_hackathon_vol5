import discord
from discord import app_commands
from discord.ext import commands

from config import settings
from apps import numer_on_app


class NumerOnAppCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        super().__init__()
        self.bot = bot
        self.app = None
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Cogs", "NumerOnAppCog is reloaded.")
    

    @commands.command(name="nu")
    async def numer_on(self, ctx: commands.Context):
        await ctx.send("NumerOnを開始します")
        self.app = numer_on_app.NumerOnApp(numer_on_app.random_number(3))
        await ctx.send(f"origin = {self.app.origin}")
        
    @commands.command(name="j")
    async def judge(self, ctx: commands.context, digit: str = ""):
        if digit == "":
            await ctx.send(f"引数として数字を入力してください")
        if not digit.isdigit():
            await ctx.send(f"数字を入力してください")
            return
        await ctx.send("start")
        await ctx.send(f"digit = {digit}")
        

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        if message.content[0] ==  self.bot.command_prefix:
            await message.channel.send("bot prefix")
            return
        try:
            message_value = int(message.content.split()[0])
            if message_value == 0:
                await message.channel.send("zero !")
            else:
                await message.channel.send("other")
                self.app.judge()
                await message.channel.send(f"n = {self.app.judge_count}")
        except (IndexError, ValueError):
            await message.send("Invalid input. Please provide a number.")

async def setup(bot):
    await bot.add_cog(NumerOnAppCog(bot))