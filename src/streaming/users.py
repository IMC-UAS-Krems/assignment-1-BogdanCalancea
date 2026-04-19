"""
users.py
--------
Implement the class hierarchy for platform users.

Classes to implement:
  - User (base class)
    - FreeUser
    - PremiumUser
    - FamilyAccountUser
    - FamilyMember
"""

class User():
    """
    Base class for all platform users
    Attributes: user_id, name, age, sessions
    """
    def __init__(self, user_id, name, age):
        self.user_id = user_id
        self.name = name
        self.age = age
        self.sessions = []

    def add_session(self, session):
        self.sessions.append(session)

    def total_listening_seconds(self):
        total = 0
        for session in self.sessions:
            total += session.duration_listened_seconds
        return total

    def total_listening_minutes(self):
        total = 0
        for session in self.sessions:
            total += session.duration_listened_minutes()
        return total

    def unique_tracks_listened(self):
        total = []
        for session in self.sessions:
            total.append(session.track.track_id)
        return set(total)

class FamilyAccountUser(User):
    """
    A user who owns a family plan
    Attributes: sub_users
    """
    def __init__(self, user_id, name, age):
        super().__init__(user_id, name, age)
        self.sub_users = []
        
    def add_sub_user(self, user):
        self.sub_users.append(user)
    
    def all_members(self):
        return [self] + self.sub_users

class FamilyMember(FamilyAccountUser):
    """
    A sub-user of the family account
    Attributes: parent
    """
    def __init__(self, user_id, name, age, parent):
        super().__init__(user_id, name, age)
        self.parent = parent

class FreeUser(User):
    """
    A user on the free plan with limited skips
    """
    MAX_SKIPS_PER_HOUR = 6

class PremiumUser(User):
    """
    A paying user with full access
    Attributes: subscription_start
    """
    def __init__(self, user_id, name, age, subscription_start):
        super().__init__(user_id, name, age)
        self.subscription_start = subscription_start
        