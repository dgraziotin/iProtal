from appscript import app
import models
import fetchers

class IProtal(object):
    def __init__(self):
        self.library =  app('iTunes').library_playlists['Libreria']
        self.itunes_tracks = self.fetch_itunes_tracks()
        self.bands = self.fetch_bands()
        
    def fetch_itunes_tracks(self):
        return self.library.tracks()
    
    def fetch_bands(self):
        bands = []
        artists_seen = []
        
        for track in self.itunes_tracks:
            artist = track.artist()
            genre = track.genre()
            origin = u'Libreria'
            if not artist in artists_seen:
                band = models.Band()
                band.name = artist
                band.genre = genre
                band.origin = origin
                bands.append(band)
                artists_seen.append(artist)
        return bands
    
    def get_itunes_tracks(self, artist):
        artist = artist.lower()
        tracks = []
        for track in self.itunes_tracks:
            if track.artist.get().lower() == artist:
                tracks.append(track)
        return tracks
    
    
    
if __name__=="__main__":
    iprotal = IProtal()
    tool = iprotal.get_itunes_tracks("tool")
    progarchives = fetchers.ProgArchives()
    print tool[0].genre.get()
    print progarchives.search("tool")[0].genre
    
    
    