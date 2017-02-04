from graphics import *
from BTree import *
from AVLTree import *
import random

def drawTree(tree, windowTitle):
	cellSize = 50
	nodeSize = 24
	halfCellSize = cellSize / 2			
	tree.markOrder()
	if (tree.rootNode != None):
	
		h = tree.rootNode.height
		w = tree.numNodes		
		win = GraphWin(windowTitle, w*cellSize, (h+1)*cellSize)
		
		for x in range(0,tree.numNodes):
			p1 = Point(x*cellSize,0)
			p2 = Point((x+1)*cellSize, (h+1)*cellSize)
			rect = Rectangle(p1,p2)
			rect.setFill(color_rgb(250 - (x%2)*5,240 - (x%2)*5, 245 - (x%2)*5))
			rect.draw(win)
			
		c = tree.getFirst()		
		while (c != None):
			if (c.parent != None):
				p1 = Point(c.order*cellSize+halfCellSize, (c.depth*cellSize+halfCellSize))
				p2 = Point(c.parent.order*cellSize+halfCellSize, (c.parent.depth*cellSize+halfCellSize))
				lin = Line(p1,p2)
				lin.draw(win)
			c = c.next()
		
		c = tree.getFirst()
		column = 0
		while (c != None):
			p = Point(column*cellSize+halfCellSize, (c.depth*cellSize+halfCellSize))
			circ = Circle(p, nodeSize)
			circ2 = Circle(p, nodeSize-5)
			txt = Text(p, c.keyData)
			
			if (c == tree.currentNode):
				circ.setFill(color_rgb(0,255,0))
			elif (tree.currentNode != None):
				if (c == tree.currentNode.next()):
					circ.setFill(color_rgb(0,0,255))
				elif (c == tree.currentNode.prev()):
					circ.setFill(color_rgb(255,0,0))
				else:
					circ.setFill(color_rgb(0,0,0))
			else:
				circ.setFill(color_rgb(0,0,0))
				
			circ2.setFill(color_rgb(255,255,255))
			circ.draw(win)
			circ2.draw(win)
			txt.draw(win)
			c = c.next()
			column += 1
			
		input("Press Enter to continue...")
		win.close()
