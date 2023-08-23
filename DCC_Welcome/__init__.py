from .DCC_Welcome import DCC_WELCOME

async def setup(bot):
    await bot.add_cog(DCC_WELCOME(bot))
