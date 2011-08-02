import lxml.html
import lxml.html.soupparser
import lxml.etree
import dbmanager
import models

def is_hash_different(html_element, old_hash):
    html_element_string = lxml.html.tostring(html_element)
    new_hash = hash(html_element_string)
    return new_hash != old_hash

class Progarchives(object):
    
    def __init__(self):
        self.artists = []
        
    def fetch(self):
        self.artists = []
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
                band.origin = u"Progarchives"
                self.artists.append(band)
            except UnicodeDecodeError, e:
                print str(e)
            except UnicodeEncodeError, e:
                print str(e)
        return self.artists
    
    def save(self, store):
        for artist in self.artists:
            store.add(artist)
        store.commit()