import sys
import csv
import time
from bs4 import BeautifulSoup
from selenium import webdriver


def get_xml_data(source):
    """Gets tags given an XML source

    Parameters
    ----------
    source: object
        a XML page source

    Returns
    -------
    dictionary
        a python dictionary containing all tagnames as a key and a list of tags as value
        
    """

    file_data = {'nameOfIssuer':[], 'titleOfClass':[], 'cusip':[], 
                'value':[], 'sshPrnamt':[], 'sshPrnamtType':[], 
                'investmentDiscretion':[], 'Sole':[], 'Shared':[]}
    for header in file_data:
        file_data[header] = source.findAll(header)
    return file_data


def write_tsv_file(cik, page_source):
    """Writes a tab seperated .tsv file to disk

    Parameters
    ----------
    cik : str
        The CIK for the fund on EDGAR
    page_source : object
        An XML source file with which to get and write data from
    """

    output_filename = 'holdings_data_'+ cik + '.tsv'
    page_data = get_xml_data(page_source)
    data_len = len(page_data['nameOfIssuer'])

    with open(output_filename, 'wt') as holdings_data_file:
        tsv_file_writer = csv.writer(holdings_data_file, delimiter='\t')
        tsv_file_writer.writerow(page_data.keys())
        for i in range(data_len):
            row = [page_data['nameOfIssuer'][i].text, page_data['titleOfClass'][i].text, page_data['cusip'][i].text,
                    page_data['value'][i].text, page_data['sshPrnamt'][i].text, page_data['investmentDiscretion'][i].text,
                    page_data['Sole'][i].text, page_data['Shared'][i].text]
            tsv_file_writer.writerow(row)


def get_xml_page(driver):
    """Gets XML page source

    Parameters
    ----------
    driver : object
        A browser driver object to navigate webpage

    Returns
    -------
    object
        a XML page source
    """

    #find the 13F report document button and navigate to its page
    driver.find_element_by_xpath('//*[@id="documentsbutton"]').click()

    #get the XML page containing fund holdings
    driver.implicitly_wait(2) 
    keyword = "able.xml"
    links = driver.find_elements_by_partial_link_text(keyword)
    try:
        links[0].click()
    except:
        print('could not find info table')

    driver.implicitly_wait(2) 
    return BeautifulSoup(driver.page_source, 'xml')


def scrape_holdings(cik):
    url = "https://www.sec.gov/cgi-bin/browse-edgar?CIK="+cik.replace(" ", "")+"&owner=exclude&action=getcompany"
    driver = webdriver.Firefox(executable_path=r'./geckodriver')
    driver.get(url)

    xml_page_source = get_xml_page(driver)

    write_tsv_file(cik, xml_page_source)

    driver.quit()


def main():
    args1 = None
    try:
        args1 = sys.argv[1]
    except:
        print("give a ticker or CIK as an argument")

    try:
        args1 = sys.argv[1].split("|")
    except:
        args1 = sys.argv[1]

    if len(args1) > 1:
        cik = args1[1]
        scrape_holdings(cik)
    else:
        cik = args1[0]
        scrape_holdings(cik)


if __name__ == "__main__":
    main()