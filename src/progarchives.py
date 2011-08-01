import lxml.html
import lxml.html.soupparser
import lxml.etree
import dbmanager
import models

def is_hash_different(html_element, old_hash):
    html_element_string = lxml.html.tostring(html_element)
    new_hash = hash(html_element_string)
    return new_hash != old_hash


def save_entries(processed_table):
    bands = []
    band_list = []
    database = dbmanager.DBManager()
    for row in processed_table[1:]:
        band_list = []
        try:
            for col in row:
                band_list.append(col.text_content().strip())
            band = models.Band(name=band_list[0], genre=band_list[1], country=band_list[2])
            bands.append(band)
        except UnicodeDecodeError, e:
            print str(e)
        except UnicodeEncodeError, e:
            print str(e)
    print len(bands)
    database.save("bands", bands)


if __name__ == '__main__':
    parsed_page = lxml.html.parse(open('/Users/dgraziotin/Projects/iProtal/src/progarchives.html','r')).getroot()
    table = parsed_page.xpath("//table")[0]
    #save_entries(table)
    
    bands = dbmanager.DBManager().get("bands")
    for band in bands:
        print band.name.encode('utf-8')
    