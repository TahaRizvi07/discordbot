# bot.py
import os
import random
import discord
from dotenv import load_dotenv

from discord.ext import commands
from youtube_search import YoutubeSearch
import youtube_dl


load_dotenv()
TOKEN = #hidden for privacy purposes
GUILD = 'Fluffster\'s Server'

bot = commands.Bot(command_prefix=',')
bot.remove_command('help')


#command line message
@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.name == GUILD:
            break

    print(f'{bot.user.name} is connected to the following server:\n'
          f'{guild.name}(id: {guild.id})'
    )

#member welcome
@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server! Remember, you\'re awesome!'
    )


#bot event to respond to someone sending owo
@bot.event
async def on_message(message):

    if message.author == bot.user:
        return

    owo_list = ["owo","òwó","ówò","ówó","ỏwỏ","õwõ","ọwọ","òwò",
                "ôwô","ồwố","ốwồ","ốwố","ồwồ","ổwổ","ỗwỗ","ộwộ",
                "ơwơ","ờwớ","ớwớ","ớwờ","ờwờ","ởwở","ỡwỡ","ợwợ",
                "uwu!! not what you expected, huh?"]

    uwu_list = ["uwu","ùwú","úwú","úwù","ùwù","ủwủ","ũwũ","ụwụ",
                "ưwư","ứwứ","ứwừ","ừwứ","ừwừ","ửwử","ữwữ","ựwự",
                "owo!! foiled by Bot-san!"]

    if "owo" in message.content.lower():
        response = random.choice(owo_list)
        await message.channel.send(response)

    if "uwu" in message.content.lower():
        response = random.choice(uwu_list)
        await message.channel.send(response)

    await bot.process_commands(message)


############ COMMANDS - specific message responses to user commands ################


#command for help for every other command
@bot.command(name='help', help='Shows all events and commands for this bot')
async def help(ctx):
    help_dict = {',f': 'Gives you a fortune. That\'s it.', #fortune
                 ',roast <roast1> <roast2> <roast3>':'Takes roast1 (and roast2 [and roast 3]) and inserts them into a roast *at specific spots.* Type ,roasthelp for a full list of roasts. A multi-word roast can be inserted by adding quotation marks around it, e.g. "steph\'s entropic pants" idea chem',
                 ',help': 'Shows all events and commands for this bot', #help
                 ',math': 'NOTE: message must be within quotation marks.\nHelps you with your math homework! :)',
                 ',mock <mock_message>': 'NOTE: message must be within quotation marks.\nResponds with a SpongeBob parroting version of <mock_message>',
                 ',mood <mood>':'Responds with a YouTube link to a song that fits the mood provided.',
                 ',pl <message>':'NOTE: message must be within quotation marks.\nTranslates <message> to Pig Latin.', #pig latin
                 ',pos':'Responds with a message of positivity', #pos
                 ',rate <@person>':'Gives the @\'d person a rating! :)', #rate
                 ',groast <roast1> <roast2> <roast3>':'Takes roast1 [and roast2 and roast3] and inserts \
                    \nthem randomly into a roast. May or may not make sense\
                    \nType ,roasthelp for a full list of roasts\
                    \nA multi-word roast can be inserted by adding quotation marks around it,\
                    \ne.g. "steph\'s entropic pants" idea chem',
                 ',roasthelp':'List of roasts to use for ,roast and ,groast\
                    \nw1, w2, and w3 stand for user-inputted words',
                 ',rxn':'Returns chemistry-related video', #rxn
                 ',s':'Takes part of two Shakespearean insults and mashes them together.\
                    \nDoesn\'t work perfectly.',
                 'Other events:':'owo: *responds with a varied owo* \nuwu: *responds with varied uwu*'}

    embedVar = discord.Embed(title="Bot-san Help", \
               description="Provides a list of commands and events that Bot-san processes", \
               color=0x00ff00)

    try:
        for k,v in help_dict.items():
            embedVar.add_field(name=k, value=v, inline=False)

        embedVar.add_field(name="__Up next:__", value="math insult command")
        #embedVar.add_field(name="__In need to fixing:__", value="mood, rxn")
        embedVar.set_footer(text="Made by Fluffster#2413 | Version 1.13")

    except:
        print("Sorry that didn't work try again")
        raise

#    await message.channel.send(embed=embedVar)
    await ctx.send(embed=embedVar)

#command to create a new channel; only to be used by admins
@bot.command(name='create-channel', help='Creates a new channel named <channel_name>')
@commands.has_role('soff but swole')
async def create_channel(ctx, channel_name: str):
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if not existing_channel:
        print(f'Creating a new channel: {channel_name}')
        await guild.create_text_channel(channel_name)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')

