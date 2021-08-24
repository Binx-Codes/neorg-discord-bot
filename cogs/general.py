from discord.ext import commands
import discord

class general(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_message(self, message):
		if 'sus' in message.content.lower():
			await message.add_reaction("<:sus:867395030988881921>")

	@commands.Cog.listener()
	async def on_raw_reaction_add(self, payload):
		if payload.emoji.name in '📑🔖':
			msg = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
			author = msg.author

			if msg.content != "":
				bookmark = discord.Embed(description=msg.content, colour = 0x4878BE)
				bookmark.set_author(name=author.name, icon_url=author.avatar_url)
				user = await self.bot.fetch_user(payload.user_id)
				await user.send(embed=bookmark)

def setup(bot):
    bot.add_cog(general(bot))
