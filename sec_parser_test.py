from bs4 import BeautifulSoup
import pytest
import requests
from sec_parser import *


def test_validate_cik_return_type():
    test_input = "0001166559"
    assert type(validate_cik(test_input)) is str

def test_cik_lookup_return_type():
    test_cik = "0001166559"
    test_file_type="13F-HR"
    assert type(cik_lookup(test_cik, test_file_type)) is bs4

def test_soup_from_url_return_type():
    url = 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={}&type={}%25&dateb=&owner=include&start=0&count=10'
    assert type(soup_from_url(url)) is bs4

def test_populate_headers_return_type():
    test_url = 'https://www.sec.gov/Archives/edgar/data/1166559/000110465918068485/0001104659-18-068485.txt'
    test_soup = soup_from_url(test_url, 'xml')
    assert type(populate_header(test_soup)) is list

def test_populate_rows_return_type():
    test_url = 'https://www.sec.gov/Archives/edgar/data/1166559/000110465918068485/0001104659-18-068485.txt'
    test_soup = soup_from_url(test_url, 'xml')
    headers = populate_header(test_soup)
    assert type(populate_rows(test_soup, headers)) is list