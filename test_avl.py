import unittest

from avl import BinaryTree
import random

class TestAVLMethods(unittest.TestCase):

    def setUp(self):
        self.bst = BinaryTree()
        
    def tearDown(self):
        self.bst = None
        
    def test_adding_and_removing(self):
        vals = []
        for _ in range(20):
            n = random.randint(1,1000)
            vals.append(n)
            if not n in self.bst:
                self.bst.add(n)
                self.assertTrue(self.bst.assertAVLProperty())
    
        ## iteriranje kroz stablo - inorder()
       
        for x in self.bst:
            print(x)
            
        ## remove all    
        for r in vals:
            self.bst.remove(r)
            self.assertFalse(r in self.bst)
            self.assertTrue(self.bst.assertAVLProperty())


        
if __name__ == '__main__':
    unittest.main()
    MyBst = BinaryTree()
    MyBst.add(200)
    
   
