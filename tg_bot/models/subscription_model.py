from sqlite3 import Connection


class SubscriptionModel:

    def __init__(self, connection: Connection) -> None:
        self.connection = connection

    def get_subscribing(self, user_identifier: int):
        cursor = self.connection.cursor()
        result = cursor.execute(
            "SELECT ID, USER_ID, SUBSCRIBING, CHANGE_TIMESTAMP FROM V$SUBSCRIPTION WHERE IDENTIFIER=?;",
            [user_identifier]).fetchone()
        cursor.close()
        return result

    def subscribe_user(self, user_identifier, subscribe):
        self.connection
        pass
