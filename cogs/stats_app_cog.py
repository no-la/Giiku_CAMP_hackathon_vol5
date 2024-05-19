import discord
from discord import app_commands
from discord.ext import commands
from collections import defaultdict

from config import settings
from apps import stats_app


class StatsAppCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        super().__init__()
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Cogs", "StatsAppCog is reloaded.")
    
    # ここに具体的な処理を書く
    @commands.command(name="stats")
    async def send_stats(self, ctx: commands.Context):
        d = stats_app.load_stats()
        d_for_user = defaultdict(lambda: [0, 0]) # 参加数, 勝利数
        for v in d["stats"]:
            if ctx.author.id in v["participant_ids"]:
                d_for_user[v["name"]][0] += 1
                d_for_user[v["name"]][1] += v["winner_id"]==ctx.author.id
        
        embed = discord.Embed(title="過去のデータ", description="", color=0x99ba99)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
        for k in d_for_user:
            embed.add_field(name=f"{k}", value=f"- 参加回数 : {d_for_user[k][0]}\n- 勝利数 : {d_for_user[k][1]}\n")
        
        await ctx.send(embed=embed)

    @commands.command(name="ranking")
    async def send_ranking(self, ctx: commands.Context):
        members: list[discord.Member] = [m async for m in ctx.guild.fetch_members()]
        d = stats_app.load_stats()
        d_for_games = defaultdict(lambda: {m.id:[0, 0, m.nick or m.name] for m in members})
        # d_for_games["name"]["user"] : [win_num, count]
        for v in d["stats"]:
            for u in v["participant_ids"]:
                d_for_games[v["name"]][u][0] += 1
            d_for_games[v["name"]][v["winner_id"]][1] += 1

        
        embed = discord.Embed(title="ランキング", description="", color=0xffea65)
        for k in d_for_games:
            value = ""
            print(k, d_for_games[k])
            for i, temp in enumerate(sorted(d_for_games[k].items(), key=lambda x: x[1], reverse=True)):
                _, v = temp
                value += f"**{i+1}位 {v[2]}** (勝利数 : {v[0]}, 参加回数 : {v[1]})\n"
            embed.add_field(name=f"{k}", value=value, inline=False)
        
        await ctx.send(embed=embed)
    
async def setup(bot):
    await bot.add_cog(StatsAppCog(bot))