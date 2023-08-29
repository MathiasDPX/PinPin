from dotenv import load_dotenv
from discord.ext import commands
import discord 
import os
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=".", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    await bot.tree.sync()
    print("Context Menu command sync")

@bot.tree.context_menu(name="Pin")
async def pin(interaction: discord.Interaction, message: discord.Message):
        if message.channel.type == discord.ChannelType.public_thread or message.channel.type == discord.ChannelType.private_thread:
            if message.author == interaction.user:
                try:
                    await message.pin()
                    await interaction.response.send_message(f"Message épingle avec succès", ephemeral=True)
                except Exception as e:
                    await interaction.response.send_message("Impossible d'épingler votre message", ephemeral=True)
                    print(e)
            else:
                await interaction.response.send_message("Vous devez être l'auteur de ce post pour épinglé des messages", ephemeral=True)
        else:
            await interaction.response.send_message("Vous devez être dans un post pour effectuer cette interaction", ephemeral=True)
            
@bot.tree.context_menu(name="Unpin")
async def pin(interaction: discord.Interaction, message: discord.Message):
        if message.channel.type == discord.ChannelType.public_thread or message.channel.type == discord.ChannelType.private_thread:
            if message.author == interaction.user:
                if message.pinned:
                    try:
                        await message.unpin()
                        await interaction.response.send_message(f"Message deépingle avec succès", ephemeral=True)
                    except Exception as e:
                        await interaction.response.send_message("Impossible de deépingler votre message", ephemeral=True)
                        print(e)
                else:
                    await interaction.response.send_message("Le message doit être épinglé", ephemeral=True)
            else:
                await interaction.response.send_message("Vous devez être l'auteur de ce post pour deépinglé des messages", ephemeral=True)
        else:
            await interaction.response.send_message("Vous devez être dans un post pour effectuer cette interaction", ephemeral=True)
            
            
try:
    bot.run(os.getenv("TOKEN"))
except Exception as e:
    print(f"Error when logging in: {e}")