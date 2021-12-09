#Discord bot instructions from:
#https://realpython.com/how-to-make-a-discord-bot-python/#creating-a-discord-connection

import discord
import random
import numpy as np
import os

def get_token():
    #Get the API Key from Heroku Config Vars
    print('Trying to get the Token')
    token = str(os.environ.get(DISCORD_API))
    print(token)
    return token

def get_server():  # If this was a real bot I would have to figure out how to get the server of where it was installed
    #Get the API Key from the Notepad
    f = open('discord_server.txt', "r")
    server = f.read()
    f.close()
    return server

def roll_dice(n, d):
    rolls = np.zeros(n)
    print('Running Roll Dice')
    if n == 1:
        response = str(random.randint(1, d))
        return response
    else:
        for i in range(n):
            rolls[i] = random.randint(1, d)

        total = np.sum(rolls)  # Get the Total of all the dice rolling
        rolls_as_str = [str(int(i)) for i in rolls]
        response = ' + '.join(rolls_as_str) + f' = {str(int(total))}'

        return response

def interpret_roll(message):
    data = message.lower().split('d')
    if data[0] == '':
        n = 1
    else:
        n = int(data[0])
    d = int(data[1])
    return n, d

print('Loading Tokens...')
#Load the Token and Server Name
TOKEN = get_token()
SERVER = get_server()
client = discord.Client()  #Declare instance of this bot account

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    for guild in client.guilds:
        if guild.name == SERVER:
            break

    print(
        f'{client.user} is connected to the following guild:\n',
        f'{guild.name}(id: {guild.id})')

@client.event
async def on_message(message):
    #print(f'interpreting a message...{message.content}')
    if message.author == client.user:  #If the message was sent buy the bot itself
        return  #Do nothing
    if message.content[0:4].lower() == 'roll':  #The message begins with 'roll'
        try:
            #print(f'trying to get dice rolls... {message.content[5:]}')
            n, d = interpret_roll(message.content[5:])
            response = roll_dice(n, d)
            await message.channel.send(response)  # Send the dice roll response back
        except:
            err_response = '''Something went wrong, enter your command as 'roll 2d6', one roll at a time '''
            await message.channel.send(err_response)

client.run(TOKEN)  # Run the bot inside the server