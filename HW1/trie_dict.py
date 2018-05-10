class NodeInfo:
    def __init__(self):
        self.child = dict()
        self.leaf = False
        self.part = []


class TrieDict:
    def __init__(self):
        self.dictionary = NodeInfo()

    def insertMorpheme(self, morpheme, part):
        letters = list(morpheme)
        curnode = self.dictionary
        for idx in range(len(letters)):
            if not self.checkExistLetter(curnode.child, letters[idx]):
                curnode.child[letters[idx]] = NodeInfo()

            curnode = curnode.child[letters[idx]]

            if idx == (len(letters)-1):
                curnode.leaf = True
                # check exist part of speech
                if part not in curnode.part:
                    curnode.part.append(part)


    def printMorpheme(self):
        f = open("morph_dict.txt", 'w')
        rootNode = self.dictionary
        letters = ''
        self.searchMorph(rootNode, letters, f)
        f.close()


    def searchMorph(self, curnode, prev_letters, file):
        if curnode.child == {}:
            return

        for idx, (letter, node) in enumerate(curnode.child.items()):
            morph = prev_letters + letter
            self.searchMorph(node, morph, file)

            if node.leaf is True:
                data = morph + ' '
                for pt in node.part:
                    data += '['+pt+']'
                data += '\n'
                file.write(data)
                # print(morph)


    def checkExistLetter(self, dict, letter):
        if letter in dict:
            retval = True
        else:
            retval = False

        return retval

