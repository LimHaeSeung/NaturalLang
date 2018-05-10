모든 function은 CKY_Parser라는 class에 구현되어 있습니다.

Grammar는 grammar.txt 파일에서 각 라인별로 Read한 후, addGrammar 함수를 통해 변수에 저장합니다.

CKY Parser는 문장을 Read한 후, Parser함수로 동작 수행합니다.
 - checkWord 함수는 각 단어별로 한번씩 동작하면서 품사를 찾음
 - Phrase grammar는 checkPhrase 함수로 확인
 - checkOnetoOne 함수는 과제의 Grammar에는 없지만, S -> VP 처럼 input이 하나인 경우를 위한 함수
