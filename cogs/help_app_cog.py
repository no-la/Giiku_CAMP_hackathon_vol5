import discord
from discord import app_commands
from discord.ext import commands

from config import settings
from apps import help_app


class HelpAppCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        super().__init__()
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Cogs", "HelpAppCog is reloaded.")
    
    # ここに具体的な処理を書く
    @commands.command(name="commands")
    async def send_help(self, ctx: commands.Context):
        embed = discord.Embed()
        embed.title = "コマンドの説明"
        embed.description = ""
        embed.add_field(
            name="五目並べ",
            value="""
                `/gomoku` で開始
                """,
            inline=False
        )
        embed.add_field(
            name="Just Time",
            value="""
            `/ju` で開始
            """,
            inline=False
        )
        embed.add_field(
            name="数字当てゲーム",
            value="""
            `/nu` で開始
            """,
            inline=False
        )
        embed.color = 0xD5D5E4
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(HelpAppCog(bot))