#positivity message
@bot.command(name='pos', help='Responds with a message of positivity')
async def positivity(ctx):

    test_messages = ['insert positivity message here',
                     'you\'re amazing!',
                     'tomorrow will be a great day!',
                     'don\'t give up!',
                     'you can do it!',
                     'I\'m so proud of you'
                    ]

    response = random.choice(test_messages)
    await ctx.send(response)


#SpongeBob parroting meme
@bot.command(name='mock', \
             help='NOTE: message must be within quotation marks.\
             \nResponds with a SpongeBob parroting version of <mock_message>\
             \nE.g. "SpongeBob" becomes SpOnGeBoB')
async def mock(ctx, mock_message: str):

    i = 0
    mocked = ""
    while i < len(mock_message):
        if i % 2 == 0:
            mocked += mock_message[i].upper()
        else:
            mocked += mock_message[i].lower()
        i+=1

    await ctx.send(mocked)



#create a random roast with user-inputted words
@bot.command(name='roast',help='Takes roast1 [and roast2] and inserts \n\
                          them randomly into a roast. May or may not make sense\n\
                          Type ,roasthelp for a full list of roasts')
async def roast(ctx, roast1: str, roast2: str):

    roast_list = ["If laughter is the best medicine, your face must be curing the world.",
                    "Being ugly is no crime. Which is good, otherwise you'd be in prison.",
                    "You had a good idea once... but it died of loneliness.",
                    "You have an answer for everything - the wrong one.",
                    "You have no equal. Everyone else is better.",
                    "You only have one bad habit... breathing.",
                    "Your head looks like a pear.",
                    "You make onions cry."]

    #select a random roast from the list and split it into its constituent words
    roast = random.choice(roast_list).split()

    #replacing first word in roast with first user-inputted word
    roast[random.randint(0, len(roast))] = roast1

    #replacing second word - may be same as first
    roast[random.randint(0, len(roast))] = roast2

    #putting the sentence back together
    roast = " ".join(roast)

    await ctx.send(roast)

#create a random roast with user-inputted words
@bot.command(name='groast',help='Takes roast1 (and roast2 [and roast 3]) and inserts\n\
                            them into a roast *at specific spots.*\n\
                            Type ,roasthelp for a full list of roasts\n\
                            A multi-word roast can be inserted by adding quotation marks around it,\n\
                            e.g. "steph\'s entropic pants" idea chem')
async def groast(ctx, roast1: str, roast2: str, roast3: str):

    roast_list = ["If w1 is the best medicine, w2 's w3 must be curing the world.",
                    "Being w1 is no crime. Which is good, otherwise w2 would be in w3.",
                    "w1 had a good w2 once... but it died of w3.",
                    "w1 has a w2 for everything - the w3 one.",
                    "w1 has no w2. w3 is better.",
                    "w1 only has one bad habit... w2.",
                    "w1 's head looks like a w2.",
                    "w1 makes onions cry.",
                    "w1 has a big w2 in their w3",
                    "w1 sounds like a w2",
                    "w1 is the reason w2 w3",
                    "w1 is a w2 on the w3"]

    #select a random roast from the list and split it into its constituent words
    roast = random.choice(roast_list).split()

    if "w1" in roast:
        roast[roast.index("w1")] = roast1
    if "w2" or "w2." in roast:
        roast[roast.index("w2")] = roast2
    if "w3" or "w3." in roast:
        roast[roast.index("w3")] = roast3

    roast = " ".join(roast)

    await ctx.send(roast)

#create a random roast with user-inputted words
@bot.command(name='roasthelp',help='List of roasts to use for ,roast and ,groast\n\
                                w1, w2, and w3 stand for user-inputted words')
async def roasthelp(ctx):

    roast_list = ["If w1 is the best medicine, w2 's w3 must be curing the world.",
                    "Being w1 is no crime. Which is good, otherwise w2 would be in w3.",
                    "w1 had a good w2 once... but it died of w3.",
                    "w1 has a w2 for everything - the w3 one.",
                    "w1 has no w2. w3 is better.",
                    "w1 only has one bad habit... w2.",
                    "w1 's head looks like a w2.",
                    "w1 makes onions cry.",
                    "w1 has a big w2 in their w3",
                    "w1 sounds like a w2",
                    "w1 is the reason w2 w3",
                    "w1 is a w2 on the w3"]

    rlist = "**List of roast templates:**\n>"
    for r in roast_list:
        rlist = rlist + r + "\n>"
    rlist = rlist[:-1]

    await ctx.send(rlist)



#Mashed up Shakespearean insults
@bot.command(name='s', help='Takes part of two Shakespearean insults and mashes them together.\n \
                             Doesn\'t work perfectly.')
