class DefaultMessagesHandler:
    def __call__(self, update, context):
        # update userdata
        context.user_data.update(
            {context.user_data["next"]: update.message.text}
        )

        try:
            message, next_value = next(context.user_data["dialog"])
            context.user_data["next"] = next_value
        except StopIteration:
            # clean user data
            del context.user_data["next"]
            del context.user_data["dialog"]

            message = context.user_data["handler"].process_dialog(
                update, context
            )

        context.bot.send_message(
            chat_id=update.effective_chat.id, text=message
        )
