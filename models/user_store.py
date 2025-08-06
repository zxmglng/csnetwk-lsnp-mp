from collections import defaultdict

class UserStore:
    def __init__(self):
        self.users = {}
        self.usernames = {}
        self.followers = defaultdict(set)
    
    """
    Registers a new user in the system.

    Args:
        address (tuple): A (host, port) tuple representing the user's socket address.
        username (str): The username to associate with this address.

    Returns:
        bool: True if registration is successful, False if the username is already taken.
    """
    def register(self, address, username):
        if username in self.usernames:
            return False

        self.users[address] = username
        self.usernames[username] = address
        self.followers[username] = set()
        return True
    
    """
    Retrieves the socket address associated with a given username.

    Args:
        username (str): The username whose address is being requested.

    Returns:
        tuple or None: The (host, port) address if the user exists, else None.
    """
    def get_address(self, username):
        return self.usernames.get(username)
    
    """
    Retrieves the username associated with a given socket address.

    Args:
        address (tuple): The client's (host, port) socket address.

    Returns:
        str: The registered username
    """
    def get_username(self, address):
        return self.users.get(address, f"Anon{address[1]}")

    """
    Makes one user follow another.

    Args:
        follower_address (tuple): The follower's socket address.
        target_username (str): The username of the person to follow.
    """
    def follow(self, follower_address, target_username):
        follower = self.get_username(follower_address)
        self.followers[target_username].add(follower)
    
    """
    Makes one user unfollow another.

    Args:
        follower_address (tuple): The follower's socket address.
        target_username (str): The username of the person to unfollow.
    """
    def unfollow(self, follower_address, target_username):
        follower = self.get_username(follower_address)
        self.followers[target_username].discard(follower)
    
    """
    Returns the set of followers for a specific user.

    Args:
        username (str): The username whose followers are to be retrieved.

    Returns:
        set: A set of usernames following the given user.
    """
    def get_followers(self, username):
        return self.followers.get(username, set())

    """
    Returns all registered users.

    Returns:
        dict: A mapping of addresses to usernames.
    """
    def all_users(self):
        return self.users