import discord
from discord.ext import commands
from discord.utils import get

from datetime import datetime
import asyncio


client = discord.Client()

#WSPÓLNE GRANIE:
channelid = #staff ticket channel
staff = #staff role id
recruitment_category = #ticketing category id

base_ticket = "https://images-ext-1.discordapp.net/external/g4dI0KitJwLA18h541sQmBfn_GoewWXVVkw6J4OcMJM/%3Fsize%3D1024/https/cdn.discordapp.com/icons/282162608939728896/a_e6d6f4481d2e6d830631906f6f52368b.gif"


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name='🔶Rekrutacja xDWGx'))
    print("bot is ONLINE")


@client.event
async def on_message(message):

    if message.author == client.user:
        return
        
    if message.channel == message.author.dm_channel:

        channel = client.get_channel(channelid)
        attachments = message.attachments
        content = message.content

        embed = discord.Embed(
            description = f'‎\nPojawiła się **nowa aplikacja** do Dywizjonu.\n‎',
            color = 0xfbbb02)
        embed.set_author(name=f'{message.author}', icon_url=message.author.avatar_url)
        if attachments:
         embed.set_image(url=attachments[0])
        embed.set_thumbnail(url=(base_ticket))
        if content: 
         embed.add_field(name="📄 ‎‎Treść", value=f'{content}\n‎', inline=False)
        if not content:
         embed.add_field(name="📄 ‎‎Treść", value=f'Ticket zawiera tylko załącznik.\n‎', inline=False)
        embed.add_field(name='🆔 User ID', value=f'{message.author.id}', inline=True)
        embed.add_field(name='👤 Username', value=f'{message.author.mention}', inline=True)
        embed.add_field(name='📆 Data utworzenia', value=datetime.now().strftime('Ticket został utworzony o `%H:%M` `%d.%m.%Y`'), inline=False)
        if attachments:
         embed.add_field(name='🔗 Załączniki', value=f'Załącznik znajduje się pod tym [linkiem]( {attachments[0]}).', inline=True)
        if not attachments:
         embed.add_field(name='🔗 Załączniki', value=f'Ticket nie zawiera załączników.', inline=True)
        embed.set_footer(text='‎ \n📩 - Utwórz kanał | ✅ - Rekrut przyjęty | ⛔ - Odrzuć rekruta | 🗑️ - Usuń ticket', icon_url = "")
        msg = await channel.send(embed=embed)

        await msg.add_reaction("📩")
        await msg.add_reaction("✅")
        await msg.add_reaction("⛔")
        await msg.add_reaction("🗑️")

        await message.add_reaction("✅") #adds an reaction to DM 
        await message.channel.send('Twoja aplikacja do **xDWGx** została wysłana! 🔶')

                              
