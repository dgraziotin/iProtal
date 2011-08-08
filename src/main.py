import itunes
import models
import fetchers
import os

"""
Main application
"""
class IProtal(object):

    def __init__(self, library_name=None):
        self.itunes = itunes.ITunes(library_name)

        self.bands = self.filter_bands_from_tracks()

        self.tracks_delayed = {}
        self.tracks_no_genre_found = []
    
    def filter_bands_from_tracks(self, tracks=None):
        bands = []
        artists_seen = []

        if tracks:
            to_be_filtered = tracks
        else:
            to_be_filtered = self.itunes.tracks
        
        for track in to_be_filtered:
            artist = track.artist()
            genre = track.genre()
            origin = self.itunes.library_name
            if not artist in artists_seen:
                band = models.Band()
                band.name = artist
                band.genre = genre
                band.origin = origin
                bands.append(band)
                artists_seen.append(artist)
        return bands
    
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
                filtered_tracks = self.itunes.filter_tracks(band)
                for track in filtered_tracks:
                    self.tracks_no_genre_found.append(track)
            elif len(proposed_genre) == 1:
                print "New Genre: " + proposed_genre[0]
            else:
                print "Multiple Genres Proposed: "
                band.genre_proposed = proposed_genre
                band.tracks = self.itunes.filter_tracks(band)
                for genre in band.genre_proposed:
                    print genre + ", ",
                    self.tracks_delayed[band.name] = band
                print "\nQueued for later."

if __name__=="__main__":
    while True:
        os.system('/usr/bin/clear')
        print "Welcome to iProtal."
        print "Please select an iTunes library playlist:"

        itunes_library_playlists = itunes.ITunes.get_library_playlists()
        print "-1 - Use highlighted tracks in iTunes. Remember to select some tracks in iTunes first."
        for i in range (len(itunes_library_playlists)):
            print str(i) + " - " + itunes_library_playlists[i].name.get()
        try:
            choice = int(raw_input("Enter Library id Number or -1 for using selected tracks: "))
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
        if iprotal.tracks_delayed:
            for key, value in iprotal.tracks_delayed.items():
                os.system('/usr/bin/clear')
                print "There are some not processed artists for multiple genre:"
                band = value
                print "Artist: " + band.name
                print "Current Genre: " + band.genre
                print "Proposed Genres: "
                for i in range(len(band.genre_proposed)):
                    print str(i) + " - " + band.genre_proposed[i]
                while True:
                    try:
                        choice = int(raw_input("Enter the Genre number: "))
                        print "You selected: " + band.genre_proposed[choice]
                        break
                    except ValueError:
                        pass
                    except IndexError:
                        pass
                
        if iprotal.tracks_no_genre_found:
            os.system('/usr/bin/clear')
            print "There are some artists for which no genre was found:"
            bands_no_genre_found = iprotal.filter_bands_from_tracks(tracks=iprotal.tracks_no_genre_found)
            for band in bands_no_genre_found:
                print band.name

    else:
        print "Bye."
        exit(0)