async def shakesult(ctx):

    with open("shakesults.txt", "r") as text_file:
        shakesults = text_file.readlines()

    i = 0
    while i < len(shakesults):
        shakesults[i] = shakesults[i][:-1]
        i+=1

    insult1 = random.choice(shakesults)
    groups = insult1.split(' ')
    n = len(groups)//2
    if n >= 1:
        insult1a = ' '.join(groups[:n])
        insult1b = ' '.join(groups[n:])
    else:
        insult1a = groups[0]
        insult1b = groups[0]

    insult2 = random.choice(shakesults)
    groups = insult2.split(' ')
    n = len(groups)//2

    if n >= 1:
        insult2a = ' '.join(groups[:n])
        insult2b = ' '.join(groups[n:])
    else:
        insult2a = groups[0]
        insult2b = groups[0]

    first_half_options = [insult1a, insult2a]
    second_half_options = [insult1b, insult2b]

    done = False
    while done == False:
        response = str(random.choice(first_half_options) + " " + random.choice(second_half_options))
        if response != insult1 and response != insult2:
            done = True

    response = response + "\nMade using these insults: " + insult1 + " and " + insult2

    await ctx.send(response)

#returns music based on mood provided
@bot.command(name='mood', help='Responds with a YouTube link to a \
song that fits the mood provided.')
async def mood(ctx):

    ydl_opts = {'format': 'bestaudio', 'noplaylist': True, 'no_warnings': True}

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        video = ydl.extract_info(f'ytsearch10:{mood}', download=False)['entries'][random.randint(0,9)]

    results = video['webpage_url']

    r = random.randint(0,10)
    if r % 2 == 0:
        results = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"


    await ctx.send(f"{video['webpage_url']}")

@bot.command(name='rxn', help='Returns chemistry-related video')
async def rxn(ctx):

    ydl_opts = {'format': 'bestaudio', 'noplaylist': True, 'no_warnings': True}

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        video = ydl.extract_info(f'ytsearch10:chemistry', download=False)['entries'][random.randint(0,4)]

    await ctx.send(f"{video['webpage_url']}")



@bot.command(name='rate', help="Gives the @\'d person a rating! :)")
async def rate(ctx, target: discord.Member):

    #target.mention for mentioning users

    x = "~"
    #list of compliments/insults
    rate_list = [x + ", you look like you could use some sleep. Are you sure you\'re not a raccoon? \'Cuz you sure look like one.",
                 x + ", if you were twice as smart, you'd still be stupid",
                 x + ", you really put meaning into the phrase \'Three's a crowd\'.",
                 "Please learn some style, " + x + ". It'd do you a lot of good.",
                 "Neither good nor bad, you're just average, " + x,
                 "Lookin' pretty good, " + x,
                 "You're a great human bean, " + x,
                 "You're wonderful, " + x + "!",
                 "You look amazing, " + x + "! I'm sure you'd look even better if you dressed to the nines",
                 x + ", are you from Tennesee? \'Cuz you're the only ten I see ;)",
                 "Two, four, six, eight, who do we appreciate?" + target.mention + "!!!"]


    comp = rate_list[random.randint(5,10)]
    compliment = comp.replace("~", target.mention)

    if target.mention != ctx.message.author.mention:
        ins = rate_list[random.randint(0,4)]
        insult = ins.replace("~", ctx.message.author.mention)
        response = compliment + "\n" + insult
    else:
        response = compliment

    await ctx.send(response)

#fortune cookie message
@bot.command(name='f', help='Gives you a fortune. That\'s it.')
async def fortune(ctx):

    with open("fortunes.txt", "r") as text_file:
        fortunes = text_file.readlines()

    fortune = fortunes[random.randint(0,len(fortunes)-1)]

    await ctx.send(fortune)

@bot.command(name='pl')
async def piglatin(ctx, source: str):

    vowels = ['a', 'e', 'i', 'o', 'u']
    final = []

    #split inputted string into separate words
    source = source.split(" ")
    try:
        for word in source:
            word = word.lower()

            #retrieve and store first consonant (cluster) from word if it doesn't start with a vowel
            if word[0] not in vowels:
                i = 0
                to_move = ""
                stay = ""
                while i < len(word):
                    #add rest of word to 'stay'
                    if word[i] in vowels:
                        stay += word[i:]
                        break
                    to_move += word[i]
                    i+=1
                word = stay + to_move + "ay"
            else:
                word += "yay"

            final.append(word)
        final = " ".join(final)
    except:
        print("Well that didn't work")
        raise

    await ctx.send(final)


@bot.command(name='math')
async def mathinsult(ctx, source: str):

    symbols = ['1','2','3','4','5','6','7','8','9','0','+','=','-','/','*',]

    mathu = False

    i = 0
    while i < len(source):
        if source[i] in symbols:
            mathu = True
            break
        i += 1

    if mathu:
        result = "Why are you asking me to do math? Use your own brain, dumdum"
    else:
        result = "There isn't even any math involved here... learn your subjects, dumdum"

    await ctx.send(result)

####################### END OF COMMANDS SECTION ####################


bot.run(TOKEN)

#    embed = discord.Embed()
#    embed.set_image(url = 'http://youtube.com/watch?v=c8WmY0StIys')
