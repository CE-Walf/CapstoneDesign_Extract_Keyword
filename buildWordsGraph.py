from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import normalize
import numpy as np

#단어들간의 유사도 계산
def buildWordsGraph(sentence_noun):
    cnt_vec = CountVectorizer()
    cnt_vec_mat = normalize(cnt_vec.fit_transform(sentence_noun).toarray().astype(float), axis=0)
    vocab = cnt_vec.vocabulary_
    index2word = {idx: word.upper() for word, idx in vocab.items()}  # 단어를 대문자로 저장
    return np.dot(cnt_vec_mat.T, cnt_vec_mat), index2word