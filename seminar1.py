from avl import BinaryNode, BinaryTree
from model import ActorsData

def parseLine(line):
    tokens = line.strip().split("\t")
    return ActorsData(int(tokens[0]), tokens[1], tokens[2])
    
def createBinaryTree (inputFile):
    bt = BinaryTree()
    file = open(inputFile, "r")
    for line in file:
        a = parseLine(line)
        bt.add(a.shortName, a)
    return bt

if __name__ == '__main__':

    bt = createBinaryTree("actors10.txt")
    actorsList = (bt.find("Irving Aaronson"))
    for a in actorsList:
        print (a.actorsData)
        
    print (bt)
    print (bt.height())
    print (bt.minimum())
    print (bt.maximum())
