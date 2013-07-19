"""
Tree Data Structures and Algorithms.

Copyright (c) Maurice H.T. Ling <mauriceling@acm.org>

Date created: 19th March 2008
"""

import string
from treenodes import *

class RBTreeIter(object):

    def __init__ (self, tree):
        self.tree = tree
        self.index = -1  # ready to iterate on the next() call
        self.node = None
        self.stopped = False

    def __iter__ (self):
        """ Return the current item in the container
        """
        return self.node.value

    def next (self):
        """ Return the next item in the container
            Once we go off the list we stay off even if the list changes
        """
        if self.stopped or (self.index + 1 >= self.tree.__len__()):
            self.stopped = True
            raise StopIteration
        #
        self.index += 1
        if self.index == 0:
            self.node = self.tree.firstNode()
        else:
            self.node = self.tree.nextNode (self.node)
        return self.node.value
    

class OrderedBinaryTree:
    """
    Adapted from http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/286239
    Original author: Lawrence Oluyede
    """
    def __init__(self):
        """Initializes the root member"""
        self.root = None
    
    def addNode(self, data):
        # creates a new node and returns it
        return Node(data)

    def insert(self, root, data):
        # inserts a new data
        if root == None:
            # it there isn't any data
            # adds it and returns
            return self.addNode(data)
        else:
            # enters into the tree
            if data <= root.data:
                # if the data is less than the stored one
                # goes into the left-sub-tree
                root.left = self.insert(root.left, data)
            else:
                # processes the right-sub-tree
                root.right = self.insert(root.right, data)
            return root
        
    def lookup(self, root, target):
        # looks for a value into the tree
        if root == None:
            return 0
        else:
            # if it has found it...
            if target == root.data:
                return 1
            else:
                if target < root.data:
                    # left side
                    return self.lookup(root.left, target)
                else:
                    # right side
                    return self.lookup(root.right, target)
        
    def minValue(self, root):
        # goes down into the left
        # arm and returns the last value
        while(root.left != None):
            root = root.left
        return root.data

    def maxDepth(self, root):
        if root == None:
            return 0
        else:
            # computes the two depths
            ldepth = self.maxDepth(root.left)
            rdepth = self.maxDepth(root.right)
            # returns the appropriate depth
            return max(ldepth, rdepth) + 1
            
    def size(self, root):
        if root == None:
            return 0
        else:
            return self.size(root.left) + 1 + self.size(root.right)

    def printTree(self, root):
        # prints the tree path
        if root == None:
            pass
        else:
            self.printTree(root.left)
            print root.data,
            self.printTree(root.right)

    def printRevTree(self, root):
        # prints the tree path in reverse
        # order
        if root == None:
            pass
        else:
            self.printRevTree(root.right)
            print root.data,
            self.printRevTree(root.left)
            

