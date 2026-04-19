"""
platform.py
-----------
Implement the central StreamingPlatform class that orchestrates all domain entities
and provides query methods for analytics.

Classes to implement:
  - StreamingPlatform
"""
from datetime import datetime, timedelta
from .users import PremiumUser, FamilyMember, User
from .tracks import Song, AlbumTrack, Track
from .playlists import Playlist, CollaborativePlaylist
from .artists import Artist


class StreamingPlatform:
    """
    Central class that manages the whole platform
    Attributes: name, catalogue, users, artists, albums, playlists, sessions
    """
    def __init__(self, name: str):
        self.name = name
        self._catalogue = {}
        self._users = {}
        self._artists = {}
        self._albums = {}
        self._playlists = {}
        self._sessions = []

    def add_track(self, track):
        self._catalogue[track.track_id] = track

    def add_user(self, user):
        self._users[user.user_id] = user

    def add_artist(self, artist):
        self._artists[artist.artist_id] = artist

    def add_album(self, album):
        self._albums[album.album_id] = album

    def add_playlist(self, playlist):
        self._playlists[playlist.playlist_id] = playlist

    def record_session(self, session):
        self._sessions.append(session)
        session.user.sessions.append(session)

    def get_track(self, track_id):
        return self._catalogue.get(track_id)

    def get_user(self, user_id):
        return self._users.get(user_id)

    def get_artist(self, artist_id):
        return self._artists.get(artist_id)

    def get_album(self, album_id):
        return self._albums.get(album_id)

    def all_users(self):
        return list(self._users.values())

    def all_tracks(self):
        return list(self._catalogue.values())
    
    # Q1 - Total listening time in minutes for a given time window
    """
    Loops through all sessions and adds up the duration (in minutes)
    of those whose timestamp falls between start and end (inclusive).
    Returns 0.0 if no sessions match the window.
    """
    
    def total_listening_time_minutes(self, start: datetime, end: datetime) -> float:
        total = 0.0
        for session in self._sessions:
            if start <= session.timestamp <= end:
                total += session.duration_listened_minutes()
        return total
    
    # Q2 - Average number of unique tracks listened to by premium users in the last N days
    """
    Filters users to only PremiumUser instances, then for each one
    collects distinct track ids from sessions within the last N days
    Divides total unique tracks by number of premium users
    Returns 0.0 if there are no premium users
    """
               
    def avg_unique_tracks_per_premium_user(self, days: int = 30) -> float:
        start = datetime.today() - timedelta(days=days)
        premium_users = []
        total = 0
        for user in self._users.values():
            if isinstance(user, PremiumUser):
                premium_users.append(user)
        if len(premium_users) == 0:
            return 0.0
        else: 
            for usr in premium_users:
                unique = [s.track.track_id for s in usr.sessions if s.timestamp >= start]
                total += len(unique)
            return float(total / len(premium_users))
            
    # Q3 - Track that was listened to by the most different users
    """
    Builds a dict mapping each track to a set of user ids that listened to it
    Returns the track whose set is the largest
    Returns None if there are no sessions
    """
    
    def track_with_most_distinct_listeners(self) -> Track | None:
        total = {}
        if len(self._sessions) == 0:
            return None
        else: 
            for session in self._sessions:
                track_id = session.track.track_id
                if track_id not in total:
                    total[track_id] = set()
                total[track_id].add(session.user.user_id)
            best_id = max(total, key=lambda t: len(total[t]))
            return self._catalogue[best_id]
    
    # Q4 - Average session length per user type, sorted longest to shortest
    """
    Groups session durations by the class name of the session's user
    Calculates the average duration per group
    Returns a list of (type_name, avg_seconds) tuples sorted longest to shortest
    """
    
    def avg_session_duration_by_user_type(self) -> list[tuple[str, float]]:
        total = {}
        for session in self._sessions:
            type_name = type(session.user).__name__
            if type_name not in total:
                total[type_name] = []
            total[type_name].append(session.duration_listened_seconds)
        result = []
        for type_name, time in total.items():
            result.append((type_name, sum(time)/len(time)))
        return sorted(result, key=lambda x:x[1], reverse=True)
    
    # Q5 - Total listening time of underage family members in minutes
    """
    Loops through users, keeps only FamilyMember instances under age_threshold
    then sums up their session durations converted to minutes
    Returns 0.0 if no matching users or sessions exist
    """                  
    def total_listening_time_underage_sub_users_minutes(self, age_threshold: int = 18) -> float:
        total = 0.0
        for usr in self._users.values():
            if isinstance(usr, FamilyMember) and usr.age < age_threshold:
                for session in usr.sessions:
                    total += session.duration_listened_minutes()
        return total
    
    # Q6 - Top N artists ranked by total listening time
    """
    Loops through sessions, couning only where track is Song/AlbumTrack
    Accumulates total listening minutes per artist
    Sorts artists by total time descending and returns the top N as (Artist, minutes) tuples
    """
    def top_artists_by_listening_time(self, n: int = 5) -> list[tuple[Artist, float]]:
        total = {}
        for session in self._sessions:
            if isinstance(session.track, (Song, AlbumTrack)):
                artist = session.track.artist
                if artist.artist_id not in total:
                    total[artist.artist_id] = 0
                total[artist.artist_id] += session.duration_listened_minutes()
        results = []
        for artist_id, time in total.items():
            artist = self._artists[artist_id]
            results.append((artist, time))
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:n]
    
    # Q7 - A user's most listened genre and what percent of their time it takes up
    """
    Looks up the user by id, returns None if not found or has no sessions
    Groups session durations by genre, finds the genre with the highest total
    Returns (genre, percentage_of_total_time) tuple
    """    
    def user_top_genre(self, user_id: str) -> tuple[str, float] | None:
        user = self._users.get(user_id)
        if not user or not user.sessions:
            return None
        total = {}
        for session in user.sessions:
            genre = session.track.genre
            if genre not in total:
                total[genre] = 0
            total[genre] += session.duration_listened_seconds
        best = max(total, key=lambda g: total[g])
        seconds = sum(total.values())
        percentage = (total[best] / seconds) * 100
        return (best, percentage)
    
    # Q8 - Collaborative playlists that have more than N different artists
    """
    Loops through playlists, keeping only CollaborativePlaylist instances
    For each one counts distinct artists across Song/AlbumTrack tracks
    Returns playlists where the distinct artist count exceeds the threshold
    """
    
    def collaborative_playlists_with_many_artists(self, threshold: int = 3) -> list[CollaborativePlaylist]:
        result = []
        for playlist in self._playlists.values():
            if isinstance(playlist, CollaborativePlaylist):
                artists = set()
                for trk in playlist.tracks:
                    if isinstance(trk, (Song, AlbumTrack)):
                        artists.add(trk.artist.artist_id)
                if len(artists) > threshold:
                    result.append(playlist)
        return result
                
    # Q9 - Average number of tracks per playlist type
    """
    Separates playlists into standard Playlist and CollaborativePlaylist groups
    Calculates the average track count for each group
    Returns a dict with keys 'Playlist' and 'CollaborativePlaylist', 0.0 if a type has none
    """
    
    def avg_tracks_per_playlist_type(self) -> dict[str, float]:
        standard = []
        collaborative = []
        for playlist in self._playlists.values():
            if type(playlist) == Playlist:
               standard.append(playlist) 
        for playlist in self._playlists.values():
            if isinstance(playlist, CollaborativePlaylist):
                collaborative.append(playlist)
        return {"Playlist": sum(len(playlist.tracks) for playlist in standard) / len(standard) if standard else 0.0,
                "CollaborativePlaylist": sum(len(playlist.tracks) for playlist in collaborative) / len(collaborative) if collaborative else 0.0}
    
    # Q10 - Users who listened to every track on at least one album
    """
    For each user collects the set of track ids from all their sessions
    For each album checks if its track ids are a subset of the user's listened tracks
    Returns a list of (User, [album_titles]) for users who completed at least one album
    Skips albums with no tracks
    """
    
    def users_who_completed_albums(self) -> list[tuple[User, list[str]]]:
        result = []
        for usr in self._users.values():
            listened = {session.track.track_id for session in usr.sessions}
            completed = []
            for album in self._albums.values():
                if not album.tracks:
                    continue
                if album.track_ids().issubset(listened):
                    completed.append(album.title)
            if completed:
                result.append((usr, completed))
        return result
