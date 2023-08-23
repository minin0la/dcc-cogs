from .DCC_Announcer import DCC_ANNOUNCER

async def setup(bot):
    await bot.add_cog(DCC_ANNOUNCER(bot))
