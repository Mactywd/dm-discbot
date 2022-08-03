import time
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import json


load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", case_insensitive=True, intents=intents)


#####################
## UTILS FUNCTIONS ##
#####################

def reply_message(roles):
    return "Da ora in poi pingerò questi ruoli: " + ", ".join(roles)

def roles_exist(ctx, all_roles):
    found_roles = []
    guild = ctx.author.guild
    for role_ in all_roles:
        role = discord.utils.get(guild.roles, name=role_)
        if role is not None:
            found_roles.append(role.name)
    
    return found_roles


def parse_roles(ctx, roles):
    found_roles = []
    guild = ctx.author.guild
    for role_ in roles:
        role = discord.utils.get(guild.roles, name=role_)
        if role is not None:
            found_roles.append(role)

    return found_roles

def operate_json(action, data):
    existing = open

##################
## BOT COMMANDS ##
##################

@bot.command()
async def setroles(ctx, *roles):
    '''
    Set the roles that will be pinged. If a role doesn't exist it will be ignored
    '''
    print("Setting the roles...")
    roles = roles_exist(ctx, set(roles))

    with open('roles.json', 'w') as f:
        f.write(json.dumps(roles))
    
    await ctx.reply(reply_message(roles))

@bot.command()
async def addroles(ctx, *roles):
    '''
    Add roles to the ones that will be pinged. If a role doesn't exist it will be ignored
    '''
    roles = roles_exist(ctx, roles)

    with open('roles.json') as f:
        data = json.load(f)
    
    data = [*data, *roles]

    with open('roles.json', 'w') as f:
        f.write(json.dumps(data))
    
    await ctx.reply(reply_message(data))

@bot.command()
async def remroles(ctx, *roles):
    '''
    Remove roles from the ones that will be pinged. If a role doesn't exist or isn'tin the list it will be ignored
    '''
    roles = roles_exist(ctx, roles)

    with open('roles.json') as f:
        data = json.load(f)

    for role in roles:
        if role in data:
            data.remove(role)

    with open('roles.json', 'w') as f:
        f.write(json.dumps(data))
    
    await ctx.reply(reply_message(data))


@bot.command()
async def seeroles(ctx):
    '''
    Lets you see all the roles that will be pinged
    '''
    with open('roles.json') as f:
        data = json.load(f)
    
    await ctx.reply("I ruoli che verranno pingati: " + ', '.join(data))


@bot.command()
async def dm(ctx, message):
    '''
    Dm's all the users that have the pre-selected roles
    '''
    start = time.perf_counter()
    with open("roles.json") as f:
        roles = parse_roles(ctx, json.load(f))
    
    dm_users = []
    for role in roles:
        for member in role.members:
            if not member in dm_users:
                dm_users.append(member)

                await member.send(message)
    
    await ctx.reply(f"Fatto! Pingato {len(dm_users)} utenti in {round(time.perf_counter() - start, 1)} secondi")

@bot.command()
async def comandi(ctx):
    '''
    Sends the help message
    '''
    await ctx.reply('''\
!setroles {ruolo/i}: Imposta i ruoli da pingare
!addroles {ruolo/i}: Aggiunge ruoli a quelli da pingare
!remroles {ruolo/i}: Rimuove ruoli da quelli da pingare    
!seeroles: Fa vedere tutti i ruoli che verranno pingati
!dm: Invia un dm a tutti i ruoli selezionati
    ''')

# Finally run the bot
bot.run(TOKEN)
