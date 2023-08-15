#멀티 프로세싱을 시험해볼 장소입니다.
# 4코어로 진행해 보자.
#미완성

#라이브러리 import
import time  # time.sleep() for Crawling
from datetime import datetime # Chect runtime
import multiprocessing

#셀레니움 관련 라이브러리
from selenium import webdriver
from selenium.webdriver.common.keys import Keys # Keys.RETURN, Keys.ENTER, Keys.TAB
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager # 웹 드라이버 자동 관리
from selenium.webdriver.chrome.options import Options # Selenium에 UserAgent, Headless Chrome의 사용을 위해 필요

#GET MODULE
from crawlingArticle import crawlingTitleAndContents
from contentsToSentences import contentsToSentences
from getNounsFromSentences import getNounsInSentences
from buildWordsGraph import buildWordsGraph
from getRanks import getRanks
from keywords import keywords
from getFixedKeyword import FixedKeywordCrawler

#멀티 프로세싱은 전역변수를 공유하지 않는다.
# =================== 크롤링 진행 함수 ======================
def CrawlingFunction(i):


    for j in range(1,6):
        time_elem = driver.find_element(By.XPATH, '//*[@id="section_body"]/ul[' + str(i) + ']/li[' + str(j) + ']/dl/dd/span[3]')
        time.sleep(sleep_sec)
        article_time = time_elem.text
        if article_time == '4시간전':  # 1일전으로 설정
            escape_flag = True;
            break;
        #둘의 XPATH가 다름.
        try:  # 일반적인 경우(썸네일이 존재할때)
            article_elem = driver.find_element(By.XPATH, '//*[@id="section_body"]/ul[' + str(i) + ']/li[' + str(j) + ']/dl/dt[2]/a')
        except:  # 썸네일 미 존재시
            article_elem = driver.find_element(By.XPATH, '//*[@id="section_body"]/ul[' + str(i) + ']/li[' + str(j) + ']/dl/dt/a')
        time.sleep(sleep_sec)
        url = article_elem.get_attribute('href')  # 고른 기사의 네이버 뉴스 링크 추출

        #기사와
        title, contents = crawlingTitleAndContents(url)

        # ===아예 같은 제목이 존재하는 경우에는 크롤링을 하지 않도록 코드작성 필요===
        for duplicated_index in range(news_index):
            if news_dict[duplicated_index]['title'] == title:
                duplicated_flag = True

        if duplicated_flag:
            duplicated_flag = False
            continue

        # 제목과 본문을 합친다.
        news_contents = title + contents
        sentence = contentsToSentences(news_contents)
        nouns = getNounsInSentences(sentence)
        words_graph, idx2word = buildWordsGraph(nouns)
        word_rank_idx = getRanks(words_graph)
        sorted_word_rank_idx = sorted(word_rank_idx, key=lambda k: word_rank_idx[k], reverse=True)
        keyword_list = keywords(sorted_word_rank_idx, idx2word)

        # 키워드 순위 측정
        for keyword in keyword_list:
            if keyword in keyword_dict:
                keyword_dict[keyword] += 1
            else:
                keyword_dict[keyword] = 1

        news_dict[news_index] = {'title': title,
                                 'contents': contents,
                                 'keyword': keyword_list}

        news_index += 1
        if escape_flag:
            break;

#============================================찐 메인 함수============================================

if __name__ == '__main__':
    # 글로벌 함수 선언
    global driver
    global news_index

    # 고정 키워드를 크롤링
    print("======= 고정 키워드 크롤링을 시작합니다 =======")
    fixedKeyword = FixedKeywordCrawler()
    print(fixedKeyword)
    print("======= 고정 키워드 크롤링을 마칩니다. =======")

    # 어제의 일일 키워드 크롤링, 분석
    print("======= 어제의 일일 키워드 크롤링을 시작합니다 =======")
    print("코드 실행 시작 시간 : ", datetime.now())
    code_start = time.time() # 코드 최초 실행 시간

    # 헤더 설정 (이게 없으면 크롤링이 동작하지 않음)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}

    # 동적 크롤링을 위한 time.sleep, 0.5초로 설정 (전역변수로 사용하자.)
    sleep_sec = 0.5

    # 컨텐츠를 담을 빈 Dictionary, 인덱스
    news_dict = {}
    news_index = 0

    # 키워드의 순위를 지정할 리스트
    keyword_dict = dict()

    # 크롬 드라이버 위치를 입력(리눅스 서버에서 실행시 크롬 드라이버 설치 후 그 위치에 경로 설정)
    chromedriver = 'C:/dev_python/Webdriver/chromedriver.exe'

    # Headless Chrome 옵션 설정
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Headless 모드 활성화
    chrome_options.add_argument('--disable-gpu')  # GPU 사용 비활성화 (Linux에서 필요한 경우)

    driver = webdriver.Chrome(service=Service(chromedriver), options=chrome_options)

    # 반복문 탈출을 위한 flag 설정 (Flag는 전역변수로)
    escape_flag = False
    duplicated_flag = False

    #초기 페이지는 1페이지 설정
    page = 1
    while True:
        driver.get("https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=101#&date=%2000:00:00&page=" + str(page))  # 경제뉴스 페이지로 이동
        time.sleep(sleep_sec)

        pool = multiprocessing.Pool(processes=4)
        pool.map(CrawlingFunction, range(1, 5))  # 페이지 범위를 적절하게 수정하세요
        pool.close()
        pool.join()

        page += 1

    # End of Chrome Driver
    driver.quit()

    print(keyword_dict)
    sorted_data = sorted(keyword_dict.items(), key=lambda x: x[1], reverse=True)

    yesterdayKeyword = list()
    wordcloud_data = list()
    for item in sorted_data:
        yesterdayKeyword.append(item[0])
        if len(yesterdayKeyword) == 15:
            break

    for element in fixedKeyword:
        if element in yesterdayKeyword:
            yesterdayKeyword.remove(element)

    yesterdayKeyword = yesterdayKeyword[:10]

    for item in sorted_data:
        wordcloud_data.append([item[0], item[1]])
        if len(wordcloud_data) == 30:
            break

    for item in sorted_data:
        print(item[0], item[1])

    print("===고정 키워드====")
    print(fixedKeyword)
    print("===일일 키워드====")
    print(yesterdayKeyword)
    print("===워드 클라우드 사용 데이터====")
    print(wordcloud_data)

    #코드 종료 시간
    code_end = time.time()
    print("수행시간: %f 초" % (code_end - code_start))
    print("코드 실행 종료 시각 : ", datetime.now())

#==========================================찐 메인 함수 종료==========================================