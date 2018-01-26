import unittest
from unittest import mock
from helpers import create_db, get_url
from tasks import parse_gps


class TestHelperMethods(unittest.TestCase):
    def test_is_table_created(self):
        result = create_db('test.db')
        self.assertEqual(result, 1)

    def test_is_proper_url(self):
        url = get_url(100, 1, 'new york')
        expected_url = 'https://api.flickr.com/services/rest?sort=relevance&parse_tags=1&content_type=7&extras=can_comment%2Ccount_comments%2Ccount_faves%2Cdescription%2Cisfavorite%2Clicense%2Cmedia%2Cneeds_interstitial%2Cowner_name%2Cpath_alias%2Crealname%2Crotation%2Curl_c%2Curl_l%2Curl_m%2Curl_n%2Curl_q%2Curl_s%2Curl_sq%2Curl_t%2Curl_z&per_page=100&page=1&lang=en-US&text=new+york&viewerNSID=&method=flickr.photos.search&csrf=&api_key=25085db99e01bb6230eedb4ec26f7f6d&format=json&hermes=1&hermesClient=1&reqId=43c76475&nojsoncallback=1'
        self.assertEqual(url, expected_url)


class TestParseMethods(unittest.TestCase):
    @mock.patch('tasks.insert_into_db', return_value=1)
    def test_parse_gps(self, mocked_insert_into_db):
        photo_json = {"owner": "parismadrid", "id": "4114141113", "filename": "asasd"}
        self.assertEqual(parse_gps(photo_json), 1)


if __name__ == '__main__':
    unittest.main()
