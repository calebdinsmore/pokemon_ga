# pylint disable=C
"""Experimenting with decision tree idea"""

class DecisionTree(object):
    def __init__(self, data="", operator="", left=None, right=None):
        self.operator = operator
        self.left = left
        self.right = right
        self.isLeaf = False
        if left == None and right == None:
            self.isLeaf = True
        self.data = data

    def perform_if(self, input):
        ifString = "%s %s %s" % (input, self.operator, self.data)

        if eval(ifString):
            if not self.right.isLeaf:
                print("right-dec")
                #self.right.perform_if("3")
            else:
                print("right-if")
        else:
            if not self.left.isLeaf:
                print("left-if")
            else:
                print("left-dec")

dl = DecisionTree("d")
dr = DecisionTree("c")

dt = DecisionTree("4", ">", dl, dr)

dt.perform_if("5")
