from .DCC_General import DCC_GENERAL

async def setup(bot):
    await bot.add_cog(DCC_GENERAL(bot))
