from discord.ext import commands

import logging

async def mysend(self: commands.Context, content, **kwargs):
    print(f"[SEND] `{content}` to {self.channel.name}")
    await self.send_origin(content, **kwargs)
    
commands.Context.send_origin = commands.Context.send
commands.Context.send = mysend
