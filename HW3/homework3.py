import codecs
import math


class NodeInfo:
    def __init__(self):
        self.name = ''

class HMM_POS_Tagging:
    def __init__(self):
        self.morpheme_Cnt = dict()
        self.morpheme_Prob = dict()
        self.unigram_Cnt = dict()
        self.bigram_Cnt = dict()
        self.bigram_Prob = dict()
        self.NumVoca = 0

        self.unigram_Cnt['$'] = 0

    def CountMorphemes(self, input_word):
        if '+/' in input_word:
            input_word = input_word.replace('+', ';')
            input_word = input_word.replace(';/', '+/')
            morpheme_list = input_word.split(';')
        else:
            morpheme_list = input_word.split('+')

        prev_PoS = '$'
        self.unigram_Cnt['$'] += 1
        for morphemeInfo in morpheme_list:
            #print(data)
            if morphemeInfo[0] == '/':
                temp = morphemeInfo.split('/')
                morpheme = '/'
                PoS = temp[0]
            else:
                temp = morphemeInfo.split('/')
                morpheme = temp[0]
                PoS = temp[1]

            # Counting unigram
            if PoS not in self.unigram_Cnt:
                self.unigram_Cnt[PoS] = 1
            else:
                self.unigram_Cnt[PoS] += 1

            # Counting bigram
            if PoS not in self.bigram_Cnt:
                self.bigram_Cnt[PoS] = dict()
                self.bigram_Cnt[PoS][prev_PoS] = 1
            else:
                if prev_PoS not in self.bigram_Cnt[PoS]:
                    self.bigram_Cnt[PoS][prev_PoS] = 1
                else:
                    self.bigram_Cnt[PoS][prev_PoS] += 1

            # Counting Num of morpheme
            if morpheme not in self.morpheme_Cnt:
                self.morpheme_Cnt[morpheme] = dict()
                self.morpheme_Cnt[morpheme][PoS] = 1
                self.NumVoca += 1
            else:
                if PoS not in self.morpheme_Cnt[morpheme]:
                    self.morpheme_Cnt[morpheme][PoS] = 1
                    self.NumVoca += 1
                else:
                    self.morpheme_Cnt[morpheme][PoS] += 1

            prev_PoS = PoS


    def GenUnkownBigram(self):
        for key1 in self.unigram_Cnt:
            if key1 not in self.bigram_Cnt:
                self.bigram_Cnt[key1] = dict()

            for key2 in self.unigram_Cnt:
                if key2 not in self.bigram_Cnt[key1]:
                    self.bigram_Cnt[key1][key2] = 0


    def getProbability(self):
        self.GenUnkownBigram()

        # transition probability
        for key1 in self.bigram_Cnt:
            if key1 not in self.bigram_Prob:
                self.bigram_Prob[key1] = dict()

            for key2, val in self.bigram_Cnt[key1].items():
                # Laplace smoothing
                self.bigram_Prob[key1][key2] = (self.bigram_Cnt[key1][key2] + 1) / (self.unigram_Cnt[key2] + len(self.unigram_Cnt))

        # observation probability
        for key1 in self.morpheme_Cnt:
            if key1 not in self.morpheme_Prob:
                self.morpheme_Prob[key1] = dict()

            for key2, val in self.morpheme_Cnt[key1].items():
                self.morpheme_Prob[key1][key2] = self.morpheme_Cnt[key1][key2] / self.unigram_Cnt[key2]

        # unkown words
        self.morpheme_Prob['?UNK?'] = dict()
        for key1 in self.unigram_Cnt:
            self.morpheme_Prob['?UNK?'][key1] = 1 / self.unigram_Cnt[key1]


    def HMM_Probbility(self, input_word):
        if '+/' in input_word:
            input_word = input_word.replace('+', ';')
            input_word = input_word.replace(';/', '+/')
            morpheme_list = input_word.split(';')
        else:
            morpheme_list = input_word.split('+')

        logProb = 0
        prev_PoS = '$'
        for morphemeInfo in morpheme_list:
            if morphemeInfo[0] == '/':
                temp = morphemeInfo.split('/')
                morpheme = '/'
                PoS = temp[0]
            else:
                temp = morphemeInfo.split('/')
                morpheme = temp[0]
                PoS = temp[1]

            if morpheme not in self.morpheme_Prob:
                morpheme = '?UNK?'

            ObervProb = math.log(self.morpheme_Prob[morpheme][PoS])
            TransProb = math.log(self.bigram_Prob[PoS][prev_PoS])

            logProb += (ObervProb + TransProb)
            prev_PoS = PoS

        return logProb


if __name__ == '__main__':

    PoSTagger = HMM_POS_Tagging()

    f = codecs.open("train.txt", 'r')
    lines = f.read().splitlines()
    for line in lines:
        if '/' in line:
            train_words = line.split('\t')
            PoSTagger.CountMorphemes(train_words[1])

    PoSTagger.getProbability()
    f.close()

    f = codecs.open("result.txt", 'r')
    outfile = codecs.open("output.txt", 'w')
    TestText = f.read()
    lines = TestText.replace('\n\n', '\n').split('\n')

    prob_results = []
    morph_list = []
    start_flag = 0
    for line in lines:
        if '. ' in line:
            test_word = line.split('. ')
            if test_word[0] == ' 1':
                start_flag = 1
            morph_list.append(test_word[1])
            prob_results.append(PoSTagger.HMM_Probbility(test_word[1]))

        else:
            if start_flag == 1:
                maxidx = prob_results.index(max(prob_results))
                print(morph_list[maxidx])

                outfile.write(morph_list[maxidx] + '\n')

            start_flag = 0
            prob_results = []
            morph_list = []

    f.close()

