import json
import urllib2

if __name__ == "__main__":
    # http://www.metal-archives.com/search/ajax-band-search/?field=name&query=*&sEcho=1&iDisplayStart=0
    base_url = 'http://www.metal-archives.com/search/ajax-band-search/?field=name&query=*&sEcho=1&iDisplayStart='

    idisplaystart = 0
    url = base_url + str(idisplaystart)
    
    json_file = urllib2.urlopen(url)
    json_string = json.load(json_file)

    itotalrecords =  int(json_string['iTotalRecords'])

    print itotalrecords

    """for i in range(0, itotalrecords, 100):
        idisplaystart = i
        url = base_url + str(idisplaystart)
        print url"""

    url = base_url + str(idisplaystart)