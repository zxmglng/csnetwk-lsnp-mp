from collections import defaultdict

class UserStore:
    def __init__(self):
        self.users = {}
        self.usernames = {}
        self.followers = defaultdict(set)
    
    def register(self, address, username):
        if username in self.usernames:
            return False

        self.users[address] = username
        self.usernames[username] = address
        self.followers[username] = set()
        return True
    
    def get_address(self, username):
        return self.usernames.get(username)
    
    def get_username(self, address):
        return self.users.get(address, f"Anon{address[1]}")

    def follow(self, follower_address, target_username):
        follower = self.get_username(follower_address)
        self.followers[target_username].add(follower)
    
    def unfollow(self, follower_address, target_username):
        follower = self.get_username(follower_address)
        self.followers[target_username].discard(follower)
    
    def get_followers(self, username):
        return self.followers.get(username, set())

    def all_users(self):
        return self.users