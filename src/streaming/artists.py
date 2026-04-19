"""
artists.py
----------
Implement the Artist class representing musicians and content creators.

Classes to implement:
  - Artist
"""

class Artist():
  """
  A musician or content creator on the platform
  Attributes: artist_id, name, genre, tracks
  """
  def __init__(self, artist_id, name, genre, tracks = None):
    self.artist_id = artist_id
    self.name = name
    self.genre = genre
    self.tracks = tracks if tracks is not None else []
      
  def add_track(self, track):
    self.tracks.append(track)
  
  def track_count(self):
    if self.tracks is None:
      return 0
    else:
      return len(self.tracks)