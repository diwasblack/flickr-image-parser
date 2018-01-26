import sqlite3


conn = sqlite3.connect('flickr.db')


def get_url(per_page, page, city):
    '''
    Construct the URL
    '''

    API_KEY = '25085db99e01bb6230eedb4ec26f7f6d'

    url = 'https://api.flickr.com/services/rest?sort=relevance&parse_tags=1&content_type=7&extras=can_comment%2Ccount_comments%2Ccount_faves%2Cdescription%2Cisfavorite%2Clicense%2Cmedia%2Cneeds_interstitial%2Cowner_name%2Cpath_alias%2Crealname%2Crotation%2Curl_c%2Curl_l%2Curl_m%2Curl_n%2Curl_q%2Curl_s%2Curl_sq%2Curl_t%2Curl_z&per_page={}&page={}&lang=en-US&text={}&viewerNSID=&method=flickr.photos.search&csrf=&api_key={}&format=json&hermes=1&hermesClient=1&reqId=43c76475&nojsoncallback=1'.format(per_page, page, city, API_KEY)
    return url


def create_db():
    '''
    Creates a table if it does not exist
    '''

    conn = sqlite3.connect('flickr.db')
    c = conn.cursor()
    sql = 'create table if not exists photos (filename text, longitude text, latitude text)'
    c.execute(sql)
    conn.commit()
    conn.close()


def insert_into_db(row):
    '''
    Inserts a row into the photos table
    '''

    c = conn.cursor()
    sql = 'insert into photos values (?,?,?)'
    c.execute(sql, row)
    conn.commit()