@client.event
async def on_raw_reaction_add(payload):

    channel = client.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)

    if channel.type == discord.ChannelType.private:
      return

    if not message.author == client.user:
      return


    priorEmbed = message.embeds[0]
    emoji = payload.emoji
    reaction = get(message.reactions, emoji=emoji.name)


    if emoji.name == "🗑️" and reaction.count == 2:

        embed = discord.Embed(
            title="🗑️ Ticket został usunięty",
            description= f"Ta wiadomość zostanie usunięta za 7 sekund.",
            color=0xc5c0c0) #FF0000

        await message.clear_reactions()
        await message.edit(embed=embed)
        await asyncio.sleep(7)
        await message.delete()


    elif emoji.name == "📩" and reaction.count == 2:

        recruit = await client.fetch_user(priorEmbed.fields[1].value)
        category = discord.utils.get(channel.guild.categories, id=recruitment_category)
        
        overwrites = {
            channel.guild.default_role: discord.PermissionOverwrite(read_messages=False,read_message_history=False),
            channel.guild.get_role(staff): discord.PermissionOverwrite(read_messages=True,read_message_history=True, send_messages=True, manage_channels=True),
            recruit: discord.PermissionOverwrite(read_messages=True,read_message_history=True, send_messages=True),
        }

        proces = await channel.guild.create_text_channel(f'{recruit}', category=category, overwrites=overwrites, topic=f'Kanał rekrutacyjny dla {priorEmbed.author.name}', reason=f'Rozpoczęto rekrutację {priorEmbed.author.name}')

        await proces.send(f'**Witaj na kanale rekrutacyjnym Dywizjonu Wspólnego Grania {recruit.mention} !**')
        embed = discord.Embed(
            description = f'‎\nNa początek zadamy Ci parę pytań wstępnych. **Odpowiedz na każde z nich poniżej na tym kanale**. Za jakiś czas skontaktuje się z Tobą dowództwo, również za pośrednictwem tego kanału.\n‎',
            color = 0xfbbb02)
        embed.set_thumbnail(url=(base_ticket))
        embed.add_field(name='PYTANIE 1️⃣', value=f'Zdajesz sobie sprawę, że w xDWGx szukamy osób do grania SQB? Jeżeli tak, to jakie masz doświadczenie na SQB? Powiedz w jakich dywizjonach byłeś i ile mniej więcej bitew zagrałeś.\n‎', inline=True)
        embed.add_field(name='PYTANIE 2️⃣', value=f'Posiadasz czołg lub samolot przynajmniej V ery, który nie ma statusu premium, ani nie jest kupiony na rynku? W jakich nacjach znajdują się u ciebie takie maszyny?\n‎', inline=False)
        embed.add_field(name='PYTANIE 3️⃣', value=f'Posiadasz działający, niepierdzący mikrofon i jesteś w stanie zapewnić kulturę gamingu podczas rozgrywek? Co rozumiesz poprzez **kulturę gamingu**?\n‎', inline=True)
        embed.add_field(name='PYTANIE 4️⃣', value=f'Czy dostosowałeś swój nick na serwerze do regulaminu serwera?\n‎', inline=False)
        embed.add_field(name='PYTANIE 5️⃣', value=f'Czy zapoznałeś się z treścią kanałów w sekcji **🔸DYWIZJON🔸**?\n‎', inline=True)
        embed.add_field(name='PYTANIE 6️⃣', value=f'Czy przesłuchałeś nasz podcast o SQB? Link do niego znajduje się na kanale <#435205086889902080>\n‎', inline=False)
        embed.add_field(name='PYTANIE 7️⃣', value=f'Jaki jest najlepszy czołg 2 Wojny Światowej?\n‎', inline=True)
        await proces.send(embed=embed)


        embed = discord.Embed(
            description = f'‎\nKanał rekrutacyjny dla tej aplikacji został **otwarty**.\n‎',
            color = priorEmbed.colour)
        embed.set_author(name=priorEmbed.author.name, icon_url=priorEmbed.author.icon_url)
        embed.set_thumbnail(url=(base_ticket))
        embed.set_image(url=priorEmbed.image.url) 
        embed.add_field(name=priorEmbed.fields[0].name, value=priorEmbed.fields[0].value, inline=False)
        embed.add_field(name=priorEmbed.fields[1].name, value=priorEmbed.fields[1].value, inline=True)
        embed.add_field(name=priorEmbed.fields[2].name, value=priorEmbed.fields[2].value, inline=True)
        embed.add_field(name=priorEmbed.fields[3].name, value=priorEmbed.fields[3].value, inline=False)
        embed.add_field(name=priorEmbed.fields[4].name, value=priorEmbed.fields[4].value, inline=False)
        embed.add_field(name='🆔 Channel ID', value=f'{proces.id}', inline=True)
        embed.add_field(name='#️⃣ Kanał rekrutacyjny', value=f'<#{proces.id}>', inline=True)
        embed.set_footer(text='‎ \n🗑️ - Usuń ticket', icon_url = "")
        await message.edit(embed=embed)

        await message.clear_reactions()
        await message.add_reaction("✅")
        await message.add_reaction("⛔")
        await message.add_reaction("🗑️")


    elif emoji.name == "⛔" and reaction.count == 2:

        recruit = await client.fetch_user(priorEmbed.fields[1].value)
        await recruit.send('Przykro nam, ale Twoja aplikacja do **xDWGx** została odrzucona ☹️')

        try:
            proces = await client.fetch_channel(priorEmbed.fields[5].value)
            await proces.delete()
        except:
            pass

        embed = discord.Embed(
            description = f'‎\nTa aplikacja do Dywizjonu została **odrzucona**.\n‎',
            color = 0x821c1d)
        embed.set_author(name=priorEmbed.author.name, icon_url=priorEmbed.author.icon_url)
        embed.set_thumbnail(url=(base_ticket))
        embed.set_image(url=priorEmbed.image.url) 
        embed.add_field(name=priorEmbed.fields[0].name, value=priorEmbed.fields[0].value, inline=False)
        embed.add_field(name=priorEmbed.fields[1].name, value=priorEmbed.fields[1].value, inline=True)
        embed.add_field(name=priorEmbed.fields[2].name, value=priorEmbed.fields[2].value, inline=True)
        embed.add_field(name=priorEmbed.fields[3].name, value=priorEmbed.fields[3].value, inline=False)
        embed.add_field(name='⛔ Data odrzucenia', value=datetime.now().strftime('Aplikacja została odrzucona o `%H:%M` `%d.%m.%Y`'), inline=True)
        embed.add_field(name=priorEmbed.fields[4].name, value=priorEmbed.fields[4].value, inline=False)
        embed.set_footer(text='‎ \n🗑️ - Usuń ticket', icon_url = "")

        await message.edit(embed=embed)
        await message.clear_reactions()
        await message.add_reaction("🗑️")


    elif emoji.name == "✅" and reaction.count == 2:

        recruit = await client.fetch_user(priorEmbed.fields[1].value)
        await recruit.send('Twoja aplikacja do **xDWGx** została rozpatrzona pozytywnie 🧡')

        try:
            proces = await client.fetch_channel(priorEmbed.fields[5].value)
            await proces.delete()
        except:
            pass

        embed = discord.Embed(
            description = f'‎\nAplikacja do Dywizjonu została rozpatrzona **pozytywnie**.\n‎',
            color = 0x58d68d)
        embed.set_author(name=priorEmbed.author.name, icon_url=priorEmbed.author.icon_url)
        embed.set_thumbnail(url=(base_ticket))
        embed.set_image(url=priorEmbed.image.url) 
        embed.add_field(name=priorEmbed.fields[0].name, value=priorEmbed.fields[0].value, inline=False)
        embed.add_field(name=priorEmbed.fields[1].name, value=priorEmbed.fields[1].value, inline=True)
        embed.add_field(name=priorEmbed.fields[2].name, value=priorEmbed.fields[2].value, inline=True)
        embed.add_field(name=priorEmbed.fields[3].name, value=priorEmbed.fields[3].value, inline=False)
        embed.add_field(name='✅ Data przyjęcia', value=datetime.now().strftime('Rekrut został przyjęty o `%H:%M` `%d.%m.%Y`'), inline=True)
        embed.add_field(name=priorEmbed.fields[4].name, value=priorEmbed.fields[4].value, inline=False)
        embed.set_footer(text='‎ \n🗑️ - Usuń ticket', icon_url = "")

        await message.clear_reactions()
        await message.edit(embed=embed)
        await message.add_reaction("🗑️")
        

client.run('TOKEN HERE')  
