class DefaultCallbacksHandler:
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
