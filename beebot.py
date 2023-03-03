import discord
import re
import typing
import asyncpraw
import random
import requests
import os
import random
import collections
import asyncio
import sqlite3
from datetime import datetime, timedelta
from PIL import Image
from io import BytesIO
import re
from prometheus_client import start_http_server, Counter, Histogram, Gauge, Summary
import openai
import replicate

class BeeClient(discord.Client):
    
    promSummary = Summary('summaryCommands', 'Commands exectued', ['command'])
    promNickGauge = Gauge('gaugeNicknames', 'Amount of nicknames in the database as Gauge')
    defaultPersonality = 'The following is a conversation with a discord AI chatbot. The chatbot is generally friendly and is themed around bees.'
    personality = 'The following is a conversation with a discord AI chatbot. The chatbot is generally friendly and is themed around bees.'
    nextChat = datetime.now()
    with open('openaiToken') as f:
        openai.api_key = f.read()
    
    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')
        
        # channel = await client.fetch_channel('330158485704802305')
        
        #afterDate = datetime.datetime(2022, 05, 02, hour=0, minute=0, second=0, microsecond=0, tzinfo=datetime.tzinfo().tzname('UTC'))

        # with open('markov2.txt' , "w+", encoding="utf-8") as output_file:
        #     async for message in channel.history(after=afterDate, limit=100000):
        #         output = message.content + "\n"
        #         output_file.write(output)
        
        # while True:
        #     await asyncio.sleep(random.randint(7200, 14400))
        #     chance = random.randint(1, 3)
        #     if chance == 1:
        #         seedWord = random.choice(wordList)
        #         sentenceLength = random.randint(7, 25)

        #         sentence = seedWord.capitalize()
        #         for i in range(0, sentenceLength):
        #             nextWord = random.choice(markovTable[seedWord])
        #             seedWord = nextWord

        #             sentence += " " + seedWord
                
        #         channel = await client.fetch_channel('330158485704802305')
        #         await channel.send(sentence)
        #     elif chance == 2:
        #         channel = await client.fetch_channel('330158485704802305')
        #         await channel.send("Bzzzz...")
        #     elif chance == 3:
        #         channel = await client.fetch_channel('330158485704802305')
        #         await channel.send("*lays down a smooth saxophone solo*")     
            
    async def on_reaction_add(self, reaction, user):
        roleList = []
        modID = 383445089806188545
        guild = await client.fetch_guild('330158485704802305')
        member = await guild.fetch_member(user.id)
        
        for r in member.roles:
            roleList.append(r.id)
            
        if (modID in roleList or user.id == 162571470256472066) and str(reaction) == '🗑️' and reaction.message.author.id == 948158071279083531:
            await reaction.message.delete()

    async def on_message(self, message):
        if message.author.id == self.user.id:
            return
        
        chance = random.randint(1, 9999999)
        if chance == 255:
            await message.channel.send('https://i.imgur.com/5NxrG0r.jpg')
            
        if message.content.startswith('!personality'):
            self.promSummary.labels('personality').observe(1)
            self.personality = f'The following is a conversation with a discord AI chatbot. {str(message.content)[13:]}'
            await message.channel.send('Personality for the next !chat command changed.')
        
        if message.content.startswith('!chat'):
            print(datetime.now())
            print(self.nextChat)
            if datetime.now() < self.nextChat:
                return
            
            self.promSummary.labels('chat').observe(1)
            msg = str(message.content)[6:]
            
            try:
                response = openai.Completion.create(
                    model="text-davinci-003",
                    prompt=f"{self.personality}\n\nHuman: {msg} AI:",
                    temperature=0.9,
                    max_tokens=150,
                    top_p=1,
                    frequency_penalty=0.0,
                    presence_penalty=0.6,
                    stop=[" Human:", " AI:"]
                )
            except openai.error.RateLimitError:
                await message.channel.send('Monthly token limit reached. If you want to increase this, consider a small donation <3')
                return
            
            returnText = response['choices'][0]['text'].strip() 
            self.promSummary.labels('tokensUsed').observe(response['usage']['total_tokens'])
            self.promSummary.labels('bonbyChat').observe(returnText.lower().count('bonby'))
            await message.channel.send(returnText)
            self.personality = self.defaultPersonality
            self.nextChat = datetime.now() + timedelta(seconds=120)

        if message.content.startswith('!hugemoji') or message.content.startswith('!hm'):
            self.promSummary.labels('hugemoji').observe(1)
            try:
                sentEmoji = get_message_emojis(message)[0]
            except IndexError:
                return
            
            if sentEmoji.animated:
                await message.delete()
                await message.channel.send(f'https://cdn.discordapp.com/emojis/{sentEmoji.id}.gif?quality=lossless')
                return
            else:
                response = requests.get(f'https://cdn.discordapp.com/emojis/{sentEmoji.id}.png?quality=lossless')
                img = Image.open(BytesIO(response.content))
                imgName = random.randint(1000000, 9999999)
                basewidth = 512
                wpercent = (basewidth/float(img.size[0]))
                hsize = int((float(img.size[1])*float(wpercent)))
                
                option = str(message.content).split(' ')[-1]

                if option == 'aa':
                    img = img.resize((basewidth,hsize), Image.ANTIALIAS)
                else:
                    img = img.resize((basewidth,hsize))
                    
                img.save(f'{imgName}.png')
                with open(f'{imgName}.png', 'rb') as f:
                    pic = discord.File(f)
                    await message.delete()
                    await message.channel.send(file=pic)
                os.remove(f'{imgName}.png')
                
        if message.content.startswith('!racon'):
            self.promSummary.labels('racon').observe(1)
            await message.channel.send('Buzzing for a trashy image...')
            reddit = asyncpraw.Reddit(
                client_id=redditID,
                client_secret=redditSecret,
                user_agent="android:com.beebot:v0.0.1 (by u/michaellaneous)",
            )
            
            subreddit = await reddit.subreddit('Raccoons')
            while True:            
                submission = await subreddit.random()
                image_formats = ('png', 'jpg', 'jpeg', 'gif')
                if str(submission.url).split('.')[-1] in image_formats:
                    await message.channel.send(submission.url)
                    await reddit.close()
                    return
                
        if message.content.startswith('!frog'):
            self.promSummary.labels('frog').observe(1)
            await message.channel.send('Buzzing for a ribbit...')
            reddit = asyncpraw.Reddit(
                client_id=redditID,
                client_secret=redditSecret,
                user_agent="android:com.beebot:v0.0.1 (by u/michaellaneous)",
            )
            
            subreddit = await reddit.subreddit('frogs')
            while True:            
                submission = await subreddit.random()
                image_formats = ('png', 'jpg', 'jpeg', 'gif')
                if str(submission.url).split('.')[-1] in image_formats:
                    await message.channel.send(submission.url)
                    await reddit.close()
                    return
                
        if message.content.startswith('!capybara'):
            self.promSummary.labels('capybara').observe(1)
            await message.channel.send('Buzzing for a chill image...')
            reddit = asyncpraw.Reddit(
                client_id=redditID,
                client_secret=redditSecret,
                user_agent="android:com.beebot:v0.0.1 (by u/michaellaneous)",
            )
            
            subreddit = await reddit.subreddit('capybara')
            while True:            
                submission = await subreddit.random()
                image_formats = ('png', 'jpg', 'jpeg', 'gif')
                if str(submission.url).split('.')[-1] in image_formats:
                    await message.channel.send(submission.url)
                    await reddit.close()
                    return

        if message.content == ('!bee'):
            self.promSummary.labels('bee').observe(1)
            await message.channel.send('Buzzing for a friend...')
            reddit = asyncpraw.Reddit(
                client_id=redditID,
                client_secret=redditSecret,
                user_agent="android:com.beebot:v0.0.1 (by u/michaellaneous)",
            )
            
            subreddit = await reddit.subreddit('bees')
            while True:            
                submission = await subreddit.random()
                image_formats = ('png', 'jpg', 'jpeg', 'gif')
                if str(submission.url).split('.')[-1] in image_formats:
                    await message.channel.send(submission.url)
                    await reddit.close()
                    return
                
        if message.content == ('!burger'):
            self.promSummary.labels('burger').observe(1)
            await message.channel.send('Buzzing for a burg...')
            reddit = asyncpraw.Reddit(
                client_id=redditID,
                client_secret=redditSecret,
                user_agent="android:com.beebot:v0.0.1 (by u/michaellaneous)",
            )
            
            subreddit = await reddit.subreddit('burgerporn')
            while True:            
                submission = await subreddit.random()
                image_formats = ('png', 'jpg', 'jpeg', 'gif')
                if str(submission.url).split('.')[-1] in image_formats:
                    await message.channel.send(submission.url)
                    await reddit.close()
                    return

        if message.content.startswith('!pomo'):
            self.promSummary.labels('pomo').observe(1)
            await message.channel.send('Buzzing for a small, good boy...')
            reddit = asyncpraw.Reddit(
                client_id=redditID,
                client_secret=redditSecret,
                user_agent="android:com.beebot:v0.0.1 (by u/michaellaneous)",
            )
            
            subreddit = await reddit.subreddit('pomeranians')
            while True:            
                submission = await subreddit.random()
                image_formats = ('png', 'jpg', 'jpeg', 'gif')
                if str(submission.url).split('.')[-1] in image_formats:
                    await message.channel.send(submission.url)
                    await reddit.close()
                    return
                

        if message.content.startswith('!bird'):
            self.promSummary.labels('bird').observe(1)
            await message.channel.send('Buzzing for a loud birb...')
            reddit = asyncpraw.Reddit(
                client_id=redditID,
                client_secret=redditSecret,
                user_agent="android:com.beebot:v0.0.1 (by u/michaellaneous)",
            )
            
            subreddit = await reddit.subreddit('birbs')
            while True:            
                submission = await subreddit.random()
                image_formats = ('png', 'jpg', 'jpeg', 'gif')
                if str(submission.url).split('.')[-1] in image_formats:
                    await message.channel.send(submission.url)
                    await reddit.close()
                    return

                
        if message.content.startswith('!dog'):
            self.promSummary.labels('dog').observe(1)
            await message.channel.send('Buzzing for a good boy...')
            reddit = asyncpraw.Reddit(
                client_id=redditID,
                client_secret=redditSecret,
                user_agent="android:com.beebot:v0.0.1 (by u/michaellaneous)",
            )
            
            subreddit = await reddit.subreddit('dogpictures')
            while True:            
                submission = await subreddit.random()
                image_formats = ('png', 'jpg', 'jpeg', 'gif')
                if str(submission.url).split('.')[-1] in image_formats:
                    await message.channel.send(submission.url)
                    await reddit.close()
                    return
                
        if message.content == ('!cat'):
            self.promSummary.labels('cat').observe(1)
            await message.channel.send('Buzzing for a sneaky feline...')
            reddit = asyncpraw.Reddit(
                client_id=redditID,
                client_secret=redditSecret,
                user_agent="android:com.beebot:v0.0.1 (by u/michaellaneous)",
            )
            
            subreddit = await reddit.subreddit('catpictures')
            while True:            
                submission = await subreddit.random()
                image_formats = ('png', 'jpg', 'jpeg', 'gif')
                if str(submission.url).split('.')[-1] in image_formats:
                    await message.channel.send(submission.url)
                    await reddit.close()
                    return

        
        if message.content.startswith('!hearsay'):
            self.promSummary.labels('hearsay').observe(1)
            hearsayImages = ('https://i.imgur.com/i1PQNeH.gif',
                             'https://media.discordapp.net/attachments/492731531379605504/978334696024973392/9lsj7zyx.gif',
                             'https://cdn.discordapp.com/attachments/841397604536680509/979840713346928760/9BCF52E4-FF3D-404D-8B3C-E67A3DA288A8.gif',
                             'https://media.discordapp.net/attachments/729451939854680196/963380255152799774/possum-1.gif',
                             'https://cdn.discordapp.com/attachments/273670786148073473/989325553372897360/unknown.png',
                             'https://cdn.discordapp.com/attachments/772155378393546762/997254489549586442/6E5DFD66-199E-4EDD-8CE5-1F931331E482.gif',
                             'https://tenor.com/view/nerding-speech-bubble-pepe-nerd-gif-26077806')
                         
            await message.delete()
            await message.channel.send(random.choice(hearsayImages))
            return
        
        if message.content.startswith('!lux'):
            self.promSummary.labels('lux').observe(1)
            chance = random.randint(100000, 200000)
            if chance == 122124:
                await message.channel.send('https://i.imgur.com/tLjNhGl.png')
                return

            luxImages = ('https://i.imgur.com/gpz4gu6.png',
                         'https://i.imgur.com/pt34yJB.png',
                         'https://i.imgur.com/9aHMEdy.png',
                         'https://i.imgur.com/oBdRWWf.png',
                         'https://i.imgur.com/gWMLTRr.png',
                         'https://i.imgur.com/HbGm9e8.png',
                         'https://i.imgur.com/eajc20F.png',
                         'https://i.imgur.com/Fx3lge3.png',
                         'https://i.imgur.com/l15o54u.png',
                         'https://i.imgur.com/maRR8Du.png',
                         'https://i.imgur.com/bBWue2J.png',
                         'https://i.imgur.com/XipBsTW.png',
                         'https://i.imgur.com/iUzx8Ic.png',
                         'https://i.imgur.com/hwTavot.png',
                         'https://i.imgur.com/FEjjZyv.png',
                         'https://i.imgur.com/0aPrwrr.png',
                         'https://i.imgur.com/DxpJ6DL.png',
                         'https://i.imgur.com/Z0ohaU5.png',
                         'https://i.imgur.com/JpuDZdl.png',
                         'https://i.imgur.com/okTa4vv.png',
                         'https://i.imgur.com/uC3eAfM.png',
                         'https://i.imgur.com/NY3rhJy.png',
                         'https://i.imgur.com/YGG2WQg.png',
                         'https://i.imgur.com/8zBalFx.png',
                         'https://i.imgur.com/rXNXXg1.png',
                         'https://i.imgur.com/w9dz2aH.png',
                         'https://i.imgur.com/Tdj4e8j.png',
                         'https://i.imgur.com/hYP4trT.png',
                         'https://i.imgur.com/CAEGblO.png',
                         'https://i.imgur.com/KIO17gK.png',
                         'https://i.imgur.com/YEL9QRx.png')
                         
            await message.channel.send(random.choice(luxImages))
            return
        
        if message.content.startswith('!boober'):
            self.promSummary.labels('boober').observe(1)
            booberImages = ('https://cdn.discordapp.com/attachments/330158485704802305/971049950546898964/boobergrab.png',
                            'https://cdn.discordapp.com/attachments/330158485704802305/971050030507106364/boobergold.png',
                            'https://cdn.discordapp.com/attachments/330158485704802305/971050375266304040/boobersaiyan.png')
            await message.channel.send(random.choice(booberImages))
            return

        if message.content.startswith('!rat'):
            self.promSummary.labels('rat').observe(1)
            ratVids = ('https://cdn.discordapp.com/attachments/916068519307784302/979159552186527804/vertically_spinning_rat.mp4',
                       'https://cdn.discordapp.com/attachments/916068519307784302/979159552496914532/2_rats.mp4',
                       'https://media.discordapp.net/attachments/330158485704802305/978393356554096680/rat-ao5dfabunkv81.mp4',
                       'https://cdn.discordapp.com/attachments/380247119086354432/937909896228274186/eight_rats.mp4',
                       'https://cdn.discordapp.com/attachments/380247119086354432/937909927198990376/one_thousand_twenty_four_rats.mp4',
                       'https://cdn.discordapp.com/attachments/380247119086354432/937909945083514890/sixteen_thousand_three_hundred_eighty_four_rats.mp4',
                       'https://cdn.discordapp.com/attachments/380247119086354432/938306998443843624/Thats_a_lot_of_rats.mp4',
                       'https://cdn.discordapp.com/attachments/380247119086354432/938499646274289775/lot_of_rats.mp4',
                       'https://cdn.discordapp.com/attachments/916068519307784302/979162047029870632/Rat_multiplying_meme.mp4',
                       'https://cdn.discordapp.com/attachments/916068519307784302/979789713797959680/ratboop.mp4',
                       'https://cdn.discordapp.com/attachments/916068519307784302/979885167432847370/Erratically_Spinning_Rat.mp4',
                       'https://cdn.discordapp.com/attachments/561629402245627926/985195018841100378/25_Rats.mp4',
                       'https://cdn.discordapp.com/attachments/330158485704802305/994609071820914738/best_movie_ever.mp4',
                       'https://cdn.discordapp.com/attachments/330158485704802305/996167152119853136/High_quality_horizontally_spinning_rat.mp4',
                       'https://cdn.discordapp.com/attachments/916068519307784302/1000701086031695872/Little_Dark_Age_-_Horizontally_Spinning_Rat.mp4',
                       'https://cdn.discordapp.com/attachments/828687981460062238/1001539892087631922/IMG_2898.MP4',
                       'https://cdn.discordapp.com/attachments/647407524152344586/1008499175685627964/rtx.mp4',
                       'https://cdn.discordapp.com/attachments/547301402137985034/1018327723032191077/VID_20220907_150746_252.mp4',
                       'https://cdn.discordapp.com/attachments/890184536393150494/1053364552303136778/youare.mp4')
            await message.channel.send(random.choice(ratVids))
            return
        
        if message.content.startswith('!hammerstein'):
            self.promSummary.labels('hammerstein').observe(1)
            await message.channel.send('Buzzing for a bad image...')
            reddit = asyncpraw.Reddit(
                client_id=redditID,
                client_secret=redditSecret,
                user_agent="android:com.beebot:v0.0.1 (by u/michaellaneous)",
            )
            
            subreddit = await reddit.subreddit('pizzacrimes')
            self.promSummary.labels('pizzacrimes').observe(1)
            while True:            
                submission = await subreddit.random()
                image_formats = ('png', 'jpg', 'jpeg', 'gif')
                if str(submission.url).split('.')[-1] in image_formats:
                    await message.channel.send(submission.url)
                    await reddit.close()
                    return
                
        if message.content.startswith('!geology'):
            self.promSummary.labels('geology').observe(1)
            await message.channel.send('Buzzing for a rocky image...')
            reddit = asyncpraw.Reddit(
                client_id=redditID,
                client_secret=redditSecret,
                user_agent="android:com.beebot:v0.0.1 (by u/michaellaneous)",
            )
            
            subreddit = await reddit.subreddit('geologyporn')
            while True:            
                submission = await subreddit.random()
                image_formats = ('png', 'jpg', 'jpeg', 'gif')
                if str(submission.url).split('.')[-1] in image_formats:
                    await message.channel.send(submission.url)
                    await reddit.close()
                    return

        if message.content.startswith('!kill'):
            self.promSummary.labels('kill').observe(1)
            if not message.author.id == 162571470256472066:
                await message.channel.send(f"I'm sorry {message.author.name}, I'm afraid I can t do that")
            else:
                os.kill(os.getpid(),11)
        
        if message.content.startswith('!talk') or message.content.startswith('!speak') or message.content.startswith('!tay'):
            self.promSummary.labels('talk').observe(1)
            seedWord = random.choice(wordList)
            sentenceLength = random.randint(7, 25)

            sentence = seedWord.capitalize()
            for i in range(0, sentenceLength):
                nextWord = random.choice(markovTable[seedWord])
                seedWord = nextWord

                sentence += " " + seedWord
            
            await message.channel.send(sentence)
            return
            
        if message.content.startswith('!nickme'):
            self.promSummary.labels('nickme').observe(1)
            seedWord = random.choice(wordList)
            nickLength = random.randint(1, 2)

            newNick = seedWord
            for i in range(0, nickLength):
                nextWord = random.choice(markovTable[seedWord])
                seedWord = nextWord

                newNick += " " + seedWord
            
            newNick += f' | {message.author.name}'
            
            await message.author.edit(nick=newNick[:31])
            await message.channel.send(f'Nickname set to {newNick[:31]}')
            return
        
        if message.content.startswith('!nickname'):
            self.promSummary.labels('nickname').observe(1)
            rowCount = 0
            for row in cur.execute('SELECT COUNT(*) FROM nicknames'):
                rowCount = row[0]
            
            self.promNickGauge.set(float(rowCount))

            option = str(message.content).split(' ')[-1]
            
            if option == '!nickname':
                for i in range(0, 10):
                    seedWord = random.choice(wordList)
                    nickLength = random.randint(1, 2)

                    newNick = seedWord
                    for i in range(0, nickLength):
                        nextWord = random.choice(markovTable[seedWord])
                        seedWord = nextWord

                        newNick += " " + seedWord
                    
                    cur.execute(f"INSERT INTO nicknames VALUES ('{newNick}')")
                con.commit()
                
                toSend = '```Your choices are:'
                for row in cur.execute('SELECT * FROM(SELECT ROWID,nick from nicknames ORDER BY ROWID DESC LIMIT 10) ORDER BY ROWID ASC'):
                    toSend += f'\n{row[0]}. {row[1]}'
                toSend += '```'
                await message.channel.send(toSend)
                return
            elif int(option) > rowCount:
                await message.channel.send("I don't have that many nicknames on offer.")
                return
            else:
                for row in cur.execute(f'SELECT nick FROM nicknames WHERE ROWID = {option}'):
                    newNick = f'{row[0]} | {message.author.name}'
                await message.author.edit(nick=newNick[:31])
                await message.channel.send(f'Nickname set to {newNick[:31]}')           
                return
            
        if message.content.startswith('!quote'):
            self.promSummary.labels('quote').observe(1)
            if message.reference is None:
                for row in cur.execute('SELECT * FROM quotes ORDER BY RANDOM() LIMIT 1'):
                    await message.channel.send(f"\"{row[0]}\"")
                    return
            else:
                msg = await message.channel.fetch_message(message.reference.message_id)
                cleanMsg = re.sub(r'(<.*>)', '', msg.content).strip()
                cur.execute(f'INSERT INTO quotes VALUES ("{cleanMsg}", {msg.author.id})')
                con.commit()
                await message.channel.send("Added quote.")
                return
            
        if message.content.startswith('!dropquote'):
            self.promSummary.labels('dropquote').observe(1)
            roleList = []
            modID = 383445089806188545
            
            for r in message.author.roles:
                roleList.append(r.id)
                
            if modID in roleList or message.author.id == 162571470256472066:
                msg = await message.channel.fetch_message(message.reference.message_id)
                msgStr = str(msg.system_content).strip("\"")
                cur.execute(f"DELETE FROM quotes WHERE quote LIKE '{msgStr}'")
                con.commit()
                await message.channel.send("Deleted quote.")
                return
            else:
                await message.channel.send("Only moderators can do this.")
                return  
            
        if message.content.startswith('!emma'):
            self.promSummary.labels('emma').observe(1)
            return

        if message.content.startswith('!help'):
            self.promSummary.labels('help').observe(1)
            msg = """```beebot Version 0.0.1bee
            
Available commands:
!help - Display this message.
!nickme - Give yourself a random nickname.
!nickname - Generate a list of nicknames you can pick from.
!nickname <number> - Pick one of them.
!hugemoji :emoji: / !hugemoji :emoji: aa - A massive version of the emoji of your choice. aa might make some emojis look better when enlargened. [aliases: !hm]
!talk - Spout nonsense, inspired by goons. [aliases: !speak, !tay]
!tag <tag> - Tag yourself for one of our many games.
!color <color> - Give yourself a fancy new look.
!racon, !capybara, !bee, !frog, !bird, !pomo - For all your animal needs.
!hearsay - Make the post above you look real silly.
!quote - Reply to a message and !quote to add it as a quite, or simply type !quote to get a random quote.```
"""

        if message.content.startswith('!modhelp'):
            self.promSummary.labels('modhelp').observe(1)

            msg = """```beebot Version 0.0.1bee
            
Available commands:
!addcommand <name> <url> - Add a command that displays an image/vieo/etc.
!delcommand <name> - Delete command.
!addcolor <name> <id> - Add a new color. Name should be formated as color-xxx. To get ID, enable Discord developer option and RMB -> Copy ID on the role
!delcolor <name> - Delete color with the given name.
!addtag <name> <id> - Add a new color. Name should be formated as tag-xxx. To get ID, enable Discord developer option and RMB -> Copy ID on the role
!deltag <name> - Delete tag with the given name.``` 
"""
            roleList = []
            modID = 383445089806188545
            
            for r in message.author.roles:
                roleList.append(r.id)
                
            if modID in roleList or message.author.id == 162571470256472066:
                await message.channel.send(msg)
            return
        
        if message.content.startswith('!tag'):
            self.promSummary.labels('tag').observe(1)
            try:
                roles = {}
                for row in cur.execute('SELECT * FROM tags'):
                    roles[row[0]] = row[1]
                role = roles[str(message.content).split(' ')[-1]]
            except KeyError:
                await message.channel.send('Role does not exist.')
                return
                
            roleList = []
            
            for r in message.author.roles:
                roleList.append(r.id)
                
            roleObj = discord.Object(role)
            if role not in roleList:
                await message.author.add_roles(roleObj, reason='User request')
                await message.channel.send('Role added.')
            elif role in roleList:
                await message.author.remove_roles(roleObj, reason='User request')
                await message.channel.send('Role removed.')
                
        if message.content.startswith('!addtag'):
            self.promSummary.labels('addtag').observe(1)
            roleList = []
            modID = 383445089806188545
            
            for r in message.author.roles:
                roleList.append(r.id)
                
            if modID in roleList or message.author.id == 162571470256472066:
                tag = message.content.split(' ')[1]
                id = message.content.split(' ')[2]
                cur.execute(f'INSERT INTO tags VALUES ("{tag}", {id})')
                con.commit()
                await message.channel.send('Tag added.')
            return
        
        if message.content.startswith('!deltag'):
            self.promSummary.labels('deltag').observe(1)
            roleList = []
            modID = 383445089806188545
            
            for r in message.author.roles:
                roleList.append(r.id)
                
            if modID in roleList or message.author.id == 162571470256472066:
                tag = message.content.split(' ')[1]
                cur.execute(f"DELETE FROM tags WHERE tag LIKE '{tag}'")
                con.commit()
                await message.channel.send('Tag deleted.')
            return
                
        if message.content.startswith('!color'):
            self.promSummary.labels('color').observe(1)            
            try:
                roles = {}
                for row in cur.execute('SELECT * FROM colors'):
                    roles[row[0]] = row[1]
                role = roles[str(message.content).split(' ')[-1]]
            except KeyError:
                await message.channel.send('Color does not exist.')
                return
                
            roleList = []
            
            for r in message.author.roles:
                roleList.append(r.id)
                            
            if role not in roleList:
                inter = set(roleList) & set(roles.values())
                for x in inter:
                    roleObj = discord.Object(x)
                    await message.author.remove_roles(roleObj, reason='User request')
                roleObj = discord.Object(role) 
                await message.author.add_roles(roleObj, reason='User request')
                await message.channel.send('Color added.')
            elif role in roleList:
                roleObj = discord.Object(role) 
                await message.author.remove_roles(roleObj, reason='User request')
                await message.channel.send('Color removed.')
                
        if message.content.startswith('!addcolor'):
            self.promSummary.labels('addcolor').observe(1)
            roleList = []
            modID = 383445089806188545
            
            for r in message.author.roles:
                roleList.append(r.id)
                
            if modID in roleList or message.author.id == 162571470256472066:
                color = message.content.split(' ')[1]
                id = message.content.split(' ')[2]
                cur.execute(f'INSERT INTO colors VALUES ("{color}", {id})')
                con.commit()
                await message.channel.send('Color added.')
            return
        
        if message.content.startswith('!delcolor'):
            self.promSummary.labels('delcolor').observe(1)
            roleList = []
            modID = 383445089806188545
            
            for r in message.author.roles:
                roleList.append(r.id)
                
            if modID in roleList or message.author.id == 162571470256472066:
                command = message.content.split(' ')[1]
                cur.execute(f"DELETE FROM colors WHERE color LIKE '{command}'")
                con.commit()
                await message.channel.send('Color deleted.')
            return
                
        if message.content.startswith('!addcommand'):
            self.promSummary.labels('addcommand').observe(1)
            roleList = []
            modID = 383445089806188545
            
            for r in message.author.roles:
                roleList.append(r.id)
                
            if modID in roleList or message.author.id == 162571470256472066:
                command = message.content.split(' ')[1]
                text = message.content.split(' ')[2]
                cur.execute(f'INSERT INTO commands VALUES ("{command}", "{text}")')
                con.commit()
                await message.channel.send('Command added.')
            return
        
        if message.content.startswith('!delcommand'):
            self.promSummary.labels('delcommand').observe(1)
            roleList = []
            modID = 383445089806188545
            
            for r in message.author.roles:
                roleList.append(r.id)
                
            if modID in roleList or message.author.id == 162571470256472066:
                command = message.content.split(' ')[1]
                cur.execute(f"DELETE FROM commands WHERE command LIKE '{command}'")
                con.commit()
                await message.channel.send('Command deleted.')
            return
        
        if message.content.startswith('!metrics'):
            self.promSummary.labels('metrics').observe(1)
            await message.channel.send('https://animeistrash.org:3000/public-dashboards/d4a212aefbf245c29ce1b95352b03d43')
            return
        
        if message.content.startswith('!list'):
            self.promSummary.labels('list').observe(1)
            msg = ''
            for row in cur.execute('SELECT command FROM commands'):
                msg = msg + row[0] + ', '
            await message.channel.send(msg[:-2])
            return    
    
        if message.content.startswith('!'):
            command = message.content.split(' ')[0][1:]
            for row in cur.execute('SELECT * FROM commands'):
                if command == row[0]:
                    if 'local/' in str(row[1]):
                        self.promSummary.labels(command).observe(1)
                        await message.channel.send(file=discord.File(str(row[1])))
                    else:
                        self.promSummary.labels(command).observe(1)
                        await message.channel.send(row[1])
                    return
                

