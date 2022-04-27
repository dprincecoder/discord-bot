import discord # discord.py module
import os # os module
import requests # requests module
import json # json module
import random # random module
from replit import db

#bot_secret = os.environ['BOT_TOKEN'] # Get the bot secret from .env

#initialize discord client
client = discord.Client()

#sad words to response list
sad_words = ['sad', 'depressed', 'unhappy', 'angry', 'hate myself']

#starter encouragement message
starter_encouragements = ["I'm glad you're here! I'm here to help you get through this difficult time.", 'Just cheer up', 'Hang in there', 'You can do this', 'I believe in you', 'You are a great person']


if 'responding' not in db.keys():
    db['responding'] = True

#get quote
def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " - " + json_data[0]['a']
    return quote

#update encouragement message as the bot learns
def update_encouragements(encrg_message):
    if 'encouragements' in db.keys():
        encouragements = db['encouragements']
        encouragements.append(encrg_message)
        db['encouragements'] = encouragements
    else:
        db['encouragements'] = [encrg_message]


#del encouraement message from the list
def del_encouragement(index):
    encouragements = db['encouragements']
    if len(encouragements) > index:
        del encouragements[index]
        db['encouragements'] = encouragements


@client.event
#listen for async event on ready
@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))
    print('------')
    


#listen for message event
@client.event
async def on_message(message):
    #if message is from bot, ignore
    if message.author == client.user:
        return

    msg = message.content.lower()

  
    #if message is from user, print message
    if msg.startswith('inspire me'):
        quote = get_quote()
        await message.channel.send('here is a quote for you: ' + quote)

    if db['responding'] == True:
        options = starter_encouragements
        if 'encouragements' in db.keys():
            options = options + list(db['encouragements'])
        if any(word in msg for word in sad_words):
            await message.channel.send(random.choice(options))

    if msg.startswith('!new '):
        new_encouragement = msg.split('!new ',1)[1]
        update_encouragements(new_encouragement)
        await message.channel.send('New encouragement message added!')

    if msg.startswith('!del'):
        encouragements = []
        index = int(msg.split('!del',1)[1])
        del_encouragement(index)
        encouragements = list(db['encouragements'])
        await message.channel.send(encouragements)

    if msg.startswith('!list'):
        encouragements = []
        if 'encouragements' in db.keys():
           encouragements=  list(db['encouragements'])
        await message.channel.send(encouragements)

    if msg.startswith('!responding'):
        value = msg.split('!responding ',1)[1]

        if value.lower() == 'true':
            db['responding'] = True
            await message.channel.send('Responding to messages')
        else:
            db['responding'] = False
            await message.channel.send('Not responding to messages')

my_secret = os.environ['BOT_TOKEN']
#run bot
client.run(my_secret)
