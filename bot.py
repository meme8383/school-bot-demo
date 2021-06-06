# -*- coding: utf-8 -*-

# school-bot-demo
# All doxxing information has been removed.

#Image-------------------------------------------------------------------------

import re
#try:
#    from PIL import Image
#except ImportError:
#    import Image
#import pytesseract
#
#pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
#
#def readimage(imagepath):
#    return(pytesseract.image_to_string(Image.open(imagepath)))
#
#
#def findclasses(theschedule):
#    person = []
#    for i in range(len(classdata)):
#        try:
#            m = re.search(classdata['Key'][i], theschedule.lower())
#            if m:
#                person.append(i)
#        except AttributeError:
#            continue
#    if 7 in person and 18 in person:
#        person.remove(7)
#    return person

#Data--------------------------------------------------------------------------
    
import pandas as pd

botpath = ''
#botpath = './'
#botpath = ''
#botpath = ''


classdata = pd.read_csv(botpath + 'classes.csv')
classdata = classdata.set_index('ID')

usrdata = pd.read_csv(botpath + 'users.csv')

    
graderole = {'6': '6th Grade', '7': '7th Grade', '8': '8th Grade', '9': 'Freshman', '10': 'Sophomore', '11': 'Junior', '12': 'Senior', '13': 'Graduate', '14': 'Teacher'}
guestStatus = {0 : "Not in SCHOOL", 1 : "SCHOOL 1", 2 : "SCHOOL 2", 3 : "Other SCHOOL", '0' : "Not in SCHOOL", '1' : "SCHOOL 1", '2' : "SCHOOL 2", '3' : "Other SCHOOL"}

#Register----------------------------------------------------------------------

