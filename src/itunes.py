from appscript import app

"""
Wraps operations to be performed in iTunes
"""
class ITunes(object):

    """
    Returns the name of the Library Playlists of iTunes
    """
    @staticmethod
    def get_library_playlists():
        return app('iTunes').library_playlists.get()

    """
    If Library name is given, automatically stores in memory all iTunes tracks.
    Otherwise, it stores in memory the selected tracks in iTunes
    """
    def __init__(self, library_name=None):
        self.library_name = library_name
        self.itunes = app('iTunes')
        if self.library_name:
            self.itunes_library = self.itunes.library_playlists[self.library_name]
            self.tracks = self.fetch_tracks()
        else:
            self.itunes_library = None
            self.tracks = self.fetch_tracks(selection=True)

    """
    Returns the selected tracks (or the Library tracks) of iTunes
    """
    def fetch_tracks(self, selection=False):
        if selection:
            return self.itunes.selection()
        else:
            return self.itunes_library.tracks()

    """
    Returns tracks of a given band from iTunes Library or from the selected iTunes tracks
    """
    def filter_tracks(self, band, tracks=None):
        filtered_tracks = []
        for track in self.tracks:
            if track.artist.get().lower() == band.name.lower():
                filtered_tracks.append(track)
        return filtered_tracks

    """
    For a given band, updates the band's genre in the iTunes Library or in the selected iTunes tracks
    """
    def set_itunes_tracks_genre(self, genre, band=None, tracks=None):
        if tracks:
            for track in tracks:
                track.genre.set(genre)
        else:
            tracks = self.filter_tracks(band)
            for track in tracks:
                track.genre.set(genre)


