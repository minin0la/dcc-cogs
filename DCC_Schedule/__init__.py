from .DCC_Schedule import DCC_SCHEDULE

def setup(bot):
    bot.add_cog(DCC_SCHEDULE(bot))