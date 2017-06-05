"""
    AVL Implementation of Binary Tree.
    
    
    Subclasses can override key methods for customizing methods in 
    BinaryTree (newNode) and BinaryNode (newNode, compareTo). For now,
    these support standard <= and >= semantics 
    
"""
from model import ActorsData

class BinaryNode:

    def __init__ (self, value = None, actorsData = None):
        """Create binary node."""
        self.value  = value #key
        self.left   = None
        self.right  = None
        self.height = 0
        self.actorsData = actorsData
        self.numberOfLeftRotations = 0
        self.numberOfRightRotations = 0
        
        
    def computeHeight (self):
        """Compute height of node in BST."""
        height = -1
        if self.left:
            height = max(height, self.left.height)
        if self.right:
            height = max(height, self.right.height)
            
        self.height = height + 1

    def dynamicHeight (self):
        """Compute height of node in BST."""
        height = -1
        if self.left:
            height = max(height, self.left.dynamicHeight())
        if self.right:
            height = max(height, self.right.dynamicHeight())
            
        return height + 1

    def dynamicHeightDifference (self):
        """Compute height difference of node's children in BST."""
        leftTarget = 0
        rightTarget = 0
        if self.left:
            leftTarget = 1 + self.left.dynamicHeight()
        if self.right:
            rightTarget = 1 + self.right.dynamicHeight()
            
        return leftTarget - rightTarget

    def heightDifference (self):
        """Compute height difference of node's children in BST."""
        leftTarget = 0
        rightTarget = 0
        if self.left:
            leftTarget = 1 + self.left.height
        if self.right:
             rightTarget = 1 + self.right.height
                   
        return leftTarget - rightTarget

    def assertAVLProperty (self):
        """Validate AVL property for BST node."""
        if abs(self.dynamicHeightDifference()) > 1:
            return False
        if self.left:
            if not self.left.assertAVLProperty():
                return False
        if self.right:
            if not self.right.assertAVLProperty():
                return False

        return True

    def rotateRight (self):
        """Perform right rotation around given node."""
        self.numberOfRightRotations += 1
        newRoot = self.left
        grandson = newRoot.right
        self.left = grandson
        newRoot.right = self

        self.computeHeight()
        
        return newRoot

    def rotateLeft (self):
        """Perform left rotation around given node."""
        self.numberOfLeftRotations += 1
        newRoot = self.right
        grandson = newRoot.left
        self.right = grandson
        newRoot.left = self
    
        self.computeHeight()
        return newRoot

    def rotateLeftRight (self):
        """Perform left, then right rotation around given node."""
        self.numberOfRightRotations += 1
        self.numberOfLeftRotations += 1
        child = self.left
        newRoot = child.right
        grand1  = newRoot.left
        grand2  = newRoot.right
        child.right = grand1
        self.left = grand2
    
        newRoot.left = child
        newRoot.right = self
    
        child.computeHeight()
        self.computeHeight()
        
        return newRoot

    def rotateRightLeft (self):
        """Perform right, then left rotation around given node."""
        self.numberOfRightRotations += 1
        self.numberOfLeftRotations += 1
        child = self.right
        newRoot = child.left
        grand1  = newRoot.left
        grand2  = newRoot.right
        child.left = grand2
        self.right = grand1
    
        newRoot.left = self
        newRoot.right = child
    
        child.computeHeight()
        self.computeHeight()
      
        return newRoot

    def compareTo (self, value):
        """
        Returns 0 if equal, negative if smaller and positive if greater.
        Suitable for overriding.
        """
        if self.value == value:
            return 0
        if self.value < value:
            return -1
        return +1
        
    def add (self, val, actorsData):
        """Adds a new node to BST with value and rebalance as needed."""
        newRoot = self

        # if val <= self.value        
        if self.compareTo(val) >= 0:
            self.left = self.addToSubTree (self.left, val, actorsData)
            if self.heightDifference() == 2:
                #if val <= self.left.value:
                
                if self.left.compareTo(val) >= 0:
                    newRoot = self.rotateRight()
                else:
                    newRoot = self.rotateLeftRight()
        else:
            self.right = self.addToSubTree (self.right, val, actorsData)
            if self.heightDifference() == -2:
                #if val > self.right.value:
                if self.right.compareTo(val) < 0:
                    newRoot = self.rotateLeft()
                else:
                    newRoot = self.rotateRightLeft()

        newRoot.computeHeight()
        return newRoot

    def newNode (self, val, actorsData):
        """Return new Binary Node, amenable to subclassing."""
        return BinaryNode(val, actorsData)

    def addToSubTree (self, parent, val, actorsData):
        """Add val to parent subtree (if exists) and return root in case it has changed because of rotation."""
        if parent is None:
            return self.newNode(val, actorsData)

        parent = parent.add(val, actorsData)
        return parent
           
    def removeFromParent (self, parent, val):
        """Helper method for remove. Ensures proper behavior when removing node that 
        has children."""
        if parent:
            return parent.remove(val)
        return None

    def remove (self, val):
        """
         Remove val from BinaryTree. Works in conjunction with remove
         method in BinaryTree.
        """
        newRoot = self
        rc = self.compareTo(val)
        if rc == 0:
            if self.left is None:
                return self.right

            child = self.left
            while child.right:
                child = child.right
            
            childKey = child.value;
            self.left = self.removeFromParent(self.left, childKey)
            self.value = childKey;

            if self.heightDifference() == -2:
                if self.right.heightDifference() <= 0:
                    newRoot = self.rotateLeft()
                else:
                    newRoot = self.rotateRightLeft()
        elif rc > 0:
            self.left = self.removeFromParent(self.left, val)
            if self.heightDifference() == -2:
                if self.right.heightDifference() <= 0:
                    newRoot = self.rotateLeft()
                else:
                    newRoot = self.rotateRightLeft()
        else:
            self.right = self.removeFromParent(self.right, val)
            if self.heightDifference() == 2:
                if self.left.heightDifference() >= 0:
                    newRoot = self.rotateRight()
                else:
                    newRoot = self.rotateLeftRight()

        newRoot.computeHeight()
        return newRoot

    def __repr__ (self):
        """Useful debugging function to produce linear tree representation."""
        leftS = ''
        rightS = ''
        if self.left:
            leftS = str(self.left)
        if self.right:
            rightS = str(self.right)
        return "(L:" + leftS + " " + str(self.value) + " R:" + rightS + ")"

    def inorder (self):
        """In order traversal generator of tree rooted at given node."""
        if self.left:
            for n in self.left.inorder():
                yield n

        yield self.value

        if self.right:
            for n in self.right.inorder():
                yield n

