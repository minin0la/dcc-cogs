from .DCC_Blacklist import DCC_BLACKLIST

async def setup(bot):
    await bot.add_cog(DCC_BLACKLIST(bot))
