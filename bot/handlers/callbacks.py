class DefaultCallbacksHandler:
    @staticmethod
    def show(update, context):
        context.user_data["handler"].show(update, context)

    @staticmethod
    def create(update, context):
        context.user_data["handler"].create(update, context)

    @staticmethod
    def delete(update, context):
        context.user_data["handler"].delete(update, context)
