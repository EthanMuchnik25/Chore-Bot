import os
import discord
from keep_alive import keep_alive
from collections import deque
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from discord.ext import commands
from datetime import datetime
from pytz import timezone
import random

# Constants
# waiter duties channel const 1021528282446970970
waiterDutiesChannelID = 1021528282446970970
uploadingNamesChannelID = 1067347506171748392
winnickUserID = 304068912033824769
# winick user id 509535039533482007
# Persuasive Phrases To Get People To Do Waiter Duties
harrassmentList = [
  "Ok, you have until the end of the day to do your goddamn dishes or else...",
  "Do dishes or it's kneecapping time.",
  "That was the last straw. Do your dishes you sack of shit. I know where you live.",
  "Your free trial of life outside of waiter duties has expired.... Do. Them",
  "I swear to god. Next time you fuck up Waiter Duties I will castrate you. I'm watching you.",
  "When he said it was dishin time that sent chills down my spine. Anyway do dishes or I will make you watch morbius for the next 3 calender weeks."
]

# Queue
queue = deque([])

# Create Client
client = discord.Client(intents=discord.Intents.all())
announceChannel = client.get_channel(waiterDutiesChannelID)
winnickChannel = client.get_channel(uploadingNamesChannelID)


# Notify People of Daily Waiter Duties
async def notifyAssignments():
  # c = bot.get_channel(812588887200497674)
  announceChannel = client.get_channel(waiterDutiesChannelID)
  winnickChannel = client.get_channel(uploadingNamesChannelID)
  # print(waiterDutiesChannelID)
  random_index = random.randint(0, len(harrassmentList) - 1)
  if queue:
    await announceChannel.send(
      f"{queue.popleft()} {queue.popleft()} {harrassmentList[random_index]} \n"
    )
  else:
    await winnickChannel.send("<@" + str(winnickUserID) + ">" +
                              "GOD DAMNIT. PUT THE NEW NAMES INTO THE QUEUE")


@client.event
async def on_ready():
  print("I'm in")
  print(client.user)
  scheduler = AsyncIOScheduler()

  #sends "s!t" to the channel when time hits 10/20/30/40/50/60 seconds, like 12:04:20 PM
  scheduler.add_job(notifyAssignments, CronTrigger(hour="15"))

  #starting the scheduler
  scheduler.start()


@client.event
async def on_message(message):
  global queue
  if message.channel.id == uploadingNamesChannelID:
    if (message.content.startswith('$add')):
      mentionLen = len(message.mentions)
      for user in message.mentions:
        if user != client.user:
          queue.append(user.mention)
      await message.channel.send(f"Successfully added {mentionLen} user(s)")
      await message.channel.send(f"The queue currently looks like this {queue}"
                                 )
    elif (message.content.startswith('$delete')):
      if message.author != client.user:
        queue = deque()
        await message.channel.send("Successfully deleted queue")
        await message.channel.send(
          f"The queue currently looks like this {queue}")
    elif (message.content.startswith('$')):
      # else:
      if message.author != client.user:
        await message.channel.send(
          "You idiot sandwhich. Can't even write a command")
        await message.channel.send(
          "($add <tag user>) to add users | ($delete) deletes everyone from the queue"
        )

keep_alive()
my_secret = os.environ['DISCORD_BOT_SECRET']
client.run(my_secret)