async def Register(user):
    global usrdata
    issues = 0
    print(datetime.datetime.now(), "Registering", user.name)
    await user.send("Welcome to the SCHOOL 1 discord (unofficial)! You may say 'cancel' at any point to exit and '" + prefix + "register' to retry.")
    
    embed = discord.Embed(title = "Are you currently in SCHOOL? (Graduates included)", description = "0: Not in SCHOOL\n1: In SCHOOL 1\n2: SCHOOL 2\n3: Other SCHOOL School", color = discord.Color.dark_purple())
    chooseGuest = await user.send(embed = embed)
    
    emojilist = [str(i) + "\N{combining enclosing keycap}" for i in range(0,4)]
    for i in emojilist:
        await chooseGuest.add_reaction(i)
    def check2(reaction, person):
        nonlocal emojilist
        return person == user and str(reaction) in emojilist
    try:
        reaction, _ = await client.wait_for('reaction_add', timeout = 600.0, check = check2)
    except asyncio.TimeoutError:
        print(datetime.datetime.now(), "Registration for", user.name, "failed: Timed out at choose from list")
        await user.send("Registration failed. You may do " + prefix + "register to retry.")
        return None
    guest = str(reaction)[0]
    
    await user.send("What is your real name? (First and last, if you would not like to give your name say 'Anonymous')")
    print(datetime.datetime.now(), user.name, "on step name")
    while True:
        def check(m):
            return m.guild == None and m.author == user
        try:
            msg = await client.wait_for('message', timeout = 300.0, check = check)
        except asyncio.TimeoutError:
            print(datetime.datetime.now(), "Registration for", user.name, "failed: Timed out at name")
            await user.send("Registration failed. You may do " + prefix + "register to retry.")
            return None
        
        if msg.content.lower() == "cancel":
            await user.send("Cancelled registration. You may do " + prefix + "register to retry.")
            print(datetime.datetime.now(), "User", user.name, "cancelled registration with", issues, "issues at name")
            return None
        elif ''.join(re.split(' |-|,', msg.content)).isalpha():
            irlname = msg.content.lower()
            break
        else:
            await user.send("Please only use letters a-z in your name. Enter your name again and contact an admin if you continue having issues.")
            issues += 1
            print(datetime.datetime.now(), "User", user.name, "had issue", issues, "with register at name")
            continue
        
        
    await user.send("Now, please say your grade (number 6-12, graduate = 13, teacher = 14)")
    print(datetime.datetime.now(), user.name, "on step grade")
    while True:
        try:
            msg2 = await client.wait_for('message', timeout = 300.0, check = check)
        except asyncio.TimeoutError:
            print(datetime.datetime.now(), "Registration for", user.name, "failed: Timed out at grade")
            await user.send("Registration failed. You may do " + prefix + "register to retry.")
            return None
        if msg2.content in graderole:
            grade = msg2.content
            break
        elif msg2.content.lower() == "cancel":
            await user.send("Cancelled registration. You may do " + prefix + "register to retry.")
            print(datetime.datetime.now(), "User", user.name, "cancelled registration with", issues, "issues at grade")
            return None
        else:
            await user.send("Please only use numbers 6-14 in your grade. Enter your grade again and contact an admin if you continue having issues.")
            issues += 1
            print(datetime.datetime.now(), "User", user.name, "had issue", issues, "with register at grade")
            continue
        
    if guest == "1":
        await user.send("Great, now begin to list your classes one by one (most abbreviations are allowed) or send a picture of your schedule (Coming soon!) and say 'done' when you are done. (Say done now to skip) (For precalc use 'pre-calc')")
        print(datetime.datetime.now(), user.name, "on step classes")
        listofclasses = []
        while True:
            if listofclasses:
                embed = discord.Embed(title = "Classes for " + user.name + ":", description = ''.join([classdata.loc[i]['Name'] + "\n" for i in listofclasses]), color = discord.Color.dark_purple())
                embed.set_footer(text = "Continue listing your classes and say 'done' when all of your classes are on this list")
                embed.set_thumbnail(url = user.avatar_url)
                await user.send(embed = embed)
            try:
                msg3 = await client.wait_for('message', timeout = 300.0, check = check)
            except asyncio.TimeoutError:
                print(datetime.datetime.now(), "Registration for", user.name, "failed: Timed out at classes")
                await user.send("Registration failed. You may do " + prefix + "register to retry.")
                return None
            
            
            if msg3.attachments:
                await user.send("Feature not implemented yet, please list your classes through text.")
                continue
                # await user.send("Reading schedule...")
                # await msg3.attachments[0].save(botpath + 'Saved/sched_' + user.name + '.png')
                # print(datetime.datetime.now(), "Saved schedule from", user.name, "as sched_" + user.name + ".png")
                # classes = pytesseract.image_to_string(Image.open(botpath + 'Saved/sched_' + user.name + '.png'))
                # listofclasses.append(findclasses(classes))
                # if len(listofclasses) >= 7:
                #     embed = discord.Embed(title = "Classes for " + user.name + ":", description = ''.join([classdata.loc[i]['Name'] + "\n" for i in listofclasses]), color = discord.Color.dark_purple())
                #     embed.set_thumbnail(url = user.avatar_url)
                #     await user.send(embed = embed)
                #     await user.send("Is this correct?")
                    
                #     try:
                #         msg4 = await client.wait_for('message', timeout = 60.0, check = check)
                #     except asyncio.TimeoutError:
                #         print(datetime.datetime.now(), "Registration for", user.name, "failed: Timed out at check classes")
                #         await user.send("Registration failed. You may do " + prefix + "register to retry.")
                #         return None
                #     if msg4.content.lower().startswith("y"):
                #         listofclasses.sort()
                #         usrdata = usrdata.append(pd.DataFrame({'User':['a' + str(user.id)], 'Classes':[str(listofclasses)], 'IRL' : [irlname], 'Grade' : [grade]}), sort = False, ignore_index = True)
                #         usrdata.to_csv(botpath + 'users.csv', index = False, encoding = 'utf8')
                #         usrdata = pd.read_csv(botpath + 'users.csv')
                #         print(datetime.datetime.now(), "Registered", user.name, "with classes in users.csv and", issues, "issues")
                #         break
                #     elif msg4.content.lower() == "cancel":
                #         await user.send("Cancelled registration. You may do " + prefix + "register to retry.")
                #         print(datetime.datetime.now(), "User", user.name, "cancelled registration with", issues, "issues at image (Check classes)")
                #         return None
                #     else:
                #         await user.send("Please send a better image or say no to skip adding classes. You may contact an admin if you continue having issues.")
                #         issues += 1
                #         print(datetime.datetime.now(), "User", user.name, "had issue", issues, "with register at image (incorrect classes)")
                #         continue
                # else:
                #     await user.send("Only found " + str(len(listofclasses)) + " classes, please send a better image or say no to skip adding classes. You may contact an admin if you continue having issues.")
                #     issues += 1
                #     print(datetime.datetime.now(), "User", user.name, "had issue", issues, "with register at image (too few classes - " + str(len(listofclasses)) + ")")
                #     continue
            
            
            elif msg3.content.lower() == "cancel":
                await user.send("Cancelled registration. You may do " + prefix + "register to retry.")
                print(datetime.datetime.now(), "User", user.name, "cancelled registration with", issues, "issues at classes (send)")
                return None
            
            
            elif msg3.content.lower() == "done":
                if len(listofclasses) >= 7:
                    listofclasses.sort()
                    usrdata = usrdata.append(pd.DataFrame({'User':['a' + str(user.id)], 'Classes':[str(listofclasses)], 'IRL' : [irlname], 'Grade' : [grade], 'Guest' : [guest]}), sort = False, ignore_index = True)
                    usrdata.to_csv(botpath + 'users.csv', index = False, encoding = 'utf8')
                    usrdata = pd.read_csv(botpath + 'users.csv')
                    print(datetime.datetime.now(), "Registered", user.name, "with classes in users.csv and", issues, "issues")
                    break
                elif listofclasses:
                    await user.send("You have only added " + str(len(listofclasses)) + " classes, are you sure?")
                    try:
                        msg4 = await client.wait_for('message', timeout = 300.0, check = check)
                    except asyncio.TimeoutError:
                        print(datetime.datetime.now(), "Registration for", user.name, "failed: Timed out at check classes")
                        await user.send("Registration failed. You may do " + prefix + "register to retry.")
                        return None
                    if msg4.content.lower().startswith("y"):
                        listofclasses.sort
                        usrdata = usrdata.append(pd.DataFrame({'User':['a' + str(user.id)], 'Classes':[str(listofclasses)], 'IRL' : [irlname], 'Grade' : [grade], 'Guest' : [guest]}), sort = False, ignore_index = True)
                        usrdata.to_csv(botpath + 'users.csv', index = False, encoding = 'utf8')
                        usrdata = pd.read_csv(botpath + 'users.csv')
                        print(datetime.datetime.now(), "Registered", user.name, "with classes in users.csv and", issues, "issues")
                        break
                    elif msg4.content.lower() == "cancel":
                        await user.send("Cancelled registration. You may do " + prefix + "register to retry.")
                        print(datetime.datetime.now(), "User", user.name, "cancelled registration with", issues, "issues at classes (Check classes)")
                        return None
                    else:
                        await user.send("Please continue listing classes one by one and say 'done' when all of your classes are added.")
                        continue
                else:
                    await user.send("No classes added. Are you sure you would like to continue without adding your classes?")
                    try:
                        msg4 = await client.wait_for('message', timeout = 300.0, check = check)
                    except asyncio.TimeoutError:
                        print(datetime.datetime.now(), "Registration for", user.name, "failed: Timed out at check classes")
                        await user.send("Registration failed. You may do " + prefix + "register to retry.")
                        return None
                    if msg4.content.lower().startswith("y"):
                        listofclasses = [0]
                        usrdata = usrdata.append(pd.DataFrame({'User':['a' + str(user.id)], 'Classes':['[0]'], 'IRL' : [irlname], 'Grade' : [grade], 'Guest' : [guest]}), sort = False, ignore_index = True)
                        usrdata.to_csv(botpath + 'users.csv', index = False, encoding = 'utf8')
                        usrdata = pd.read_csv(botpath + 'users.csv')
                        print(datetime.datetime.now(), "Registered", user.name, "without classes in users.csv and", issues, "issues")
                        break
                    elif msg4.content.lower() == "cancel":
                        await user.send("Cancelled registration. You may do " + prefix + "register to retry.")
                        print(datetime.datetime.now(), "User", user.name, "cancelled registration with", issues, "issues at classes (Check classes)")
                        return None
                    else:
                        await user.send("Please continue listing classes one by one and say 'done' when all of your classes are added.")
                        continue
                    
                    
            else:
                classmatches = []
                for i in range(len(classdata)):
                    matches = 0
                    for word in msg3.content.lower().split(" "):
                        if word == "i":
                            word = "1"
                        elif word == "ii":
                            word = "2"
                        elif word == "iii":
                            word = "3"
                        classname = classdata['Name'][i].lower().split(" ")
                        for part in range(len(classname)):
                            if classname[part] == "i":
                                classname[part] = "1"
                            elif classname[part] == "ii":
                                classname[part] = "2"
                            elif classname[part] == "iii":
                                classname[part] = "3"
                        classname = ''.join([i + " " for i in classname])[:-1]
                        if word in classname:
                            matches += 1
                    if matches == len(msg3.content.split(" ")):
                        classmatches.append(i)
                if len(classmatches) == 0:
                    await user.send("Class " + msg3.content + " not found, please try again. Write the class as it is written on the schedule, but abbreviations such as 'honors chem' and 'ap lang' are allowed.")
                    issues += 1
                    print(datetime.datetime.now(), "User", user.name, "had issue", issues, "with register at listclasses (class not found - " + msg3.content + ")")
                    continue
                elif len(classmatches) == 1:
                    await user.send("Found class " + classdata['Name'][classmatches[0]] + ", is this correct?")
                    try:
                        msg4 = await client.wait_for('message', timeout = 300.0, check = check)
                    except asyncio.TimeoutError:
                        print(datetime.datetime.now(), "Registration for", user.name, "failed: Timed out at choose from list")
                        await user.send("Registration failed. You may do " + prefix + "register to retry.")
                        return None
                    if msg4.content.lower().startswith("y"):
                        listofclasses.append(classmatches[0])
                        await user.send("Class " + classdata['Name'][classmatches[0]] + " added to your schedule.")
                        continue
                    else:
                        await user.send("Please try again. Write the class as it is written on the schedule, but abbreviations such as 'honors chem' and 'ap lang' are allowed.")
                        issues += 1
                        print(datetime.datetime.now(), "User", user.name, "had issue", issues, "with register at listclasses (incorrect classes)")
                        continue
                elif len(classmatches) > 8:
                    await user.send("Found " + str(len(classmatches)) + " matches, please be more specific.")
                else:
                    embed = discord.Embed(title = "Multiple classes found, please select the correct one by number:", description = "0: None of these\n" + ''.join([str(j + 1) + ": " + classdata['Name'][classmatches[j]] + "\n" for j in range(len(classmatches))]), color = discord.Color.dark_purple())
                    chooseclass = await user.send(embed = embed)
                    
                    emojilist = ['0\N{combining enclosing keycap}'] + [str(i + 1) + '\N{combining enclosing keycap}' for i in range(len(classmatches))]
                    for i in emojilist:
                        await chooseclass.add_reaction(i)
                    def check2(reaction, person):
                        nonlocal emojilist
                        return person == user and str(reaction) in emojilist
                    try:
                        reaction, _ = await client.wait_for('reaction_add', timeout = 300.0, check = check2)
                    except asyncio.TimeoutError:
                        print(datetime.datetime.now(), "Registration for", user.name, "failed: Timed out at choose from list")
                        await user.send("Registration failed. You may do " + prefix + "register to retry.")
                        return None
                    if str(reaction)[0] == "0":
                        await user.send("Please try again. Write the class as it is written on the schedule, but abbreviations such as 'honors chem' and 'ap lang' are allowed.")
                        issues += 1
                        print(datetime.datetime.now(), "User", user.name, "had issue", issues, "with register at listclasses (incorrect classes)")
                        continue
                    else:              
                        listofclasses.append(classmatches[int(str(reaction)[0]) - 1])
                        await user.send("Class " + classdata['Name'][classmatches[int(str(reaction)[0]) - 1]] + " added to your schedule.")
                        continue
    else:
        listofclasses = [0]
        usrdata = usrdata.append(pd.DataFrame({'User':['a' + str(user.id)], 'Classes':['[0]'], 'IRL' : [irlname], 'Grade' : [grade], 'Guest' : [guest]}), sort = False, ignore_index = True)
        usrdata.to_csv(botpath + 'users.csv', index = False, encoding = 'utf8')
        usrdata = pd.read_csv(botpath + 'users.csv')
        print(datetime.datetime.now(), "Registered", user.name, "without classes in users.csv and", issues, "issues")
    if guest == "0":
        await discord.utils.find(lambda m: m.id == user.id, schoolserver.members).add_roles(discord.utils.get(schoolserver.roles, name = "Not in SCHOOL"))
    elif guest == "2":
        await discord.utils.find(lambda m: m.id == user.id, schoolserver.members).add_roles(discord.utils.get(schoolserver.roles, name = "SCHOOL 2"))
    elif guest == "3":
        await discord.utils.find(lambda m: m.id == user.id, schoolserver.members).add_roles(discord.utils.get(schoolserver.roles, name = "Other SCHOOL"))
    elif guest == "1":
        await discord.utils.find(lambda m: m.id == user.id, schoolserver.members).add_roles(discord.utils.get(schoolserver.roles, name = graderole[grade]))
    await user.send("Thank you for registering! Your info is now visible through the .userinfo (user) command and you will be given access to the proper channels")
    await editwhois()




