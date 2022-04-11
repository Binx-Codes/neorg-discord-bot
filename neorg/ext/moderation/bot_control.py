import discord
# yapf: disable
from discord.ext.commands import (
    BadArgument, CheckFailure, Cog, CommandNotFound, Context, MissingRequiredArgument, command, has_any_role
)
# yapf: enable
from icecream import ic

from neorg import constants
from neorg.log import get_logger
from neorg.neorg import Neorg

log = get_logger(__name__)


class BotControl(Cog):
    """Moderation tools, to control the bot."""

    def __init__(self, bot: Neorg):
        self.bot = bot

    @command()
    async def shutdown(self, ctx: Context) -> None:
        """Shutdown the bot."""

        await ctx.send(embed=discord.Embed(description="Shutting down...", colour=discord.Color.red()))
        await self.bot.close()
        log.info("Bot shutdown.")

    @command()
    async def reload(self, ctx: Context, cog: str) -> None:  # noqa ignore
        """Reload a cog without restarting the bot."""
        if not cog:
            await ctx.send('Specify the cog to reload!')
            return
        try:
            #  TODO(vsedov) (18:32:18 - 10/04/22): Load modules using walk extension
            Neorg.unload_extension(cog)
            Neorg.load_extension(cog)
            await ctx.send(embed=discord.Embed(description=f"Cog **{cog}** reloaded", colour=discord.Color.red()))
        except Exception as ae:
            await ctx.send(ae)
            log.warning(ic.format(f"{cog} could not be loaded"))

    async def cog_check(self, ctx: Context) -> bool:
        """Only allow moderators to invoke the commands in this cog."""
        return await has_any_role(*constants.MODERATION_ROLES).predicate(ctx)

    async def cog_command_error(self, ctx: Context, error: Exception) -> None:
        """Cog Role error, if not mod or admin, output will output and error."""
        error_dict = {
            CommandNotFound: "Command not found.",
            CheckFailure: "You do not have permission to run this command.",
            MissingRequiredArgument: "You are missing a required argument.",
            BadArgument: "You have provided an invalid argument."
        }

        for error_type, error_message in error_dict.items():
            if isinstance(error, error_type):
                await ctx.send(embed=discord.Embed(description=error_message, colour=discord.Color.red()))

        log.warning(ic.format(f"{ctx.author} tried to run {ctx.command} but got {error}"))


def setup(bot: Neorg) -> None:
    """Add Cog to Bot."""
    bot.add_cog(BotControl(bot))
