import discord
from discord import app_commands
from discord.ext import commands

from config import settings
from apps import numer_on_app

from enum import Enum
from apps import stats_app

TITLE = "NumerOn"
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
        await ctx.send("NumerOnを開始します\n3桁の数字を当ててください")
        self.app_manager = numer_on_app.NumerOnAppManager(3)
        self.app_manager.start()
        print(f"origin = {self.app_manager.get_origin()}") 
        
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        if message.content[0] == self.bot.command_prefix:
            print(f"bot prefix. message.content[0] {self.bot.command_prefix}")
            return
        
        if self.app_manager is not None:
            print(f"state = {self.app_manager.state}")
            
            if self.app_manager.state == numer_on_app.NumerOnAppState.INIT:
                return
            if self.app_manager.state == numer_on_app.NumerOnAppState.PLAYING:
                print(f"start judge")
                eat, bite = self.app_manager.judge(message.content)
                print(f"Target: {message.content}, Eat: {eat}, Bite: {bite}")
                await message.channel.send(f"Eat: {eat}, Bite: {bite}")
                
                # register participant
                self.app_manager.add_participant(message.author.id)
                
                if eat == 3:
                    winner = message.author.nick
                    winner_id = message.author.id
                    if winner is None:
                        winner = message.author.name
                    await message.channel.send(f"クリア！勝者は{winner}です！\n正解するまでに: {self.app_manager.get_judge_count()}回かかりました")
                    self.app_manager.state = numer_on_app.NumerOnAppState.FINISHED
                    stats_app.save_stats(TITLE, self.app_manager.participant_ids, winner) 
                return
            else:
                print(f"Game is finished.")
                return


async def setup(bot):
    await bot.add_cog(NumerOnAppCog(bot))