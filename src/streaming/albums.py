"""
albums.py
---------
Implement the Album class for collections of AlbumTrack objects.

Classes to implement:
  - Album
"""
class Album():
  """
  A collection of tracks by an artist.
  Attributes: album_id, title, artist, release_year, tracks
  """
  def __init__(self, album_id, title, artist, release_year, tracks = None):
    self.album_id = album_id
    self.title = title
    self.artist = artist
    self.release_year = release_year
    self.tracks = tracks if tracks is not None else []
      
  def add_track(self, track):
    track.album = self
    self.tracks.append(track)
    self.tracks.sort(key = lambda x : x.track_id, reverse=True)
  
  def duration_seconds(self):
      if not self.tracks:
          return 0 
      total = 0
      for t in self.tracks:
          total += t.duration_seconds 
      return total
  
  def track_ids(self):
    return {t.track_id for t in self.tracks}
    
    
    
    