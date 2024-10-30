import discord
from discord import ApplicationContext, IntegrationType, message_command
from discord.ext.commands import Cog
from googletrans import RateLimitError

from main import translator_handler


class MessageCommands(Cog):
  def __init__(self, bot):
    self.bot = bot

    self.locales = {
      "id": "id",
      "da": "da",
      "de": "de",
      "en-GB": "en",
      "en-US": "en",
      "es-ES": "es",
      "es-419": "es",
      "fr": "fr",
      "hr": "hr",
      "it": "it",
      "lt": "lt",
      "hu": "hu",
      "nl": "nl",
      "no": "no",
      "pl": "pl",
      "pt-BR": "pt",
      "ro": "ro",
      "fi": "fi",
      "sv-SE": "sv",
      "vi": "vi",
      "tr": "tr",
      "cs": "cs",
      "el": "el",
      "bg": "bg",
      "ru": "ru",
      "uk": "uk",
      "hi": "hi",
      "th": "th",
      "zh-CN": "zh-CN",
      "ja": "ja",
      "zh-TW": "zh-TW",
      "ko": "ko",
    }

  async def split_message_into_parts(self, message, max_length=2000):
    parts = []
    while len(message) > max_length:
      # Trouver la position du dernier espace avant la limite max_length
      last_space = message.rfind(" ", 0, max_length)
      if last_space != -1:
        # Couper le message au dernier espace
        parts.append(message[:last_space])
        message = message[last_space + 1 :]
      else:
        # Si aucun espace n'est trouvé, couper au caractère max_length
        parts.append(message[:max_length])
        message = message[max_length:]
    # Ajouter le reste du message s'il en reste
    if message:
      parts.append(message)
    return parts

  ########################
  # Translate to english #
  ########################

  @message_command(
    name="Translate to english",
    integration_types={
      IntegrationType.guild_install,
      IntegrationType.user_install,
    },
  )
  @translator_handler
  async def translate_to_english(
    self, ctx: ApplicationContext, message: discord.Message
  ):
    await ctx.defer(ephemeral=True)
    try:
      trad = await self.bot.trad.translate(message.content, dest="en", src="auto")
    except RateLimitError:
      raise
    except Exception:
      try:
        trad = await self.bot.trad.translate_to_detect(
          message.content, dest="en", src="auto"
        )
      except RateLimitError:
        raise
      except Exception:
        await ctx.respond("An error occurred.", ephemeral=True)
        return

    if len(trad.text) > 2000:
      parts = await self.split_message_into_parts(trad.text)
      for part in parts:
        await ctx.respond(f"{part}", ephemeral=True)
    elif len(trad.text) == 0:
      await ctx.respond(
        "The message does not contain text. If you think this is an error, you can join the [support server](https://discord.gg/gqfFqJp) and explain your problem.",
        ephemeral=True,
      )
    else:
      await ctx.respond(f"{trad.text}", ephemeral=True)

  #######################
  # Translate to french #
  #######################

  @message_command(
    name="Translate to french",
    integration_types={
      IntegrationType.guild_install,
      IntegrationType.user_install,
    },
  )
  @translator_handler
  async def translate_to_french(
    self, ctx: ApplicationContext, message: discord.Message
  ):
    await ctx.defer(ephemeral=True)
    try:
      trad = await self.bot.trad.translate(message.content, dest="fr", src="auto")
    except RateLimitError:
      raise
    except Exception:
      try:
        trad = await self.bot.trad.translate_to_detect(
          message.content, dest="fr", src="auto"
        )
      except RateLimitError:
        raise
      except Exception:
        await ctx.respond("An error occurred.", ephemeral=True)
        return

    if len(trad.text) > 2000:
      parts = await self.split_message_into_parts(trad.text)
      for part in parts:
        await ctx.respond(f"{part}", ephemeral=True)
    elif len(trad.text) == 0:
      await ctx.respond(
        "The message does not contain text. If you think this is an error, you can join the [support server](https://discord.gg/gqfFqJp) and explain your problem.",
        ephemeral=True,
      )
    else:
      await ctx.respond(f"{trad.text}", ephemeral=True)

  ########################
  # Translate to russian #
  ########################

  @message_command(
    name="Translate to russian",
    integration_types={
      IntegrationType.guild_install,
      IntegrationType.user_install,
    },
  )
  @translator_handler
  async def translate_to_russian(
    self, ctx: ApplicationContext, message: discord.Message
  ):
    await ctx.defer(ephemeral=True)
    try:
      trad = await self.bot.trad.translate(message.content, dest="ru", src="auto")
    except RateLimitError:
      raise
    except Exception:
      try:
        trad = await self.bot.trad.translate_to_detect(
          message.content, dest="ru", src="auto"
        )
      except RateLimitError:
        raise
      except Exception:
        await ctx.respond("An error occurred.", ephemeral=True)
        return

    if len(trad.text) > 2000:
      parts = await self.split_message_into_parts(trad.text)
      for part in parts:
        await ctx.respond(f"{part}", ephemeral=True)
    elif len(trad.text) == 0:
      await ctx.respond(
        "The message does not contain text. If you think this is an error, you can join the [support server](https://discord.gg/gqfFqJp) and explain your problem.",
        ephemeral=True,
      )
    else:
      await ctx.respond(f"{trad.text}", ephemeral=True)

  #######################
  # Translate to custom #
  #######################

  @message_command(
    name="Translate",
    integration_types={
      IntegrationType.guild_install,
      IntegrationType.user_install,
    },
  )
  @translator_handler
  async def translate(self, ctx: ApplicationContext, message: discord.Message):
    await ctx.defer(ephemeral=True)

    cursor = await self.bot.db.cursor()

    await cursor.execute(
      f"SELECT language FROM personal_language WHERE user_id = {ctx.author.id}"
    )
    result = await cursor.fetchone()
    if result is not None:
      result = result[0]
    else:
      result = self.locales[ctx.interaction.locale]

    try:
      trad = await self.bot.trad.translate(message.content, dest=result, src="auto")
    except RateLimitError:
      raise
    except Exception:
      try:
        trad = await self.bot.trad.translate_to_detect(
          message.content, dest=result, src="auto"
        )
      except RateLimitError:
        raise
      except Exception:
        await ctx.respond("An error occurred.", ephemeral=True)
        return

    if len(trad.text) > 2000:
      parts = await self.split_message_into_parts(trad.text)
      for part in parts:
        await ctx.respond(f"{part}", ephemeral=True)
    elif len(trad.text) == 0:
      await ctx.respond(
        "The message does not contain text. If you think this is an error, you can join the [support server](https://discord.gg/gqfFqJp) and explain your problem.",
        ephemeral=True,
      )
    else:
      await ctx.respond(f"{trad.text}", ephemeral=True)


def setup(bot):
  print("Message Commands are ready !")
  bot.add_cog(MessageCommands(bot))