class RBTree(object):

    def __init__(self, cmpfn=cmp, unique=True):
        self.sentinel = RBNode()
        self.sentinel.left = self.sentinel.right = self.sentinel
        self.sentinel.color = BLACK
        self.sentinel.nonzero = 0
        self.root = self.sentinel
        self.elements = 0
        
        #SF: If self.unique is True, all elements in the tree have 
        #SF  to be unique and an exception is raised for multiple 
        #SF insertions of a node
        #SF If self.unique is set to False, nodes can be added multiple 
        #SF times. There is still only one node, but all insertions are
        #SF counted in the variable node.count
        self.unique = unique
        # changing the comparison function for an existing tree is dangerous!
        self.__cmp = cmpfn

    def __len__(self):
        return self.elements

    def __del__(self):
        # unlink the whole tree

        s = [self.root]

        if self.root is not self.sentinel:
            while s:
                cur = s[0]
                if cur.left and cur.left != self.sentinel:
                    s.append(cur.left)
                if cur.right and cur.right != self.sentinel:
                    s.append(cur.right)
                cur.right = cur.left = cur.parent = None
                cur.key = cur.value = None
                s = s[1:]

        self.root = None
        self.sentinel = None

    def __str__(self):
        return "<RBTree object>"

    def __repr__(self):
        return "<RBTree object>"

    def __iter__ (self):
        return RBTreeIter (self)

    def rotateLeft(self, x):

        y = x.right

        # establish x.right link
        x.right = y.left
        if y.left != self.sentinel:
            y.left.parent = x

        # establish y.parent link
        if y != self.sentinel:
            y.parent = x.parent
        if x.parent:
            if x == x.parent.left:
                x.parent.left = y
            else:
                x.parent.right = y
        else:
            self.root = y

        # link x and y
        y.left = x
        if x != self.sentinel:
            x.parent = y

    def rotateRight(self, x):

        #***************************
        #  rotate node x to right
        #***************************

        y = x.left

        # establish x.left link
        x.left = y.right
        if y.right != self.sentinel:
            y.right.parent = x

        # establish y.parent link
        if y != self.sentinel:
            y.parent = x.parent
        if x.parent:
            if x == x.parent.right:
                x.parent.right = y
            else:
                x.parent.left = y
        else:
            self.root = y

        # link x and y
        y.right = x
        if x != self.sentinel:
            x.parent = y

    def insertFixup(self, x):
        #************************************
        #  maintain Red-Black tree balance  *
        #  after inserting node x           *
        #************************************

        # check Red-Black properties

        while x != self.root and x.parent.color == RED:

            # we have a violation

            if x.parent == x.parent.parent.left:

                y = x.parent.parent.right

                if y.color == RED:
                    # uncle is RED
                    x.parent.color = BLACK
                    y.color = BLACK
                    x.parent.parent.color = RED
                    x = x.parent.parent

                else:
                    # uncle is BLACK
                    if x == x.parent.right:
                        # make x a left child
                        x = x.parent
                        self.rotateLeft(x)

                    # recolor and rotate
                    x.parent.color = BLACK
                    x.parent.parent.color = RED
                    self.rotateRight(x.parent.parent)
            else:

                # mirror image of above code

                y = x.parent.parent.left

                if y.color == RED:
                    # uncle is RED
                    x.parent.color = BLACK
                    y.color = BLACK
                    x.parent.parent.color = RED
                    x = x.parent.parent

                else:
                    # uncle is BLACK
                    if x == x.parent.left:
                        x = x.parent
                        self.rotateRight(x)

                    x.parent.color = BLACK
                    x.parent.parent.color = RED
                    self.rotateLeft(x.parent.parent)

        self.root.color = BLACK

    def insertNode(self, key, value):
        #**********************************************
        #  allocate node for data and insert in tree  *
        #**********************************************

        # we aren't interested in the value, we just
        # want the TypeError raised if appropriate
        hash(key)

        # find where node belongs
        current = self.root
        parent = None
        while current != self.sentinel:
            # GJB added comparison function feature
            # slightly improved by JCG: don't assume that ==
            # is the same as self.__cmp(..) == 0
            rc = self.__cmp(key, current.key)
            if rc == 0:
                #SF This item is inserted for the second, 
                #SF third, ... time, so we have to increment 
                #SF the count
                if self.unique == False: 
                    current.count += 1
                else: # raise an Error
                    print "Warning: This element is already in the list ... \
                    ignored!"
                    #SF I don't want to raise an error because I want to keep 
                    #SF the code compatible to previous versions
                    #SF But here would be the right place to do this
                    #raise IndexError ("This item is already in the tree.")
                return current
            parent = current
            if rc < 0:
                current = current.left
            else:
                current = current.right

        # setup new node
        x = RBNode(key, value)
        x.left = x.right = self.sentinel
        x.parent = parent

        self.elements = self.elements + 1

        # insert node in tree
        if parent:
            if self.__cmp(key, parent.key) < 0:
                parent.left = x
            else:
                parent.right = x
        else:
            self.root = x

        self.insertFixup(x)
        return x

    def deleteFixup(self, x):
        #************************************
        #  maintain Red-Black tree balance  *
        #  after deleting node x            *
        #************************************

        while x != self.root and x.color == BLACK:
            if x == x.parent.left:
                w = x.parent.right
                if w.color == RED:
                    w.color = BLACK
                    x.parent.color = RED
                    self.rotateLeft(x.parent)
                    w = x.parent.right

                if w.left.color == BLACK and w.right.color == BLACK:
                    w.color = RED
                    x = x.parent
                else:
                    if w.right.color == BLACK:
                        w.left.color = BLACK
                        w.color = RED
                        self.rotateRight(w)
                        w = x.parent.right

                    w.color = x.parent.color
                    x.parent.color = BLACK
                    w.right.color = BLACK
                    self.rotateLeft(x.parent)
                    x = self.root

            else:
                w = x.parent.left
                if w.color == RED:
                    w.color = BLACK
                    x.parent.color = RED
                    self.rotateRight(x.parent)
                    w = x.parent.left

                if w.right.color == BLACK and w.left.color == BLACK:
                    w.color = RED
                    x = x.parent
                else:
                    if w.left.color == BLACK:
                        w.right.color = BLACK
                        w.color = RED
                        self.rotateLeft(w)
                        w = x.parent.left

                    w.color = x.parent.color
                    x.parent.color = BLACK
                    w.left.color = BLACK
                    self.rotateRight(x.parent)
                    x = self.root

        x.color = BLACK

    def deleteNode(self, z, all=True):
        #****************************
        #  delete node z from tree  *
        #****************************

        if not z or z == self.sentinel:
            return
            
        #SF If the object is in this tree more than once the node 
        #SF has not to be deleted. We just have to decrement the 
        #SF count variable
        #SF we don't have to check for uniquness because this was
        #SF already captured in insertNode() and for this reason 
        #SF z.count cannot be greater than 1
        #SF If all=True then the complete node has to be deleted
        if z.count > 1 and not all: 
            z.count -= 1
            return          

        if z.left == self.sentinel or z.right == self.sentinel:
            # y has a self.sentinel node as a child
            y = z
        else:
            # find tree successor with a self.sentinel node as a child
            y = z.right
            while y.left != self.sentinel:
                y = y.left

        # x is y's only child
        if y.left != self.sentinel:
            x = y.left
        else:
            x = y.right

        # remove y from the parent chain
        x.parent = y.parent
        if y.parent:
            if y == y.parent.left:
                y.parent.left = x
            else:
                y.parent.right = x
        else:
            self.root = x

        if y != z:
            z.key = y.key
            z.value = y.value

        if y.color == BLACK:
            self.deleteFixup(x)

        del y
        self.elements = self.elements - 1

    def findNode(self, key):
        #******************************
        #  find node containing data
        #******************************

        # we aren't interested in the value, we just
        # want the TypeError raised if appropriate
        hash(key)
        
        current = self.root

        while current != self.sentinel:
            # GJB added comparison function feature
            # slightly improved by JCG: don't assume that ==
            # is the same as self.__cmp(..) == 0
            rc = self.__cmp(key, current.key)
            if rc == 0:
                return current
            else:
                if rc < 0:
                    current = current.left
                else:
                    current = current.right

        return None

    def traverseTree(self, f):
        if self.root == self.sentinel:
            return
        s = [None]
        cur = self.root
        while s:
            if cur.left:
                s.append(cur)
                cur = cur.left
            else:
                f(cur)
                while not cur.right:
                    cur = s.pop()
                    if cur is None:
                        return
                    f(cur)
                cur = cur.right
        # should not get here.
        return

    def nodesByTraversal(self):
        """return all nodes as a list"""
        result = []
        def traversalFn(x, K=result):
            K.append(x)
        self.traverseTree(traversalFn)
        return result

    def nodes(self):
        """return all nodes as a list"""
        cur = self.firstNode()
        result = []
        while cur:
            result.append(cur)
            cur = self.nextNode(cur)
        return result

    def firstNode(self):
        cur = self.root
        while cur.left:
            cur = cur.left
        return cur

    def lastNode(self):
        cur = self.root
        while cur.right:
            cur = cur.right
        return cur

    def nextNode(self, prev):
        """returns None if there isn't one"""
        cur = prev
        if cur.right:
            cur = prev.right
            while cur.left:
                cur = cur.left
            return cur
        while 1:
            cur = cur.parent
            if not cur:
                return None
            if self.__cmp(cur.key, prev.key)>=0:
                return cur

    def prevNode(self, next):
        """returns None if there isn't one"""
        cur = next
        if cur.left:
            cur = next.left
            while cur.right:
                cur = cur.right
            return cur
        while 1:
            cur = cur.parent
            if cur is None:
                return None
            if self.__cmp(cur.key, next.key)<0:
                return cur


