"""
playlists.py
------------
Implement playlist classes for organizing tracks.

Classes to implement:
  - Playlist
    - CollaborativePlaylist
"""

class Playlist():
    """
    An users's collection of tracks
    Attributes: playlist_id, name, owner, tracks
    """
    def __init__(self, playlist_id, name, owner, tracks = None):
        self.playlist_id = playlist_id
        self.name = name
        self.owner = owner
        self.tracks = tracks if tracks is not None else []

    def add_track(self, track):
        if track not in self.tracks:
            self.tracks.append(track)
        
    def remove_track(self, track_id):
        for t in self.tracks:
            if track_id == t.track_id:
                self.tracks.remove(t)
            
      
    def total_duration_seconds(self) -> int:
        total = 0
        for t in self.tracks:
            total += t.duration_seconds
        return total

class CollaborativePlaylist(Playlist):
    """
    A playlist with multiple contributors
    Attributes: contributors
    """
    def __init__(self, playlist_id, name, owner):
        super().__init__(playlist_id, name, owner)
        self.contributors = [owner]
        
    def add_contributor(self, user):
        if user not in self.contributors:
            self.contributors.append(user)
        
    def remove_contributor(self, user):
        if user in self.contributors and user != self.owner:
            self.contributors.remove(user)
  
  
  
    