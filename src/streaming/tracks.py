"""
tracks.py
---------
Implement the class hierarchy for all playable content on the platform.

Classes to implement:
  - Track (abstract base class)
    - Song
      - SingleRelease
      - AlbumTrack
    - Podcast
      - InterviewEpisode
      - NarrativeEpisode
    - AudiobookTrack
"""
from abc import ABC

class Track(ABC):
    """
    Base class for any track/type track
    Attributes: track_id, title, duration_seconds, genre
    """
    def __init__(self, track_id, title, duration_seconds, genre):
        self.track_id = track_id
        self.title = title
        self.duration_seconds = duration_seconds
        self.genre = genre
      
    def duration_minutes(self):
        return (self.duration_seconds / 60)
    
    def __eq__(self, other):
        if not isinstance(other, Track):
            return False
        return self.track_id == other.track_id
        

class Song(Track):
    """
    A track linked to an artist
    Attributes: artist
    """
    def __init__(self, track_id, title, duration_seconds, genre, artist):
        super().__init__(track_id, title, duration_seconds, genre)
        self.artist = artist

class SingleRelease(Song):
    """
    A single/not in an album
    Attributes: release_date
    """
    def __init__(self, track_id, title, duration_seconds, genre, artist, release_date):
        super().__init__(track_id, title, duration_seconds, genre, artist)
        self.release_date = release_date

class AlbumTrack(Track):
    """
    A song that belongs to an album
    Attributes: artist, track_number, album
    """
    def __init__(self, track_id, title, duration_seconds, genre, artist, track_number, album = None):
        super().__init__(track_id, title, duration_seconds, genre)
        self.artist = artist
        self.track_number = track_number
        self.album = None

class Podcast(Track):
    """
    A podcast episode with a host
    Attributes: host, description
    """
    def __init__(self, track_id, title, duration_seconds, genre, host="Host", description = ""):
        super().__init__(track_id, title, duration_seconds, genre)
        self.host = host
        self.description = description

class NarrativeEpisode(Podcast):
    """
    A narration
    Attributes: season, episode_number
    """
    def __init__(self, track_id, title, duration_seconds, genre, host, season, episode_number):
        super().__init__(track_id, title, duration_seconds, genre, host)
        self.season = season
        self.episode_number = episode_number


class InterviewEpisode(Podcast):
    """
    An interview with a guest
    Attributes: guest
    """
    def __init__(self, track_id, title, duration_seconds, genre, host, description = "", guest = ""):
        super().__init__(track_id, title, duration_seconds, genre, host, description)
        self.guest = guest


class AudiobookTrack(Track):
    """
    An audiobook
    Attributes: author, narrator
    """
    def __init__(self, track_id, title, duration_seconds, genre, author, narrator):
        super().__init__(track_id, title, duration_seconds, genre)
        self.author = author
        self.narrator = narrator