def get_message_emojis(m: discord.Message) -> typing.List[discord.PartialEmoji]:
    """ Returns a list of custom emojis in a message. """
    emojis = re.findall('<(?P<animated>a?):(?P<name>[a-zA-Z0-9_]{2,32}):(?P<id>[0-9]{18,22})>', m.content)
    return [discord.PartialEmoji(animated=bool(animated), name=name, id=id) for animated, name, id in emojis]

intents = discord.Intents.default()
intents.members = True
client = BeeClient(intents=intents)

with open('redditID') as f:
    redditID = f.read()
    
with open('redditSecret') as f:
    redditSecret = f.read()

with open('markovClean.txt') as input_file:
    text = input_file.read()
    
def createMarkov(normalized_text):
    words = normalized_text.split()
    markovTable = collections.defaultdict(list)
    for current, next in zip(words, words[1:]):
        markovTable[current].append(next)    
    return markovTable

markovTable = createMarkov(text)
wordList = list(markovTable.keys())
nicknameList = {}

con = sqlite3.connect('beebot.db')
cur = con.cursor()

start_http_server(8000)

with open('token') as f:
    token = f.read()
client.run(token)


# TODO: Learning commands, buzzwords for random zings on certain messages
# TODO: Markov chain https://www.codereversing.com/blog/archives/412
# TODO Role changer
