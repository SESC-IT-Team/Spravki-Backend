fake_db = {
    "user":{
        "password": "1",
        "full_name": "user_user",
        "class": "XX"
    }
}

class UserRepository:
    def get_user(self, username: str):
        return fake_db.get(username)

def get_user_repository() -> UserRepository:
    return UserRepository()