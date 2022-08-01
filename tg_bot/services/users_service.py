import aiogram

from tg_bot.models import UsersModel, SubscriptionModel


class UsersService:

    def __init__(self) -> None:
        self.subscription_model = None
        self.users = None
        self.admins_ids = None

    def set_parameters(self, connection, admins: list):
        self.users = UsersModel(connection)
        self.subscription_model = SubscriptionModel(connection)
        self.admins_ids = admins

    def get_subscribing_user(self, telegram_user: aiogram.types.user.User):
        self.subscription_model.get_subscribing(telegram_user.id)

    def adding_user_or_set_active_status(self, telegram_user: aiogram.types.user.User) -> None:
        """
        Метод выполняет проверку существует ли в базе данных переданный пользователь.
        В случае если пользователь существует, то выполняется проверка статуса 'Активен'.
        При неактивности пользователя значение поля меняется на True.
        Если пользователь не существует, он добавляется в базу данных.
        """
        if self.users.is_exist(telegram_user.id):
            if not self.users.is_active_user(telegram_user.id):
                self.users.enable_user(telegram_user.id)
        else:
            self.users.add(user_id=telegram_user.id,
                           full_name=telegram_user.full_name,
                           first_name=telegram_user.first_name,
                           last_name=telegram_user.last_name)

    def disable_user(self, telegram_user: aiogram.types.user.User):
        if telegram_user.id not in self.admins_ids:
            self.users.disable_user(telegram_user.id)

    def count_all_users(self):
        pass

    def count_active_users(self):
        print('count_active_users')
        pass

    def get_identifier_all_active_users(self) -> list:
        return self.users.get_identifier_active_users()
