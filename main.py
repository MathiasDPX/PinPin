from discord.ext import commands
import discord, json

intents = discord.Intents.default()
intents.message_content = True
intents.presences = True

with open("config.json", "r") as f:
    config = json.load(f)
    
bot = commands.Bot(command_prefix=config["BOT_PREFIX"], intents=intents)

@bot.event
async def on_ready():
    print(f'Connecté en tant que {bot.user}')
    await bot.tree.sync()
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=config["Activity"]))
    print("Activité mise sur 'Regarde "+config["Activity"]+"'")

@bot.tree.context_menu(name="Pin")
async def pin(interaction: discord.Interaction, message: discord.Message):
        if message.channel.type == discord.ChannelType.public_thread or message.channel.type == discord.ChannelType.private_thread:
            if message.author == interaction.user:
                try:
                    await message.pin()
                    await interaction.response.send_message(config["messages"]["pin"]["success"], ephemeral=True)
                    message = await interaction.original_response()
                    print(config["logs"]["pin"].replace("{user}", interaction.user.name).replace("{messageId}", str(message.id)).replace("{channel}", message.channel.name))
                except Exception as e:
                    await interaction.response.send_message(config["messages"]["pin"]["error"], ephemeral=True)
                    print(e)
                                else:
                await interaction.response.send_message(config["messages"]["owner_only"], ephemeral=True)
        else:
            await interaction.response.send_message(config["messages"]["post_only"], ephemeral=True)
            
@bot.tree.context_menu(name="Unpin")
async def pin(interaction: discord.Interaction, message: discord.Message):
        if message.channel.type == discord.ChannelType.public_thread or message.channel.type == discord.ChannelType.private_thread:
            if message.author == interaction.user:
                if message.pinned:
                    try:
                        await message.unpin()
                        await interaction.response.send_message(config["messages"]["unpin"]["success"], ephemeral=True)
                        message = await interaction.original_response()
                        print(config["logs"]["unpin"].replace("{user}", interaction.user.name).replace("{messageId}", str(message.id)).replace("{channel}", message.channel.name))
                    except Exception as e:
                        await interaction.response.send_message(config["messages"]["unpin"]["error"], ephemeral=True)
                        print(e)
                else:
                    await interaction.response.send_message(config["messages"]["unpin"]["need"], ephemeral=True)
            else:
                await interaction.response.send_message(config["messages"]["owner_only"], ephemeral=True)
        else:
            await interaction.response.send_message(config["messages"]["post_only"], ephemeral=True)
            
            
try:
    bot.run(config["TOKEN"])
except Exception as e:
    print(f"Erreur lors de la connexion: {e}")
