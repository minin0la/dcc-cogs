from .DCC_Promotion import DCC_PROMOTION

async def setup(bot):
    await bot.add_cog(DCC_PROMOTION(bot))
