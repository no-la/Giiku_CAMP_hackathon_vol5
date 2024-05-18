import discord
from discord import app_commands
from discord.ext import commands

from config import settings
from apps import gomoku_app


class GomokuAppCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        super().__init__()
        self.bot = bot
        self.gomoku: gomoku_app.Gomoku = None
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("[Cogs]", "GomokuAppCog is reloaded.")
    
    # ここに具体的な処理を書く
    @commands.command(name="gomoku")
    async def start(self, ctx: commands.Context):
        if self.gomoku is not None:
            await ctx.send(f"You already have a game.", embed=self.make_gomoku_embed())
            return
        
        self.gomoku = gomoku_app.Gomoku(10)
        await ctx.send(f"Gomoku started.", embed=self.make_gomoku_embed())
    
    @commands.command(name="put")
    async def put_piece(self, ctx: commands.Context, x: int, y: int):
        if self.gomoku is None:
            await ctx.send("Please start it with `/gomoku`.")
            return
        
        try:
            self.gomoku.put_piece(x, y)
            embed = self.make_gomoku_embed()
            if self.gomoku.winner is not None:
                embed.color = 0xaa1111
                self.gomoku = None
            await ctx.send(embed=embed)
        except (ValueError, IndexError) as e:
            await ctx.send(f"[ERROR]"+e.args[0])
        
        
    def make_gomoku_embed(self) -> discord.Embed:
        embed = discord.Embed()
        embed.title = f"Turn for: {self.gomoku.get_turn()} (count: {self.gomoku.count})"
        if self.gomoku.winner is not None:
            embed.title = f"Winner {self.gomoku.get_turn()}"
        embed.description = self.gomoku.get_formatted_board()
        embed.color = 0x1111aa
        return embed
    
async def setup(bot):
    await bot.add_cog(GomokuAppCog(bot))