class BinaryTree:

    def __init__ (self):
        """Create empty binary tree."""
        self.root = None

    def __repr__ (self):
        if self.root is None:
            return "avl:()"
        return "avl:" + str(self.root)
                
    def newNode (self, value, actorsData):
        """Return new BinaryNode object. Suitable for overriding."""
        return BinaryNode(value, actorsData)
    
    def add (self, value, actorsData):
        """Insert value into proper location in Binary Tree."""
        if self.root is None:
            self.root = self.newNode(value, actorsData)
        else:
            self.root = self.root.add(value, actorsData)

    def __contains__ (self, target):
        """Check whether BST contains target value."""
        node = self.root
        while node:
            rc = node.compareTo(target)
            if rc > 0:
                node = node.left
            elif rc < 0:
                node = node.right
            else:
                return True
            
                
        return False

    def remove (self, val):
        """Remove value from tree."""
        if self.root:
            self.root = self.root.remove(val)

    def __iter__ (self):
        """In order traversal of elements in the tree."""
        if self.root:
            return self.root.inorder()
                        
    def assertAVLProperty (self):
        """Validate AVL property for BST Tree."""
        if self.root:
            return self.root.assertAVLProperty()
        else:
            return True

    def find(self, key):
        listOfNodes = list()
        if key[-1] == "*":
            key = key[0:-1]
            self.find_in_subtree_wildcard (self.root, key, listOfNodes )
        else:
            self.find_in_subtree (self.root, key, listOfNodes )
        return listOfNodes
    
    def find_in_subtree (self,  node, key, listOfNodes):
        if node is None:
            return None  # key not found
        if key < node.value:
            return self.find_in_subtree(node.left, key, listOfNodes)
        elif key > node.value:
            return self.find_in_subtree(node.right, key, listOfNodes)
        else:  # key is equal to node key
            listOfNodes.append(node)
            self.find_in_subtree_wildcard(node.left, key, listOfNodes)
            self.find_in_subtree_wildcard(node.right, key, listOfNodes)
        
    def find_in_subtree_wildcard (self,  node, key, listOfNodes):
        
        if node is None:
            return None  # key not found
        lengthOfkey = len(key)
        tempNodeValue = node.value[0:lengthOfkey]
        if key < tempNodeValue:
            return self.find_in_subtree_wildcard(node.left, key, listOfNodes)
        elif key > tempNodeValue:
            return self.find_in_subtree_wildcard(node.right, key, listOfNodes)
        else:  # key is equal to node key
            listOfNodes.append(node)
            self.find_in_subtree_wildcard(node.left, key, listOfNodes)
            self.find_in_subtree_wildcard(node.right, key, listOfNodes)

    def height(self):
        return self.findHeight(self.root)
    
    def findHeight(self, aNode):
        if aNode is None:
            return -1

        lefth = self.findHeight(aNode.left)
        righth = self.findHeight(aNode.right)

        if lefth > righth:
            return lefth + 1
        else:
            return righth + 1

    def minimum(self):
        current = self.root
        while current.left is not None:
            current = current.left
        return current

    def maximum(self):
        current = self.root
        while current.right is not None:
            current = current.right
        return current

    def numberOfRightRotations (self):
        return self.rightRotations(self.root)

    def numberOfLeftRotations (self):
        return self.leftRotations(self.root)
    
    def rightRotations (self, node):
        if node is None:
            return 0

        return self.rightRotations(node.left) + self.rightRotations(node.right) + node.numberOfRightRotations

    def leftRotations (self, node):
        if node is None:
            return 0

        return self.leftRotations(node.left) + self.leftRotations(node.right) + node.numberOfLeftRotations

    def printNodeInRange(self, key1, key2):
        if key1[-1] == "*":
            key1 = key1[0:-1]
        if key2[-1] == "*":
            key2 = key2[0:-1] 
        self.inorderForKeys(self.root, key1, key2)
        
    def inorderForKeys(self, root, k1, k2):
        """if not k1 > root.value:
            self.inorderForKeys(root.left,k1,k2)
        if k1 < root.value and k2 > root.value:
            print (root.value)
        if not k2 < root.value:
            self.inorderForKeys(root.right,k1,k2)"""
        ans = []
        if root is None:
            return ans
        queue = [root]
        index = 0
        while index < len(queue):
            if queue[index] is not None:
                if queue[index].value[0:len(k1)] >= k1 and \
                    queue[index].value[0:len(k2)] <= k2:
                    ans.append(queue[index].value)

                queue.append(queue[index].left)
                queue.append(queue[index].right)

            index += 1
        ans = sorted(ans)
        f = open("temp.txt", "w")
        f.write(str(ans))
        f.close()
        
      
"""
Change Log
----------
2014.05.23     removeFromParent
               defect:    elif value < parent.val:
               fix:       elif value < parent.value

2014.06.16     added inorder iterator capability to allow 'for x in bt'
2015.05.18     updated to python 3.0 with timeit
2015.05.19     added ability to override core methods.
"""
