from .DCC_Inactive import DCC_INACTIVE

async def setup(bot):
    await bot.add_cog(DCC_INACTIVE(bot))
