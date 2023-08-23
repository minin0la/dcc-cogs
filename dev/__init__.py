from .dev import dev

def setup(bot):
    bot.add_cog(dev(bot))
