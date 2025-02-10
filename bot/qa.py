import instructor
from pydantic import BaseModel, Field
import hikari
import lightbulb
from openai import OpenAI


plugin = lightbulb.Plugin("Q&A", "📝 Q&A Automation")


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin)


class QuestionReply(BaseModel):
    response: str = Field(
        description="The response to the question provided, in Vietnamese. Keep it less than 200 words.")


class ChatBot:
    def __init__(self):
        self.client = instructor.from_openai(OpenAI())
        self.contexts = {}
        self.response_count = {}

    def ask_with_context(self, thread_id, image_urls, question) -> str:
        """Submits a question with images and context to the Instructor API and returns the response."""

        content = """
        You are a helpful teaching assistant for the Data Science course. Please respond to the following question in Vietnamese, keeping your answer concise and under 200 words.
        """

       # Initialize conversation history if it doesn't exist
        messages = self.contexts.setdefault(
            thread_id, [{"role": "system", "content": content}])

        # Add user's question, including images if provided
        user_message = {"role": "user", "content": question}
        if image_urls:
            user_message["images"] = image_urls

        # Append to conversation history
        messages.append(user_message)

        # Generate a reply based on the entire conversation history
        reply = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            response_model=QuestionReply,
        )

        # Append the assistant's response to maintain context
        messages.append({"role": "assistant", "content": reply.response})

        # Update the context and response count for this thread
        self.contexts[thread_id] = messages
        self.response_count[thread_id] = self.response_count.get(
            thread_id, 0) + 1

        return reply.response


@plugin.listener(hikari.StartingEvent)
async def on_starting(event: hikari.StartingEvent) -> None:
    plugin.app.d.bot = ChatBot()


@plugin.listener(hikari.GuildThreadCreateEvent)
async def on_thread_create(event: hikari.GuildThreadCreateEvent) -> None:
    """Handles the creation of a new thread in the question center and responds to the first message."""
    thread: hikari.GuildThreadChannel = await event.fetch_channel()

    if thread.parent_id == 1301822138319114302:
        messages = await thread.fetch_history()
        if messages:
            message: hikari.Message = messages[0]
            attachments = [att.url for att in message.attachments]
            response = plugin.app.d.bot.ask_with_context(
                thread.id, attachments, message.content)
            await event.thread.send(response)
    else:
        print("Not question center")


@plugin.listener(hikari.GuildMessageCreateEvent)
async def on_message_create(event: hikari.GuildMessageCreateEvent) -> None:
    """Handles new messages in the question center thread to respond to follow-up questions."""
    message = event.message
    if message.author.is_bot:
        return

    thread: hikari.GuildThreadChannel = await message.fetch_channel()
    if thread.parent_id != 1301822138319114302:
        return
    if len(await thread.fetch_history()) <= 1:
        return
    if 1302689724431073310 in thread.applied_tag_ids:
        print("Already responded")
        return

    response_count = plugin.app.d.bot.response_count.get(thread.id, 0)
    if response_count >= 4:
        ta_role_id = 1194665960376901773
        await thread.send(f"Bạn đợi các bạn TA <@&{ta_role_id}> một xíu nha!")
        await thread.edit(
            applied_tags=[1302689724431073310]
        )

    else:
        attachments = [att.url for att in message.attachments]
        response = plugin.app.d.bot.ask_with_context(
            thread.id, attachments, message.content)
        await thread.send(response)
