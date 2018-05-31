import json


filename = "NEtaggedCorpus_test.json"
outfile = "NEtaggedCorpus_test.txt"

with open(filename, 'r', encoding='utf-8-sig') as json_file:
    with open(outfile, 'w', encoding='utf-8-sig') as CoNLL_file:
        json_data = json.load(json_file)

        for sentence in json_data['sentence']:
            NER_labels = dict()
            for NER in sentence['NE']:
                NER_labels[NER['begin']] = 'B-' + NER['type']
                for id_idx in range(NER['begin']+1, NER['end']+1):
                    NER_labels[id_idx] = 'I-' + NER['type']

            for morph in sentence['morp']:
                outdata = morph['lemma'] + '/' + morph['type']
                if morph['id'] in NER_labels:
                    outdata = outdata + ' ' + NER_labels[morph['id']]
                else:
                    outdata = outdata + ' ' + 'O'

                CoNLL_file.write(outdata+'\n')

            CoNLL_file.write('\n')