import discord
from discord import app_commands
from discord.ext import commands

from config import settings
from apps import just_time_app


class JustTimeAppCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        super().__init__()
        self.bot = bot
        self.app_manager = None
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Cogs", "JustTimeAppCog is reloaded.")

    @commands.command(name="ju")
    async def numer_on(self, ctx: commands.Context):
        await ctx.send("Just Timeを開始します。5秒経ったら何らかのメッセージを送ってください。\n準備ができたら`/start`を入力してください。計測が始まります。")
        self.app_manager = just_time_app.JustTimeAppManager()
        self.app_manager.start()
        
    @commands.command(name="start")
    async def start(self, ctx: commands.Context):
        start_time = ctx.message.created_at
        self.app_manager.start(start_time)
        await ctx.send("計測を開始しました。5秒経ったら何らかのメッセージを送ってください。")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        if message.content[0] == self.bot.command_prefix:
            print(f"bot prefix. message.content[0] {self.bot.command_prefix}")
            return

        if self.app_manager is not None:
            participant = message.author.nick
            if participant is None:
                participant = message.author.name
            print(f"participant = {participant}")
            time = message.created_at
            print(f"time = {time}")
            diff = self.app_manager.judge(time)
            print(f"diff = {diff}")
            await message.channel.send(f"{participant}さんの時間は{diff:.2f}秒でした。")
#             print(f"state = {self.app_manager.state}")
# 
#             if self.app_manager.state == numer_on_app.NumerOnAppState.INIT:
#                 return
#             if self.app_manager.state == numer_on_app.NumerOnAppState.PLAYING:
#                 print(f"start judge")
#                 eat, bite = self.app_manager.judge(message.content)
#                 print(f"Target: {message.content}, Eat: {eat}, Bite: {bite}")
#                 await message.channel.send(f"Eat: {eat}, Bite: {bite}")
#                 if eat == 3:
#                     winner = message.author.nick
#                     if winner is None:
#                         winner = message.author.name
#                     await message.channel.send(f"クリア！勝者は{winner}です！\n正解するまでに: {self.app_manager.get_judge_count()}回かかりました")
#                     self.app_manager.state = numer_on_app.NumerOnAppState.FINISHED
#                 return
#             else:
#                 print(f"Game is finished.")
#                 return



async def setup(bot):
    await bot.add_cog(JustTimeAppCog(bot))