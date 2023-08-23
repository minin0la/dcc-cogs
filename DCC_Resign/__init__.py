from .DCC_Resign import DCC_RESIGN

async def setup(bot):
    await bot.add_cog(DCC_RESIGN(bot))
