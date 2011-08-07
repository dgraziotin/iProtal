from appscript import app
import models
import fetchers
import os

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
    
    def set_itunes_tracks_genre(self, artist, genre):
        tracks = self.get_itunes_tracks(artist)
        for track in tracks:
            track.genre.set(genre)
    
    def fetch_genre(self, artist, fetcher="ProgArchives"):
        results = []
        if fetcher == 'ProgArchives':
            fetcher = fetchers.ProgArchives()
            results = fetcher.search(artist)
            if not results:
                print "No results from ProgArchives. Falling back to MetalArchives"
                results = self.fetch_genre(artist, 'MetalArchives')
        elif fetcher == 'MetalArchives':
            fetcher = fetchers.MetalArchives()
            results = fetcher.search(artist)
            if not results:
                print "No results from MetalArchives. Sorry."
        else:
            fetcher = None
        
        return results
        
    
    
if __name__=="__main__":
    os.system('/usr/bin/clear')
    print "Welcome to iProtal."
    print "Loading iTunes Library..."
    iprotal = IProtal()
    os.system('/usr/bin/clear')
    print "Welcome to iProtal."
    print "You have " + str(len(iprotal.bands)) + " artists in your iTunes Library."
    print "Do you want to search for them and adjust their genre?"
    choice = raw_input("Enter your choice (Y/N): ")
    if choice.upper() == 'Y':    
        for band in iprotal.bands:
            print "Current Band: " + band.name
            print "Current Genre: " + band.genre
            proposed_genre = iprotal.fetch_genre(band.name)
            if len(proposed_genre) == 0:
                print "No results for this artist."
            elif len(proposed_genre) == 1:
                print "New Genre: " + proposed_genre[0]
            else:
                print "Multiple Genres Proposed: "
                for genre in proposed_genre:
                    print genre + ", ",
    else:
        print "Bye."
        exit(0)
    
    
    