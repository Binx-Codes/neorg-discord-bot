import re

import discord
import requests
from bs4 import BeautifulSoup
from discord.ext.commands import Cog, Context, hybrid_command
from icecream import ic
from neorg import constants as c

from neorg.log import get_logger
from neorg.neorg import Neorg

log = get_logger(__name__)


class NeorgCmd(Cog):
    """
    NeorgCmd custom call to inspect neorg wiki, Using beautiful soup to webscrap
    Neorgs github wiki page to retreive links
    """

    def __init__(self, bot: Neorg):
        self.bot = bot

    @hybrid_command()
    async def wiki(self, ctx: Context, query: str = '') -> None:
        """
        Neorg Wiki search handle to search neorg wiki for query
        n.wiki <query>
        """
        query = query.strip().lower().replace(' ', '-')
        neorg_wiki = {}
        wiki_url = "https://github.com/nvim-neorg/neorg/wiki"

        soup = BeautifulSoup(requests.get(wiki_url).text, 'lxml')
        lis = soup.find_all("div", {"class": "Box-body wiki-custom-sidebar markdown-body"})[0]

        for li in lis.find_all('li'):
            if li.a is None:
                continue

            part = li.a['href']
            #  TODO(vsedov) (13:39:53 - 06/04/22): remove hardcode
            neorg_wiki[part[37:].lower()] = part

        wiki = [neorg_wiki[k] for k in neorg_wiki if query in k.lower()]
        log.debug(ic.format(wiki))

        if not wiki:
            await ctx.send(embed=discord.Embed(description="No Results Found!", colour=c.NORG_BLUE))
            return

        wikis_em = []
        for i in wiki:
            em = discord.Embed(description=i, colour=c.NORG_BLUE)
            wikis_em.append(em)

        await ctx.send(embeds=wikis_em[:5])

    # TODO: needs complete rewrite from: https://github.com/nvim-neorg/norg-specs
    @hybrid_command()
    async def spec(self, ctx: Context, *, query: str) -> None:
        """Spec search handle to search neorg spec for query
        n.spec <query>
        Similar to n.wiki but for spec files
        """
        query = query.strip().lower().replace(' ', '-')
        url = "https://raw.githubusercontent.com/nvim-neorg/neorg/main/docs/NFF-0.1-spec.md"
        og_url = "https://github.com/nvim-neorg/neorg/blob/main/docs/NFF-0.1-spec.md"

        soup = re.findall(r"\[(.+)\]\((.+)\)", requests.get(url).text[:1500])
        neorg_specs = {k.lower().replace(' ', '-'): og_url + v for k, v in soup}
        spec = [neorg_specs[k] for k in neorg_specs if query in k.lower()]

        if not spec:
            await ctx.send(embed=discord.Embed(description="No Results Found!", colour=c.NORG_BLUE))
            return

        for i in spec:
            em = discord.Embed(description=i, colour=c.NORG_BLUE)
            await ctx.send(embed=em)

    @hybrid_command()
    async def neorg(self, ctx: Context) -> None:
        """Fetch the Neorg repository"""
        await ctx.send("Neorg - https://github.com/nvim-neorg/neorg")


async def setup(bot: Neorg) -> None:
    """Add Cog to Bot."""
    await bot.add_cog(NeorgCmd(bot))
