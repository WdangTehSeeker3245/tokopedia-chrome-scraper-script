import time
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

url = "https://www.tokopedia.com/search?st=product&q=handphone&srp_component_id=02.01.00.00&srp_page_id=&srp_page_title=&navsource="
# path = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome()
driver.get(url)

data = []

for i in range(2):
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#zeus-root")))
    time.sleep(3)

    for j in range(7):
        driver.execute_script("window.scrollBy(0,750)")
        time.sleep(1)

    driver.execute_script("window.scrollBy(50, 0)")
    time.sleep(1)

    soup = BeautifulSoup(driver.page_source,"html.parser")
    # print(soup)

    ##### Algoritma Scraping ######
    items = soup.findAll("div", class_="css-974ipl")
    for item in items:
        nama_produk = item.find("div", class_="css-3um8ox").text
        harga = item.find("div", class_="css-1ksb19c").text
        # print(nama_produk)
        # print(harga)
        tjl = item.findAll("span", class_="css-1duhs3e")
        if len(tjl) > 0:
            terjual = item.find("span", class_="css-1duhs3e").text
            # print(terjual)

        else :
            terjual=""
            # print(terjual)
        rtg = item.findAll("span", class_="css-t70v7i")
        if len(rtg) > 0 :
            rating = item.find("span", class_="css-t70v7i").text
            # print(rating)
  
        else:
            rating = ""
            # print(rating)

        for item2 in item.findAll("div", class_="css-1rn0irl"):
            lokasi = item2.findAll("span", class_="css-1kdc32b")[0].text
            toko = item2.findAll("span", class_="css-1kdc32b")[1].text
            # print(toko)
            # print(lokasi) 

            data.append(
                    (toko,lokasi,nama_produk,harga,terjual,rating)
            )        
             # print("=========")

    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR, "Button[aria-label='Laman berikutnya']").click()
    time.sleep(3)

df = pd.DataFrame(data, columns = ["toko","lokasi","nama_produk","harga","terjual","rating"])
print(df)

# saving to excel
df.to_excel("tokopedia-handphone-scraping-dataset.xlsx", index=False)
print("data telah tersimpan")


driver.close()