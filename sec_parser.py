import requests
from bs4 import BeautifulSoup as bs4
from lxml import html
import re
import pandas as panda

def main():
    cik_raw = raw_input("Please enter CIK: ")
    cik = validate_cik(cik_raw)
    file_type="13F-HR"
    print ("Parsing " + cik + "'s latest " + file_type)

    # Edgar search per fund-type and cik (set to only 13F-HR for now)
    search_results_soup = cik_lookup(cik, file_type) 
    filings_page_soup = get_filings_soup(search_results_soup)
    xml_soup = get_xml_soup(filings_page_soup)

    headers = populate_header(xml_soup)
    rows = populate_rows(xml_soup, headers)
    pd =  panda.DataFrame(data=rows,columns=headers)
    file_name = cik + '_' + file_type + '.tsv'
    pd.to_csv(file_name, sep='\t')
    print("Parsing Complete, Please check the folder")

def validate_cik(cik):
    cik
    if len(cik) is not 10:
        print("Please try again.")
        main()
    return cik

def cik_lookup(cik, file_type="13F-HR"):
    base_url = 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={}&type={}%25&dateb=&owner=include&start=0&count=10'
    search_results_soup = soup_from_url(base_url.format(cik, file_type))
    if search_results_soup.findAll(string='No matching CIK.'):
        print('Invalid. Please try another CIK')
        main()
    return search_results_soup

def get_filings_soup(soup):
    #Check if theres a documents button; If there isn't a documents button
    #than there are no 13F Forms for this company
    url = soup.find('a', {'id' : 'documentsbutton'})
    if url:
        form_url = 'http://www.sec.gov' + url['href']
        filings_page_soup = soup_from_url(form_url)
    else:
        print('There are no 13F-HR for this company')
        main()
    return filings_page_soup

def get_xml_soup(soup):
    #Get the SEC Accession No. Add .txt to it and go to that url.  
    #*.txt format is always "Accession No".txt
    sec_text = soup.find('div', {'id' : 'secNum'}).text
    acc_no_url = sec_text.split(" ")[3].replace("\n", "") + ".txt"
    xml_url = 'http://www.sec.gov' + soup.find('a', text=acc_no_url)['href']
    xml_soup = soup_from_url(xml_url, 'xml')
    return xml_soup

def populate_header(soup):
    for table in soup.find_all('infoTable'):
        headers = []
        for line in table.findChildren():
            if check_line_validity(line):
                headers.append(line.name)
    return headers

def populate_rows(soup, headers):
    rows = []
    # Iteratre through the whole infoTable and iterate through the list headers
    # to find the appropriate row of information. 
    for table in soup.find_all('infoTable'):
        row = []
        for column in headers:
            row.append(table.find(column).text)
        rows.append(row)
    return rows

def check_line_validity(soup_line):
    return False if soup_line.string is None else True

def soup_from_url(url, parse_type='html.parser'):
    resp = requests.get(url)
    resp_str = resp.text
    resp_soup = bs4(resp_str, parse_type)
    return resp_soup

if __name__ == "__main__":
    main()