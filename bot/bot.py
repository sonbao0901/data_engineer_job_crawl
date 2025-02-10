import lightbulb
import os

bot = lightbulb.BotApp(
    token=os.getenv("DISCORD_TOKEN"),  # Ensure the DISCORD_TOKEN env variable has your bot token
    intents=hikari.Intents.ALL_UNPRIVILEGED | hikari.Intents.GUILD_MESSAGES | hikari.Intents.GUILD_MESSAGE_REACTIONS
)

# Load your plugin
from q_a_plugin import plugin
bot.add_plugin(plugin)

# Run the bot
bot.run()
