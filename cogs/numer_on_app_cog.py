import discord
from discord import app_commands
from discord.ext import commands

from config import settings
from apps import numer_on_app


class NumerOnAppCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        super().__init__()
        self.bot = bot
        self.app = numer_on_app.NumerOnApp()
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Cogs", "NumerOnAppCog is reloaded.")
    
    # ここに具体的な処理を書く

    @commands.command()
    async def numer_on(self, ctx: commands.Context):
        await ctx.send("start numer_on")

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
                self.app.increment()
                await message.channel.send(f"n = {self.app.n}")
        except (IndexError, ValueError):
            await message.send("Invalid input. Please provide a number.")

async def setup(bot):
    await bot.add_cog(NumerOnAppCog(bot))