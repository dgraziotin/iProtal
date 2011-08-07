import lxml.html
import lxml.html.soupparser
import lxml.etree
import dbmanager
import models
import urllib2
import json

def is_hash_different(html_element, old_hash):
    html_element_string = lxml.html.tostring(html_element)
    new_hash = hash(html_element_string)
    return new_hash != old_hash

class ProgArchives(object):

    def search(self, name):
        results = []
        for artist in self.fetch(name):
            if artist.name.lower() == name.lower():
                results.append(artist)
        return results
            
    def fetch(self, name):
        results = []
        parsed_page = lxml.html.parse(open('/Users/dgraziotin/Projects/iProtal/src/progarchives.html','r')).getroot()
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
                band.origin = u"ProgArchives"
                results.append(band)
            except UnicodeDecodeError, e:
                print str(e)
            except UnicodeEncodeError, e:
                print str(e)
        return results

        
class MetalArchives(object):
    
    def search(self, name):
        return self.fetch(name)
    
    def fetch(self, artist):
        results = []
        artist = urllib2.quote(artist)
        base_url = 'http://www.metal-archives.com/search/ajax-band-search/?field=name&query='+artist+'&sEcho=1&iDisplayStart='
        
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
                band.origin = u"MetalArchives"
            except UnicodeDecodeError, e:
                print str(e)
            except UnicodeEncodeError, e:
                print str(e)
            results.append(band)
        
        return results