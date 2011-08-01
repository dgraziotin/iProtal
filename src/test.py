from appscript import *
import models
import dbmanager

class IProtal(object):
    def __init__(self):
        self.library =  app('iTunes').library_playlists['Libreria']
        self.store = dbmanager.DBManager().store()
        
    def get_artists_from_library(self):
        tracks = self.library.tracks()
        bands = []
        artists_seen = []

        for track in tracks:
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
        for band in bands:
            self.store.add(band)
        self.store.commit()
        
    def update_artists_from_library(self):
        tracks = self.library.tracks()

        for track in tracks:
            track.genre = self.get_artist(track.artist()).genre
            
            
        
    def get_artist(self, name):
        return self.store.find(models.Band, models.Band.name == name).one()
    
    
if __name__=="__main__":
    pass