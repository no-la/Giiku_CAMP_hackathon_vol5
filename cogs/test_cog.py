from discord.ext import commands
import discord
from discord import app_commands

class TestCog(commands.Cog):
    def __init__(self, bot) -> None:
        super().__init__()
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("[Cogs]", "TestCog is reloaded.")
    
    @commands.command()
    async def test01(self, ctx: commands.Context):
        await ctx.send("test01が呼ばれました")

    @commands.command()
    async def test02(self, ctx: commands.Context):
        await ctx.send("test02が呼ばれました", ephemeral=True)

    # うごかない
    @app_commands.command(name="modal")
    async def modal_test(self, interaction: discord.Interaction):
        modal = MyModal()
        await interaction.response.send_modal(modal)



class MyModal(discord.ui.Modal, title="modalのテスト"):
    text_input = discord.ui.TextInput(
        label="入力"
    )
    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"{interaction.user.mention} send {self.text_input.value}.")


async def setup(bot):
    await bot.add_cog(TestCog(bot))
