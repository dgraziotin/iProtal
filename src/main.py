from appscript import app
import models
import fetchers
import os

class IProtal(object):

    @staticmethod
    def get_itunes_library_playlists():
        return app('iTunes').library_playlists.get()

    def __init__(self, library_name=None):
        self.itunes = app('iTunes')
        if library_name:
            self.library =  self.itunes.library_playlists[library_name]
            self.itunes_tracks = self.fetch_itunes_tracks()
            self.bands = self.fetch_bands()
        else:
            self.library = None
            self.itunes_selected_tracks = self.get_itunes_selected_tracks()
            self.itunes_tracks = self.itunes_selected_tracks
            self.bands = self.fetch_bands()
        
    def fetch_itunes_tracks(self, selection=False):
        if selection:
            return self.itunes.selection()
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

    def get_itunes_selected_tracks(self):
        return self.itunes.selection.get()
    
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

    def update_itunes_tracks_genre(self):
        for band in self.bands:
            print "Current Band: " + band.name
            print "Current Genre: " + band.genre
            proposed_genre = self.fetch_genre(band.name)
            if len(proposed_genre) == 0:
                print "No results for this artist."
            elif len(proposed_genre) == 1:
                print "New Genre: " + proposed_genre[0]
            else:
                print "Multiple Genres Proposed: "
                for genre in proposed_genre:
                    print genre + ", ",
        
    
    
if __name__=="__main__":
    while True:
        os.system('/usr/bin/clear')
        print "Welcome to iProtal."
        print "Please select an iTunes library playlist:"

        itunes_library_playlists = IProtal.get_itunes_library_playlists()
        print "-1 - Use highlighted tracks in iTunes. Remember to select some tracks in iTunes first."
        for i in range (len(itunes_library_playlists)):
            print str(i) + " - " + itunes_library_playlists[i].name.get()
        try:
            choice = int(raw_input("Enter Library id Number: "))
            if choice == -1:
                iprotal = IProtal()
                break
            else:
                iprotal = IProtal(itunes_library_playlists[choice].name.get())
                break
        except ValueError:
            pass
        except IndexError:
            pass
    os.system('/usr/bin/clear')
    print "Welcome to iProtal."
    print "You have " + str(len(iprotal.bands)) + " artists selected."
    print "Do you want to search for them and adjust their genre?"

    choice = raw_input("Enter your choice (Y/N): ")
    if choice.upper() == 'Y':
        iprotal.update_itunes_tracks_genre()
    else:
        print "Bye."
        exit(0)
