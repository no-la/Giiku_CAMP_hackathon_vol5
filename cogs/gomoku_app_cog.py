import discord
from discord import app_commands
from discord.ext import commands

from config import settings
from apps import gomoku_app
from apps import stats_app


class GomokuAppCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        super().__init__()
        self.bot = bot
        self.gomoku: gomoku_app.Gomoku = None
        self.participant_ids = None
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("[Cogs]", "GomokuAppCog is reloaded.")
    
    # ここに具体的な処理を書く
    @commands.command(name="go")
    async def ready(self, ctx: commands.Context):
        if self.gomoku is not None:
            await ctx.send(f"進行中のゲームがあります", embed=self.make_gomoku_embed(),
                           file=discord.File(gomoku_app.IMG_PATH))
            return
        if self.participant_ids is None:
            self.participant_ids = [ctx.author.id]
            await ctx.send("もう一人の参加者も`/go`と送信してください")
        else:
            if ctx.author.id in self.participant_ids:
                await ctx.send("参加済みです")
                return
            self.participant_ids.append(ctx.author.id)

            await ctx.send(f"<@{self.participant_ids[0]}> が先手、<@{self.participant_ids[1]}> が後手です")
            self.gomoku = gomoku_app.Gomoku(19)
            self.gomoku.make_board_img()
            await ctx.send(embed=self.make_gomoku_embed(),
                        file=discord.File(gomoku_app.IMG_PATH))
    
    @commands.command(name="put")
    async def put_piece(self, ctx: commands.Context, x: int, y: int):
        if self.gomoku is None:
            await ctx.send("`/go`コマンドでゲームを始めてください")
            return
        
        try:
            if ctx.author.id!=self.participant_ids[self.gomoku.get_turn()]:
                await ctx.send(f"<@{self.participant_ids[self.gomoku.get_turn()]}> の手番です")
                return
            self.gomoku.put_piece(y, x)
            self.gomoku.make_board_img()
            embed = self.make_gomoku_embed()
            if self.gomoku.winner is not None:
                embed.color = 0xaa1111
                self.gomoku = None
                self.participant_ids = None
            await ctx.send(embed=embed, file=discord.File(gomoku_app.IMG_PATH))
        except (ValueError, IndexError) as e:
            await ctx.send(f"[ERROR]"+e.args[0])
    
    @commands.command(name="gofin")
    async def fin(self, ctx: commands.Context):
        self.gomoku = None
        self.participant_ids = None
        
        await ctx.send("ゲームを終了しました")
        
    def make_gomoku_embed(self) -> discord.Embed:
        embed = discord.Embed()
        turn_text = ("先手番", "後手番")[self.gomoku.get_turn()]
        embed.title = f"{turn_text} ({self.gomoku.count+1}手目)"
        embed.description = "`/put [行番号] [列番号]` で手番を進めてください\n`/gofin` でゲームを終了します"
        if self.gomoku.winner is not None:
            embed.title = f"{turn_text[:2]}の勝ち"
            embed.description = "ゲームは終了しました"

            stats_app.save_stats("五目並べ", self.participant_ids, self.participant_ids[self.gomoku.winner])
        # embed.description = self.gomoku.get_formatted_board()
        embed.color = 0x1111aa
        return embed
    
async def setup(bot):
    await bot.add_cog(GomokuAppCog(bot))