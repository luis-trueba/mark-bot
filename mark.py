# mark.py
import os
import socket
import random
import time
import asyncio
import subprocess

import discord
from dotenv import load_dotenv

from youtubesearchpython import searchYoutube as YoutubeSearch
from google_images_search import GoogleImagesSearch
from PIL import Image
from PIL import ImageEnhance

load_dotenv()
token = os.getenv("discordtoken")

gis = GoogleImagesSearch(os.getenv("gis1"), os.getenv("gis2"))

timeoutlist = []
lastImage = {}
savedImages = []

client = discord.Client()
@client.event
async def on_ready():
    print('Ready')

@client.event
async def on_message(message):
    sendImage = False
    #print(message.channel)
    debugchannel = client.get_channel(715460456227274752)
    if message.author == client.user and message.attachments == []:
        return

    if message.author.id in timeoutlist:
        if "i am sorry" in message.content.lower() or "i'm sorry" in message.content.lower() or "i apologize" in message.content.lower() or "i’m sorry" in message.content.lower() or message.content.lower().startswith("sorry"):
            timeoutlist.remove(message.author.id)
            await message.channel.send("All is forgiven")
        else:
            await message.channel.send(message.author.mention + ", apologize for what you did to regain message privileges")
            await message.delete()
        return

    if message.attachments != []:
        if ('.png' in message.attachments[0].filename or '.jpg' in message.attachments[0].filename or '.jpeg' in message.attachments[0].filename) and message.author.id != client.user.id:
            print(message.attachments)
            await message.attachments[0].save("/home/pi/mark/images/" + message.attachments[0].filename)
            imagepath = "/home/pi/mark/images/" + message.attachments[0].filename
            im1 = Image.open(imagepath)
            width, height = im1.size

            if width < 4096 and height < 4096:
                im1.save("/home/pi/mark/images/" + str(message.channel.id) + ".png")
            else:
                os.remove(imagepath)

        elif message.author.id == client.user.id:
            lastImage[message.channel.id] = message.id
            print(lastImage)


    if message.content.lower().startswith("mark, ") or message.content.lower().startswith("dr. mark, ") or message.content.lower().startswith("dr mark"):

        if 'mark, reboot' in message.content.lower() and message.author.id == 235221408274186242:
            await message.channel.send("Rebooting...")
            os.system("sudo reboot")

        elif 'mark, ifconfig' in message.content.lower() and message.author.id == 235221408274186242:
            cmd = "ifconfig -a"
            inet = subprocess.check_output(cmd, shell = True)
            #inet = wlan.decode("utf-8")
            #inet_addr = inet[inet.index("inet")+1]
            await message.channel.send(str(inet))

        elif 'mark, roll' in message.content.lower():
            diceinput = message.content.lower().replace(' ', "").split('mark,roll', 1)[-1].split('d')
            #print(diceinput)
            print(str(diceinput))
            numberdice = diceinput[0]
            diesides = diceinput[1]
            if numberdice == "":
                numberdice = "1"
            if int(numberdice) > 100:
                await message.channel.send('Cannot roll more than 100 dice!')
            elif int(numberdice) == 0:
                await message.channel.send('Cannot roll 0 dice!')
            else:
                if diesides.isdigit():
                    if int(diesides) !=0:
                        results = []
                        for x in range(0, int(numberdice)):
                            output = random.randrange(int(diesides)) + 1
                            #print(output)
                            results.append(output)
                        payload = "rolled `" + message.content.lower().replace(' ', "").split('mark,roll', 1)[-1] + "` and got `" + str(results).replace("[", "").replace("]", "") + "`" + ' = ' + str(sum(results))
                        await message.channel.send(payload)
                    else:
                        await message.channel.send("Dice can't have 0 sides!")

                else:
                    payload = "You didn't give me a number!"
                    await message.channel.send(payload)

        elif 'mark, should i' in message.content.lower():

            if ' or ' in message.content.lower():
                payload = "You should "
                answers = message.content.lower().split("should i ",1)[1].split(" or ")

            else:
                payload = ""
                answers = ["Yes", "No"]

            await message.channel.send(payload + random.choice(answers))

        elif 'mark, say ' in message.content.lower():
            saystart = message.content.lower().find("mark, say") + 10
            await message.channel.send(message.content[saystart:])
            await message.delete()

        elif 'mark, can we bust' in message.content.lower():
            await message.channel.send('https://www.youtube.com/watch?v=0tdyU_gW6WE')

        elif 'mark, can we get' in message.content.lower():
            results = YoutubeSearch(message.content.lower().split("can we get",1)[1], max_results = 1, mode = "dict", offset = 1).result()
            await debugchannel.send("```" + str(results) + "```")
            if results == {'search_result': []}:
                results = YoutubeSearch(message.content.lower().split("can we get",1)[1], max_results = 1, mode = "dict", offset = 1).result()
            if results == {'search_result': []}:
                await message.channel.send("Couldn't find anything on Youtube. <@!235221408274186242> shitt's fucked")
            else:
                link = results["search_result"][0]["link"]
                print(results)
                await message.channel.send(link)
        elif 'mark, show me' in message.content.lower():
            _search_params = {

                'q': message.content.lower().split("mark, show me",1)[1],

                'num': 1,

                'safe': 'off',

            }

            gis.search(search_params=_search_params, path_to_dir = "/home/pi/mark/images/")
            print(str(gis.results()[0].path))
            if '.png' in gis.results()[0].path or '.jpg' in gis.results()[0].path or '.jpeg' in gis.results()[0].path:
                print(os.path.getsize(gis.results()[0].path))
                im1 = Image.open(gis.results()[0].path)
                width, height = im1.size
                if width > 4096 or height > 4096:
                    print("Nope!")
                    await message.channel.send(str(gis.results()[0].url))

                else:
                    im1.save("/home/pi/mark/images/" + str(message.channel.id) + ".png")
