import discord
from discord import app_commands
from discord.ext import commands

from config import settings
from apps import numer_on_app

from enum import Enum

class NumerOnAppCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        super().__init__()
        self.bot = bot
        self.app_manager = None
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Cogs", "NumerOnAppCog is reloaded.")
    

    @commands.command(name="nu")
    async def numer_on(self, ctx: commands.Context):
        await ctx.send("NumerOnを開始します")
        self.app_manager = numer_on_app.NumerOnAppManager(3)
        self.app_manager.start()
        await ctx.send(f"origin = {self.app_manager.get_origin()}") 
        
    @commands.command(name="j")
    async def judge(self, ctx: commands.context, target: str = ""):
        # Precondition
        if target == "":
            await ctx.send(f"引数として数字を入力してください")
        if not target.isdigit():
            await ctx.send(f"数字を入力してください")
            return
    
        try:
            eat, bite = self.app_manager.judge(target)
            await ctx.send(f"Target: {target}, Eat: {eat}, Bite: {bite}")
        except ValueError as e:
            print(e)
        

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        if message.content[0] ==  self.bot.command_prefix:
            await message.channel.send("bot prefix")
            return
        
        if self.app_manager is not None:
            await message.channel.send(f"state = {self.app_manager.state}")
            if self.app_manager.state == numer_on_app.NumerOnAppState.PLAYING:
                await message.channel.send(f"playing")
            
            if self.app_manager.state == numer_on_app.NumerOnAppState.INIT:
                return
            if self.app_manager.state == numer_on_app.NumerOnAppState.PLAYING:
                await message.channel.send(f"start judge")
                eat, bite = self.app_manager.judge(message.content)
                await message.channel.send(f"Target: {message.content}, Eat: {eat}, Bite: {bite}")
                if eat == 3:
                    await message.channel.send("Game is finished.")
                    self.app_manager.state = numer_on_app.NumerOnAppState.FINISHED
                return
            else:
                await message.channel.send("Game is finished.")
                return
        


async def setup(bot):
    await bot.add_cog(NumerOnAppCog(bot))