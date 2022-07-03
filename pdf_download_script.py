
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
def download_pdfs(sample_num ,excel_file, converted_excel_output_directory, xlsx_name, pdf_path):
    """Specify the number of pdfs to download, excel file containing the url links, path for the converted excel, 
    and the path for where you want to store the downloaded pdfs which will be scraped from the converted excel"""
    #convert old xls to xlsx and split them into one xlsx per sheet, choose sheet with relevant information
    with xw.App(visible=False) as app:
        wb = app.books.open(excel_file)
        for sheet in wb.sheets:
            wb_new = app.books.add()
            sheet.copy(after=wb_new.sheets[0])
            wb_new.sheets[0].delete()
            if not os.path.isfile(converted_excel_output_directory + f'/{sheet.name}.xlsx'):
                wb_new.save(converted_excel_output_directory + f'/{sheet.name}.xlsx')
            wb_new.close()

    #Specify xlsx_name, based on the relevant sheet
    xlsx_file = open(xlsx_name, 'rb') 
    out_file = io.StringIO()
    xlsx2html(xlsx_file, out_file, locale='en')
    out_file.seek(0)
    result_html = out_file.read()

    #Extract all links from the html 
    links = re.findall('"(https?://.*?)"', result_html)

    #Download pdfs needed
    DOWNLOADS_DIR = pdf_path
    count = 0
    for url in links[:int(sample_num)]: 
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
# %%
if __name__ == '__main__':
    download_pdfs(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
# %%
