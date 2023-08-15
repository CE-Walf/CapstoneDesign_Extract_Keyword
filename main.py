# Import Module
from Fixed_Extract_Keyword import FixedKeywordCrawler
from Day_Extract_Keyword import DayKeywordCrawler

# Import Python Library
from datetime import datetime
import time

# 코드 실행 시간 확인 (시작)
start_time = datetime.now()
code_start = time.time()
print("=> 코드 실행 시각 : ", start_time)
print('\n')

# 고정 키워드를 추출
# Python list 형태로 10개의 고정 키워드를 추출한다 (통계청 - 뉴스기반검색 경제 키워드 이용)
print("======= 고정 키워드 크롤링을 시작합니다 =======")
fixedKeyword = FixedKeywordCrawler()
print("- 고정 키워드")
print(fixedKeyword)
print("======= 고정 키워드 크롤링을 마칩니다. =======")
print('\n')


# 어제의 일일 키워드를 추출, 분석
# 일일 키워드는, 고정 키워드와 비교해, 고정키워드에 나온 키워드는 제외하고 상위 10개를 추출하게 됩니다.
# 워드 클라우드를 만들기 위한 데이터는, 빈도수 상위 30개를 가져옵니다.
print("======= 어제의 일일 키워드 크롤링을 시작합니다 =======")
dayKeyword, wordcloudData = DayKeywordCrawler()


print("- 어제의 일일 키워드")
print(dayKeyword)
print("- 워드 클라우드 사용 데이터")
print(wordcloudData)
print("======= 어제의 일일 키워드 크롤링을 마칩니다. =======")
print('\n')


# 코드 실행 시간 확인 (종료)
code_end = time.time()
end_time = datetime.now()
print("=> 코드 실행 종료 시각 : ", end_time)
print("수행시간: %f 초" % (code_end - code_start))