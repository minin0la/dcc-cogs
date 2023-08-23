from .DCC_Blacklist import DCC_BLACKLIST

def setup(bot):
    bot.add_cog(DCC_BLACKLIST(bot))
