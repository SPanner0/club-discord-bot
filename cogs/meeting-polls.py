# TODO: Add functionality to exclude certain times of the day from the polls (via reactions?)

from typing import List, Optional
from discord.ext import commands
import discord
import asyncio
import datetime


class MeetingPolls(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.dates = []
        self.hours = []
        self.polls = []
        self.all_poll_votes = []


    @commands.command(name="meetingpoll")
    @commands.has_permissions(administrator=True)
    async def create_meeting_poll(self, ctx, duration = commands.parameter(default=1, description="The duration of the poll (in days)"),
    minDaysTilMeeting = commands.parameter(default=3, description="The minimum number of days until the next meeting"),
    maxDaysTilMeeting = commands.parameter(default=5, description="The maximum number of days until the next meeting"),
    minHour = commands.parameter(default=9, description="The minimum hour (time of day) that the meeting will start"),
    maxHour = commands.parameter(default=18, description="The maximum hour (time of day) that the meeting will start")):

        """
        !meetingpoll [duration] [minDaysTilMeeting] [maxDaysTilMeeting] [minHour] [maxHour]
        Example: Create a poll that lasts [1] day for a meeting between [3] and [5] days anywhere from [9:00] to [18:00]
        !meetingpoll 1 3 5 9 18
        """


        # Checks to see if the arguments passed meet the requirements and are logically sound, informs the user if they are not
        if minDaysTilMeeting > maxDaysTilMeeting:
            await ctx.send("The maximum number of days until the meeting must be greater than the minimum")
            return
        if minHour > maxHour or minHour < 0 or maxHour > 24:
            await ctx.send("Invalid minimum or maximum hour entered. Please note that the hours are expressed in 24 hour format")
            return
        if (maxHour - minHour) > 10:
            await ctx.send("The number of hours between the maximum hour and the minimum hour must not exceed 10")
            return

        # Delete the command message sent by the user
        await ctx.message.delete()

        for i in range(minDaysTilMeeting, maxDaysTilMeeting + 1):
            self.dates.append(datetime.date.today() + datetime.timedelta(days=i))
            self.polls.append(Poll(ctx))

        for i in range(minHour, maxHour + 1):
            self.hours.append(f"{i}:00")

        for i, poll in enumerate(self.polls):
            await poll.create_poll(f"Meeting times for {self.dates[i]}", self.hours)

        await asyncio.sleep(duration*60*60*24)

        for poll in self.polls:
            self.all_poll_votes.append(await poll.tally_votes())


        # Creates a list of max votes and the indexes of those votes for each poll
        # in this form: ((4, [1, 3, 5]), (2, [2, 3, 6]...))
        max_votes_indices = []
        for i, poll_votes in enumerate(self.all_poll_votes):
            max_votes = max(poll_votes)
            max_votes_indices.append((max_votes, []))
            for j, vote in enumerate(poll_votes):
                if vote == max_votes:
                    max_votes_indices[i][1].append(j)

        await ctx.send(embed=self.create_final_embed(max_votes_indices))
        

    def create_final_embed(self, max_vote_indices):
        embed = discord.Embed(title="Highest voted meeting time(s) for each day", color=discord.Color.blue())
        for i, date in enumerate(self.dates):
            embed.add_field(name=f'Number of votes for: {date}', value=max_vote_indices[i][0], inline=False)
            for index in max_vote_indices[i][1]:
                embed.add_field(name=f'{self.hours[index]}', value=' ', inline=False)

        return embed



class Poll():
    def __init__(self, ctx):
        self.ctx = ctx
        self.emoji_list = [chr(0x0030 + i) + chr(0x20E3) for i in range(1, 10)]
        self.emoji_list.append('🔟')
        self.poll_message = None
        self.options = []


    async def create_poll(self, question: str, options: List[str]):

        self.options = options

        # Send poll message and add reaction options
        self.poll_message = await self.ctx.send(embed=self.create_poll_embed(question, options))
        for i, option in enumerate(self.options):
            await self.poll_message.add_reaction(self.emoji_list[i])


    async def tally_votes(self):
        votes = [0 for _ in range(len(self.options))]
        self.poll_message = await self.ctx.fetch_message(self.poll_message.id)
        for reaction in self.poll_message.reactions:
            if reaction.emoji in self.emoji_list:
                index = self.emoji_list.index(reaction.emoji)
                votes[index] += reaction.count - 1

        return votes


    def create_poll_embed(self, question, options: List[str], votes: Optional[List[int]] = None) -> discord.Embed:
        embed = discord.Embed(title=question, color=discord.Color.blue())
        for i, option in enumerate(options):
            if votes:
                embed.add_field(name=f'{i+1}. {option}', value=votes[i], inline=False)
            else:
                embed.add_field(name=f'{i+1}. {option}', value='\u200b', inline=False)
                
        return embed



async def setup(bot):
    await bot.add_cog(MeetingPolls(bot))