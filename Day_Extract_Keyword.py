# Import Library
import time  # time.sleep() for Crawling
from datetime import datetime # Chect runtime
from konlpy.tag import Komoran # Komoran 형태소 분석기

# About Selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys # Keys.RETURN, Keys.ENTER, Keys.TAB
from selenium.webdriver.common.by import By # Search Element
from selenium.webdriver.chrome.service import Service # Chrome 경로 설정
from webdriver_manager.chrome import ChromeDriverManager # 웹 드라이버 자동 관리
from selenium.webdriver.chrome.options import Options # Selenium에 UserAgent, Headless Chrome

#GET MODULE
from crawlingArticle import crawlingTitleAndContents
from contentsToSentences import contentsToSentences
from getNounsFromSentences import getNounsInSentences
from buildWordsGraph import buildWordsGraph
from getRanks import getRanks
from keywords import keywords

# Extract Day Keyword
def DayKeywordCrawler():

    print("어제의 키워드 크롤링 코드 실행 시작 시간 : ", datetime.now())

    # 동적 크롤링을 위한 time.sleep, 0.5초로 설정
    sleep_sec = 0.5

    # 컨텐츠를 담을 빈 Dictionary, 인덱스
    news_dict = {}
    news_index = 0

    # 키워드의 순위를 지정할 리스트
    keyword_dict = dict()

    # 뉴스 개수를 세는 변수
    newsCount = 0

    # Komoran 형태소 분석기 사용자 사전 추가
    komoran = Komoran(userdic='user_dictionary.txt')

    #크롬 드라이버 위치를 입력(리눅스 서버에서 실행시 크롬드라이버 설치 후 그 위치에 경로 설정)
    chromedriver = 'C:/dev_python/Webdriver/chromedriver.exe'

    # Headless Chrome 옵션 설정
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Headless 모드 활성화
    chrome_options.add_argument('--disable-gpu')  # GPU 사용 비활성화 (Linux에서 필요한 경우)

    driver = webdriver.Chrome(service=Service(chromedriver), options=chrome_options)

    # 반복문 탈출을 위한 flag 설정
    escape_flag = False
    duplicated_flag = False

    page = 1
    while True:
        driver.get("https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=101#&date=%2000:00:00&page=" + str(
            page))  # 경제뉴스 페이지로 이동
        time.sleep(sleep_sec)
        for i in range(1, 5):
            for j in range(1, 6):
                time_elem = driver.find_element(By.XPATH, '//*[@id="section_body"]/ul[' + str(i) + ']/li[' + str(
                    j) + ']/dl/dd/span[3]')
                time.sleep(sleep_sec)
                article_time = time_elem.text
                print(article_time)
                if article_time == '4시간전':  # 1일전으로 설정
                    escape_flag = True;
                    break;
                try:  # 일반적인 경우(썸네일이 존재할때)
                    article_elem = driver.find_element(By.XPATH, '//*[@id="section_body"]/ul[' + str(i) + ']/li[' + str(
                        j) + ']/dl/dt[2]/a')
                except:  # 썸네일 미존재시
                    article_elem = driver.find_element(By.XPATH, '//*[@id="section_body"]/ul[' + str(i) + ']/li[' + str(
                        j) + ']/dl/dt/a')
                time.sleep(sleep_sec)
                url = article_elem.get_attribute('href')  # select한 기사의 네이버 제휴 url 추출
                title, contents = crawlingTitleAndContents(url)
                # ===아예 같은 제목이 존재하는 경우에는 크롤링을 하지 않도록 코드작성 필요===
                for duplicated_index in range(news_index):
                    if news_dict[duplicated_index]['title'] == title:
                        duplicated_flag = True

                if duplicated_flag:
                    duplicated_flag = False
                    continue
                ##===========여기까지========##

                # 제목과 본문을 합친다.
                news_contents = title + contents
                sentence = contentsToSentences(news_contents)
                nouns = getNounsInSentences(komoran, sentence)
                words_graph, idx2word = buildWordsGraph(nouns)
                word_rank_idx = getRanks(words_graph)
                sorted_word_rank_idx = sorted(word_rank_idx, key=lambda k: word_rank_idx[k], reverse=True)
                keyword_list = keywords(sorted_word_rank_idx, idx2word)
                newsCount += 1

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
        if escape_flag:
            break;
        time.sleep(sleep_sec)
        page += 1
    #End of While

    # Quit Chrome Driver
    driver.quit()

    # 많은 기사에 나온 순서대로 keyword_dict을 내림차순으로 정렬
    sorted_data = sorted(keyword_dict.items(), key=lambda x: x[1], reverse=True)

    # 어제의 일일 키워드, 워드클라우드를 사용하기위한 데이터를 담을 리스트
    yesterdayKeyword = list()
    wordcloud_data = list()

    # 상위 15개만 담기.
    for item in sorted_data:
        yesterdayKeyword.append(item[0])
        if len(yesterdayKeyword) == 15:
            break

    # 워드클라우드 ["부동산" 31] 이런 형태로 30개정도 뽑아, append
    for item in sorted_data:
        wordcloud_data.append([item[0], item[1]])
        if len(wordcloud_data) == 30:
            break

    print("======= 어제의 일일 키워드 크롤링을 종료합니다 =======")
    print("어제의 키워드 크롤링 코드 실행 종료 시간 : ", datetime.now())

    return yesterdayKeyword, wordcloud_data, newsCount