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
        await ctx.send("Just Timeを開始します。`/start`が実行されてから5秒経ったと思うタイミングでメッセージを送ってください！\nまずは参加者を登録します。参加する方は何かしらメッセージを送ってください\n`/start`を入力すると参加者の募集が終わり計測が始まります。")
        self.app_manager = just_time_app.JustTimeAppManager()
        self.app_manager.register()
    
    @commands.command(name="register")
    async def register(self, ctx: commands.Context):
        id = ctx.author.id
        self.app_manager.add_participant(id)
    
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
            print(f"bot prefix. message[0]: {message.content[0]}")
            return
        if self.app_manager is None:
            return
        
        if self.app_manager.state == just_time_app.JustTimeAppState.INIT:
            print(f"state = {self.app_manager.state}")
            return
        elif self.app_manager.state == just_time_app.JustTimeAppState.FINISHED:
            print(f"state = {self.app_manager.state}")
            return
        elif self.app_manager.state == just_time_app.JustTimeAppState.REGISTERING:
            print(f"state = {self.app_manager.state}")
            self.app_manager.add_participant(message.author.id)
            return
        elif self.app_manager.state == just_time_app.JustTimeAppState.PLAYING:
            print(f"state = {self.app_manager.state}")
            participant_id = message.author.id
            time = message.created_at
            self.app_manager.record_time(message.author.id, time)
            print(f"participant_id = {participant_id}, time = {time}")

            if self.app_manager.is_finished():
                for participant_id, diff in self.app_manager.get_diff():
                    member = await message.guild.fetch_member(participant_id)
                    if member is not None:
                        name = member.nick if member.nick is not None else member.name
                        print(f"member: {repr(member)}, name: {name}")
                        await message.channel.send(f"{name}さんの時間は{diff:.2f}秒でした。")
                    else:
                        print(f"Member with ID {participant_id} not found")




async def setup(bot):
    await bot.add_cog(JustTimeAppCog(bot))