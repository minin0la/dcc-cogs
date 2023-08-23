from .dev import dev

async def setup(bot):
    await bot.add_cog(dev(bot))
