import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from multiprocessing import Process
from multiprocessing import Pool


def propertyScan(parcel_major):
    df = pd.DataFrame(columns=['Property_ID',
                               'Taxpayer1',
                               'Taxpayer2',
                               'Taxpayer_Address',
                               'Property_Address',
                               'Use',
                               'Acres',
                               'Sale_Date',
                               'Sale_Price',
                               'PLSS',
                               'Title_Source',
                               'School_District',
                               'Watershed_District'])

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(
        executable_path='/usr/bin/chromedriver', options=chrome_options)

    for minor in range(0, 999):
        idsfound = 0
        for seq in range(0, 9999, 10):
            if((seq > 1000) and (idsfound == 0)):
                break

            if(seq % 1000 == 0):
                driver.close()
                driver = webdriver.Chrome(
                    executable_path='/usr/bin/chromedriver', options=chrome_options)
            parcelid = (parcel_major * 100000000) + (minor * 100000) + (seq)
            url = 'https://gis.co.carver.mn.us/publicparcel/?pin=' + \
                str("{0:09}".format(parcelid))
            driver.get(url)
            results = []
            content = driver.page_source

            soup = BeautifulSoup(content, features="html.parser")
            table = soup.find('table', attrs={'class': 'propDetails'})
            if(table):
                idsfound = idsfound + 1
                print(str("{0:09}".format(parcelid)) + " Found")

                d = table.find_all('td', attrs={'class': 'data'})
                l = table.find_all('td', attrs={'class': 'lable'})
                tp1 = ''
                tp2 = ''
                tpaddr = ''
                paddr = ''
                use = ''
                acres = ''
                saledate = ''
                saleprice = ''
                plss = ''
                titlesrc = ''
                school = ''
                watershed = ''
                if(d != [] and l != []):
                    for idx, item in enumerate(l):
                        stritem = item.text.strip()
                        if(stritem == "Taxpayer"):
                            tp1 = d[idx].text.strip()
                        elif(stritem == "Taxpayer 2"):
                            tp2 = d[idx].text.strip()
                        elif(stritem == "Taxpayer Address"):
                            tpaddr = d[idx].text.strip() + " " + \
                                d[idx+1].text.strip()
                        elif(stritem == "Property Address"):
                            paddr = d[idx].text.strip() + " " + \
                                d[idx+1].text.strip()
                        elif(stritem == "Use 1"):
                            use = d[idx].text.strip()
                        elif(stritem == "Mapped Acres"):
                            acres = d[idx].text.strip()
                        elif(stritem == "Last Sale Date"):
                            saledate = d[idx].text.strip()
                        elif(stritem == "Last Sale Price"):
                            saleprice = d[idx].text.strip()
                        elif(stritem == "PLSS"):
                            plss = d[idx].text.strip()
                        elif(stritem == "Title Source"):
                            titlesrc = d[idx].text.strip()
                        elif(stritem == "School District"):
                            school = d[idx].text.strip()
                        elif(stritem == "Watershed District"):
                            watershed = d[idx].text.strip()

                    df = df.append({'Property_ID': str(parcelid),
                                    'Taxpayer1': tp1,
                                    'Taxpayer2': tp2,
                                    'Taxpayer_Address': tpaddr,
                                    'Property_Address': paddr,
                                    'Use': use,
                                    'Acres': acres,
                                    'Sale_Date': saledate,
                                    'Sale_Price': saleprice,
                                    'PLSS': plss,
                                    'Title_Source': titlesrc,
                                    'School_District': school,
                                    'Watershed_District': watershed,
                                    }, ignore_index=True)
            else:
                print(str("{0:09}".format(parcelid)) + " NOT Found")

            filename = 'GIS_' + str(parcel_major) + '.csv'
            df.to_csv(filename, index=False, encoding='utf-8')

    driver.close()


if __name__ == "__main__":
    majid = int(input("Enter starting Parcel ID: "))
    propertyScan(majid)
