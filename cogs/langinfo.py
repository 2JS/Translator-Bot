from discord import (
  ApplicationContext,
  Embed,
  InteractionContextType,
  default_permissions,
  option,
)
from discord.ext.commands import Cog, slash_command


class LangInfo(Cog):
  def __init__(self, bot):
    self.bot = bot

  @slash_command(
    name="langinfo",
    description="Get the informations from which language the original message come from.",
    contexts={InteractionContextType.guild},
  )
  @option(
    name="enabled",
    description='"True" to get the flag before the translation. "False" to don\'t.',
    required=True,
    type=bool,
  )
  @default_permissions(administrator=True)
  async def langinfo(self, ctx: ApplicationContext, enabled):
    await ctx.defer(ephemeral=True)

    EmbedMessage = Embed(
      description="Language information setting have been set", color=0x00FF00
    )

    if enabled is True:
      enabled = "enabled"
    elif enabled is False:
      enabled = "disabled"

    await self.bot.cursor.execute(
      f"SELECT info FROM langinfo WHERE guild_id = {ctx.guild.id}"
    )
    result = await self.bot.cursor.fetchone()

    if result is None:
      if enabled == "enabled":
        sql = "INSERT INTO langinfo(guild_id, info) VALUES(?,?)"
        val = (ctx.guild.id, enabled)

        await self.bot.cursor.execute(sql, val)
        await self.bot.db.commit()

    if result is not None:
      if enabled == "disabled":
        sql = f"DELETE FROM langinfo WHERE guild_id = {ctx.guild.id}"
        await self.bot.cursor.execute(sql)

      else:
        sql = "UPDATE langinfo SET info = ? WHERE guild_id = ?"
        val = (enabled, ctx.guild.id)

        await self.bot.cursor.execute(sql, val)
      await self.bot.db.commit()

    await ctx.respond(embed=EmbedMessage, ephemeral=True)


def setup(bot):
  print("Language Information Command is ready !")
  bot.add_cog(LangInfo(bot))
