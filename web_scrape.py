import urllib.request as ul
from bs4 import BeautifulSoup as bs
import re
import xlsxwriter
import os

###Open URL
def open_url(url):
    try:
        pg = ul.urlopen(url).read()
        s = bs(pg,"lxml")
        return s
    except:
        return ("Page Not Found")

### Scrape data from redirected page
def next_page(str):

    s = open_url(str)
    if (s == "Page Not Found"):
        return ("NA")
    
    new_page_data = []
    tbody = s('div',{"class":"pest-header-content"})

    try:
        origin = tbody[0].find_all("strong")[1].next_sibling
        new_page_data.append(origin)
    except:
        try:
            tbody = s.find('div',{"id":"content_div_2393636"})
            para = tbody.find_all('p')

        except:
            tbody = s.find('div', {"id":"collapsefaq"})
            para = tbody.find_all('div')[13]
            identify_pest = para.find_all("strong")[2].next_sibling
            identify_pest1 = para.find_all("strong")[2].find_next_siblings("em")[0].text.strip()
            identify_pest2 = para.find_all("strong")[2].find_next_siblings("em")[0].next_sibling
            identify_pest3 = para.find_all("strong")[2].find_next_siblings("em")[1].text.strip()
            identify_pest4 = para.find_all("strong")[2].find_next_siblings("em")[1].next_sibling
            identify_pest = identify_pest + identify_pest1 +" "+ identify_pest2 +" "+ identify_pest3 +" "+ identify_pest4
            

            new_page_data.append("NA")
            new_page_data.append(identify_pest)
            new_page_data.append("NA")
            new_page_data.append("NA")
            return new_page_data

        origin = para[1].text.strip()
        new_page_data.append(origin)

        identify_pest = para[3].text.strip()+' '+para[4].text.strip()
        new_page_data.append(identify_pest)

        check_legal = para[5].text.strip()
        new_page_data.append(check_legal)

        new_page_data.append("NA")
        
        return new_page_data
    
    identify_pest = s.find('div',{"id":"collapsefaq"})
    i_p = identify_pest.find_all("div")[-3].text.strip()
    new_page_data.append(i_p)

    check_legal = identify_pest.find_all("div")[-2].text.strip()
    new_page_data.append(check_legal)

    s_a_s = identify_pest.find_all("div")[-1].text.strip()
    new_page_data.append(s_a_s)

    return new_page_data

#### Scrape data from redirected page
def diff_page(str):
    s = open_url(str)
    if s=="Page Not Found":
        return "NA"
    new_page_data = []
    try:
        tbody = s('table')[0].find_all('li')
    except:
        return "NA"
    identify_pest = [ele.text.strip() for ele in tbody]
    i_p = (',').join(identify_pest)
    return i_p

### For downloading the image to local directory
def img_download(link):
    directory = os.path.join(os.getcwd(),'images')
    if not os.path.exists(directory):
        os.makedirs(directory)
    image_name = link.split('/')[-1]
    ul.urlretrieve(link, directory+"\\"+image_name)
    return directory+"\\"+image_name
    
url = "http://www.agriculture.gov.au/pests-diseases-weeds/plant#identify-pests-diseases"
page = ul.urlopen(url).read()

a = bs(page,"lxml")

tbody = a('li', {"class":"flex-item"})

global r
r=0
c=0
workbook = xlsxwriter.Workbook('scrape_data.xlsx')
worksheet = workbook.add_worksheet()

worksheet.write('A1', 'Disease name')
worksheet.write('B1', 'Image link')
worksheet.write('C1', 'Origin')
worksheet.write('D1', 'See if you can identify the pest')
worksheet.write('E1', 'Check what can legally come into Australia')
worksheet.write('F1', 'Secure any suspect specimens')
  
for i in range(len(tbody)):
    r += 1
    row = []
    row.append(tbody[i].text.strip())
    a = tbody[i].find_all('a')
    img = tbody[i].find_all('img')
    img_link = url[:29]+img[0].get('src')
    img_link = img_download(img_link)
    row.append(img_link)
    str = url[:29]+a[0].get('href')

##### To check whether the redirected page belongs to the same domain name or not#####  
    x = re.search('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', a[0].get('href'))

    if not x:
        new_page = next_page(str)
        row.extend(new_page)
    else:
        d_f = diff_page(a[0].get('href'))
        row.append('NA')
        row.append(d_f)
        row.extend(['NA','NA'])  ## Inserting NA for missing data

##### Inserting the data to exel sheet #####
        
    c=0
    for col in row:
        worksheet.write(r,c,col)
        c+=1

workbook.close()
    