#Discord-----------------------------------------------------------------------

import asyncio
#import nest_asyncio
#nest_asyncio.apply()
import datetime
import discord
from discord.ext import commands

prefix = "."
client = commands.Bot(command_prefix = prefix)
client.remove_command('help')

schoolserver = ''
whoischannel = ''



@client.event
async def on_ready():
    print(datetime.datetime.now(), "Connected as", client.user)
    await client.change_presence(activity = discord.Game(".register to be added!"))
    global schoolserver, whoischannel
    schoolserver = client.get_guild(InsertID)
    whoischannel = schoolserver.get_channel(InsertID)
    global teacherlist, graduatelist, seniorlist, juniorlist, sophomorelist, freshmanlist, eighthlist, seventhlist, sixthlist, school2list, otherschoollist, notinschoollist
    teacherlist = await whoischannel.fetch_message(InsertID)
    graduatelist = await whoischannel.fetch_message(InsertID)
    seniorlist = await whoischannel.fetch_message(InsertID)
    juniorlist = await whoischannel.fetch_message(InsertID)
    sophomorelist = await whoischannel.fetch_message(InsertID)
    freshmanlist = await whoischannel.fetch_message(InsertID)
    eighthlist = await whoischannel.fetch_message(InsertID)
    seventhlist = await whoischannel.fetch_message(InsertID)
    sixthlist = await whoischannel.fetch_message(InsertID)
    school2list = await whoischannel.fetch_message(InsertID)
    otherschoollist = await whoischannel.fetch_message(InsertID)
    notinschoollist = await whoischannel.fetch_message(InsertID)
    
    
    
    
@client.event
async def on_member_join(member):
    print(datetime.datetime.now(), member.name, "joined, attempting to register")
    if 'a' + str(member.id) in usrdata.values:
        print(datetime.datetime.now(), "Not registering", member.name + ", already registered")
    else:
        await Register(member)




@client.event
async def on_member_remove(member):
    print(datetime.datetime.now, member.name, "left, attempting to remove from data")
    global usrdata
    if 'a' + str(member.id) in usrdata.values:
        usrdata = usrdata.set_index('User')
        usrdata = usrdata.drop('a' + str(member.id), axis = 0)
        usrdata.to_csv(botpath + 'users.csv', encoding = 'utf8')
        usrdata = pd.read_csv(botpath + 'users.csv')
        print(datetime.datetime.now(), "Deleted info for", member.name, "from users.csv")
        await editwhois()
    else:
        print(datetime.datetime.now, member.name, "was not registered")




@client.command()
async def ping(ctx):
    await ctx.send("Pong! (Latency: " + str(round(client.latency * 1000, 1)) + " ms)")
    print(datetime.datetime.now(), "Pinged by", ctx.author.name, ", latency was", str(round(client.latency * 1000, 1)), "ms")




@client.command()
async def reloadclasses(ctx):
    print(datetime.datetime.now(), ctx.author.name, "did command reloadclasses")
    global classdata
    if ctx.message.author.guild_permissions.administrator:
        classdata = pd.read_csv(botpath + 'classes.csv')
        classdata = classdata.set_index('ID')
        await ctx.send("Reloaded classes.csv")
        print(datetime.datetime.now(), "Reloaded classes.csv")
    else:
        print(datetime.datetime.now(), "Didn't reload, insufficient permissions")
        await ctx.send("You do not have permissions for this command!")
    
    
    
    
@client.command()   
async def reloadusers(ctx):
    print(datetime.datetime.now(), ctx.author.name, "did command reloadusers")
    global usrdata
    if ctx.message.author.guild_permissions.administrator:
        usrdata = pd.read_csv(botpath + 'users.csv')
        await ctx.send("Reloaded users.csv")
        print(datetime.datetime.now(), "Reloaded users.csv")
    else:
        print(datetime.datetime.now(), "Didn't reload, insufficient permissions")
        await ctx.send("You do not have permissions for this command!")




@client.command()
async def register(ctx, args = ''):
    if args and ctx.message.author.guild_permissions.administrator:
        try:
            user = ctx.message.mentions[0]
            await ctx.send("Messaged " + user.name)
        except IndexError:
            user = ctx.message.author
    else:
        user = ctx.message.author
    print(datetime.datetime.now(), ctx.author.name, "did command register for", user.name)
    if 'a' + str(user.id) in usrdata.values:
        if user == ctx.message.author:
            await ctx.send("Your info has already been saved! Use " + prefix + "delinfo to change it.")
        else:
            await ctx.send(user.name, "has already been registered!")
        print(datetime.datetime.now(), "Not registering", user.name + ", already registered")
    else:
        if ctx.guild:
            if user == ctx.message.author:
                await ctx.send("You have been messaged, please answer the messages through DM")
        elif user != ctx.message.author:
            await ctx.send(user, "has been messaged.")
        await Register(user)
       
        
        
            
