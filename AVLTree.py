
class AVLTreeNode(object):

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
		
	def leftSubTreeHeight(self):
		leftSubTreeHeight = -1
		if (self.left != None):
			leftSubTreeHeight = self.left.height
		return leftSubTreeHeight
		
	def rightSubTreeHeight(self):
		rightSubTreeHeight = -1
		if (self.right != None):
			rightSubTreeHeight = self.right.height
		return rightSubTreeHeight
			
	def maxSubTreeHeight(self):
		leftSubTreeHeight = self.leftSubTreeHeight()
		rightSubTreeHeight = self.rightSubTreeHeight()
		if (leftSubTreeHeight > rightSubTreeHeight):
			return leftSubTreeHeight
		else:
			return rightSubTreeHeight
			
	def isBalanced(self):
		leftSubTreeHeight = -1
		rightSubTreeHeight = -1
		if (self.left != None):
			leftSubTreeHeight = self.left.height
		if (self.right != None):
			rightSubTreeHeight = self.right.height
		if (abs(rightSubTreeHeight - leftSubTreeHeight) > 1):
			return False
		else:
			return True
		
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
			return None
		elif (self.keyData > keyData):
			if (self.left == None):
				self.left = AVLTreeNode(keyData)
				self.left.parent = self
				self.left.depth = self.depth+1
				delegateTree.numNodes += 1
				return self.left
			else:
				return self.left.insert(delegateTree, keyData)
		else:
			if (self.right == None):
				self.right = AVLTreeNode(keyData)
				self.right.parent = self
				self.right.depth = self.depth+1
				delegateTree.numNodes += 1
				return self.right
			else:
				return self.right.insert(delegateTree, keyData)		

	def remove(self, delegateTree):
		if (self.isLeaf()):
			if (self.isLeftChild()):
				self.parent.left = None
				self.parent.bubbleUp(delegateTree)
			elif (self.isRightChild()):
				self.parent.right = None
				self.parent.bubbleUp(delegateTree)
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
			
	def bubbleUp(self, delegateTree):
		self.height = self.maxSubTreeHeight() + 1
		if (self.isBalanced() == False):
			#print("imbalance at " + str(self.keyData) + " node")
			self.rotate(delegateTree)
		if (self.parent != None):
			self.parent.bubbleUp(delegateTree)
			
	def rotate(self, delegateTree):	
		p = self.parent
		if (self.leftSubTreeHeight() > self.rightSubTreeHeight()):
			if (self.left.leftSubTreeHeight() > self.left.rightSubTreeHeight()):
				#    z
				#  y/
				#x/
				z = self
				y = self.left
				x = self.left.left					
				T_0 = x.left
				T_1 = x.right
				T_2 = y.right
				T_3 = z.right
			else:
				#    z
				#x/
				#  \y
				z = self
				y = self.left.right
				x = self.left
				T_0 = x.left
				T_1 = y.left 
				T_2 = y.right 
				T_3 = z.right 
			if (z.isLeftChild()):
				p.left = y
			elif (z.isRightChild()):
				p.right = y
			else:
				delegateTree.rootNode = y
		else:
			if (self.right.rightSubTreeHeight() > self.right.leftSubTreeHeight()):
				#x
				# \y
				#   \z
				z = self.right.right
				y = self.right
				x = self 
				T_0 = x.left 
				T_1 = y.left 
				T_2 = z.left 
				T_3 = z.right 
			else:
				#x
				#   \z
				# y/
				z = self.right 
				y = self.right.left 
				x = self 
				T_0 = x.left 
				T_1 = y.left 
				T_2 = y.right 
				T_3 = z.right
			if (x.isLeftChild()):
				p.left = y
			elif (x.isRightChild()):
				p.right = y
			else:
				delegateTree.rootNode = y
			
		y.parent = p
		y.left = x
		y.right = z
		
		x.parent = y
		z.parent = y
		
		if (T_0 != None):
			T_0.parent = x
		if (T_1 != None):
			T_1.parent = x
		if (T_2 != None):
			T_2.parent = z
		if (T_3 != None):
			T_3.parent = z
		
		x.left = T_0
		x.right = T_1
		z.left = T_2
		z.right = T_3
		
		x.height = x.maxSubTreeHeight()+1
		z.height = z.maxSubTreeHeight()+1
		y.height = y.maxSubTreeHeight()+1
					
		if (p != None):
			y.setDepth(p.depth+1)
		else:
			y.setDepth(0)
			
	def setDepth(self, depth):
		if (self.left != None):
			self.left.setDepth(depth+1)
		self.depth = depth
		if (self.right != None):
			self.right.setDepth(depth+1)
			

class AVLTree(object):

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
			self.rootNode = AVLTreeNode(keyData)
			self.rootNode.height = 0
			self.rootNode.depth = 0
			self.numNodes = 1
		else:
			newNode = self.rootNode.insert(self, keyData)
			if (newNode != None):
				newNode.bubbleUp(self)
	
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


