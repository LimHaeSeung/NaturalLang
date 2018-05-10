import codecs


class NodeInfo:
    def __init__(self):
        self.name = ''
        self.child = []


class CKY_Parser:
    def __init__(self, file):
        self.grammar = dict()
        self.outfile = file

    def addGrammar(self, input):
        if '->' in input:
            grammar_list = input.split('->')
            grammar_list[0] = grammar_list[0].strip()
            grammar_list[1] = grammar_list[1].strip()
            out_part = grammar_list[0]
            in_part = grammar_list[1]

            if in_part not in self.grammar:
                self.grammar[in_part] = [out_part]
            else:
                self.grammar[in_part].append(out_part)

            # print(input)


    def Parser(self, sentence):
        sentence = sentence.strip('.')
        word_list = sentence.split(' ')
        TriTable = [[[] for cols in range(len(word_list))] for rows in range(len(word_list))]
        self.rootNode = NodeInfo()

        for endidx in range(len(word_list)):
            for initidx in range(endidx, -1, -1):
                if initidx == endidx:
                    node = NodeInfo()
                    node.name = word_list[endidx]
                    self.checkWord(node, TriTable[initidx][endidx])

                else:
                    for kk in range(initidx, endidx):
                        for left_node in TriTable[initidx][kk]:
                            for right_node in TriTable[kk+1][endidx]:
                                self.checkPhrase(left_node, right_node, TriTable[initidx][endidx])


        print('최종 파스트리:')
        self.outfile.write('최종 파스트리:\n')
        for result in TriTable[0][-1]:
            outdata = ''
            if result.name == 'S':
                outdata = self.outTree(result, outdata)
                print(outdata)
                self.outfile.write(outdata + '\n')

        self.outfile.write('\n')
        print('')

    def outTree(self, node, outdata):
        # print(node.name)
        if len(node.child) != 0:
            outdata += '(' + node.name + ' '
            for curnode in node.child:
                outdata = self.outTree(curnode, outdata)

            outdata += ')'

        else:
            outdata += node.name

        return outdata


    def checkWord(self, node, table_data):
        if node.name in self.grammar:
            for res in self.grammar[node.name]:
                foutdata = res + ' -> ' + node.name
                print(foutdata)
                self.outfile.write(foutdata + '\n')

                for res2 in self.grammar[res]:
                    next_node = NodeInfo()
                    next_node.child = [node]
                    next_node.name = res2
                    foutdata = next_node.name + ' -> ' + res
                    print(foutdata)
                    self.outfile.write(foutdata + '\n')

                table_data.append(next_node)
                self.checkWord(next_node, table_data)

        else:
            return


    def checkPhrase(self, left_node, right_node, table_data):
        node_combi = left_node.name + ' ' + right_node.name
        if node_combi in self.grammar:
            for res in self.grammar[node_combi]:
                next_node = NodeInfo()
                next_node.child = [left_node, right_node]
                next_node.name = res
                table_data.append(next_node)

                foutdata = next_node.name + ' -> ' + node_combi
                print(foutdata)
                self.outfile.write(foutdata + '\n')
                self.checkOnetoOne(next_node, table_data)

        else:
            return


    def checkOnetoOne(self, node, table_data):
        if node.name in self.grammar:
            for res in self.grammar[node.name]:
                next_node = NodeInfo()
                next_node.child = [node]
                next_node.name = res
                table_data.append(next_node)

                foutdata = next_node.name + ' -> ' + node.name
                print(foutdata)
                self.outfile.write(foutdata + '\n')

        else:
            return




if __name__ == '__main__':

    outfile = codecs.open("output.txt", 'w')
    CKY = CKY_Parser(outfile)

    # read grammar
    f = codecs.open("grammar.txt", 'r', 'utf-8-sig')
    lines = f.read().splitlines()
    for line in lines:
        CKY.addGrammar(line)

    f = codecs.open("input.txt", 'r', 'utf-8-sig')
    lines = f.read().splitlines()
    for line in lines:
        print(line)
        CKY.Parser(line)
    f.close()

    outfile.close()
