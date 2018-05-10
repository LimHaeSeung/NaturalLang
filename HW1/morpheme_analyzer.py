class TPtable:
    def __init__(self):
        self.morpheme = []
        self.part = []


class MorphemeAnalyzer:
    def __init__(self, morph_dict, morph_rule):
        self.dictionary = morph_dict
        self.rule = morph_rule

    def Analysis(self, sentence):
        words_list = sentence.split(' ')

        res_cnt = [0] * len(words_list)
        morphAnaly = [[] for cols in range(len(words_list))]

        for word_idx, word in enumerate(words_list):
            TpResulst = self.TabularParsing(word)

            for res in TpResulst:
                morph_list = res.morpheme.split('+')
                for part in res.part:
                    morphAnaly[word_idx].append('')
                    part_list = part.split('+')
                    for idx in range(len(morph_list)):
                        morphAnaly[word_idx][res_cnt[word_idx]] += morph_list[idx] + '/' + part_list[idx]
                        if idx != len(morph_list)-1:
                            morphAnaly[word_idx][res_cnt[word_idx]] += '+'

                    res_cnt[word_idx] = res_cnt[word_idx] + 1

        num_res = 1
        for cnt in res_cnt:
            num_res *= cnt
        Result = ['' for cols in range(num_res)]

        cnt = 0
        for idx in range(len(res_cnt)):
            for idx2 in range(num_res):
                Result[idx2] += morphAnaly[idx][idx2 % res_cnt[idx]]
                if idx != (len(res_cnt) - 1):
                    Result[idx2] += ' '

        return Result




    def SearchDict(self, morpheme):
        letter_list = list(morpheme)
        curnode = self.dictionary
        for letter in letter_list:
            if letter in curnode.child:
                curnode = curnode.child[letter]
            else:
                return False, []

        if curnode.leaf is True:
            return True, curnode.part
        else:
            return False, []


    def TabularParsing(self, word):
        TriTable = [[[] for cols in range(len(word))] for rows in range(len(word))]
        checkstart = [0] * len(word)

        for endidx in range(len(word)):
            for initidx in range(endidx, -1, -1):
                morph = word[initidx:endidx + 1]
                retval, parts = self.SearchDict(morph)
                if retval:
                    temp_TpInfo = TPtable()
                    temp_TpInfo.morpheme = word[initidx:endidx+1]
                    temp_TpInfo.part = parts
                    TriTable[initidx][endidx].append(temp_TpInfo)
                    #TriTable[initidx][endidx][0].morpheme = word[initidx:endidx+1]
                    #TriTable[initidx][endidx][0].part = parts
                    # print(TriTable[initidx][endidx][0].morpheme)

                for kk in range(checkstart[initidx], endidx):
                    for ii in range(len(TriTable[initidx][kk])):
                        for jj in range(len(TriTable[kk+1][endidx])):
                            rule_pass = False
                            temp_part = []
                            for left_part in TriTable[initidx][kk][ii].part:
                                for right_part in TriTable[kk+1][endidx][jj].part:
                                    checkLeft = left_part.split('+')[-1]
                                    checkRight = right_part.split('+')[0]
                                    if (checkRight in self.rule[checkLeft].Right) and (checkLeft in self.rule[checkRight].Left):
                                        rule_pass = True
                                        temp_part.append(left_part+'+'+right_part)

                            if rule_pass:
                                TpInfo = TPtable()
                                TpInfo.morpheme = TriTable[initidx][kk][ii].morpheme + '+' + TriTable[kk+1][endidx][jj].morpheme
                                TpInfo.part = temp_part
                                TriTable[initidx][endidx].append(TpInfo)
                                if endidx > checkstart[initidx]:
                                    checkstart[initidx] = endidx

                                #print(endidx, initidx, kk, ii, jj)
                                #print(checkstart)
                                #print(TpInfo.morpheme)

        #for TriData in TriTable[0][-1]:
        #    print(TriData.morpheme)
        #    print(TriData.part)
        return TriTable[0][-1]

