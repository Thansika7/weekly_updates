import json
import os

class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role


class UserManagement:
    def __init__(self, users_file="users.json"):
        self.users_file = users_file
        self.users = {}
        self.current_user = None
        self.load_users()

    def load_users(self):
        if os.path.exists(self.users_file):
            try:
                with open(self.users_file, 'r', encoding='utf-8') as file:
                    users_dict = json.load(file)
                    for username, data in users_dict.items():
                        self.users[username] = User(
                            username,
                            data['password'],
                            data['role']
                        )
                print(f"Loaded {len(self.users)} users")
            except Exception as e:
                print(f"Error loading users: {e}")
        else:
            print("Users file not found!")

    def save_users(self):
        try:
            users_dict = {}
            for username, user in self.users.items():
                users_dict[username] = {
                    'password': user.password,
                    'role': user.role
                }

            with open(self.users_file, 'w', encoding='utf-8') as file:
                json.dump(users_dict, file, indent=4)

        except Exception as e:
            print(f"Error saving users: {e}")

    def login(self, username, password):
        if username in self.users:
            user = self.users[username]
            if user.password == password:
                self.current_user = user
                print(f"Welcome {username}! (Role: {user.role})")
                return True

        print("Invalid username or password!")
        return False

    def logout(self):
        if self.current_user:
            print(f"Goodbye {self.current_user.username}!")
            self.current_user = None
            return True
        return False

    def register_user(self, username, password, role):
        if self.current_user is None or self.current_user.role != 'faculty':
            print("Only faculty can register new users!")
            return False

        if role not in ['faculty', 'student']:
            print("Invalid role! Use 'faculty' or 'student'")
            return False

        if username in self.users:
            print("Username already exists!")
            return False

        self.users[username] = User(username, password, role)
        self.save_users()
        print(f"User '{username}' registered successfully as {role}")
        return True
