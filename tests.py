#!/usr/bin/env python3

import requests
import unittest

BASE_URL= "http://test.loc/"
BASE_APP_URL = BASE_URL + "app/"

class APPTestCase(unittest.TestCase):
    def test_base_url(self):
        response = requests.get(BASE_URL)
        # status code must be 200
        self.assertEqual(response.status_code, 200, "Unexpected status code")
        # body must be Hello from base index.html
        self.assertEqual(response.text.strip(), "Hello from base index.html")
        # no redirects
        self.assertFalse(response.history, "There are redirects")

    def test_app_direct_html(self):
        response = requests.get(BASE_APP_URL + "index.html")
        # status code must be 200
        self.assertEqual(response.status_code, 200, "Unexpected status code")
        # body must be Hello from base index.html
        self.assertEqual(response.text.strip(), "Hello from app/index.html")
        # no redirects
        self.assertFalse(response.history, "There are redirects")

    def test_app_direct_file(self):
        response = requests.get(BASE_APP_URL + "file.txt")
        # status code must be 200
        self.assertEqual(response.status_code, 200, "Unexpected status code")
        # body must be Hello from base index.html
        self.assertEqual(response.text.strip(), "Hello from app/file.txt")
        # no redirects
        self.assertFalse(response.history, "There are redirects")
        
    def test_app_url_without_slash(self):
        # Must be redirect to http://test.loc/app => http://test.loc/app/fr/
        # add load the app/fr/index.html
        # remove slash from url
        BASE_APP_URL_WO_SLASH = BASE_APP_URL[:-1]
        response = requests.get(BASE_APP_URL_WO_SLASH)
        # status code must be 200
        self.assertEqual(response.status_code, 200, "Unexpected status code")
        # body must be Hello from base index.html
        self.assertEqual(response.text.strip(), "Hello from app/fr/index.html")
        # new url must be
        self.assertEqual(response.url, BASE_APP_URL + "fr/")
        # Check if there is exactly one redirection and it's a 302
        self.assertEqual(len(response.history), 1, "There should be exactly one redirection")
        self.assertEqual(response.history[0].status_code, 302, "Redirection should be a 302")

    def test_app_url_with_slash(self):
        # Must be redirect to http://test.loc/app/ => http://test.loc/app/fr/
        # add load the app/fr/index.html
        response = requests.get(BASE_APP_URL)
        # status code must be 200
        self.assertEqual(response.status_code, 200, "Unexpected status code")
        # body must be Hello from base index.html
        self.assertEqual(response.text.strip(), "Hello from app/fr/index.html")
        # new url must be
        self.assertEqual(response.url, BASE_APP_URL + "fr/")
        # Check if there is exactly one redirection and it's a 302
        self.assertEqual(len(response.history), 1, "There should be exactly one redirection")
        self.assertEqual(response.history[0].status_code, 302, "Redirection should be a 302")

    def test_app_url_with_slash_with_en_lang_header(self):
        # add lang header with en
        # Must be redirect to http://test.loc/app/ => http://test.loc/app/en/
        # add load the app/en/index.html
        headers = {'Accept-Language': 'en'}
        response = requests.get(BASE_APP_URL, headers=headers)
        # status code must be 200
        self.assertEqual(response.status_code, 200, "Unexpected status code")
        # body must be Hello from base index.html
        self.assertEqual(response.text.strip(), "Hello from app/en/index.html")
        # new url must be
        self.assertEqual(response.url, BASE_APP_URL + "en/")
        # Check if there is exactly one redirection and it's a 302
        self.assertEqual(len(response.history), 1, "There should be exactly one redirection")
        self.assertEqual(response.history[0].status_code, 302, "Redirection should be a 302")

    def test_app_url_with_different_lang_in_url_than_in_header(self):
        # add lang header with en
        # http://test.loc/app/en/ must not be redirected
        # add load the app/fr/index.html
        headers = {'Accept-Language': 'fr'}
        response = requests.get(BASE_APP_URL + "en/", headers=headers)
        # status code must be 200
        self.assertEqual(response.status_code, 200, "Unexpected status code")
        # body must be Hello from base index.html
        self.assertEqual(response.text.strip(), "Hello from app/en/index.html")
        # new url must be
        self.assertEqual(response.url, BASE_APP_URL + "en/")
        # no redirects
        self.assertFalse(response.history, "There are redirects")

    def test_app_url_without_lang_but_subpath(self):
        # call to http://test.loc/app/dashboard => http://test.loc/app/fr/dashboard
        # add load the app/fr/index.html
        response = requests.get(BASE_APP_URL + "/dashboard")
        # status code must be 200
        self.assertEqual(response.status_code, 200, "Unexpected status code")
        # body must be Hello from base index.html
        self.assertEqual(response.text.strip(), "Hello from app/fr/index.html")
        # new url must be
        self.assertEqual(response.url, BASE_APP_URL + "fr/dashboard")
        # Check if there is exactly one redirection and it's a 302
        self.assertEqual(len(response.history), 1, "There should be exactly one redirection")
        self.assertEqual(response.history[0].status_code, 302, "Redirection should be a 302")

    def test_app_url_without_lang_but_lang_header_but_subpath(self):
        # call to http://test.loc/app/dashboard => http://test.loc/app/en/dashboard with 'Accept-Language': 'en'
        # add load the app/en/index.html
        headers = {'Accept-Language': 'en'}
        response = requests.get(BASE_APP_URL + "/dashboard", headers=headers)
        # status code must be 200
        self.assertEqual(response.status_code, 200, "Unexpected status code")
        # body must be Hello from base index.html
        self.assertEqual(response.text.strip(), "Hello from app/en/index.html")
        # new url must be
        self.assertEqual(response.url, BASE_APP_URL + "en/dashboard")
        # Check if there is exactly one redirection and it's a 302
        self.assertEqual(len(response.history), 1, "There should be exactly one redirection")
        self.assertEqual(response.history[0].status_code, 302, "Redirection should be a 302")

    def test_app_url_without_lang_but_lang_header_but_subpath(self):
        # call to http://test.loc/app/fr/dashboard
        # no redirect
        # add load the app/en/index.html
        headers = {'Accept-Language': 'en'}
        response = requests.get(BASE_APP_URL + "fr/dashboard", headers=headers)
        # status code must be 200
        self.assertEqual(response.status_code, 200, "Unexpected status code")
        # body must be Hello from base index.html
        self.assertEqual(response.text.strip(), "Hello from app/fr/index.html")
        # new url must be
        self.assertEqual(response.url, BASE_APP_URL + "fr/dashboard")
        # no redirects
        self.assertFalse(response.history, "There are redirects")


if __name__ == "__main__":
    unittest.main()