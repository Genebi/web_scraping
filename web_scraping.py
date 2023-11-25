import requests
from bs4 import BeautifulSoup as bs
import random
from datetime import datetime
import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import undetected_chromedriver as uc
from openpyxl import Workbook
import sys
import ssl

# La linea del SSL es necesaria para la ejecucion en MacOs
ssl._create_default_https_context = ssl._create_unverified_context

# El error que tenia con undetected_chromedriver lo solucione editando 
# el archivo __init__.py en la linea 799 agregué el try-except

if __name__ == '__main__':
    
    url = sys.argv[1] # Tomamos la URL pasada como argumento
    
    browser = uc.Chrome(use_subprocess=True)
    browser.get(url)
    browser.implicitly_wait(10);

    html = browser.page_source
    soup = bs(html, 'html.parser')

    browser.close()
    browser.quit()

    #########################################################
    
    jobs = soup.find_all('td', {'class':'resultContent'})
    
    titles = []
    links = []
    companies = []
    salaries = []

    for job in jobs:
        
        # Si no tiene salario especificado nos saltamos al siguiente
        if job.find('div', {'class':'salary-snippet-container'}) == None:
            continue
        
        title = job.find('h2', {'class':'jobTitle'}).text.strip()
        link = job.find('a', {'class':'jcs-JobTitle'}).attrs['href']
        link = 'https://mx.indeed.com' + link
        company = job.find('span', {'data-testid':'company-name'}).text.strip()
        salary = salary = job.find('div', {'class':'salary-snippet-container'}).text.strip()
        salary = salary.replace('Hasta', '').replace('por mes', '').replace('por hora', '').replace('a', '-')

        
        titles.append(title)
        links.append(link)
        companies.append(company)
        salaries.append(salary)
        
    
    # Creamos el dataframe
    df = pd.DataFrame(
            {
                "Empleo": titles, 
                "Salario": salaries,
                "Empresa": companies,
                "Link": links 
            }
        )
    
    # df.to_excel("vacantes_indeed.xlsx", sheet_name="Sheet1", engine="xlsxwriter", index=False)
    
    now = datetime.now()
    date_string = now.strftime('%Y%m%d')
    time_string = now.strftime('%H%M%S')
    now = f"{date_string}_{time_string}"
    
    # Crea un writer del excel de pandas usando XlsxWriter como motor
    with pd.ExcelWriter('vacantes_indeed_'+ now +'.xlsx', engine='openpyxl') as writer:
        # Escribimos el dataframe al excel
        df.to_excel(writer, sheet_name='Sheet1', index=False)

        # Accede al XlsxWriter workbook y los objectos worksheet
        workbook = writer.book
        worksheet = writer.sheets['Sheet1']

        # Ancho de las columnas
        width_measures = [40, 40, 40, 130]
        
        for col_num, value in enumerate(df.columns.values, 1):
            column_letter = chr(64 + col_num)
            worksheet.column_dimensions[column_letter].width = width_measures[col_num - 1]
            
    print("Terminando proceso...")
        