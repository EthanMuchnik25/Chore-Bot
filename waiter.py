# Import OS Module
import os

# Import Discord Module
import discord

# Import Keep Alive WebServer Function
from keep_alive import keep_alive

# Import Scheduler/Asynchrnous Execution Modules
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

# Import Gspread Module For Google Sheets Integration
import gspread

# Import Modules Related To Dates/Time
from datetime import datetime, timedelta
import pytz

# Import Random Module
import random

# Constants Pertaining To Channel ID's
waiterDutiesChannelID = Redacted
uploadingNamesChannelID = Redacted

# Previous Kitchen Manager ID - Change If New Kitchen Manager
winnickUserID = Redacted

sa = gspread.service_account("service_account.json")

sh = sa.open('F21-S22 Waiter Duties')

wks = sh.worksheet("Waiter Duties")

# Dictionary Matching Andrew IDs (Used In Spreadsheet) to Discord IDs

validPersonDict = {
  'Redacted': Redacted,
  'Redacted': Redacted,
  'Redacted': Redacted,
  'Redacted': Redacted,
  'Redacted': Redacted,
  'Redacted': Redacted,
  'Redacted': Redacted,
  'Redacted': Redacted,
  'Redacted': Redacted,
  'Redacted': Redacted,
  'Redacted': Redacted,
  'Redacted': Redacted,
  'Redacted': Redacted,
  'Redacted': Redacted,
  'Redacted': Redacted,
  'Redacted': Redacted,
  'Redacted': Redacted,
  'Redacted': Redacted,
  'Redacted': Redacted,
  'Redacted': Redacted,
  'Redacted': Redacted,
  'Redacted': Redacted,
  'Redacted': Redacted,
  'Redacted': Redacted,
  'Redacted': Redacted,
  'Redacted': Redacted,
  'Redacted': Redacted,
  'Redacted': Redacted,
  'Redacted': Redacted,
  'Redacted': Redacted,
  'Redacted': Redacted,
  'Redacted': Redacted,
  'Redacted': Redacted
}

# Create client for discord API With All Perms Enabled
client = discord.Client(intents=discord.Intents.all())

# Get Channel For Waiter Duties Announcements
announceChannel = client.get_channel(waiterDutiesChannelID)

# Get Channel For Mangaement of Waiter Duties Bot
winnickChannel = client.get_channel(uploadingNamesChannelID)

# Set Timezone
tz = pytz.timezone('America/New_York')

weekOffset = 2  # Offset From Date To Beginning Of Names

weekSize = 11  # Rows Each Week Takes Up Spreadsheet

startDateRow = 5  # First Date Row in Spreadsheet
startDateCol = 2  # First Date Col in Spreadsheet
nameStartCol = 3  # Column Where names Start


# Notify Relevant People of Daily Waiter Duties
async def notifyAssignments():
  # Current Day
  today = datetime.now(tz)
  print(today)

  # Weekday of Current Day
  weekday = today.weekday()
  print(weekday)

  # Date of Beginning of Week
  begOfWeek = today - timedelta(days=weekday)

  # Date At Beginning of Spreadsheet
  val = wks.cell(5, 2).value
  print(val)

  # Extract Datetime Object from the Value in Spreadsheet
  begOfSpread = datetime.strptime(val, '%m/%d/%Y')

  # Adjust Datetime to Correct Timezone
  begOfSpreadTz = begOfSpread.replace(tzinfo=tz)
  print(begOfWeek)
  print(begOfSpreadTz)

  # Get Week Difference Between Beginning of Week and First Date in Spreadsheet
  dateDif = begOfWeek - begOfSpreadTz
  dayDif = dateDif.days
  weekDif = dayDif // 7

  # Calculate Row Pertaining To Current Waiter Duties Assignment
  startDateCellRow = weekDif * weekSize + startDateRow + weekOffset + weekday
  print(startDateCellRow)

  # Append Waiter Duties names to List
  names = []
  names.append(wks.cell(startDateCellRow, nameStartCol).value)
  names.append(wks.cell(startDateCellRow, nameStartCol + 1).value)

  # Generate Random Threat Index and ReInitialize Channel Variables
  announceChannel = client.get_channel(waiterDutiesChannelID)
  winnickChannel = client.get_channel(uploadingNamesChannelID)

  # If Both Cells Are Not Ping People To Do Waiter Duties
  if names[0] != None and names[1] != None:
    await announceChannel.send(
      f"<@{validPersonDict[names[0]]}> <@{validPersonDict[names[1]]}> \n")
  # If One Name Is Missing, Assume misinput and Ping Kitchen Manager
  elif (names[0] != None) ^ (names[1] != None):
    await winnickChannel.send(
      "<@" + str(winnickUserID) + ">" +
      "Spreadsheet doesn't have the neccesary data in it.")
  # If Both Inputs Blank, Assume That Was Intended and Output Nothing
  else:
    pass


# Runs When Bot Turns On
@client.event
async def on_ready():

  # Initialize Schedule To Run Notify Assignments at 12 pm Est (Shifted TimeZone)
  scheduler = AsyncIOScheduler()
  scheduler.add_job(notifyAssignments, CronTrigger(hour="16", minute="0"))

  scheduler.start()

@client.event
async def on_message(message):
  # If The Message is From Kitchen Manager(waiter-duties) Channel
  if message.channel.id == uploadingNamesChannelID:
    # If Message is $stop, exit
    if (message.content.startswith('$stop')):
      exit()
    # If Message is $info, output information
    elif (message.content.startswith('$info')):
      await message.channel.send(
        "This bot works by tagging people in the waiterduties announcement channel along with an extra phrase appended to the end to enhance motivation to actually complete waiter duties.\n\n"
        +
        "It is designed to work without any input from the discord server admins. It is able to accomplish this by drawing from existing spreadsheet data. If the data is inadequate it will let you know in the waiterlist channel. Please message Ethan Muchnik for any additional technical questions."
      )
    # If message Starts with '$' give useful list of commands.
    elif (message.content.startswith('$')):
      if message.author != client.user:
        await message.channel.send("Here are the commands that can be used")
        await message.channel.send(
          "($stop) to terminate | ($info) for more information")


if __name__ == "__main__":
  keep_alive()
  my_secret = os.environ['DISCORD_BOT_SECRET']
  client.run(my_secret)
