from typing import List, Optional
from discord.ext import commands
import discord
from asyncio import sleep


class Poll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.emoji_list = [chr(0x0030 + i) + chr(0x20E3) for i in range(1, 11)]
        self.question = None


    @commands.command(name='poll')
    async def create_poll(self, ctx, question: str, duration: int, *options: str):
        self.question = question

        # Send poll message and add reaction options
        poll_message = await ctx.send(embed=self.create_poll_embed(options))
        for i, option in enumerate(options):
            await poll_message.add_reaction(self.emoji_list[i])

        # Sleep for specified duration and then tally votes
        await sleep(duration)

        # Reassign the poll_message object to have all the up-to-date reactions right before tallying
        poll_message = await ctx.fetch_message(poll_message.id)
        await self.tally_votes(poll_message, options)


    async def tally_votes(self, message: discord.Message, options: List[str]):
        votes = [0 for _ in range(len(options))]
        for reaction in message.reactions:
            if reaction.emoji in self.emoji_list:
                index = self.emoji_list.index(reaction.emoji)
                votes[index] += reaction.count - 1
                print(f'{reaction.emoji} has {reaction.count} votes')

        # Update the message with the tally of votes
        embed = self.create_poll_embed(options, votes)
        await message.edit(embed=embed)


    def create_poll_embed(self, options: List[str], votes: Optional[List[int]] = None) -> discord.Embed:
        embed = discord.Embed(title=self.question, color=discord.Color.blue())
        for i, option in enumerate(options):
            if votes:
                embed.add_field(name=f'{i+1}. {option}', value=votes[i], inline=False)
            else:
                embed.add_field(name=f'{i+1}. {option}', value='\u200b', inline=False)
        return embed



async def setup(bot):
    await bot.add_cog(Poll(bot))