@client.command()       
async def delinfo(ctx, args = ''):
    if ctx.message.author.guild_permissions.administrator:
        try:
            user = ctx.message.mentions[0]
        except IndexError:
            user = ctx.message.author
        global usrdata
        print(datetime.datetime.now(), ctx.author.name, "did command delinfo for", user)
        if 'a' + str(user.id) in usrdata.values:
            if user == ctx.message.author:
                await ctx.send("Are you sure you want to delete your info? This cannot be undone, and you will have to re-do .register")
            else:
                await ctx.send("Are you sure you want to delete info for " + user.name + "? This cannot be undone.")
        
            def check(m):
                return m.channel == ctx.channel and m.author == ctx.author
            
            try:
                msg = await client.wait_for('message', check = check, timeout = 60.0)
            except asyncio.TimeoutError:
                print(datetime.datetime.now(), "Delinfo for", user.name, "failed: Timed out")
                await ctx.send("Delinfo failed. You may do " + prefix + "delinfo to retry.")
                return None
            
            if msg.content.lower().startswith("y"): 
                
                await ctx.send("Deleting info...")
                usrdata = usrdata.set_index('User')
                usrdata = usrdata.drop('a' + str(user.id), axis = 0)
                usrdata.to_csv(botpath + 'users.csv', encoding = 'utf8')
                usrdata = pd.read_csv(botpath + 'users.csv')
                await ctx.send("Deleted info.")
                print(datetime.datetime.now(), "Deleted info for", user.name, "from users.csv")
                await editwhois()
            else:
                if user == ctx.message.author:
                    await ctx.send("Alright, I won't delete your info.")
                else:
                    await ctx.send("Alright, I won't delete " + user.name +  "'s info.")
        else:
            if user == ctx.message.author:
                await ctx.send("You don't have your info saved! Use " + prefix + "register to add your info.")
            else:
                await ctx.send(user.name + " doesn't have their info saved!")
    else:
        print(datetime.datetime.now(), ctx.author.name, "did command delinfo, no permissions")
        await ctx.send("You do not have permissions for this command!")
  
        
        
        
@client.command()
async def userinfo(ctx, arg = ""):
    if arg:
        try:
            user = ctx.message.mentions[0]
        except IndexError:
            user = ctx.message.author
    else:
        user = ctx.message.author
    print(datetime.datetime.now(),ctx.author.name, "did command userinfo for", user.name)
    if 'a' + str(user.id) in usrdata.values:
        for i in range(len(usrdata)):
            if usrdata['User'][i] == 'a' + str(user.id):
                embed = discord.Embed(color = discord.Color.dark_purple())
                embed.set_author(name = "Info for " + user.name + ":", icon_url = user.avatar_url)
                embed.add_field(name = "Name:", value = usrdata['IRL'][i].title(), inline = True)
                embed.add_field(name = "Grade:", value = usrdata['Grade'][i], inline = True)
                embed.add_field(name = "SCHOOL Status:", value = guestStatus[usrdata['Guest'][i]], inline = False)
                embed.add_field(name = "Classes:", value = ''.join([classdata.loc[int(j)]['Name'] + "\n" for j in usrdata['Classes'][i][1:-1].split(', ')]), inline = False)
                embed.set_thumbnail(url = user.avatar_url)
                await ctx.send(embed = embed)
    else:
        if user == ctx.message.author:
            await ctx.send("You are not registered! Use " + prefix + "register to add your info.")
        else:
            await ctx.send(user.name + " is not registered! Use " + prefix + "info to add your info.")
       
        
        

@client.command()
async def rawuserinfo(ctx, arg = ""):
    if arg:
        try:
            user = ctx.message.mentions[0]
        except IndexError:
            user = ctx.message.author
    else:
        user = ctx.message.author
    print(datetime.datetime.now(),ctx.author.name, "did command rawuserinfo for", user.name)
    if 'a' + str(user.id) in usrdata.values:
        for i in range(len(usrdata)):
            if usrdata['User'][i] == 'a' + str(user.id):
                await ctx.send(usrdata['User'][i] + ", " + str(usrdata['Guest'][i]) + ", " + str(usrdata['Grade'][i]) + ", " + str(usrdata['Classes'][i]) + ", "+ usrdata['IRL'][i])
    else:
        if user == ctx.message.author:
            await ctx.send("You are not registered! Use " + prefix + "register to add your info.")
        else:
            await ctx.send(user.name + " is not registered! Use " + prefix + "info to add your info.")




@client.command()
async def getroles(ctx):
    print(datetime.datetime.now(), ctx.author.name, "did command getroles")
    if 'a' + str(ctx.author.id) in usrdata.values:
        for i in range(len(usrdata)):
            if usrdata['User'][i] == 'a' + str(ctx.author.id):
                if int(usrdata['Guest'][i]) == 1:
                    await ctx.author.add_roles(discord.utils.get(ctx.author.guild.roles, name = graderole[usrdata['Grade'][i]]))
                else:
                    await ctx.author.add_roles(discord.utils.get(ctx.author.guild.roles, name = guestStatus[usrdata['Guest'][i]]))
    else:
        await ctx.send("You are not registered! Use " + prefix + "register to add your info.")




# @client.command()
# async def listusers(ctx):
#     print(datetime.datetime.now(), ctx.author.name, "did command listusers")
#     users = []
#     for i in range(len(usrdata)):
#         users.append(discord.utils.find(lambda m: m.id == int(usrdata['User'][i][1:]), schoolserver.members).mention + " - " + usrdata['IRL'][i].title())
#     embed = discord.Embed(title = "Registered Users:", description = ''.join([j + "\n" for j in users]), color = discord.Color.dark_purple())
#     embed.set_footer(text = "Total number of users: " + str(len(usrdata)))
#     await ctx.send(embed = embed)
    
    
    
    
@client.command()
async def listclasses(ctx):
    if ctx.message.author.guild_permissions.administrator:
        print(datetime.datetime.now(), ctx.author.name, "did command listclasses")
        classes = []
        for i in range(1, int(len(classdata)/2)):
            classes.append(classdata['Name'][i])
        embed = discord.Embed(title = "Classes:", description = ''.join([", " + j for j in classes])[2:], color = discord.Color.dark_purple())
        embed.set_footer(text = "Total number of classes: " + str(len(classdata) - 1))
        await ctx.send(embed = embed)
        classes = []
        for i in range(int(len(classdata)/2), len(classdata)):
            classes.append(classdata['Name'][i])
        embed = discord.Embed(title = "Classes:", description = ''.join([", " + j for j in classes])[2:], color = discord.Color.dark_purple())
        embed.set_footer(text = "Total number of classes: " + str(len(classdata) - 1))
        await ctx.send(embed = embed)
    else:
        print(datetime.datetime.now(), ctx.author.name, "did command listclasses, no permissions")
        await ctx.send("You do not have permissions for this command")
    



