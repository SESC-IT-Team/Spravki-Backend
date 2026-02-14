fake_db = {
    "misha":{
        "password": "123"
    }
}

class UserRepository:
    def get_user(self, username: str):
        return fake_db.get(username)

def get_user_repository() -> UserRepository:
    return UserRepository()