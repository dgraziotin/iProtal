import lxml.html
import lxml.etree
import models
import urllib2
import json

"""
Abstract base class for fetchers
"""
class Fetcher(object):
    
    """
    Base URL for fetching Artists' details 
    """
    __BASE_URL = ''
    
    """
    Unique name for fetcher, used in models.Band.origin
    """
    
    __NAME = ''
    
    """
    Given an Artist name, searches it remotely for the genre.
    It returns a list of models.Band objects or an Empty list.
    The name is internally treated as case-insensitive.
    This should be the only one method called by other objects
    """
    def search(self, name):
        raise NotImplementedError( "Should have implemented this" )
    
    """
    Fetches one or more artists under the given name.
    The name is internally treated as case-insensitive.
    This method should always be used as helper for search(name) method
    """
    def fetch(self, name):
        raise NotImplementedError( "Should have implemented this" )
    

class ProgArchives(Fetcher):
    
    __BASE_URL = 'http://www.progarchives.com/bands-alpha.asp?letter=*'
    __NAME = 'ProgArchives'

    def search(self, name):
        results = []
        for artist in self.fetch(name):
            if artist.name.lower() == name.lower():
                results.append(artist)
        return results
            
    def fetch(self, name):
        results = []
        parsed_page = lxml.html.parse(ProgArchives.__BASE_URL)
        processed_table = parsed_page.xpath("//table")[0]
        
        band_attributes = []
        for row in processed_table[1:]:
            band_attributes = []
            try:
                for col in row:
                    band_attributes.append(col.text_content().strip())
                band = models.Band()
                band.name = unicode(band_attributes[0])
                band.genre = unicode(band_attributes[1])
                band.origin = unicode(ProgArchives.__NAME)
                results.append(band)
            except UnicodeDecodeError, e:
                print str(e)
            except UnicodeEncodeError, e:
                print str(e)
        return results

        
class MetalArchives(Fetcher):
    
    __BASE_URL = 'http://www.metal-archives.com/search/ajax-band-search/?field=name&exactBandMatch=1&query='
    
    def search(self, name):
        return self.fetch(name)
    
    def fetch(self, artist):
        results = []
        artist = urllib2.quote(artist)
        base_url = MetalArchives.__BASE_URL+artist+'&sEcho=1&iDisplayStart='
        
        idisplaystart = 0
        url = base_url + str(idisplaystart)
        json_file = urllib2.urlopen(url)
        json_string = json.load(json_file)

        #itotalrecords =  int(json_string['iTotalRecords'])
        bands_json = json_string[u'aaData']
                
        for band_json in bands_json:
            name = band_json[0]
            genre = band_json[1]
            tree = lxml.html.fromstring(name)
            name_html = tree.xpath("//a")[0]
            name = name_html.text_content()
            band = models.Band()
            try:
                band.name = unicode(name)
                band.genre = unicode(genre)
                band.origin = unicode(MetalArchives.__NAME)
                results.append(band)
            except UnicodeDecodeError, e:
                print str(e)
            except UnicodeEncodeError, e:
                print str(e)
        return results