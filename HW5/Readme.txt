모든 function은 HMM_POS_Tagging class에 구현되어 있습니다.

함수 설명
CountMorphemes : unigram / bigram counting과 형태소 개수 counting
getProbability : unigram확률과 Laplace smoothing된 bigram 확률, 형태소의 observation probability 계산
		(이때, unkown word는 corpus내에서 한번 등장했다고 가정)

HMM_Probbility : 입력된 형태소 분석 결과이 HMM을 통과했을 때의 최종 확률값 계산 (log로 출력)