@client.command()
async def edit(ctx, name = '', change = '', *args):
    if ctx.message.author.guild_permissions.administrator:
        print(datetime.datetime.now(), ctx.author.name, "did command edit")
        if name and change and args:
            if change.lower() == "classes":
                to_change = 1
            elif change.lower() == "irl" or change.lower() == "name":
                to_change = 2
            elif change.lower() == "grade":
                to_change = 3
            elif change.lower() == "guest":
                to_change = 4
            else:
                await ctx.send("Invalid syntax: use " + prefix + "edit (user) (field) (value)")
                print(datetime.datetime.now(), ctx.author.name, "did command edit, invalid syntax")
                return None
            try:
                user = ctx.message.mentions[0]
            except IndexError:
                await ctx.send("Invalid syntax: use " + prefix + "edit (user) (field) (value)")
                print(datetime.datetime.now(), ctx.author.name, "did command edit, invalid syntax")  
                return None
            global usrdata
            for i in range(len(usrdata)):
                if 'a' + str(user.id) == usrdata['User'][i]:
                    person = [usrdata['User'][i], usrdata['Classes'][i], usrdata['IRL'][i], usrdata['Grade'][i], usrdata['Guest'][i]]
                    await user.remove_roles(discord.utils.get(schoolserver.roles, name = graderole[str(person[3])]))
                    await user.remove_roles(discord.utils.get(schoolserver.roles, name = guestStatus[str(person[4])]))
                    if to_change == 2 or to_change == 1:
                        person[to_change] = "".join([" " + i for i in args])[1:]
                    else:
                        person[to_change] = args[0]
                    usrdata = usrdata.set_index('User')
                    usrdata = usrdata.drop('a' + str(user.id), axis = 0)
                    usrdata.to_csv(botpath + 'users.csv', encoding = 'utf8')
                    usrdata = pd.read_csv(botpath + 'users.csv')
                    usrdata = usrdata.append(pd.DataFrame({'User' : [person[0]], 'Classes' : [person[1]], 'IRL' : [person[2]], 'Grade' : [person[3]], 'Guest' : [person[4]]}), sort = False, ignore_index = True)
                    usrdata.to_csv(botpath + 'users.csv', index = False, encoding = 'utf8')
                    usrdata = pd.read_csv(botpath + 'users.csv')
                    
                    if person[4] == "0":
                        await user.add_roles(discord.utils.get(schoolserver.roles, name = "Not in SCHOOL"))
                    elif person[4] == "2":
                        await user.add_roles(discord.utils.get(schoolserver.roles, name = "SCHOOL 2"))
                    elif person[4] == "3":
                        await user.add_roles(discord.utils.get(schoolserver.roles, name = "Other SCHOOL"))
                    elif person[4] == "1":
                        await user.add_roles(discord.utils.get(schoolserver.roles, name = graderole[str(person[3])]))
                    print(datetime.datetime.now(), "Updated", user.name, "in users.csv")
                    
                    embed = discord.Embed(color = discord.Color.dark_purple())
                    embed.set_author(name = "Info for " + user.name + ":", icon_url = user.avatar_url)
                    embed.add_field(name = "Name:", value = person[2].title(), inline = True)
                    embed.add_field(name = "Grade:", value = person[3], inline = True)
                    embed.add_field(name = "SCHOOL Status:", value = guestStatus[person[4]], inline = False)
                    embed.add_field(name = "Classes:", value = ''.join([classdata.loc[int(j)]['Name'] + "\n" for j in person[1][1:-1].split(', ')]), inline = False)
                    embed.set_thumbnail(url = user.avatar_url)
                    await ctx.send("Updated info for " + user.name, embed = embed)
                    break
            await editwhois()

        else:
            await ctx.send("Invalid syntax: use " + prefix + "edit (user) (field) (value)")
            print(datetime.datetime.now(), ctx.author.name, "did command edit, invalid syntax")
    else:
        print(datetime.datetime.now(), ctx.author.name, "did command edit, no permissions")
        await ctx.send("You do not have permissions for this command")




@client.command()
async def addclasses(ctx):
    print(datetime.datetime.now(), ctx.author.name, "did command addclasses")
    await ctx.send("You have been messaged, please answer the messages through DM")
    user = ctx.message.author
    await user.send("Begin to list your classes one by one (most abbreviations are allowed) or send a picture of your schedule (Coming soon!) and say 'done' when you are done. (For precalc use 'pre-calc')")
    listofclasses = []
    issues = 0
    global usrdata
    while True:
        if listofclasses:
            embed = discord.Embed(title = "Classes for " + user.name + ":", description = ''.join([classdata.loc[i]['Name'] + "\n" for i in listofclasses]), color = discord.Color.dark_purple())
            embed.set_footer(text = "Continue listing your classes and say 'done' when all of your classes are on this list")
            embed.set_thumbnail(url = user.avatar_url)
            await user.send(embed = embed)
        def check(m):
            return m.guild == None and m.author == user
        try:
            msg3 = await client.wait_for('message', timeout = 300.0, check = check)
        except asyncio.TimeoutError:
            print(datetime.datetime.now(), "Addclasses for", user.name, "failed: Timed out at classes")
            await user.send("Addclasses failed. You may do " + prefix + "addclasses to retry.")
            return None
        
        if msg3.attachments:
            await user.send("Feature not implemented yet, please list your classes through text.")
            continue