#                    await message.channel.send(file = discord.File("/home/pi/mark/images/" + str(message.channel.id) + ".png"))
                    sendImage = True

                os.remove(gis.results()[0].path)

            else:
                await message.channel.send(str(gis.results()[0].url))
                os.remove(gis.results()[0].path)

        elif 'mark, flip' in message.content.lower():
            im1 = Image.open("/home/pi/mark/images/" + str(message.channel.id) + ".png")
            im1 = im1.transpose(Image.FLIP_LEFT_RIGHT)
            im1.save("/home/pi/mark/images/" + str(message.channel.id) + ".png")
#            await message.channel.send(file = discord.File("/home/pi/mark/images/" + str(message.channel.id) + ".png"))
            sendImage = True

        elif 'mark, flop' in message.content.lower():
            im1 = Image.open("/home/pi/mark/images/" + str(message.channel.id) + ".png")
            im1 = im1.transpose(Image.FLIP_TOP_BOTTOM)
            im1.save("/home/pi/mark/images/" + str(message.channel.id) + ".png")
#            await message.channel.send(file = discord.File("/home/pi/mark/images/" + str(message.channel.id) + ".png"))
            sendImage = True

        elif 'mark, jpeg' in message.content.lower():
            jpeg_quality_input = message.content.lower().split("mark, jpeg ",1)[1]
            if jpeg_quality_input.isdigit() and int(jpeg_quality_input) <= 100 and int(jpeg_quality_input) > 0:
                jpeg_quality = int(jpeg_quality_input)
            else:
                print("not valid number")
                jpeg_quality = 75
            im1 = Image.open("/home/pi/mark/images/" + str(message.channel.id) + ".png")
            im1.convert('RGB').save("/home/pi/mark/images/" + str(message.channel.id) + ".jpg", quality=jpeg_quality)
            im2 = Image.open("/home/pi/mark/images/" + str(message.channel.id) + ".jpg")
            im2.save("/home/pi/mark/images/" + str(message.channel.id) + ".png")
            sendImage = True
            os.remove("/home/pi/mark/images/" + str(message.channel.id) + ".jpg")

        elif 'mark, saturation' in message.content.lower():
            saturation_input = message.content.lower().split("mark, saturation ",1)[1]
            if saturation_input.replace('.', '', 1).isdigit() and float(saturation_input) <= 5 and float(saturation_input) >= 0:
                saturation = float(saturation_input)
            else:
                print("not valid number")
                saturation = 5.0

            im1 = Image.open("/home/pi/mark/images/" + str(message.channel.id) + ".png")
            enhance = ImageEnhance.Color(im1)
            im1 = enhance.enhance(saturation)
            im1.save("/home/pi/mark/images/" + str(message.channel.id) + ".png")
            sendImage = True

        elif 'mark, sharpness' in message.content.lower():
            sharpness_input = message.content.lower().split("mark, sharpness ",1)[1]
            if sharpness_input.replace('.', '', 1).isdigit() and float(sharpness_input) <= 5 and float(sharpness_input) >= 0:
                sharpness = float(sharpness_input)
            else:
                print("not valid number")
                sharpness = 5.0

            im1 = Image.open("/home/pi/mark/images/" + str(message.channel.id) + ".png")
            enhance = ImageEnhance.Sharpness(im1)
            im1 = enhance.enhance(sharpness)
            im1.save("/home/pi/mark/images/" + str(message.channel.id) + ".png")
            sendImage = True

        elif 'mark, brightness' in message.content.lower():
            brightness_input = message.content.lower().split("mark, brightness ",1)[1]
            if brightness_input.replace('.', '', 1).isdigit() and float(brightness_input) <= 5 and float(brightness_input) >= 0:
                brightness = float(brightness_input)
            else:
                print("not valid number")
                brightness = 1.0

            im1 = Image.open("/home/pi/mark/images/" + str(message.channel.id) + ".png")
            enhance = ImageEnhance.Brightness(im1)
            im1 = enhance.enhance(brightness)
            im1.save("/home/pi/mark/images/" + str(message.channel.id) + ".png")
            sendImage = True

        elif 'mark, resize' in message.content.lower():
            size_input = message.content.lower().split("mark, resize ",1)[1]
            if size_input.replace('.', '', 1).isdigit() and float(size_input) <= 5 and float(size_input) >= 0:
                img_size = float(size_input)
            else:
                print("not valid number")
                img_size = 1.0

            im1 = Image.open("/home/pi/mark/images/" + str(message.channel.id) + ".png")
            im1 = im1.resize((int(float(im1.width)*img_size), int(float(im1.height)*img_size)))
            im1.save("/home/pi/mark/images/" + str(message.channel.id) + ".png")
            sendImage = True


        elif 'ants' in message.content.lower():
            await message.channel.send("""Ants are eusocial insects of the family Formicidae and, along with the related wasps and bees, belong to the order Hymenoptera. Ants evolved from wasp-like ancestors in the Cretaceous period, about 140 million years ago, and diversified after the rise of flowering plants. More than 12,500 of an estimated total of 22,000 species have been classified.[5][6] They are easily identified by their elbowed antennae and the distinctive node-like structure that forms their slender waists.  Ants form colonies that range in size from a few dozen predatory individuals living in small natural cavities to highly organised colonies that may occupy large territories and consist of millions of individuals. Larger colonies consist of various castes of sterile, wingless females, most of which are workers (ergates), as well as soldiers (dinergates) and other specialised groups.[7][8] Nearly all ant colonies also have some fertile males called "drones" (aner) and one or more fertile females called "queens\"""")
            await message.channel.send("""(gynes).[8] The colonies are described as superorganisms because the ants appear to operate as a unified entity, collectively working together to support the colony.[9][10] Ants gathering food  Ants have colonised almost every landmass on Earth. The only places lacking indigenous ants are Antarctica and a few remote or inhospitable islands. Ants thrive in most ecosystems and may form 15-25% of the terrestrial animal biomass.[11] Their success in so many environments has been attributed to their social organisation and their ability to modify habitats, tap resources, and defend themselves. Their long co-evolution with other species has led to mimetic, commensal, parasitic, and mutualistic relationships.[12]  Ant societies have division of labour, communication between individuals, and an ability to solve complex problems.[13] These parallels with human societies have long been an inspiration and subject of study. Many human""")
            await message.channel.send("""cultures make use of ants in cuisine, medication, and rituals. Some species are valued in their role as biological pest control agents.[14] Their ability to exploit resources may bring ants into conflict with humans, however, as they can damage crops and invade buildings. Some species, such as the red imported fire ant (Solenopsis invicta), are regarded as invasive species, establishing themselves in areas where they have been introduced accidentally.""")

        elif 'mark, timeout ' in message.content.lower():
            if 'horny' in str( message.channel):
                await message.channel.send('Horny Crimes cannot be committed in ' + message.channel.mention)
            else:
                for member in message.mentions:
                    if member.id in timeoutlist:
                        await message.channel.send(member.mention + ' is already in timeout and cannot be tried again for the same crime')
                    elif member.bot == True:
                        await message.channel.send("Bots cannot be put in timeout!")
                    else:
                        timeoutlist.append(member.id)
                        print(timeoutlist)
                        payload = 'Put ' + member.mention + ' in timeout for crimes in ' + str(message.channel.mention)
                        await message.channel.send(payload)

        elif 'mark, homestuck jail ' in message.content.lower() and message.guild.id == 650229854247321611:

            if 'homestuck' in str( message.channel) or 'horny' in str( message.channel):

                await message.channel.send('Homestuck Crimes cannot be committed in ' + message.channel.mention)

            else:

                for member in message.mentions:

                    if '715481459196166184' in str(member.roles):

                        await message.channel.send(member.mention + ' is already in homestuck jail and cannot be tried again for the same crime')

                    else:

                        await member.add_roles(discord.utils.get(message.guild.roles, id=715481459196166184))

                        payload = 'Jailed ' + member.mention + ' for homestuck crimes in ' + message.channel.mention

                        await message.channel.send(payload)

                await asyncio.sleep(120)

                for member in message.mentions:

                    if '715481459196166184' in str(member.roles):

                        await member.remove_roles(discord.utils.get(message.guild.roles, id=715481459196166184))

                        await message.channel.send('Released ' + member.mention + ' from homestuck jail after serving their time')



        elif 'mark, jailbreak adventure' in message.content.lower() and message.guild.id == 650229854247321611:

            if 'homestuck' in str( message.channel) or 'horny' in str( message.channel):

                await message.channel.send('Nice try! You cannot jailbreak from ' + message.channel.mention)

            else:

                for member in message.mentions:

                    if '715481459196166184' in str(member.roles):

                        await member.remove_roles(discord.utils.get(message.guild.roles, id=715481459196166184))

                        await message.channel.send(member.mention + ' has escaped from homestuck jail with the help of ' + message.author.mention)

                    else:

                        await message.channel.send('Justice has been served. ' + member.mention + ' is already out of jail.')


        elif ' help' in message.content.lower():
            payload = """ Hello kiddos, I'm Mark!
My prefix is `Mark, ` and I can do all sorts of things. Please, no parties on my watch, though.
-Say `Mark, roll NdXYZ` to roll N XYZ sided dice! e.g `Mark, roll 12d6` rolls 12x 6-sided dice
-Say `Mark, can we get <search term>` and I'll drop the first youtube result for that search into the chat.
-Say `Mark, should I ____` and I will respond yes or no for single choices, and will choose between multiple options separated by the substring ` or `!
-Say `Mark, show me ____` and I will find a good image matching your search parameters.
-Say `Mark, flip` or `Mark, flop` and I will invert the most recent image sent to the channel across the vertical or horizontal axis, respectively.
-Say `Mark, jpeg <1 - 100>` and I will jpeg compress the most recent image sent to the channel with that percent of quality.
-Say `Mark, saturation <0.0 - 5.0>` and I will adjust the saturation of the most recent image sent to the channel. 0 is grayscale, 1 is normal.
-Say `Mark, sharpness <0.0 - 5.0>` and I will adjust the sharpness of the most recent image sent to the channel. 0 is very blurry, 1 is normal, 5 is extremely sharp.
-Say `Mark, brightness <0.0 - 5.0>` and I will adjust the brightness of the most recent image sent to the channel. 0 is pitch black, 1 is normal, 5 is extremely bright.
-If you want more features, bap luis and he might eventually get around to it."""
            if message.guild.id == 650229854247321611:
                payload = payload + """
-Also, in this server, I can send users to Horny Jail with `Mark, jail <mention users>`
-You can free them early with `Mark, jailbreak <mention users>` but this is frowned upon as it is obstruction of justice."""
            await message.channel.send(payload)


        else:
            await message.channel.send('I do not understand this meme. Say "Mark, help" for a list of officially supported commands.')

        if sendImage == True:
            print("Trying to send image")
            print("size = " + str(os.stat("/home/pi/mark/images/" + str(message.channel.id) + ".png").st_size))
            if os.stat("/home/pi/mark/images/" + str(message.channel.id) + ".png").st_size > 8000000:
                await message.channel.send("Image too large. Try again with a smaller image")
                sendImage = False
            else:
                msg = await message.channel.send(file = discord.File("/home/pi/mark/images/" + str(message.channel.id) + ".png"))
                sendImage = False
                await asyncio.sleep(30)
                print(msg.id)
                if msg.id in savedImages:
                    print("do not delete")
                    savedImages.remove(msg.id)
                    return
                else:
                    await msg.delete()
    else:
        if 'party' in message.content.lower():
            await message.channel.send("Don't serve alcohol to minors")
        if 'thanks' in message.content.lower() or 'thank you' in message.content.lower():
            if str(await message.channel.fetch_message(lastImage[message.channel.id])) == "":
                print("no message")
            else:
                print("ight we got one")
                savedImages.append(lastImage[message.channel.id])
                print(savedImages)
                await message.add_reaction("✅")
                lastImage[message.channel.id] = 0

        print('entering grt lottery')
        if random.randrange(100) == 69:
        #if True:
            grtphrases = ["You should come to a GRT meal!", "How has your sleep been?", "Ants have very interesting social hierarcharies with complex gender roles!", "Here guys, I made some bread! :bread:", "Bustin by Neil Cicierega is about sex", "Don't let people in through the 282 entrance!", "MIT still isn't releasing statistics on what happens to professors found guilty of sexual harassment.", "I don't understand this meme", "I made hummus!", "I made boba, do you guys want any?", "Do you want some soymilk?", "I am getting in an argument with faculty.", "I am getting in an argument with MIT administration.", "I have pissed off the mighty Reif himself.", "I am arguing with Cindy Barnhart.", "I am frying some stuff, do you want some plantains?", "How are we gonna take care of the dish situation?", "I work at Exxon now", "How's your semester going?", "This seems like a bad idea", "How can we do this in a safer way?", "Can we direct this into something more productive?", "Do you think that this is an effective strategy?", "Please consider talking to S^3 for resources.", "Please remember to wear a mask", "Are you registered to vote?", "Maybe we should be more civil to other people"]
            await message.channel.send(random.choice(grtphrases))
        if 'pog' in message.content.lower() and message.author.id == 235221408274186242:
            await message.channel.send(message.author.mention + ", don't say pog")
while True:
    try:
        client.loop.run_until_complete(client.start(token))
    except BaseException:
            time.sleep(5)
