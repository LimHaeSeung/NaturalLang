class ConnectInfo:
    def __init__(self):
        self.Left = []
        self.Right = []

class MorphemeRule:
    def __init__(self):
        self.rule = dict()

    def addRule(self, part_list):
        for idx, part in enumerate(part_list):
            if part not in self.rule:
                self.rule[part] = ConnectInfo()

            if idx > 0:
                leftpart = part_list[idx-1]
                if leftpart not in self.rule[part].Left:
                    self.rule[part].Left.append(leftpart)

            if idx < len(part_list)-1:
                rightpart = part_list[idx+1]
                if rightpart not in self.rule[part].Right:
                    self.rule[part].Right.append(rightpart)

