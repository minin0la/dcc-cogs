from .DCC_Fun import DCC_Fun

async def setup(bot):
    await bot.add_cog(DCC_Fun(bot))
