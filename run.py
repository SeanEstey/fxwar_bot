#!/usr/bin/env python3
import discord
from discord.ext import commands
import sqlite3

''' CREATE TABLE tUser
                        (username text, answer1 int, answer2 int, answer3 int, answer4 int, answer5 int) '''

client = commands.Bot(command_prefix="!")


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')



@client.event
async def on_message(message):
    chan = message.channel
    try:
        user_role = message.author.roles[1]
    except Exception:
        pass
    print("Processing new message")
    print("-"*15 + "\n")
    print(message.author.name)
    print(message.author.mention)

    try:
        for r in message.author.roles:
            print(r.name)
            if r.name == "General":
                if len(message.attachments) != 0:
                    await client.send_message(discord.Object(id=506716164337041420), "User: " + message.author.name + "\n" + message.content + "\n" +
                                        message.attachments[0]["url"])
    except AttributeError:
        pass
    print(chan.id)
    print(message.content)
    print("-"*15 + "\n")
    #if message.channel_mentions and message.author.name != client.user.name and (message.author.permissions_in(message.channel_mentions[0]).send_messages or message.author.permissions_in(message.channel_mentions[0]).administrator):
    #e = discord.Embed(title=message.author.name, description=message.content,)
    print("attachments: " + str(len(message.attachments)))
    chan_old = None
    if len(message.attachments) != 0:
        for chan in message.channel_mentions:
            if chan_old != chan and message.author.name != client.user.name and (message.author.permissions_in(chan).send_messages or message.author.permissions_in(chan).administrator):
                await client.send_message(chan,"User: "+ message.author.name+ "\n" +message.content + "\n" + message.attachments[0]["url"])
                chan_old = chan
    else:
        for chan in message.channel_mentions:
            if chan_old != chan and message.author.name != client.user.name and (message.author.permissions_in(chan).send_messages or message.author.permissions_in(chan).administrator):
                    await client.send_message(chan, "User: "+ message.author.name+ "\n" +message.content)
                    chan_old = chan

    await client.process_commands(message)

@client.event
async def on_member_join(member):
    role = discord.utils.get(member.server.roles, name="Civilian")
    await client.add_roles(member,role )
    print(member.name + " joined and got new role")

@client.command(pass_context=True,name="join")
async def join(ctx):
        user_dm = ctx.message.author
        conn = sqlite3.connect('user.db')
        c = conn.cursor()
        c.execute("SELECT username FROM tUser WHERE username=?",(user_dm.name + user_dm.id,))
        if not c.fetchall():
            reactions = ["1\u20e3","2\u20e3","3\u20e3","4\u20e3","5\u20e3","6\u20e3","\U0001f44d"]
            questions = ["Your Country: ","Level of Trading Experience (Select Most Applicable)\n\n:one: Brand New"+
                     "\n:two: Up to 1 Year\n:three: 1-2 Years\n:four: 2-5 Years\n:five: 5+ Years ",
                     "\nAre You Currently Trading Live or Demo?\n:one:Live\n:two:Demo",
                     "\nThe Broker You Trade Most With?\n:one:IFX Brokers\n:two:IC Markets\n:three:XM\n:four:Pepperstone\n:five:FX Pro\n:six:Other(Enter below)",
                     "\nTrading Style or Influences(Example ICT, RTM, Elliot, Sam Seiden, Dante, Price Action, etc): "]
            await client.send_message(ctx.message.author,"Please Complete Your Application by Answering a Few Questions.")
            message = await client.send_message(ctx.message.author,questions[0])
            answer1 = await client.wait_for_message(author=ctx.message.author, channel=message.channel)

            message = await client.send_message(ctx.message.author,questions[1])
            for reaction in reactions[:5]:
                await client.add_reaction(message, reaction)
            answer2 = await client.wait_for_reaction(["1\u20e3","2\u20e3","3\u20e3","4\u20e3","5\u20e3"],message=message,user=ctx.message.author)
            message = await client.send_message(user_dm,questions[2])
            for reaction in reactions[:2]:
                await client.add_reaction(message, reaction)
            answer3 = await client.wait_for_reaction(["1\u20e3", "2\u20e3"],message=message,user=ctx.message.author)

            message = await client.send_message(user_dm,questions[3])
            for reaction in reactions[:6]:
                await client.add_reaction(message,reaction)
            answer3 = await client.wait_for_reaction(["1\u20e3","2\u20e3","3\u20e3","4\u20e3","5\u20e3","6\u20e3"],message=message,user=ctx.message.author)


            message = await client.send_message(user_dm, questions[4])
            answer5 = await client.wait_for_message(author=user_dm, channel=message.channel)

            message = await client.send_message(user_dm, "Thanks For Participating!")
            message = 0
            role = discord.utils.get(user_dm.server.roles, name="Cadet")
            await client.add_roles(user_dm,role )
            await client.send_message(user_dm,"You have been upgraded to cadet and will have access to more channels. Glad to have you onboard.")
            await client.send_message(discord.Object(id=495887974991527948), "Welcome Cadet " + user_dm.mention)
            c.execute("INSERT INTO tUser(username, answer1, answer2, answer3, answer4, answer5) VALUES(?,?,?,?,?,?);",(user_dm.name + user_dm.id,answer1.content,answer2.reaction.emoji,answer3.reaction.emoji,answer4.content,answer5.content))
            conn.commit()
        else:
            await client.send_message(user_dm, "You've already done the survey!")
@client.command(pass_context=True,name="rankup")
async def rankup(ctx, role):
    if ctx.message.author.permissions_in(ctx.message.channel).administrator:
        user = ctx.message.mentions[0]
        role = discord.utils.get(ctx.message.mentions[0].server.roles, name=role)
        await client.add_roles(user, role)
        await client.send_message(discord.Object(id=495887974991527948),"Congratulations to " + user.mention + " for reaching the rank of " + role.name)
        print("Added role successfully")




client.run("NDk4NTkzNzg5MTc5NTkyNzI0.DpwA9Q.XdvY5QJ0jJj_A-iY-Q8Bu_0RoM0")
