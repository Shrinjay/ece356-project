import sqlalchemy
from client.common.util import get_db_url


class AuthManager:
    current_user_id: int = None

    def authenticate(self):
        print("Enter 0 to continue as guest")
        print("Enter 1 to sign in")

        is_auth = int(input("Select an option: "))

        if is_auth:
            username = input("Enter username: ")
            password = input("Enter password: ")

            query = f"SELECT * FROM InternalUser where username='{username}' and password='{password}'"

            db_url = get_db_url()

            engine = sqlalchemy.engine.create_engine(url=db_url)
            connection = engine.connect()
            result = connection.execute(sqlalchemy.text(query))

            if result.rowcount > 0:
                first = result.first()
                self.current_user_id = first.tuple()[0]
                print(f"Signed in as user ID: {self.current_user_id}")
            else:
                print("Invalid Username or Password")

            connection.close()

    def get_analyst_id(self):
        if self.current_user_id is None:
            print("Signed in as Guest")
            return

        query = f"SELECT * FROM Analyst where userID={self.current_user_id}"

        db_url = sqlalchemy.URL.create(
            "mysql+pymysql",
            username="root",
            password="Sunny2002+",
            host="localhost",
            port=3306,
            database="team99"
        )
        engine = sqlalchemy.engine.create_engine(url=db_url)
        connection = engine.connect()
        result = connection.execute(sqlalchemy.text(query))

        if result.rowcount > 0:
            tuple = result.first().tuple()
            analyst_id = tuple[0]
            print(f"Signed in as analyst ID: {analyst_id}")
            connection.close()
            return analyst_id
        else:
            print("Not signed in as an Analyst")

        connection.close()


auth_manager = AuthManager()
