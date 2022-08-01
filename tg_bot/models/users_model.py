import time
from datetime import datetime
from sqlite3 import Connection


class UsersModel:

    def __init__(self, connection: Connection) -> None:
        self.connection = connection

    def is_exist(self, user_identifier: int) -> bool:
        cursor = self.connection.cursor()
        result = True if cursor.execute('select * from users where IDENTIFIER=?', [user_identifier, ]) \
            .fetchone() else False
        cursor.close()
        return result

    def add(self, user_id: int, full_name, first_name, last_name):
        self.connection.cursor().execute(
            "INSERT INTO USERS ("
            "CREATION_TIMESTAMP, "
            "IDENTIFIER, "
            "FULL_NAME, "
            "FIRST_NAME, "
            "LAST_NAME, "
            "IS_ACTIVE, "
            "CHANGE_TIMESTAMP) "
            "VALUES (?, ?, ?, ?, ?, ?, ?);",
            (time.time(), user_id, full_name, first_name, last_name, True, time.time())).close()
        self.connection.commit()

    def view_all_users(self) -> list:
        cursor = self.connection.cursor()
        result = [{
            'name': name,
            'active_status': True if active_status else False,
            'banned_status': True if banned_status else False,
            'adding_date': datetime.fromtimestamp(adding_date).strftime("%A, %B %d, %Y %I:%M:%S"),
        }
            for name, active_status, banned_status, adding_date \
            in cursor.execute("SELECT FULL_NAME, IS_ACTIVE, IS_BANNED, CREATION_TIMESTAMP FROM USERS").fetchall()]
        cursor.close()
        for row in result:
            print(row.get('adding_date'))
        return result

    def is_active_user(self, user_identifier) -> bool:
        cursor = self.connection.cursor()
        result = cursor.execute("SELECT IS_ACTIVE FROM USERS WHERE IDENTIFIER=?", [user_identifier]).fetchone()[0]
        cursor.close()
        return True if result else False

    def enable_user(self, user_identifier: int) -> None:
        self.connection.cursor() \
            .execute("UPDATE USERS SET IS_ACTIVE=True WHERE IDENTIFIER=?", [user_identifier, ]).close()
        self.connection.commit()

    def disable_user(self, user_identifier: int) -> None:
        self.connection.cursor() \
            .execute("UPDATE USERS SET IS_ACTIVE=False WHERE IDENTIFIER=?", [user_identifier, ]).close()
        self.connection.commit()

    def get_identifier_active_users(self):
        cursor = self.connection.cursor()
        identifiers = cursor.execute("SELECT IDENTIFIER FROM USERS WHERE IS_ACTIVE=TRUE").fetchall()
        cursor.close()
        return identifiers
