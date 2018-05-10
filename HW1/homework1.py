import trie_dict
import morpheme_rule
import morpheme_analyzer



if __name__ == '__main__':

    TrieDict = trie_dict.TrieDict()
    MorphRule = morpheme_rule.MorphemeRule()

    # 1-2 : Trie Dictionary
    f = open("morph_rule.txt", 'r')
    lines = f.read().splitlines()
    for line in lines:
        print(line)
        words_list = line.split(' ')

        for word in words_list:
            morpheme_list = word.split('+')

            parts = []
            for idx, morpheme in enumerate(morpheme_list):
                str_list = morpheme.split('/')
                morpheme = str_list[0]
                parts.append(str_list[1])

                TrieDict.insertMorpheme(morpheme, parts[idx])

            MorphRule.addRule(parts)
    f.close()

    # 1-2 : fprint dictionary
    TrieDict.printMorpheme()


    # 1-3 : Tabular Parsing
    Analyzer = morpheme_analyzer.MorphemeAnalyzer(TrieDict.dictionary, MorphRule.rule)

    f = open("input.txt", 'r')
    lines = f.read().splitlines()
    print()
    print('1-3.')
    for line in lines:
        print(line)
        Result = Analyzer.Analysis(line)

        for res in Result:
            print('-> ' + res)
    f.close()