class RBList(RBTree):
    """ List class uses same object for key and value
        Assumes you are putting sortable items into the list.
    """

    def __init__(self, list=[], cmpfn=cmp, unique=True):
        #SF new option: unique trees, see RBTree.__init__() for 
        #SF more information
        RBTree.__init__(self, cmpfn, unique)
        for item in list:
            self.insertNode (item, item)

    def __getitem__ (self, index):
        node = self.findNodeByIndex (index)
        return node.value

    def __delitem__ (self, index):
        node = self.findNodeByIndex (index)
        self.deleteNode (node)

    def __contains__ (self, item):
        return self.findNode (item) is not None

    def __str__ (self):
        # eval(str(self)) returns a regular list
        return '['+ string.join(map(lambda x: str(x.value), self.nodes()), ', ')+']'

    def findNodeByIndex (self, index):
        if (index < 0) or (index >= self.elements):
            raise IndexError ("pop index out of range")
        #
        if index < self.elements / 2:
            # simple scan from start of list
            node = self.firstNode()
            currIndex = 0
            while currIndex < index:
                node = self.nextNode (node)
                currIndex += 1
        else:
            # simple scan from end of list
            node = self.lastNode()
            currIndex = self.elements - 1
            while currIndex > index:
                node = self.prevNode (node)
                currIndex -= 1
        #
        return node

    def insert (self, item):
        #SF The function inserNode already checks for existing Nodes 
        #SF so this code seems to be superfluid
        #node = self.findNode (item)
        #if node is not None:
            #self.deleteNode (node)
        # item is both key and value for a list
        self.insertNode (item, item)

    def append (self, item):
        # list is always sorted
        self.insert (item)

    #SF this function is not implemented as a common list in python
    #def count (self):
        #return len(self)
        
    #SF Because we count all equal items in one node 
    #SF we now can use the function count as used in 
    #SF common python lists
    def count(self, item):
        node = self.findNode (item)
        return node.count

    def index (self, item):
        index = -1
        node = self.findNode (item)
        while node is not None:
            node = self.prevNode (node)
            index += 1
        #
        if index < 0:
            raise ValueError ("RBList.index: item not in list")
        return index

    def extend (self, otherList):
        for item in otherList:
            self.insert (item)

    def pop (self, index=None):
        if index is None:
            index = self.elements - 1
        #
        node = self.findNodeByIndex (index)
        value = node.value      # must do this before removing node
        self.deleteNode (node)
        return value

    def remove (self, item, all=True):
        #SF When called with all=True then all occurences are deleted
        node = self.findNode (item)
        if node is not None:
            self.deleteNode (node, all)

    def reverse (self): # not implemented
        raise AssertionError ("RBlist.reverse Not implemented")

    def sort (self): # Null operation
        pass

    def clear (self):
        """delete all entries"""
        self.__del__()
        #copied from RBTree constructor
        self.sentinel = RBNode()
        self.sentinel.left = self.sentinel.right = self.sentinel
        self.sentinel.color = BLACK
        self.sentinel.nonzero = 0
        self.root = self.sentinel
        self.elements = 0

    def values (self):
        return map (lambda x: x.value, self.nodes())

    def reverseValues (self):
        values = map (lambda x: x.value, self.nodes())
        values.reverse()
        return values


