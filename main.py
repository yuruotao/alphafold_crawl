import pdb_preprocess as pdb_pre

import os
from selenium import webdriver
import numpy as np
import pandas as pd


def info_crawl(sequence, crawl_website, protein_num):
    import math
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service as ChromeService
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support import expected_conditions as EC
    
    if not os.path.exists('./web_driver'):
        os.mkdir('./web_driver')
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager(version="110.0.5481.77").install()))
    driver_path = './web_driver/chromedriver.exe'
    
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
    options.use_chromium = True
    
    driver = webdriver.Chrome(executable_path = driver_path, options=options)
    

    # calculate page number
    page_num = math.ceil(protein_num / 20)
    
    # crawl the website and document the data
    Uniprot_list = []
    Protein_list = []
    Gene_list = []
    Website_list = []
    
    # page
    for i in range(page_num):
        temp = []
        if i == 0:
            driver.get(crawl_website)
        else:
            driver.get(crawl_website + "&page=" + str(i+1))
        
        # locate the element 
        
        # get uniprot name
        elements = WebDriverWait(driver, 4).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.resultRightCol.columns.small-8.medium-10'))
        )
        for item in elements:
            temp.append(item.text)
        length = len(temp)

        for j in range(int(length/4)):
            Protein_list.append(temp[4*j])
            Gene_list.append(temp[4*j+1])
            Uniprot_list.append(temp[4*j+3].rstrip("go to UniProt"))
            Website_list.append("https://alphafold.ebi.ac.uk/files/AF-" + temp[4*j+3].rstrip("go to UniProt") + "-F1-model_v4.pdb")
            
        
    
    driver.close()
    # log data to file
    data_log(sequence, protein_num, Uniprot_list, Protein_list, Gene_list, Website_list)
    # download the protein to file
    protein_download(Website_list, sequence, protein_num)
    
    

# create folder and download the protein
def protein_download(download_website_table, biome_number, total_protein_number):
    import requests
    
    if not os.path.exists('./data/microbiome' + str(biome_number)):
        os.mkdir('./data/microbiome' + str(biome_number))
    
    file_name = []
    protein_name = 'b' + str(biome_number) + 'p'
    not_info_list = [
        "HEADER",
        "TITLE",
        "COMPND",
        "SOURCE",
        "REMARK",
        "DBREF",
        "SEQRES",
        "CRYST",
        "ORIGX",
        "SCALE",
        "MODEL",
        "ENDMDL"
    ]
    
    for i in range(total_protein_number):
        file_name.append(protein_name + str(i+1) + ".pdb")
        response = requests.get(download_website_table[i])
        
        open('./data/microbiome' + str(biome_number) + '/' + file_name[i], "wb").write(response.content)
        
        print("file " + str(file_name[i]) + " is downloaded")


def website_connect(website, data):
    return 
            
# debug done
def txt_read_to_list(microbiome_log):
    import re
    
    # opening the file in read mode
    microbiome_file = open(microbiome_log, "r")
    
    # reading the file
    microbiome_file_read = microbiome_file.read()
    
    file_data = microbiome_file_read.split("\n")
    file_length = int(len(file_data))

    file_data = [item.rsplit(' (', 1) for item in file_data]
    for i in range(file_length):
        file_data[i][1] =  int(file_data[i][1].rstrip(')'))

    microbiome_file.close()
    return file_data, file_length

def data_log(sequence, biome_num, Uniprot_list, Protein_list, gene_list, website_list):
    # create logging excels
    import xlsxwriter
    workbook = xlsxwriter.Workbook('./log/' + "biome" + str(sequence)  +'.xlsx')
    xlsx_path.append('./log/' + "biome" + str(sequence)  +'.xlsx')
    worksheet = workbook.add_worksheet('CK')

    row = 0
    col = 0
        
    worksheet.write(row, col, "Index")
    worksheet.write(row, col+1, "Uniprot")
    worksheet.write(row, col+2, "Protein")
    worksheet.write(row, col+3, "Gene")
    worksheet.write(row, col+4, "Website")
    worksheet.write(row, col+5, "Center")
    worksheet.write(row, col+6, "Box Size")
    worksheet.write(row, col+7, "Energy")

        
    for n in range(len(Uniprot_list)):
        worksheet.write(n + 1, col, n+1)
        worksheet.write(row + 1 + n, col + 1, Uniprot_list[n])
        worksheet.write(row + 1 + n, col + 2, Protein_list[n])
        worksheet.write(row + 1 + n, col + 3, gene_list[n])
        worksheet.write(row + 1 + n, col + 4, website_list[n])    

    workbook.close()

def total_log(microbiome_list, microbiome_specific_website_biome):
    import xlsxwriter
    workbook = xlsxwriter.Workbook('./log/total_log.xlsx')
    worksheet = workbook.add_worksheet()
    
    row = 0
    col = 0
    
    worksheet.write(row, col, "Index")
    worksheet.write(row, col+1, "Microbiome")
    worksheet.write(row, col+2, "Total")
    worksheet.write(row, col+3, "Website")
    
    for item, cost in (microbiome_list):
        worksheet.write(row+1, col, row+1 )
        worksheet.write(row+1, col+1,     item)
        worksheet.write(row+1, col + 2, cost)
        row += 1
    row = 0
    for item in (microbiome_specific_website_biome):
        worksheet.write(row+1, col + 3, item)
        row += 1
    
    workbook.close()
    
    

if __name__ == "__main__":
    alphafold_website = "https://alphafold.ebi.ac.uk/search/text/beta-D-glucoside%20glucohydrolase"
    
     # create directory
    if not os.path.exists('./log'):
        os.mkdir('./log')
    if not os.path.exists('./data'):
        os.mkdir('./data')
    
    pdb_file_dir = "./data/"
    pdb_log_dir = "./log/"
    
    microbiome_log = pdb_log_dir + "microbiome.txt"
    
    # create a list of microbiome
    microbiome_list, biome_num = txt_read_to_list(microbiome_log)
    microbiome_specific_website_biome = []
    
    # create a list of protein info xlsx path
    xlsx_path = []
    
    for i in microbiome_list:
        microbiome_specific_website_biome.append(alphafold_website + "?organismScientificName=" + i[0].replace(" ", "%20"))
        # microbiome_specific_website_biome contains the websites for each of the microbiome
        
    # create a total catalog containing the name, quantity, website of microbiomes
    # total_log(microbiome_list, microbiome_specific_website_biome)
    
    for k in range(99, 100, 1):
        info_crawl(k+1, microbiome_specific_website_biome[k], int(microbiome_list[k][1]))
        print(str(k+1) + " microbiome is finished")
        
    

    