#            await user.send("Reading schedule...")
#            await msg3.attachments[0].save(botpath + 'Saved/sched_' + user.name + '.png')
#            print(datetime.datetime.now(), "Saved schedule from", user.name, "as sched_" + user.name + ".png")
#            classes = pytesseract.image_to_string(Image.open(botpath + 'Saved/sched_' + user.name + '.png'))
#            listofclasses.append(findclasses(classes))
#            if len(listofclasses) >= 7:
#                embed = discord.Embed(title = "Classes for " + user.name + ":", description = ''.join([classdata.loc[i]['Name'] + "\n" for i in listofclasses]), color = discord.Color.dark_purple())
#                embed.set_thumbnail(url = user.avatar_url)
#                await user.send(embed = embed)
#                await user.send("Is this correct?")
#                
#                try:
#                    msg4 = await client.wait_for('message', timeout = 60.0, check = check)
#                except asyncio.TimeoutError:
#                    print(datetime.datetime.now(), "Registration for", user.name, "failed: Timed out at check classes")
#                    await user.send("Registration failed. You may do " + prefix + "register to retry.")
#                    return None
#                if msg4.content.lower().startswith("y"):
#                    listofclasses.sort()
#                    usrdata = usrdata.append(pd.DataFrame({'User':['a' + str(user.id)], 'Classes':[str(listofclasses)], 'IRL' : [irlname], 'Grade' : [grade]}), sort = False, ignore_index = True)
#                    usrdata.to_csv(botpath + 'users.csv', index = False, encoding = 'utf8')
#                    usrdata = pd.read_csv(botpath + 'users.csv')
#                    print(datetime.datetime.now(), "Registered", user.name, "with classes in users.csv and", issues, "issues")
#                    break
#                elif msg4.content.lower() == "cancel":
#                    await user.send("Cancelled registration. You may do " + prefix + "register to retry.")
#                    print(datetime.datetime.now(), "User", user.name, "cancelled registration with", issues, "issues at image (Check classes)")
#                    return None
#                else:
#                    await user.send("Please send a better image or say no to skip adding classes. You may contact an admin if you continue having issues.")
#                    issues += 1
#                    print(datetime.datetime.now(), "User", user.name, "had issue", issues, "with register at image (incorrect classes)")
#                    continue
#            else:
#                await user.send("Only found " + str(len(listofclasses)) + " classes, please send a better image or say no to skip adding classes. You may contact an admin if you continue having issues.")
#                issues += 1
#                print(datetime.datetime.now(), "User", user.name, "had issue", issues, "with register at image (too few classes - " + str(len(listofclasses)) + ")")
#                continue
            
            
        elif msg3.content.lower() == "cancel":
            await user.send("Cancelled addclasses. You may do " + prefix + "addclasses to retry.")
            print(datetime.datetime.now(), "User", user.name, "cancelled addclasses with", issues, "issues")
            return None
        
        
        elif msg3.content.lower() == "done":
            if len(listofclasses) >= 7:
                listofclasses.sort()
                for i in range(len(usrdata)):
                    if 'a' + str(user.id) == usrdata['User'][i]:
                        person = [usrdata['User'][i], usrdata['Classes'][i], usrdata['IRL'][i], usrdata['Grade'][i], usrdata['Guest'][i]]
                        person[1] = listofclasses
                        usrdata = usrdata.set_index('User')
                        usrdata = usrdata.drop('a' + str(user.id), axis = 0)
                        usrdata.to_csv(botpath + 'users.csv', encoding = 'utf8')
                        usrdata = pd.read_csv(botpath + 'users.csv')
                        usrdata = usrdata.append(pd.DataFrame({'User' : [person[0]], 'Classes' : [person[1]], 'IRL' : [person[2]], 'Grade' : [person[3]], 'Guest' : [person[4]]}), sort = False, ignore_index = True)
                        usrdata.to_csv(botpath + 'users.csv', index = False, encoding = 'utf8')
                        usrdata = pd.read_csv(botpath + 'users.csv')
                        
                        print(datetime.datetime.now(), "Added classes for", user.name, "in users.csv")
                        
                        embed = discord.Embed(color = discord.Color.dark_purple())
                        embed.set_author(name = "Info for " + user.name + ":", icon_url = user.avatar_url)
                        embed.add_field(name = "Name:", value = person[2].title(), inline = True)
                        embed.add_field(name = "Grade:", value = person[3], inline = True)
                        embed.add_field(name = "SCHOOL Status:", value = guestStatus[person[4]], inline = False)
                        embed.add_field(name = "Classes:", value = ''.join([classdata.loc[int(j)]['Name'] + "\n" for j in str(person[1])[1:-1].split(', ')]), inline = False)
                        embed.set_thumbnail(url = user.avatar_url)
                        await user.send("Updated info for " + user.name, embed = embed)
                        break
                print(datetime.datetime.now(), "Added classes for", user.name, "in users.csv with", issues, "issues")
                break
            elif listofclasses:
                await user.send("You have only added " + str(len(listofclasses)) + " classes, are you sure?")
                try:
                    msg4 = await client.wait_for('message', timeout = 60.0, check = check)
                except asyncio.TimeoutError:
                    print(datetime.datetime.now(), "Addclasses for", user.name, "failed: Timed out at check classes")
                    await user.send("Addclasses failed. You may do " + prefix + "register to retry.")
                    return None
                if msg4.content.lower().startswith("y"):
                    listofclasses.sort
                    for i in range(len(usrdata)):
                        if 'a' + str(user.id) == usrdata['User'][i]:
                            person = [usrdata['User'][i], usrdata['Classes'][i], usrdata['IRL'][i], usrdata['Grade'][i]]
                            person[1] = listofclasses
                            usrdata = usrdata.set_index('User')
                            usrdata = usrdata.drop('a' + str(user.id), axis = 0)
                            usrdata.to_csv(botpath + 'users.csv', encoding = 'utf8')
                            usrdata = pd.read_csv(botpath + 'users.csv')
                            usrdata = usrdata.append(pd.DataFrame({'User' : [person[0]], 'Classes' : [person[1]], 'IRL' : [person[2]], 'Grade' : [person[3]], 'Guest' : [person[4]]}), sort = False, ignore_index = True)
                            usrdata.to_csv(botpath + 'users.csv', index = False, encoding = 'utf8')
                            usrdata = pd.read_csv(botpath + 'users.csv')
                            
                            print(datetime.datetime.now(), "Added classes for", user.name, "in users.csv")
                            
                            embed = discord.Embed(color = discord.Color.dark_purple())
                            embed.set_author(name = "Info for " + user.name + ":", icon_url = user.avatar_url)
                            embed.add_field(name = "Name:", value = person[2].title(), inline = True)
                            embed.add_field(name = "Grade:", value = person[3], inline = True)
                            embed.add_field(name = "SCHOOL Status:", value = guestStatus[person[4]], inline = False)
                            embed.add_field(name = "Classes:", value = ''.join([classdata.loc[int(j)]['Name'] + "\n" for j in str(person[1])[1:-1].split(', ')]), inline = False)
                            embed.set_thumbnail(url = user.avatar_url)
                            await user.send("Updated info for " + user.name, embed = embed)
                            break
                    print(datetime.datetime.now(), "Added classes for", user.name, "with", issues, "issues")
                    break
                elif msg4.content.lower() == "cancel":
                    await user.send("Cancelled addclasses. You may do " + prefix + "addclasses to retry.")
                    print(datetime.datetime.now(), "User", user.name, "cancelled addclasses with", issues, "issues at classes (Check classes)")
                    return None
                else:
                    await user.send("Please continue listing classes one by one and say 'done' when all of your classes are added.")
                    continue
            else:
                await user.send("No classes added. Are you sure you would like to continue without adding your classes?")
                try:
                    msg4 = await client.wait_for('message', timeout = 60.0, check = check)
                except asyncio.TimeoutError:
                    print(datetime.datetime.now(), "Addclasses for", user.name, "failed: Timed out at check classes")
                    await user.send("Registration failed. You may do " + prefix + "register to retry.")
                    return None
                if msg4.content.lower().startswith("y"):
                    listofclasses = [0]
                    for i in range(len(usrdata)):
                        if 'a' + str(user.id) == usrdata['User'][i]:
                            person = [usrdata['User'][i], usrdata['Classes'][i], usrdata['IRL'][i], usrdata['Grade'][i]]
                            person[1] = listofclasses
                            usrdata = usrdata.set_index('User')
                            usrdata = usrdata.drop('a' + str(user.id), axis = 0)
                            usrdata.to_csv(botpath + 'users.csv', encoding = 'utf8')
                            usrdata = pd.read_csv(botpath + 'users.csv')
                            usrdata = usrdata.append(pd.DataFrame({'User' : [person[0]], 'Classes' : [person[1]], 'IRL' : [person[2]], 'Grade' : [person[3]], 'Guest' : [person[4]]}), sort = False, ignore_index = True)
                            usrdata.to_csv(botpath + 'users.csv', index = False, encoding = 'utf8')
                            usrdata = pd.read_csv(botpath + 'users.csv')
                            
                            print(datetime.datetime.now(), "Added classes for", user.name, "in users.csv")
                            
                            embed = discord.Embed(color = discord.Color.dark_purple())
                            embed.set_author(name = "Info for " + user.name + ":", icon_url = user.avatar_url)
                            embed.add_field(name = "Name:", value = person[2].title(), inline = True)
                            embed.add_field(name = "Grade:", value = person[3], inline = True)
                            embed.add_field(name = "SCHOOL Status:", value = guestStatus[person[4]], inline = False)
                            embed.add_field(name = "Classes:", value = ''.join([classdata.loc[int(j)]['Name'] + "\n" for j in str(person[1])[1:-1].split(', ')]), inline = False)
                            embed.set_thumbnail(url = user.avatar_url)
                            await user.send("Updated info for " + user.name, embed = embed)
                            break
                    print(datetime.datetime.now(), "Registered", user.name, "with classes in users.csv and", issues, "issues")
                    break
                elif msg4.content.lower() == "cancel":
                    await user.send("Cancelled registration. You may do " + prefix + "register to retry.")
                    print(datetime.datetime.now(), "User", user.name, "cancelled registration with", issues, "issues at classes (Check classes)")
                    return None
                else:
                    await user.send("Please continue listing classes one by one and say 'done' when all of your classes are added.")
                    continue
                
                
        else:
            classmatches = []
            for i in range(len(classdata)):
                matches = 0
                for word in msg3.content.lower().split(" "):
                    if word == "i":
                        word = "1"
                    elif word == "ii":
                        word = "2"
                    elif word == "iii":
                        word = "3"
                    classname = classdata['Name'][i].lower().split(" ")
                    for part in range(len(classname)):
                        if classname[part] == "i":
                            classname[part] = "1"
                        elif classname[part] == "ii":
                            classname[part] = "2"
                        elif classname[part] == "iii":
                            classname[part] = "3"
                    classname = ''.join([i + " " for i in classname])[:-1]
                    if word in classname:
                        matches += 1
                if matches == len(msg3.content.split(" ")):
                    classmatches.append(i)
            if len(classmatches) == 0:
                await user.send("Class " + msg3.content + " not found, please try again. Write the class as it is written on the schedule, but abbreviations such as 'honors chem' and 'ap lang' are allowed.")
                issues += 1
                print(datetime.datetime.now(), "User", user.name, "had issue", issues, "with register at listclasses (class not found - " + msg3.content + ")")
                continue
            elif len(classmatches) == 1:
                await user.send("Found class " + classdata['Name'][classmatches[0]] + ", is this correct?")
                try:
                    msg4 = await client.wait_for('message', timeout = 60.0, check = check)
                except asyncio.TimeoutError:
                    print(datetime.datetime.now(), "Registration for", user.name, "failed: Timed out at choose from list")
                    await user.send("Registration failed. You may do " + prefix + "register to retry.")
                    return None
                if msg4.content.lower().startswith("y"):
                    listofclasses.append(classmatches[0])
                    await user.send("Class " + classdata['Name'][classmatches[0]] + " added to your schedule.")
                    continue
                else:
                    await user.send("Please try again. Write the class as it is written on the schedule, but abbreviations such as 'honors chem' and 'ap lang' are allowed.")
                    issues += 1
                    print(datetime.datetime.now(), "User", user.name, "had issue", issues, "with register at listclasses (incorrect classes)")
                    continue
            elif len(classmatches) > 8:
                await user.send("Found " + str(len(classmatches)) + " matches, please be more specific.")
            else:
                embed = discord.Embed(title = "Multiple classes found, please select the correct one by number:", description = "0: None of these\n" + ''.join([str(j + 1) + ": " + classdata['Name'][classmatches[j]] + "\n" for j in range(len(classmatches))]), color = discord.Color.dark_purple())
                chooseclass = await user.send(embed = embed)
                
                emojilist = ['0\N{combining enclosing keycap}'] + [str(i + 1) + '\N{combining enclosing keycap}' for i in range(len(classmatches))]
                for i in emojilist:
                    await chooseclass.add_reaction(i)
                def check2(reaction, person):
                    nonlocal emojilist
                    return person == user and str(reaction) in emojilist
                try:
                    reaction, _ = await client.wait_for('reaction_add', timeout = 60.0, check = check2)
                except asyncio.TimeoutError:
                    print(datetime.datetime.now(), "Registration for", user.name, "failed: Timed out at choose from list")
                    await user.send("Registration failed. You may do " + prefix + "register to retry.")
                    return None
                if str(reaction)[0] == "0":
                    await user.send("Please try again. Write the class as it is written on the schedule, but abbreviations such as 'honors chem' and 'ap lang' are allowed.")
                    issues += 1
                    print(datetime.datetime.now(), "User", user.name, "had issue", issues, "with register at listclasses (incorrect classes)")
                    continue
                else:              
                    listofclasses.append(classmatches[int(str(reaction)[0]) - 1])
                    await user.send("Class " + classdata['Name'][classmatches[int(str(reaction)[0]) - 1]] + " added to your schedule.")
                    continue




