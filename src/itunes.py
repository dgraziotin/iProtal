from appscript import app
import models

"""
Wraps operations to be performed in iTunes
"""
class ITunes(object):

    @staticmethod
    def get_library_playlists():
        return app('iTunes').library_playlists.get()

    def __init__(self, library_name=None):
        self.library_name = library_name
        self.itunes = app('iTunes')
        if self.library_name:
            self.itunes_library =  self.itunes.library_playlists[self.library_name]
            self.tracks = self.fetch_tracks()
        else:
            self.itunes_library = None
            self.tracks = self.fetch_tracks(selection=True)

    def fetch_tracks(self, selection=False):
        if selection:
            return self.itunes.selection()
        else:
            return self.itunes_library.tracks()

    def filter_tracks(self, band, tracks=None):
        filtered_tracks = []
        for track in self.tracks:
            if track.artist.get().lower() == band.name.lower():
                filtered_tracks.append(track)
        return filtered_tracks

    def set_itunes_tracks_genre(self, genre, band=None, tracks=None):
        if tracks:
            for track in tracks:
                track.genre.set(genre)
        else:
            tracks = self.filter_tracks(band)
            for track in tracks:
                track.genre.set(genre)


