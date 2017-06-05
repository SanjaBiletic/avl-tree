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

    bt = createBinaryTree("actors100K.txt")
    print ("--------------------------------------------")
    actorsList = (bt.find("Irving Aaronson"))
    for a in actorsList:
        print (a.actorsData)
        
    print ("Height for tree is:", bt.height())
    print ("Minimum is:", bt.minimum().actorsData)
    print ("Maximum is:", bt.maximum().actorsData)

    print ("Number of right rotations is:", bt.numberOfRightRotations())
    print ("Number of left rotations is:", bt.numberOfLeftRotations())

    bt.printNodeInRange("Cer*", "Cor*")
    print ("Please look temp.txt for range search results")
    
