import json
import urllib2
import lxml.html

if __name__ == "__main__":
    # http://www.metal-archives.com/search/ajax-band-search/?field=name&query=*&sEcho=1&iDisplayStart=0
    base_url = 'http://www.metal-archives.com/search/ajax-band-search/?field=name&query=*&sEcho=1&iDisplayStart='

    idisplaystart = 0
    url = base_url + str(idisplaystart)
    
    json_file = urllib2.urlopen(url)
    json_string = json.load(json_file)

    itotalrecords =  int(json_string['iTotalRecords'])
    i = 0
    while i <= itotalrecords:
        print "---" * 12
        print "turn: " + str(i)
        print "---" * 12
        idisplaystart = i
        url = base_url + str(idisplaystart)
        try:
            json_file = urllib2.urlopen(url)
        except urllib2.HTTPError:
            print "HTTP error from metal-archives, recovering.."
            i = i - 100 # yes this is monkey patching
            break;
        json_string = json.load(json_file)
        bands_json = json_string[u'aaData']
        
        for band_json in bands_json:
            name = band_json[0]
            genre = band_json[1]
            tree = lxml.html.fromstring(name)
            name_html = tree.xpath("//a")[0]
            name = name_html.text_content()
            try:
                print name, genre
            except UnicodeDecodeError, e:
                pass
            except UnicodeEncodeError, e:
                pass
    
        i = i + 100        
        
