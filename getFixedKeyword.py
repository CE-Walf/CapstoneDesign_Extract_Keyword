#셀레니움 관련 라이브러리
from selenium import webdriver
from selenium.webdriver.common.keys import Keys # Keys.RETURN, Keys.ENTER, Keys.TAB
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager # 웹 드라이버 자동 관리
from selenium.webdriver.chrome.options import Options # Selenium에 UserAgent, Headless Chrome의 사용을 위해 필요

import time # 동적 크롤링을 위한 time.sleep() 사용
def FixedKeywordCrawler():
    keyword_list = list()
    url = 'http://data.kostat.go.kr/social/keyword/index.do' # 통계정 경제 키워드

    # chromedriver 경로설정 및 option 설정진행
    chrome_options = Options()
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    chrome_options.add_argument('user-agent=' + user_agent)  # User-Agent 설정
    chrome_options.add_argument('--headless')  # Headless 모드 활성화
    chrome_options.add_argument('--disable-gpu')  # GPU 사용 비활성화 (Linux에서 필요한 경우)
    chromedriver = 'C:/dev_python/Webdriver/chromedriver.exe' #Chrome 위치. 나중에 수정.
    driver = webdriver.Chrome(service=Service(chromedriver), options=chrome_options)

    driver.get(url)
    time.sleep(4)

    # 상위 키워드 10개만 크롤링
    for i in range(1,11):
        keyword_elem = driver.find_element(By.XPATH, '//*[@id="text_{}"]'.format(i))
        keyword_list.append(keyword_elem.text)

    return keyword_list
