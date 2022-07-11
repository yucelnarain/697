
import sys
import pandas as pd
import re
import os
import openpyxl
from xlsx2html import xlsx2html
import xlrd
import xlwings as xw
import html2text
import io
from xlsx2html import xlsx2html
import urllib.request


# %%
def download_pdfs(sample_number, original_excel_file, path_to_store_converted_excel, converted_excel_sheet_name, path_for_pdfs):
    """Specify the number of pdfs to download, excel file containing the url links, path for the new converted excel, 
    the sheet name you want to extract files from, and the path for where you want to store the downloaded pdfs which will be scraped from the sheet"""
    #Example command line execution: 
    # python pdf_download_script.py 
    # sample_number:5 
    # original_excel_file: 'DTMB_PRO-Contract-List.xls' 
    # path_to_store_converted_excel: '/Users/narainyucel/Google Drive/MADS/capstone/legal_nlp' 
    # converted_excel_sheet_name: 'Updated 06-16-2022' 
    # path_for_pdfs: '/Users/narainyucel/Google Drive/MADS/capstone/legal_nlp'


    #convert old xls to xlsx and split them into one xlsx per sheet, choose sheet with relevant information
    print('open is assigned to %r' % open)
    with xw.App(visible=False) as app:
        wb = app.books.open(original_excel_file)
        for sheet in wb.sheets:
            wb_new = app.books.add()
            sheet.copy(after=wb_new.sheets[0])
            wb_new.sheets[0].delete()
            if not os.path.isfile(path_to_store_converted_excel + f'/{sheet.name}.xlsx'):
                wb_new.save(path_to_store_converted_excel + f'/{sheet.name}.xlsx')
            wb_new.close()

    #Specify xlsx_name, based on the relevant sheet
    xlsx_file = open(path_to_store_converted_excel + f'/{converted_excel_sheet_name}.xlsx', 'rb') 
    out_file = io.StringIO()
    xlsx2html(xlsx_file, out_file, locale='en')
    out_file.seek(0)
    result_html = out_file.read()

    #Extract all links from the html 
    links = re.findall('"(https?://.*?)"', result_html)

    #Download pdfs needed
    DOWNLOADS_DIR = path_for_pdfs
    count = 0
    for url in links[:int(sample_number)]: 
        name = url.rsplit('/', 1)[-1]

        filename = os.path.join(DOWNLOADS_DIR, name)

        if not os.path.isfile(filename):
            try:
                urllib.request.urlretrieve(url, filename)
                count += 1
                print(count)
            except HTTPError as error:
                print(error.status, error.reason)
            except URLError as error:
                print(error.reason)
            except TimeoutError:
                print("Request timed out")
    return 
if __name__ == "__main__":
    download_pdfs(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])


