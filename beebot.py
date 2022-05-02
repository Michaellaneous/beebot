import discord
import re
import typing
import asyncpraw
import random
import requests
from PIL import Image, ImageSequence
from io import BytesIO
import PIL
import os
import random

class BeeClient(discord.Client):
    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def on_message(self, message):
        if message.author.id == self.user.id:
            return

        if message.content.startswith('!hugemoji'):
            try:
                sentEmoji = get_message_emojis(message)[0]
            except IndexError:
                return
            
            if sentEmoji.animated:
                await message.channel.send(f'https://cdn.discordapp.com/emojis/{sentEmoji.id}.gif?quality=lossless')
                return
            else:
                response = requests.get(f'https://cdn.discordapp.com/emojis/{sentEmoji.id}.png?quality=lossless')
                img = Image.open(BytesIO(response.content))
                imgName = random.randint(1000000, 9999999)
                basewidth = 512
                wpercent = (basewidth/float(img.size[0]))
                hsize = int((float(img.size[1])*float(wpercent)))
                
                try:
                    option = str(message.content).split(' ')[-1]
                except:
                    pass

                if option == 'aa':
                    img = img.resize((basewidth,hsize), Image.ANTIALIAS)
                else:
                    img = img.resize((basewidth,hsize))
                    
                img.save(f'{imgName}.png')
                with open(f'{imgName}.png', 'rb') as f:
                    pic = discord.File(f)
                    await message.channel.send(file=pic)
                os.remove(f'{imgName}.png')
                
        if message.content.startswith('!racon'):
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
                
        if message.content.startswith('!lux'):
            user = await client.fetch_user('298254692444667904')
            await user.send('<3')
        
        if message.content.startswith('!bonk'):
            await message.channel.send('https://tenor.com/view/bonk-gif-24239187')
            
        if message.content.startswith('!tag'):
            roles = {
                'tag-goblin': '934217787038130256',
                'tag-racon': '471770802727944192',
                'lakers fan ': '467510519704846337',
                'noted anime lover': '467511307382554629',
                'tag-nfl': '391384162415673395',
                'tag-ffr': '616304706880274452',
                'tag-callofduty': '467487877039652875',
                'tag-warzone': '687365517996326913',
                'tag-destiny': '467488037526306816',
                'tag-marblehebrons': '467488709210669056',
                'tag-catmans': '495331994843086887',
                'tag-iamgoon': '557619083093344276',
                'tag-modoktors': '614158258881429535',
                'tag-futurefight': '467488762440712202',
                'tag-warframe': '467489166721024050',
                'tag-divisionpc': '467489534855217183',
                'tag-divisionps4': '542692921569443850',
                'tag-divisionxbox': '542692317337878530',
                'tag-battlefield': '467490101488779264',
                'tag-poe': '467496993875558401',
                'tag-idlechamps': '467498907790999582',
                'tag-marvelheroes': '467506628019879956',
                'tag-yakuza': '467520119141171203',
                'tag-known_controller_user': '467510266859487255',
                'tag-stupid-pomo': '471771027060555781',
                'tag-birb-crew': '481846091864604677',
                'tag-nba': '484882962391760917',
                'tag-lizardman': '495371684669423628',
                'tag-poo-crew': '507579793416519705',
                'tag-cold-warriors': '514967660539281410',
                'tag-anthemxbox': '529729084037791744',
                'tag-foreniter': '529729439685148672',
                'tag-anthempc': '529729684561199107',
                'tag-apexxbox': '542568902794674187',
                'tag-apexps4': '542568685760675841',
                'tag-apexpc': '542568685760675841',
                'tag-starbores': '570396728432394261',
                'tag-riskofrain': '564998370549039125',
                'tag-deeprockgalactic': '529830792826847252',
                'tag-paladins': '529830967230070800',
                'tag-stupid-people': '533715061676703754',
                'tag-diablo': '537450754785542166',
                'tag-auscrew': '538362569056976916',
                'knicks-fan-so-sorry': '540659502836351007',
                'tag-bookclub': '734545659838857297',
                'tag-bocchi-gang': '586312458369630208',
                'tag-healthcrew': '621332851429736449',
                'tag-monsterhunter': '608370823245463622',
                'tag-goose': '624357814361653279',
                'tag-borderlands': '622597242741587985',
                'tag-halo': '646212951807885313',
                'tag-magicthegathering': '653325014648487976',
                'tag-katz-korner': '655819169597620242',
                'tag-social-distance': '689902694059737183',
                'tag-titanfalling': '702722337593884752',
                'tag-bigfootgang': '702722340496343050',
                'tag-boredgamers': '702722341922406481',
                'tag-hydro-homies': '727957806233157734',
                'tag-ffa-fga-friendship-alliance': '727958021325717516',
                'tag-cryptidcrew': '742556404984053942',
                'tag-cultofthebfo': '742556543547080815',
                'tag-avengers': '750399781062574091',
                'tag-bean-and-leaf-water-crew': '742917705165832203',
                'pinners': '745136611179888755',
                'tag-amongus': '757776773491458098',
                'tag-sw-squadrons': '760035901052157973',
                'talenti squad': '762463981846790174',
                'tag-vermintide-rat-smashers': '786705363101679616',
                'tag-koahi-photo-fanclub': '800452213310750751',
                'tag-noodlegang': '804586156578308107',
                'tag-bloonpoppinmonke': '804930657863467058',
                'tag-gundamsquad': '805544985021644830',
                'tag-fightinggames': '825428579134603264',
                'tag-outriders': '826970947621093405',
                'tag-scavengers': '838465645188087838',
                'tag-edf-edf-shoot-bog': '841120733689020437',
                'tag-lostark': '841444462592524358',
                'tag-party-bus': '850533652098187264',
                'tag-gunfirebuds': '861710163344621568',
                'tag-tower-defense-games-ftw': '862411284363608095',
                'tag-quiltbagqrew': '870883582699245608',
                'tag-united-pokeman-and-women': '871088753056313364',
                'tag-splitgaters': '874537492374757446',
                'tag-aliens-ft-shoot-bog': '878388352687157299',
                'tag-back-4-blood-buds': '897584143909662730',
                'tag-wheel-of-time-skirtsmoothers': '905404882893279232',
                'tag-huntys': '907003955777785906',
                'tag-froggo-crew': '909102837835923507',
                'tag-warhammer-waaaghs-n-skinks': '909136532256985148',
                'boober': '916328104862048256',
                'tag-call-of-fishyat': '923376976742461451',
                'tag-capybara-crew': '927190264316035083',
                'tag-rainbow6-extract': '934226133694685214',
                'tag-elden-deez-rings': '945408628700110908',
                'tag-squad-up': '967945914616533002'
            }
            try:
                role = roles[str(message.content).split(' ')[-1]]
            except KeyError:
                await message.channel.send('Role does not exist.')
                return
                
            roleList = []
            
            for r in message.author.roles:
                roleList.append(r.id)
                
            roleObj = discord.Object(int(role))
            if int(role) not in roleList:
                await message.author.add_roles(roleObj, reason='User request')
                await message.channel.send('Role added.')
            elif int(role) in roleList:
                await message.author.remove_roles(roleObj, reason='User request')
                await message.channel.send('Role removed.')
                
        if message.content.startswith('!color'):
            roles = {
                'color-blue': '331674383661793282',
                'color-blizzardblue': '545442621045080094',
                'color-trueblue': '333778109889249280',
                'color-aqua': '333778961513316352',
                'color-basicblues': '545663086728577045',
                'color-periwinkle': '334513307375501314',
                'color-cosmicblue': '586613522138398721',
                'color-aquamarine': '391383743903956993',
                'color-steelblue': '391377414971719680',
                'color-blublue': '391377620656455680',
                'color-cyan': '391383484825862154',
                'color-freshwater': '545659893248688132',
                'color-cadetblue': '391377206699622413',
                'color-newblueorder': '387747381631909891',
                'color-agentblue': '550862673815011338',
                'color-indigo': '356180724505903104',
                'color-sky': '356180388646879245',
                'color-thunderblue': '582982025955508243',
                'color-deepblue': '331679561429417985',
                'color-twoblueorder': '387747500796411921',
                'color-majestic': '356180220790833163',
                'color-divcosmetic': '550862436408885279',
                'color-bfblue': '852268932521918504',
                'color-green': '331674334026268672',
                'color-green2016': '331683074972844054',
                'color-lush': '545662701825687592',
                'color-seafoamgreen': '331677622386032640',
                'color-lightfoam': '387744910830469130',
                'color-cosmicgreen': '391380602672381953',
                'color-brightfoam': '387745003075796992',
                'color-greygreen': '387748043186765824',
                'color-meangreen': '356183712163168256',
                'color-classified': '550860510887673856',
                'color-brolygreen': '535921803353128980',
                'color-palegreen': '495370092784123914',
                'color-truegreen': '331683649936293909',
                'color-avocado': '356178414299774981',
                'color-greenmarine': '387746451276693504',
                'color-pea': '356179190866771968',
                'color-greenworld': '387746246275629056',
                'color-forest': '356179616328581121',
                'color-diaperdandy': '387745595064057857',
                'color-darkgreen': '543177191609991198',
                'color-agentcommon': '550863098852933659',
                'color-yellowgreen': '391383298460614656',
                'color-toxicgrass': '391382908444868608',
                'color-newgreenorder': '391378472251162624',
                'color-yellow': '331672807165657089',
                'color-yellowtown': '582984464741695490',
                'color-cosmictoday': '333777730896396308',
                'color-paleyellowdot': '586612913968775170',
                'color-melloyellow': '387747050554654731',
                'color-classyyellow': '387749759462408205',
                'color-goldmember': '387747648699891712',
                'color-yellowdrop': '550861729098104833',
                'color-gold': '391387838228463636',
                'color-unique': '538110724304797696',
                'color-purple': '331674854015107072',
                'color-cosmicpurpz': '586613935109832715',
                'color-darkpurple': '331684169602301952',
                'color-divpurp': '550861420963561472',
                'color-brightpurple': '334517963141152770',
                'color-californiaraisen': '356180745108193290',
                'color-purpledrank': '356180492090867714',
                'color-electricpurp': '549293875097894942',
                'color-newpurpleorder': '387746642855591937',
                'color-partypurple': '331684686512521217',
                'color-purplemonkey': '549292003058253834',
                'color-palepurpledot': '586605480831614976',
                'color-plum': '387747823875129365',
                'color-bruised': '387748194945073153',
                'color-orange': '331674460442591242',
                'color-crafted': '542820534401105934',
                'color-agentorange': '549290950724288513',
                'color-orangeskies': '545664036562534437',
                'color-beachplease': '356182635548246017',
                'color-neworangeorder': '387745813390032898',
                'color-sunset': '582982986543136769',
                'color-jackedandtan': '356183347808174100',
                'color-red': '333351732744683532',
                'color-redlife': '550857316413734914',
                'color-sensualred': '501918273642823690',
                'color-raptorred': '582983773340172331',
                'color-chameleonred': '549204164266426368',
                'color-socialistred': '538114496313688094',
                'color-lightred': '331674922005037066',
                'color-burntsienna': '356182060336939020',
                'color-roseyred': '387747160260608002',
                'color-fuschia': '391379658245144586',
                'color-brown': '331676629246148619',
                'color-burgerbrown': '550852122942504963',
                'color-poobrown': '331678261270544385',
                'color-deepbrown': '331680549674418178',
                'color-copper': '549294384479207437',
                'color-bronze': '582984928405225494',
                'color-puke': '387745467812806657',
                'color-murple': '393474064276127754',
                'color-pink': '331674615988486144',
                'color-magenta': '585197768403058701',
                'color-salmon': '334505192651358220',
                'color-typicalpink': '356181548808142855',
                'color-pinkpanther': '549293137726799892',
                'color-prettyinpink': '387744491257462786',
                'color-pinky': '387748332027772929',
                'color-rose': '586611952755802112',
                'color-evilpink': '545665113475252224',
                'color-pinkdivinity': '391385840171089920',
                'color-peach': '391378104158912514',
                'color-black': '333351978006740992',
                'color-evilgrey': '331678738242863104',
                'color-goodgrey': '331678924469829632',
                'color-silver': '582984625844912251',
                'color-mayopete': '333777591938842635',
                'color-serenity': '391380608732889108'
            }
            
            try:
                role = roles[str(message.content).split(' ')[-1]]
            except KeyError:
                await message.channel.send('Color does not exist.')
                return
                
            roleList = []
            
            for r in message.author.roles:
                roleList.append(r.id)
                
            roleObj = discord.Object(int(role))
            if int(role) not in roleList:
                await message.author.add_roles(roleObj, reason='User request')
                await message.channel.send('Color added.')
            elif int(role) in roleList:
                await message.author.remove_roles(roleObj, reason='User request')
                await message.channel.send('Color removed.')

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

with open('token') as f:
    token = f.read()
client.run(token)


# TODO: Learning commands, buzzwords for random zings on certain messages
# TODO: Markov chain https://www.codereversing.com/blog/archives/412
# TODO Role changer
