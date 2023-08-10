# 키워드를 뽑아내주는 함수
def keywords(sorted_word_rank_idx,idx2word,word_num=10):
    keywords = []
    index = []
    for idx in sorted_word_rank_idx[:word_num]:
        index.append(idx)

    # index.sort()
    for idx in index:
        keywords.append(idx2word[idx])

    return keywords