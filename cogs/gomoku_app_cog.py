import discord
from discord import app_commands
from discord.ext import commands

from config import settings
from apps import gomoku_app


class GomokuAppCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        super().__init__()
        self.bot = bot
        self.app = gomoku_app.Gomoku(10)
        self.winners = -1
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Cogs", "GomokuAppCog is reloaded.")
    
    # ここに具体的な処理を書く
    @commands.command(name="gomoku")
    async def start(self):
        ...
    
    def set_winner(self, winner: int):
        self.winner = winner

async def setup(bot):
    await bot.add_cog(GomokuAppCog(bot))