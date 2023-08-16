# 키워드를 뽑아내주는 함수
def keywords(sorted_word_rank_idx,idx2word,word_num=10):
    keywords = []
    index = []
    for idx in sorted_word_rank_idx[:word_num]:
        index.append(idx)

    for idx in index:
        keywords.append(idx2word[idx])

    # 명확하지 않은 단어는, keyword로 나오지 않게 한다.
    notInKeyword = ['1월', '2월', '3월' '4월', '5월', '6월', '7월', '8월', '9월', '10월', '11월', '12월',
                    '50년', '이전', '홈페이지', '장기', '성장', '개발', '최근', '분석', '재고', '점검', '제보',
                    '적용', '참여', '기업', '만기', '요즘', '혐의', '감소', '부회장', '정비', '직원', '기존', '제공',
                    '현장', '가입', '대상', '식품', '가처분', '기술', '자금', '채소', '것으로', '공정', '세수', '사망',
                    '개월', '책임', '건축', '금융', '관광객', '계약', '진행', '개정', '증권사', '제품', '부담', '부문',
                    '인상', '작년', '원리금', '생산', '그룹', '이익', '개인', '설명', '공모', '지수', '이날', '비중',
                    '사기', '신고', '경험', '규모', '성장률', '지원', '노력', '수익률', '실적', '중단', '라며', '가구',
                    '관련', '슈퍼', '회복', '당국', '영업', '증권', '전년', '가운데', '확대',
                    '신규', '노선', '공사', '상품', '요금', '취급', '하락', '물량', '강화', '시작', '예정', '검토', '내부통제',
                    '투자자', '기조', '경우', '수령', '브랜드', '디폴트', '국내', '기대', '횡령', '이사', '구조', '추진', '설계',
                    '시장', '급여', '출시', '대표', '발생', '급등', '이후', '공개', '위안', '전지', '누락', '신청자', '고급', '시설',
                    '지난달', '사진', '사직서', '수의', '상승', '거래', '신청', '지급', '유통', '경제', '업계', '상환', '이달', '전관',
                    '시중', '관계자', '연구원', '임기', '센터', '외국인', '조정', '소재', '교수', '증가', '올해', '최대', '동결', '의원',
                    '예측', '지난해', '추가', '결과', '연령', '가상', '세계', '매수', '개선', '공급', '전력', '차량', '박스', '사과', '기간',
                    '인하', '솔루션', '목표', '국민', '반영', '물가', '방사', '사고', '중국인', '전체', '중개', '주택', '증편', '기록', '우려',
                    '영향', '부족', '지분', '제보', '수준', '제한', '기준', '회사', '문제', '수주', '법인', '산업', '강세', '둔화', '신형',
                    '정부', '계획', '평균', '여행', '전기', '재정', '활용', '감리', '부진', '사업', '전환', '방송', '생각', '프로', '지속',
                    '병조', '수익', '확보', '수요', '경영', '일시', '수요자', '환율', '때문', '안정', '업체', '침체', '매장', '경쟁', '은행',
                    '하반기',
                    '시스템', '회장', '상황', '현지', '상반기', '적발', '증여', '사장', '한화', '택배', '관리', '수급', '전망', '사용량', '소비',
                    '연장',
                    '가격', '임원', '정책', '위원회', '상장', '국채', '만원', '지역', '예상', '고객', '단체', '주도', '국제', '관광', '소득', '승주',
                    '배추',
                    '상온', '경기', '완화', '종목', '발표', '해외', '지주', '기업인', '대비', '내년', '평가', '사면', '가계', '보수', '매출',
                    '공장', '판매', '금액', '유커', '위기', '피해', '일부', '회의', '손실', '담보', '필요', '기차', '사용', '순위', '뉴시스', '건설',
                    '부품', '모델', '분기', '광고', '양가', ]

    # 들어가면 안될 단어를 리스트에서 제거
    for notKeyword in notInKeyword:
        if notKeyword in keywords:
            keywords.remove(notKeyword)

    return keywords