class RBDict(RBTree):

    def __init__(self, dict={}, cmpfn=cmp):
        RBTree.__init__(self, cmpfn)
        for key, value in dict.items():
            self[key]=value

    def __str__(self):
        # eval(str(self)) returns a regular dictionary
        return '{'+ string.join(map(str, self.nodes()), ', ')+'}'

    def __repr__(self):
        return "<RBDict object " + str(self) + ">"

    def __getitem__(self, key):
        n = self.findNode(key)
        if n:
            return n.value
        raise IndexError

    def __setitem__(self, key, value):
        n = self.findNode(key)
        if n:
            n.value = value
        else:
            self.insertNode(key, value)

    def __delitem__(self, key):
        n = self.findNode(key)
        if n:
            self.deleteNode(n)
        else:
            raise IndexError

    def get(self, key, default=None):
        n = self.findNode(key)
        if n:
            return n.value
        return default

    def keys(self):
        return map(lambda x: x.key, self.nodes())

    def values(self):
        return map(lambda x: x.value, self.nodes())

    def items(self):
        return map(tuple, self.nodes())

    def has_key(self, key):
        return self.findNode(key) <> None

    def clear(self):
        """delete all entries"""

        self.__del__()

        #copied from RBTree constructor
        self.sentinel = RBNode()
        self.sentinel.left = self.sentinel.right = self.sentinel
        self.sentinel.color = BLACK
        self.sentinel.nonzero = 0
        self.root = self.sentinel
        self.elements = 0

    def copy(self):
        """return shallow copy"""
        # there may be a more efficient way of doing this
        return RBDict(self)

    def update(self, other):
        """Add all items from the supplied mapping to this one.

        Will overwrite old entries with new ones.

        """
        for key in other.keys():
            self[key] = other[key]

    def setdefault(self, key, value=None):
        if self.has_key(key):
            return self[key]
        self[key] = value
        return value


if __name__ == "__main__":
    # create the binary tree
    BTree = OrderedBinaryTree()
    # add the root node
    root = BTree.addNode(0)
    # ask the user to insert values
    for i in range(0, 5):
        data = raw_input("insert the node value nr %d: " % i)
        # insert values
        BTree.insert(root, data)
    print
    
    BTree.printTree(root)
    print
    BTree.printRevTree(root)
    print
    data = raw_input("insert a value to find: ")
    if BTree.lookup(root, data):
        print "found"
    else:
        print "not found"
        
    print BTree.minValue(root)
    print BTree.maxDepth(root)
    print BTree.size(root)
