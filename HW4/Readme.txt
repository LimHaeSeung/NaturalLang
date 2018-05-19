구현된 부분은

1. query_word에 대해서 word2id를 이용해 이를 id, 즉 정수형태로 저장
2. query_word의 학습된 embedding vector(128x1)값을 획득하고, 이를 50,000개의 data set과의 내적값으로 similarity 계산
3. 자신을 제외하고, similarity가 가장 높은 8개의 similarity와 해당 단어 출력

입니다.


text8 코퍼스의 출력결과는 50만번 학습의 결과
나무위키 코퍼스의 출력결과는 100만번 학습의 결과