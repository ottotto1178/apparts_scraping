from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import re

url = 'https://unilife.co.jp/search/school/pref_id:33/school_id:10891/?page=1&equipment=55'
to_station_map = 'https://www.google.com/maps/dir//%E3%80%92700-0024+%E5%B2%A1%E5%B1%B1%E7%9C%8C%E5%B2%A1%E5%B1%B1%E5%B8%82%E5%8C%97%E5%8C%BA%E9%A7%85%E5%85%83%E7%94%BA%EF%BC%91%E2%88%92%EF%BC%91+%E5%B2%A1%E5%B1%B1%E9%A7%85/@34.6661868,133.8827141,13z/data=!3m1!4b1!4m9!4m8!1m0!1m5!1m1!1s0x3554064c3de389d3:0xa2d703aa2239cf57!2m2!1d133.9177335!2d34.6661212!3e2?authuser=0' #目的地を岡山駅に設定したGoogleマップの経路検索のURL
to_school_map = 'https://www.google.com/maps/dir//%E3%80%92700-0087+%E5%B2%A1%E5%B1%B1%E7%9C%8C%E5%B2%A1%E5%B1%B1%E5%B8%82%E5%8C%97%E5%8C%BA%E6%B4%A5%E5%B3%B6%E4%BA%AC%E7%94%BA%EF%BC%92%E4%B8%81%E7%9B%AE%EF%BC%91%EF%BC%90%E2%88%92%EF%BC%91+%E5%B2%A1%E5%B1%B1%E5%95%86%E7%A7%91%E5%A4%A7%E5%AD%A6/@34.6826986,133.8986422,17z/data=!4m17!1m7!3m6!1s0x355406f6b3dc2017:0x5e38a505d2cf8792!2z5bKh5bGx5ZWG56eR5aSn5a2m!8m2!3d34.6826942!4d133.9008309!16s%2Fm%2F04155fr!4m8!1m0!1m5!1m1!1s0x355406f6b3dc2017:0x5e38a505d2cf8792!2m2!1d133.9008309!2d34.6826942!3e2?authuser=0' #目的地を大学に設定したGoogleマップの経路検索のURL
driver_path = 'D:\chromedriver.exe'
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_experimental_option("excludeSwitches", ['enable-automation'])
service = Service(executable_path = driver_path)
driver = webdriver.Chrome(chrome_options = options, service = service)
driver.set_window_size('1200', '1000')

driver.get(url)
time.sleep(1)

appart_name = [] #各住居の名前
contents_link = [] #各住居のURL
rents = [] #各住居の家賃
addresses = [] #住所
nearest_stations = [] #最寄り駅
to_OkayamaStations = [] #岡山駅まで
to_schools = [] #学校までの距離
floors = [] #間取り
dedicated_equipments = [] #専用設備
common_eqipments = [] #共通設備

while True:
  contents = driver.find_elements(By.CLASS_NAME, 'ttlBox')
  title = '岡山商科大学の通学に便利な学生マンション一覧'
  confirmation_next_btn = driver.find_elements(By.XPATH, '//*[@id="conts"]/div[26]/div[3]/a')
  for i in range(len(contents)):
    if title in contents[i].text:
      continue
    elif contents[i].text in appart_name:
      continue
    else:
      appart_name.append(contents[i].text)
      contents_url = contents[i].get_attribute('href')
      contents_link.append(contents_url)
  if len(confirmation_next_btn) > 0:
    next_btn = driver.find_element(By.CLASS_NAME, 'nextBtn')
    next_btn.click()
    time.sleep(2)
  else:
    break

for i in range(len(contents_link)):
  print(i + 1)
  driver.get(contents_link[i])
  time.sleep(1)
  overview = driver.find_elements(By.CSS_SELECTOR, 'td > p')

  rent = driver.find_element(By.XPATH, '//*[@id="main"]/div[2]/div[2]/div/div/div[1]/div/table/tbody/tr[1]/td')
  rents.append(rent.text)

  un_shorted_address = overview[0].text
  pattern = '\u3000(.*)'
  address_group = re.search(pattern, un_shorted_address) #郵便番号を除いた住所を取得
  address = address_group.group(1)
  if '(1)' in address:
    address = address.split('(')[0]
    addresses.append(address)
  else:
    addresses.append(address)

  nearest_station = overview[1].text #最寄り駅までの情報を取得
  nearest_stations.append(nearest_station)

  floor = overview[2].text #間取りを取得
  floors.append(floor)

  if '年' in overview[7].text:
    dedicated_equipment = overview[8].text #専用設備の情報を取得
    dedicated_equipments.append(dedicated_equipment)
    common_eqipment = overview[9].text #共通設備の情報を取得
    common_eqipments.append(common_eqipment)
  else:
    dedicated_equipment = overview[7].text #専用設備の情報を取得
    dedicated_equipments.append(dedicated_equipment)
    common_eqipment = overview[8].text #共通設備の情報を取得
    common_eqipments.append(common_eqipment)

  driver.get(to_station_map)
  driver.implicitly_wait(3)
  input_btn = driver.find_element(By.CSS_SELECTOR, 'input')
  input_btn.send_keys(addresses[i])
  input_btn.send_keys(Keys.ENTER)
  to_OkayamaStation = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="section-directions-trip-0"]/div[1]/div[3]/div[1]/div[2]')))
  to_OkayamaStations.append(to_OkayamaStation.text)
  time.sleep(2)

  driver.get(to_school_map)
  driver.implicitly_wait(3)
  input_btn = driver.find_element(By.CSS_SELECTOR, 'input')
  input_btn.send_keys(addresses[i])
  input_btn.send_keys(Keys.ENTER)
  to_school = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="section-directions-trip-0"]/div[1]/div[3]/div[1]/div[2]')))
  to_schools.append(to_school.text)
  time.sleep(2)
  
driver.quit()

result = {
  '住居名' : appart_name,
  'url' : contents_link,
  '家賃' : rents,
  '住所' : addresses,
  '最寄り駅' : nearest_stations,
  '岡山駅までの距離' : to_OkayamaStations,
  '学校までの距離' : to_schools,
  '間取り' : floors,
  '専用設備' : dedicated_equipments,
  '共通設備' : common_eqipments
}

df = pd.DataFrame(result)
df.to_csv('apparts.csv', index = False, encoding = 'utf_8_sig')