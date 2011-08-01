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
    def fetch(self):
        parsed_page = lxml.html.parses(open('/Users/dgraziotin/Projects/iProtal/src/progarchives.html','r')).getroot()
        processed_table = parsed_page.xpath("//table")[0]
        bands = []
        band_list = []
        for row in processed_table[1:]:
            band_list = []
            try:
                for col in row:
                    band_list.append(col.text_content().strip())
                band = models.Band()
                band.name = unicode(band_list[0])
                band.genre = unicode(band_list[1])
                band.origin = u"Progarchives"
                bands.append(band)
            except UnicodeDecodeError, e:
                print str(e)
            except UnicodeEncodeError, e:
                print str(e)
        return bands
    
    def save(self):
        pass