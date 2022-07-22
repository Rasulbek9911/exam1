import datetime

from django.utils import timezone
from telegram import ParseMode, Update, InlineQueryResultArticle, InputTextMessageContent, InputMessageContent
from telegram.ext import CallbackContext

from tgbot.handlers.onboarding import static_text
from tgbot.handlers.utils.info import extract_user_data_from_update
from tgbot.models import User, Post
from tgbot.handlers.onboarding.keyboards import make_keyboard_for_start_command


def command_start(update: Update, context: CallbackContext) -> None:
    u, created = User.get_user_and_created(update, context)

    if created:
        text = static_text.start_created.format(first_name=u.first_name)
    else:
        text = static_text.start_not_created.format(first_name=u.first_name)

    update.message.reply_text(text=text)


def search_post(update: Update, context: CallbackContext) -> None:
    all = []
    query = update.inline_query.query
    post = Post.objects.filter(title__icontains=query)
    for i in post:
        all.append(
            InlineQueryResultArticle(
                id=i.id,
                title=i.title,
                url=i.image,
                input_message_content=InputTextMessageContent(message_text=i.content),
                thumb_url=i.image,
                description=i.content

            )
        )
        update.inline_query.answer(all)