@client.command()
async def manregister(ctx, usermen = '', guest = '', grade = '', classes = '', *name):
    if ctx.message.author.guild_permissions.administrator:
        print(datetime.datetime.now(), ctx.author.name, "did command manregister")
        if usermen and name and grade and classes and guest:
            try:
                user = ctx.message.mentions[0]
            except IndexError:
                await ctx.send("Invalid syntax: use " + prefix + "manregister (user) (grade) (classes, without spaces) (name)")
                print(datetime.datetime.now(), ctx.author.name, "did command manregister, invalid syntax")
                return None
            global usrdata
            if 'a' + str(user.id) in usrdata.values:
                await ctx.send("User is already registered! Use " + prefix + "edit to edit their info.")
                print(datetime.datetime.now(), ctx.author.name, "did command manregister, user registered")
                return None
            name = ''.join([" " + i for i in name])[1:]
            classes = [int(i) for i in classes[1:-1].split(",")]
            usrdata = usrdata.append(pd.DataFrame({'User': ["a" + str(user.id)], 'Classes' : [classes], 'IRL' : [name], 'Grade' : [grade], 'Guest' : [guest]}), sort = False, ignore_index = True)
            usrdata.to_csv(botpath + 'users.csv', index = False, encoding = 'utf8')
            usrdata = pd.read_csv(botpath + 'users.csv')
            
            if int(guest) == 1:
                await user.add_roles(discord.utils.get(schoolserver.roles, name = graderole[str(grade)]))
            else:
                await user.add_roles(discord.utils.get(schoolserver.roles, name = guestStatus[str(guest)]))
            print(datetime.datetime.now(), "Updated", user.name, "in users.csv")
            
            embed = discord.Embed(color = discord.Color.dark_purple())
            embed.set_author(name = "Info for " + user.name + ":", icon_url = user.avatar_url)
            embed.add_field(name = "Name:", value = name.title(), inline = True)
            embed.add_field(name = "Grade:", value = grade, inline = True)
            embed.add_field(name = "SCHOOL Status:", value = guestStatus[str(guest)], inline = False)
            embed.add_field(name = "Classes:", value = ''.join([classdata.loc[int(j)]['Name'] + "\n" for j in classes[1:-1].split(', ')]), inline = False)
            embed.set_thumbnail(url = user.avatar_url)
            await ctx.send("Updated info for " + user.name, embed = embed)
            await editwhois()
        else:
            await ctx.send("Invalid syntax: use " + prefix + "manregister (user) (grade) (classes, without spaces) (name)")
            print(datetime.datetime.now(), ctx.author.name, "did command manregister, invalid syntax")
    else:
        print(datetime.datetime.now(), ctx.author.name, "did command manregister, no permissions")
        await ctx.send("You do not have permissions for this command")
        
        
        
        
@client.command()
async def classinfo(ctx, *classn):
    if not classn:
        print(datetime.datetime.now(), ctx.author.name, "did command classinfo, no class specified")
        await ctx.send("Invalid syntax: use " + prefix + "classinfo (class)")
        return None
    classn = ''.join([i + ' ' for i in classn])[:-1]
    print(datetime.datetime.now(), ctx.author.name, "did command classinfo for", classn)
    classmatches = []
    for i in range(len(classdata)):
        matches = 0
        for word in classn.lower().split(" "):
            if word == "i":
                word = "1"
            elif word == "ii":
                word = "2"
            elif word == "iii":
                word = "3"
            classname = classdata['Name'][i].lower().split(" ")
            for part in range(len(classname)):
                if classname[part] == "i":
                    classname[part] = "1"
                elif classname[part] == "ii":
                    classname[part] = "2"
                elif classname[part] == "iii":
                    classname[part] = "3"
            classname = ''.join([i + " " for i in classname])[:-1]
            if word in classname:
                matches += 1
        if matches == len(classn.split(" ")):
            classmatches.append(i)
    if len(classmatches) == 0:
       await ctx.send("Class " + classn + " not found, please try again. Write the class as it is written on the schedule, but abbreviations such as 'honors chem' and 'ap lang' are allowed.")
       return None
    elif len(classmatches) == 1:
        classn = classmatches[0]
    elif len(classmatches) > 8:
        await ctx.send("Found " + str(len(classmatches)) + " matches, please be more specific.")
        return None
    else:
        embed = discord.Embed(title = "Multiple classes found, please select the correct one by number:", description = "0: None of these\n" + ''.join([str(j + 1) + ": " + classdata['Name'][classmatches[j]] + "\n" for j in range(len(classmatches))]), color = discord.Color.dark_purple())
        chooseclass = await ctx.send(embed = embed)
        
        emojilist = ['0\N{combining enclosing keycap}'] + [str(i + 1) + '\N{combining enclosing keycap}' for i in range(len(classmatches))]
        for i in emojilist:
            await chooseclass.add_reaction(i)
        def check2(reaction, person):
            nonlocal emojilist
            return person == ctx.author and str(reaction) in emojilist
        try:
            reaction, _ = await client.wait_for('reaction_add', timeout = 60.0, check = check2)
        except asyncio.TimeoutError:
            print(datetime.datetime.now(), "Classinfo by", ctx.author.name, "failed: Timed out at choose from list")
            await ctx.send("You took too long to choose, please do " + prefix + "classinfo to retry")
            return None
        if str(reaction)[0] == "0":
            await ctx.send("Please try again. Write the class as it is written on the schedule, but abbreviations such as 'honors chem' and 'ap lang' are allowed. (For precalc use 'pre-calc')")
            return None
        else: 
            classn = classmatches[int(str(reaction)[0]) - 1]
    users = []
    for i in range(len(usrdata)):
        usrclasses = usrdata['Classes'][i][1:-1].split(', ')
        if str(classn) in usrclasses:
            users.append(discord.utils.find(lambda m: m.id == int(usrdata['User'][i][1:]), schoolserver.members).mention + " - " + usrdata['IRL'][i].title())
    embed = discord.Embed(title = "Info for " + classdata['Name'][classn] + ":", color = discord.Color.dark_purple())
    if users:
        embed.add_field(name = "Users in class:", value = ''.join([i + "\n" for i in users]), inline = True)
    else:
        embed.add_field(name = "Users in class:", value = "No users found", inline = True)
    embed.set_footer(text = "ID: " + str(classn))
    await ctx.send(embed = embed)
    



