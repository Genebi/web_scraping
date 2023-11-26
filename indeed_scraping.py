import requests
from bs4 import BeautifulSoup as bs
import re
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
import validators
import search_jobs as sj

# If you have an issue related to undetected_chromedriver go to undetected_chromedriver module
# and edit line 799 more or less in file __init__.py and put the time.sleep(0.1) inside a try-except

# This line about SSL is required to work properly on Mac OS
# if you are working on Windows can comment this line
ssl._create_default_https_context = ssl._create_unverified_context


if __name__ == '__main__':
    
    what_job = None
    location = None
    
    match len(sys.argv):
        case 1:
            print("Es necesario pasar el trabajo a buscar como argumento.\nEjemplo: 'Python'")
            exit()
        case 2:
            what_job = sys.argv[1]
        case 3:
            what_job = sys.argv[1]
            location = sys.argv[2]
    
    # URL as argument
    url = sj.search_and_get_url(what_job, location)
    
    if validators.url(url):

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
            
            # If salary is not public we jump next job
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
            
        
        # Create DataFrame
        df = pd.DataFrame(
                {
                    "Empleo": titles, 
                    "Salario": salaries,
                    "Empresa": companies,
                    "Link": links 
                }
            )
        
        
        now = datetime.now()
        date_string = now.strftime('%Y%m%d')
        time_string = now.strftime('%H%M%S')
        now = f"{date_string}_{time_string}"
        
        with pd.ExcelWriter('vacantes_indeed_'+ now +'.xlsx', engine='openpyxl') as writer:
            
            df.to_excel(writer, sheet_name='Sheet1', index=False)

            workbook = writer.book
            worksheet = writer.sheets['Sheet1']

            # Columns width
            width_measures = [40, 40, 40, 130]
            
            for col_num, value in enumerate(df.columns.values, 1):
                column_letter = chr(64 + col_num)
                worksheet.column_dimensions[column_letter].width = width_measures[col_num - 1]
                
        print("Terminando proceso...")
    
    else:
        print("El formato de la URL no es válido.")
        