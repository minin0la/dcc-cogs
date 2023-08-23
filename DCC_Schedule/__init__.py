from .DCC_Schedule import DCC_SCHEDULE

async def setup(bot):
    await bot.add_cog(DCC_SCHEDULE(bot))