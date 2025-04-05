import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from openai import OpenAI
import asyncio
import webserver

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
OPENAI_API_KEY = os.getenv('QWEN_2_5_32B')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}!!!")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

async def generate_ai_response(prompt):
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=OPENAI_API_KEY,
    )
    try:
        response = client.chat.completions.create(
            model="qwen/qwen2.5-vl-32b-instruct:free",
            messages=[
                {"role": "system", "content": "You are a helpful career assistant specialized in helping people find jobs. Provide tailored advice based on the user's questions. Summarize answer and give response smaller than 2,000 characters."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        return "Sorry, I encountered an error while processing your request. Please try again later."

@bot.tree.command(name="jobchat", description="Start a private DM conversation for job assistance")
async def jobchat(interaction: discord.Interaction):
    """Start a private DM conversation for job help"""
    try:
        # Create DM channel if it doesn't exist
        dm_channel = interaction.user.dm_channel
        if dm_channel is None:
            dm_channel = await interaction.user.create_dm()
        
        welcome_msg = (
            "👋 Welcome to your private job assistance chat!\n"
            "I'm here to help you with:\n"
            "- Resume and cover letter advice\n"
            "- Job search strategies\n"
            "- Interview preparation\n"
            "- Career guidance\n\n"
            "Ask me anything about your job search!"
        )
        
        # Send welcome message in DM
        await dm_channel.send(welcome_msg)
        
        # Respond in the server (ephemeral so only the user sees it)
        await interaction.response.send_message(
            "I've sent you a private message with job assistance! Check your DMs.",
            ephemeral=True
        )
    except Exception as e:
        print(f"Error creating DM chat: {e}")
        await interaction.response.send_message(
            "Sorry, I couldn't send you a DM. Please make sure your DMs are open and try again.",
            ephemeral=True
        )

@bot.command(name='ask', help='Ask the AI a question')
async def ask(ctx, *, question):
    async with ctx.typing():
        response = await generate_ai_response(question)
    
    if len(response) > 2000:
        for chunk in [response[i:i+2000] for i in range(0, len(response), 2000)]:
            await ctx.send(chunk)
    else:
        await ctx.send(response)

@bot.event
async def on_message(message):
    # Don't respond to ourselves or other bots
    if message.author == bot.user or message.author.bot:
        return
    
    # Check if it's a DM (not in a server)
    if isinstance(message.channel, discord.DMChannel):
        async with message.channel.typing():
            response = await generate_ai_response(message.content)
            
            # if len(response) > 2000:
            #     for chunk in [response[i:i+2000] for i in range(0, len(response), 2000)]:
            #         await message.channel.send(chunk)
            #         await asyncio.sleep(3)
            # else:
            await message.channel.send(response)
        return
    
    # Check if the bot is mentioned in a server
    if bot.user.mentioned_in(message):
        async with message.channel.typing():
            clean_content = message.clean_content.replace(f'@{bot.user.name}', '').strip()
            response = await generate_ai_response(clean_content)
            
            if len(response) > 2000:
                for chunk in [response[i:i+2000] for i in range(0, len(response), 2000)]:
                    await message.channel.send(chunk)
            else:
                await message.channel.send(response)
    
    # Process commands
    await bot.process_commands(message)

if __name__ == '__main__':
    #webserver.keep_alive()
    bot.run(DISCORD_TOKEN)