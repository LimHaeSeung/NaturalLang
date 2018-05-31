import json


# filename = "NEtaggedCorpus_test.json"
# outfile = "NEtaggedCorpus_test.txt"

# filename = "./distribution2016/train.json"
# outfile = "train.txt"

filename = "./distribution2016/dev.json"
outfile = "dev.txt"



with open(filename, 'r', encoding='utf-8-sig') as json_file:
    with open(outfile, 'w', encoding='utf-8-sig') as CoNLL_file:
        json_data = json.load(json_file)

        for sentence in json_data['sentence']:
            # NE labeling 필요한 morpheme을 dictionary에 저장
            NE_labels = dict()
            for NE in sentence['NE']:
                NE_labels[NE['begin']] = 'B-' + NE['type']
                for id_idx in range(NE['begin']+1, NE['end']+1):
                    NE_labels[id_idx] = 'I-' + NE['type']

            for morph in sentence['morp']:
                outdata = morph['lemma'] + '/' + morph['type']
                if morph['id'] in NE_labels:        # NE check
                    outdata = outdata + ' ' + NE_labels[morph['id']]
                else:
                    outdata = outdata + ' ' + 'O'

                CoNLL_file.write(outdata+'\n')

            CoNLL_file.write('\n')