@client.command()
async def help(ctx):
    print(datetime.datetime.now(), ctx.author.name, "did command help")
    embed = discord.Embed(title = "SCHOOL Bot Commands:", description = "**.ping**: Pings the bot and returns the bot's latency\n**.register**: Register yourself in the SCHOOL Bot system\n**.addclasses**: Add your classes in the SCHOOL Bot system\n**.getroles**: Get your grade role if you do not have it already\n**.userinfo (user)**: Get information about a user, such as name, grade, and classes\n**.classinfo (class)**: Get a list of users in a specific class\n", color = discord.Color.dark_purple())
    embed.set_footer(text = "Use .adminhelp for help with admin commands")
    embed.set_thumbnail(url = client.user.avatar_url)
    await ctx.send(embed = embed)


@client.command()
async def adminhelp(ctx):
    print(datetime.datetime.now(), ctx.author.name, "did command adminhelp")
    embed = discord.Embed(title = "SCHOOL Bot Admin Commands:", description = "**.register (user)**: Begin a user's registration process\n**.manregister (user) (grade) (classes) (name)**: Manually input a user's information\n**.delinfo (user)**: Delete a user's information\n**.edit (user) (field) (value)**: Edit a specific field in a user's info\n**.rawuserinfo (user)**: Get a user's information as it is in the system\n**.reloadclasses**: Reload the class database\n**.reloadusers**: Reload the user database\n**.whois**: Send the who-is messages (DON'T USE)\n**.reloadwhois**: Reload the who-is embeds", color = discord.Color.dark_purple())
    embed.set_thumbnail(url = client.user.avatar_url)
    if not ctx.author.guild_permissions.administrator:
        embed.set_footer(text = "You do not have permissions to use these commands! Use .help for the commands you can use")
        embed.set_author(name = "You do not have permissions to use these commands!")
    await ctx.send(embed = embed)

#Who-is------------------------------------------------------------------------    



@client.command()
async def whois(ctx):
    print(datetime.datetime.now(), ctx.author.name, "did command whois")
    if ctx.message.author.guild_permissions.administrator:
        global teacherlist, graduatelist, seniorlist, juniorlist, sophomorelist, freshmanlist, eighthlist, seventhlist, sixthlist, school2list, otherschoollist, notinschoollist
        teacherlist = await ctx.send(embed = await gradeusers(14))
        graduatelist = await ctx.send(embed = await gradeusers(13))
        seniorlist = await ctx.send(embed = await gradeusers(12))
        juniorlist = await ctx.send(embed = await gradeusers(11))
        sophomorelist = await ctx.send(embed = await gradeusers(10))
        freshmanlist = await ctx.send(embed = await gradeusers(9))
        eighthlist = await ctx.send(embed = await gradeusers(8))
        seventhlist = await ctx.send(embed = await gradeusers(7))
        sixthlist = await ctx.send(embed = await gradeusers(6))
        school2list = await ctx.send(embed = await guestusers(2))
        otherschoollist = await ctx.send(embed = await guestusers(3))
        notinschoollist = await ctx.send(embed = await guestusers(0))
    else:
        print(datetime.datetime.now(), ctx.author.name, "did command whois, no permissions")
        await ctx.send("You do not have permissions for this command")


async def gradeusers(grade):
    gradename = {14 : "Teachers", 13 : "Graduates", 12 : "Seniors", 11 : "Juniors" , 10 : "Sophomores", 9 : "Freshmen", 8 : "8th Grade", 7 : "7th Grade", 6 : "6th Grade"}
    gradecolors = {14 : discord.Color.magenta(), 13 : discord.Color.green(), 12 : discord.Color.red(), 11 : discord.Color.purple(), 10 : discord.Color.gold(), 9 : discord.Color.teal(), 8 : discord.Color.blue(), 7 : discord.Color.dark_magenta(), 6 : discord.Color.dark_gold()}
    users = []
    global usrdata
    for i in range(len(usrdata)):
        if usrdata['Grade'][i] == grade and int(usrdata['Guest'][i]) == 1:
            users.append(i)
    if users:
        embed = discord.Embed(title = gradename[grade], description = ''.join([discord.utils.find(lambda m: m.id == int(usrdata['User'][i][1:]), schoolserver.members).mention + " - " + usrdata['IRL'][i].title() + "\n" for i in users]), color = gradecolors[grade])
    else:
        embed = discord.Embed(title = gradename[grade], description = "None :)", color = gradecolors[grade])
    embed.set_footer(text = "Length: " + str(len(users)))
    return embed

async def guestusers(guest):
    guestname = {0 : "Not in SCHOOL", 2 : "SCHOOL 2", 3 : "Other SCHOOL"}
    guestcolors = {0 : discord.Color.darker_grey(), 2 : discord.Color.dark_blue(), 3 : discord.Color.light_grey()}
    users = []
    global usrdata
    for i in range(len(usrdata)):
        if usrdata['Guest'][i] == guest:
            users.append(i)
    if users:
        embed = discord.Embed(title = guestname[guest], description = ''.join([discord.utils.find(lambda m: m.id == int(usrdata['User'][i][1:]), schoolserver.members).mention + " - " + usrdata['IRL'][i].title() + "\n" for i in users]), color = guestcolors[guest])
    else:
        embed = discord.Embed(title = guestname[guest], description = "None :)", color = guestcolors[guest])
    embed.set_footer(text = "Length: " + str(len(users)))
    return embed

    
async def editwhois():
    print(datetime.datetime.now(), "Refreshing who-is")
    global teacherlist, graduatelist, seniorlist, juniorlist, sophomorelist, freshmanlist, eighthlist, seventhlist, sixthlist, school2list, otherschoollist, notinschoollist
    await teacherlist.edit(embed = await gradeusers(14))
    await graduatelist.edit(embed = await gradeusers(13))
    await seniorlist.edit(embed = await gradeusers(12))
    await juniorlist.edit(embed = await gradeusers(11))
    await sophomorelist.edit(embed = await gradeusers(10))
    await freshmanlist.edit(embed = await gradeusers(9))
    await eighthlist.edit(embed = await gradeusers(8))
    await seventhlist.edit(embed = await gradeusers(7))
    await sixthlist.edit(embed = await gradeusers(6))
    await school2list.edit(embed = await guestusers(2))
    await otherschoollist.edit(embed = await guestusers(3))
    await notinschoollist.edit(embed = await guestusers(0))
    print(datetime.datetime.now(), "Refreshed who-is")


@client.command()
async def refreshwhois(ctx):
    print(datetime.datetime.now(), ctx.author.name, "did command refreshwhois")
    if ctx.message.author.guild_permissions.administrator:
        await ctx.send("Refreshing who-is...")
        try:
            await editwhois()
        except:
            await ctx.send("Error refreshing who-is. Check the log for details.")
        else:
            await ctx.send("Refreshed who-is.")
    else:
        print(datetime.datetime.now(), ctx.author.name, "did command refreshwhois, no permissions")
        await ctx.send("You do not have permissions for this command")

#------------------------------------------------------------------------------

token = open(botpath + 'token.txt').read()
client.run(token)
