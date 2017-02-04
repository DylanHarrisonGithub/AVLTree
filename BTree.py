
class BTreeNode(object):

	def __init__(self, keyData):
		self.keyData = keyData
		self.count = 1
		self.depth = 0
		self.height = 0		
		self.order = -1
		self.parent = None
		self.left = None
		self.right = None

	def isLeftChild(self):
		return ((self.parent != None) and (self.parent.left == self))

	def isRightChild(self):
		return ((self.parent != None) and (self.parent.right == self))
		
	def isLeaf(self):
		return ((self.left == None) and (self.right == None))
		
	def isRoot(self):
		return (self.parent == None)
		
	def hasGrandParent(self):
		return ((self.parent != None) and (self.parent.parent != None))
		
	def maxSubTreeHeight(self):
		leftSubTreeHeight = -1
		rightSubTreeHeight = -1
		if (self.left != None):
			leftSubTreeHeight = self.left.height
		if (self.right != None):
			rightSubTreeHeight = self.right.height
		if (leftSubTreeHeight > rightSubTreeHeight):
			return leftSubTreeHeight
		else:
			return rightSubTreeHeight
		
	def rightMostNodeInLeftSubtree(self):
		c = self
		if (c.left != None):
			c = c.left
			while (c.right != None):
				c = c.right
			return c
		else:
			return null

	def leftMostNodeInRightSubtree(self):
		c = self
		if (c.right != None):
			c = c.right
			while (c.left != None):
				c = c.left
			return c
		else:
			return null

	def parentOfNearestAncestorThatIsLeftChild(self):
		c = self
		if (c.isRightChild()):
			while (c.isRightChild()):
				c = c.parent
			if (c.isLeftChild()):
				return c.parent
			else:
				return None
		else:
			return None
	
	def parentOfNearestAncestorThatIsRightChild(self):
		c = self
		if (c.isLeftChild()):
			while (c.isLeftChild()):
				c = c.parent
			if (c.isRightChild()):
				return c.parent
			else:
				return None
		else:
			return None
								
	def next(self):
		if (self.isRoot()):
			if (self.right != None):
				return self.leftMostNodeInRightSubtree()
			else:
				return None
		elif (self.isLeftChild()):
			if (self.right != None):
				return self.leftMostNodeInRightSubtree()
			else:
				return self.parent
		else:
			if (self.right != None):
				return self.leftMostNodeInRightSubtree()
			else:
				return self.parentOfNearestAncestorThatIsLeftChild()
				
	def prev(self):
		if (self.isRoot()):
			if (self.left != None):
				return self.rightMostNodeInLeftSubtree()
			else:
				return None
		elif (self.isLeftChild()):
			if (self.left != None):
				return self.rightMostNodeInLeftSubtree()
			else:
				return self.parentOfNearestAncestorThatIsRightChild()
		else:
			if (self.left != None):
				return self.rightMostNodeInLeftSubtree()
			else:
				return self.parent
	
	def insert(self, delegateTree, keyData):
		if (self.keyData == keyData):
			self.count += 1
		elif (self.keyData > keyData):
			if (self.left == None):
				self.left = BTreeNode(keyData)
				self.left.parent = self
				self.left.depth = self.depth+1
				delegateTree.numNodes += 1
				self.left.bubbleUp()
			else:
				self.left.insert(delegateTree, keyData)
		else:
			if (self.right == None):
				self.right = BTreeNode(keyData)
				self.right.parent = self
				self.right.depth = self.depth+1
				delegateTree.numNodes += 1
				self.right.bubbleUp()
			else:
				self.right.insert(delegateTree, keyData)		

	def remove(self, delegateTree):
		if (self.isLeaf()):
			if (self.isLeftChild()):
				self.parent.left = None
				self.parent.bubbleUp()
			elif (self.isRightChild()):
				self.parent.right = None
				self.parent.bubbleUp()
			else:
				delegateTree.rootNode = None
		else:
			if ((self.left != None) and (self.right != None)):
				if (self.prev().isLeaf()):
					self.swapIn(delegateTree, self.prev().remove(delegateTree))
				else:
					self.swapIn(delegateTree, self.next().remove(delegateTree))					
			else:
				if (self.right != None):
					self.swapIn(delegateTree, self.next().remove(delegateTree))
				else:
					self.swapIn(delegateTree, self.prev().remove(delegateTree))			
		return self
			
	def swapIn(self, delegateTree, newNode):
		newNode.parent = self.parent
		newNode.left = self.left
		newNode.right = self.right
		newNode.height = self.height
		newNode.depth = self.depth
		if (self.left != None):
			self.left.parent = newNode
		if (self.right != None):
			self.right.parent = newNode
		if (self.isLeftChild()):
			self.parent.left = newNode
		if (self.isRightChild()):
			self.parent.right = newNode
		if (self.isRoot()):
			delegateTree.rootNode = newNode
			
	def bubbleUp(self):
		self.height = self.maxSubTreeHeight() + 1
		if (self.parent != None):
			self.parent.bubbleUp()
				
class BTree(object):

	def __init__(self):
		self.rootNode = None
		self.numNodes = 0
		self.currentNode = None
		
	def find(self, keyData):
		if (self.rootNode != None):
			c = self.rootNode
			while (c != None):
				if (c.keyData == keyData):
					return c
				elif (c.keyData > keyData):
					c = c.left
				else:
					c = c.right
			return c
		else:
			return None
						
	def insert(self, keyData):
		if (self.rootNode == None):
			self.rootNode = BTreeNode(keyData)
			self.rootNode.height = 0
			self.rootNode.depth = 0
			self.numNodes = 1
		else:
			self.rootNode.insert(self, keyData)
	
	def remove(self, keyData):
		removedNode = self.find(keyData)
		if (removedNode != None):
			removedNode.remove(self)
			self.numNodes -= 1
		return removedNode
			
	def printTree(self):
		if (self.rootNode != None):
			c = self.rootNode
			while (c.left != None):
				c = c.left
			while (c != None):
				print(c.keyData)
				c = c.next()
	
	def getFirst(self):
		if (self.rootNode != None):
			c = self.rootNode
			while (c.left != None):
				c = c.left
			return c
		else:
			return None
			
	def markOrder(self):
		if (self.rootNode != None):
			c = self.getFirst()
			n=0
			while (c != None):
				c.order = n
				n += 1
				c = c.next()


