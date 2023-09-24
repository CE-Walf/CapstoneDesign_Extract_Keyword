# CapstoneDesign_Extract_Keyword
캡스톤 디자인 HDAM 팀 - 어제의 경제 키워드 추출 부분 코드

ver.1

주피터 노트북에서 작업한 내용을 파이썬 파일로 옮겨, 각각의 부분을 임시로 모듈화.

ver. 1.1

Headless Chrome 구현

ver. 1.2

불필요한모듈 SumTitleAndContents 제거

ver. 2

고정 키워드 크롤링 코드 추가(통계청-뉴스기반통계검색)


ver. 2.1

상위 10개의 일일 키워드를 뽑아내는 변수 추가.(상위 15개를 뽑고 고정 키워드와 겹치는 경우 제거)

워드클라우드 사용을 위해 나온 단어 상위 30개 리스트 형태 [키워드, 나온 수]로 뽑아 오기 

ver. 3

조금 더 세밀하게 모듈화 (가시성을 높히기 위한), 몇개의 기사를 이용 하였는지 여부 추가

ver. 3.1

komoran 형태소 분석기에 사용자 정의 사전 추가, 키워드 미포함 리스트 추가 


TEST BRANCH - Multi Thread
멀티쓰레드 구현

ver. 4.0

멀티 쓰레드 구현을 main 브랜치에 merge


ver. 4.1

키워드 추출 소문자의 경우 대문자로 나오게끔 수정



고정 키워드 참조 : http://data.kostat.go.kr/social/keyword/index.do (통계청-뉴스기반통계검색)

코드 참조 : https://excelsior-cjh.tistory.com/93

불용어 참조 : https://raw.githubusercontent.com/yoonkt200/FastCampusDataset/master/korean_stopwords.txt 에 필요없는 불용어 추가