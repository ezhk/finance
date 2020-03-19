from bot.handlers.commands import DefaultCommandsHandler


class DefaultCallbacksHandler:
    """
    Based possoble callbacks for CallbackQueryHandler.
        Using by button click in different dialogs.
    """

    @staticmethod
    def show(update, context):
        context.user_data["handler"].show(update, context)

    @staticmethod
    def create(update, context):
        context.user_data["handler"].create(update, context)

    @staticmethod
    def delete_menu(update, context):
        context.user_data["handler"].delete_menu(update, context)

    @staticmethod
    def delete_item(update, context):
        context.user_data["handler"].delete_item(update, context)

    @staticmethod
    def select_item(update, context):
        context.user_data["handler"].select_item(update, context)


class CategoryCallbacksHandler(DefaultCommandsHandler):
    pass


class TransactionCallbacksHandler(DefaultCommandsHandler):
    pass
