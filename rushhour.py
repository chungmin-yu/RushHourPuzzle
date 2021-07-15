import queue
import sys
import time

#modified limit of recursive
sys.setrecursionlimit(90000000)
#create time function
now = lambda: time.time()


algorithm=input('1:BFS 2:DFS 3:IDS 4:A* 5:IDA*: ')
algorithm=int(algorithm)
while algorithm<1 or algorithm >5:
	algorithm=input('1:BFS 2:DFS 3:IDS 4:A* 5:IDA*: ')
	algorithm=int(algorithm)
textfile=input('choose an initial board layout file: ')
start = now()

#read data from file
Input=[]
with open(textfile) as f:
	lines=0
	for l in f.readlines():
		Line=l.split(' ')
		Input.append([])
		for data in Line:
			Input[lines].append(int(data))
		lines+=1
		

board=[]
answer=[]
carDir={}
carLen={}


for i in range(6):
	board.append([0,0,0,0,0,0])
#number of car
car=0
#translate input to board(2Darray)
for info in Input:
	car+=1
	index=info[0]+1
	row=info[1]
	column=info[2]
	length=info[3]
	direction=info[4]
	carDir.update({index:direction})
	carLen.update({index:length})
	#horizontal
	if direction == 1:
		for i in range(length):
			board[row][column+i]=index
	#vertical
	else:
		for i in range(length):
			board[row+i][column]=index


#encode
#translate 2Darray to string
#this can conveniently compute in following algorithm 
initial=''
for i in range(6):
	for j in range(6):
		if board[i][j]<10:
			initial+=('0'+str(board[i][j]))
		else:
			initial+=str(board[i][j])
			
			
#print('initial:')
#print(board)			
#print(initial)
	
	
#left and up	
def move1(index,state,carDir,carLen):	

	#decode
	#translate string to 2Darray
	newboard=[]
	for i in range(6):
		newboard.append([0,0,0,0,0,0])
	for i in range(0,72,2):
		(m,n)=divmod(i,12)
		n=int(n/2)
		newboard[m][n]=int(state[i]+state[i+1])
		
		
	#search
	#if search is true, this represents we find that car
	#if success is truem this represents moving is successful
	search=False
	success=False
	r=-1
	c=-1
	for i in range(6):
		if search:
			break
		for j in range(6):
			if newboard[i][j]==index:
				#horizontal
				if carDir[index]==1:
					l=carLen[index]
					if j-1>=0 and newboard[i][j-1]==0:
						newboard[i][j-1]=index
						newboard[i][j-1+l]=0
						r=i
						c=j-1
						success=True
				#vertical
				else:
					l=carLen[index]
					if i-1>=0 and newboard[i-1][j]==0:
						newboard[i-1][j]=index
						newboard[i-1+l][j]=0
						r=i-1
						c=j
						success=True
				search=True
				break	
				
								
	if not success:
		return 'none', -1, -1, -1
	else:
		#encode
		#translate 2Darray to string
		newstate=''
		for i in range(6):
			for j in range(6):
				if newboard[i][j]<10:
					newstate+=('0'+str(newboard[i][j]))
				else:
					newstate+=str(newboard[i][j])
		return newstate, index-1, r, c
		

#right and down
def move2(index,state,carDir,carLen):	

	#decode
	#translate string to 2Darray
	newboard=[]
	for i in range(6):
		newboard.append([0,0,0,0,0,0])
	for i in range(0,72,2):
		(m,n)=divmod(i,12)
		n=int(n/2)
		newboard[m][n]=int(state[i]+state[i+1])
		
		
	#search
	#if search is true, this represents we find that car
	#if success is truem this represents moving is successful
	search=False
	success=False
	r=-1
	c=-1
	for i in range(6):
		if search:
			break
		for j in range(6):
			if newboard[i][j]==index:
				if carDir[index]==1:
					#horizontal
					l=carLen[index]
					if j+l<6 and newboard[i][j+l]==0:
						newboard[i][j+l]=index
						newboard[i][j]=0
						r=i
						c=j+1
						success=True
				else:
					#vertical
					l=carLen[index]					
					if i+l<6 and newboard[i+l][j]==0:
						newboard[i+l][j]=index
						newboard[i][j]=0
						r=i+1
						c=j
						success=True
				search=True
				break
				
				
	if not success:
		return 'none', -1, -1, -1
	else:
		#encode
		#translate 2Darray to string
		newstate=''
		for i in range(6):
			for j in range(6):
				if newboard[i][j]<10:
					newstate+=('0'+str(newboard[i][j]))
				else:
					newstate+=str(newboard[i][j])
		return newstate, index-1, r, c
		


#store state to avoid duplication 
bfsPath={initial:['', -1, -1, -1]}
def BFS(state):
	bfs1=False
	bfs2=False
	#state queue
	q = queue.Queue()	
	q.put(state)
	#count queue
	c = queue.Queue()
	c.put(0)
	#if state queue is not empty, we will pop one state and try every possibility
	while not q.empty():
		if bfs1 or bfs2:
			break
		state=q.get()
		count=c.get()
		for i in range(car):
			new1, index1, row1, col1=move1(i+1,state,carDir,carLen)
			new2, index2, row2, col2=move2(i+1,state,carDir,carLen)
			if new1 !='none':
				if new1[34]=='0' and new1[35]=='1':
					bfsPath.update({new1:[state, index1, row1, col1]})
					bfs1=True
					break
				else:
					if new1 not in bfsPath:
						bfsPath.update({new1:[state, index1, row1, col1]})
						q.put(new1)
						newCount1=count+1
						c.put(newCount1)
			if new2 !='none':
				#if 2Darray[2][5] is redcar, break and print answer
				#else put in queue and continue to find
				if new2[34]=='0' and new2[35]=='1':
					bfsPath.update({new2:[state, index2, row2, col2]})
					bfs2=True
					break
				else:
					if new2 not in bfsPath:
						bfsPath.update({new2:[state, index2, row2, col2]})
						q.put(new2)
						newCount2=count+1
						c.put(newCount2)
	
	#decode
	#print answer
	output=[]
	if bfs1:
		final=new1
	elif bfs2:
		final=new2
	while final != initial:
		output.append([bfsPath[final][1], bfsPath[final][2], bfsPath[final][3]])
		final=bfsPath[final][0]
	print('step:')
	while len(output)>0:
		f.write(str(output[-1])[1:-1]+'\n')
		print(str(output.pop())[1:-1])	
				
	print('count:')
	print(count+1)
	
	
	
dfs=False
#store state to avoid duplication
dfsPath={initial:['', -1, -1, -1]}	
def DFS(state, count):
	#if we find one answer, we retrun answer
	global dfs
	if dfs:
		return
		
	#finish
	if state[34]=='0' and state[35]=='1':
		#deocde
		#print answer
		output=[]
		final=state
		while final != initial:
			output.append([dfsPath[final][1], dfsPath[final][2], dfsPath[final][3]])
			final=dfsPath[final][0]
		print('step:')
		while len(output)>0:
			f.write(str(output[-1])[1:-1]+'\n')
			print(str(output.pop())[1:-1])
			
		print('count:')
		print(count)
		dfs=True
		return
		
	#if we not try this possibility before, we try
	#else break and try another	
	for i in range(car):
		new1, index1, row1, col1=move1(i+1,state,carDir,carLen)
		new2, index2, row2, col2=move2(i+1,state,carDir,carLen)
		if new1 != 'none':
			if new1 not in dfsPath:
				dfsPath.update({new1:[state, index1, row1, col1]})
				DFS(new1, count+1)
		if new2 != 'none':
			if new2 not in dfsPath:
				dfsPath.update({new2:[state, index2, row2, col2]})
				DFS(new2, count+1)
				
				

ids=False
#store state to avoid duplication
idsPath={}		
def IDS(state, depth, maximum):
	#if we find one answer, we retrun answer
	global ids
	if ids:
		return True
		
	#if excceed the maximum depth, return and increase maximum depth
	if depth > maximum:
		return 
	
	#finish
	if state[34]=='0' and state[35]=='1':
		#deocde
		#print answer	
		output=[]
		final=state
		while final != initial:
			output.append([idsPath[final][1], idsPath[final][2], idsPath[final][3]])
			final=idsPath[final][0]
		print('step:')
		while len(output)>0:
			f.write(str(output[-1])[1:-1]+'\n')
			print(str(output.pop())[1:-1])
			
		print('depth:')
		print(depth)
		ids=True
		return True
		
	#if we not try this possibility before, we try
	#else break and try another		
	for i in range(car):
		new1, index1, row1, col1=move1(i+1,state,carDir,carLen)
		new2, index2, row2, col2=move2(i+1,state,carDir,carLen)
		if new1 != 'none':
			if new1 not in idsPath:
				idsPath.update({new1:[state, index1, row1, col1]})
				IDS(new1,depth+1, maximum)
				del idsPath[new1]
		if new2 != 'none':
			if new2 not in idsPath:
				idsPath.update({new2:[state, index2, row2, col2]})
				IDS(new2, depth+1, maximum)
				del idsPath[new2]
				

#for Astar and IDAstar algorithm, this can conveniently implement them
class Node():
	
	def __init__(self, parent=None, state=None):
		self.parent = parent
		self.state = state	
		self.g=0
		self.h=0
		self.f=0
		self.index=-1
		self.row=-1
		self.col=-1
		


def Astar(state):
	#create start node(initial state)
	start_node = Node(None, state)
	start_node.g = start_node.h = start_node.f = 0
	start_node.index=start_node.row=start_node.col = -1

	#openlist is neighbor node
	#closelist is visited node
	openList=[]	
	closeList=[]
	openList.append(start_node)
	#if neighbor node is not empty, we can continue to find
	while len(openList) > 0:
		#find the f of node is minimum to visit
		current_node = openList[0]
		current_index=0
		for index, item in enumerate(openList):
			if item.f < current_node.f:
				current_node = item
				current_index = index
				
		#remove this node from neighbor list and add it to visited list
		openList.pop(current_index)
		closeList.append(current_node)
		
		state = current_node.state
		#finish
		if state[34]=='0' and state[35]=='1':
			#deocde
			#print answer
			output=[]
			while current_node != start_node:
				output.append([current_node.index, current_node.row, current_node.col])
				current_node=current_node.parent
			count=len(output)
			print('step:')
			while len(output)>0:
				f.write(str(output[-1])[1:-1]+'\n')
				print(str(output.pop())[1:-1])
			print('count:')
			print(count)
				
			break
			
		
		#children are all possibilities of this state
		children=[]
		for i in range(car):
			new1, index1, row1, col1=move1(i+1,state,carDir,carLen)
			if new1 != 'none':
				new_node1 = Node(current_node, new1)
				new_node1.index=index1
				new_node1.row=row1
				new_node1.col=col1
				children.append(new_node1)
			new2, index2, row2, col2=move2(i+1,state,carDir,carLen)			
			if new2 != 'none':
				new_node2 = Node(current_node, new2)
				new_node2.index=index2
				new_node2.row=row2
				new_node2.col=col2
				children.append(new_node2)
				
				
		for child in children:
			#if state is visited, then ignore it
			Close=False
			for closeChild in closeList:
				if child.state == closeChild.state:
					Close=True
					break
			if Close:
				continue
				
			#update value of f,g,h		
			child.g = current_node.g+1
			#Heuristics
			redcar=False
			h_value=0
			for i in range(24,36,2):
				if child.state[i]=='0' and child.state[i+1]=='1':
					redcar=True
				else:
					if not redcar:
						continue
					else:
						if int(child.state[i:i+2]) != 0:
							h_value+=1
					
			child.h = h_value
			#print('h', h_value)
			child.f = child.g + child.h
			
			#if state is on neighborhood and g value is greater, then ignore it
			#otherwise, if g value is smaller, then add it to neighbor list
			Open=False
			for openChild in openList:
				if child.state == openChild.state and child.g >= openChild.g:
					Open=True
					break
			if Open:
				continue
					
			openList.append(child)
	
	

idastarPath = [initial]		
def IDAstar(path, maximum):
	current_node = path[-1]
	#if f value of this node exceed maximum bound, return and increase maximum bound
	if current_node.f>maximum:
		return current_node.f
		
	state = current_node.state	
	#finish
	if state[34]=='0' and state[35]=='1':
		#deocde
		#print answer
		output=[]
		while current_node != Start_node:
			output.append([current_node.index, current_node.row, current_node.col])
			current_node=current_node.parent
		print('step:')
		while len(output)>0:
			f.write(str(output[-1])[1:-1]+'\n')
			print(str(output.pop())[1:-1])
		
		return True
		
	#children are all possibilities of this state
	#we want to find minimum and not visited before, visit it	
	minimum = float('inf')
	children=[]
	for i in range(car):
		new1, index1, row1, col1=move1(i+1,state,carDir,carLen)
		if new1 != 'none':
			new_node1 = Node(current_node, new1)
			new_node1.index=index1
			new_node1.row=row1
			new_node1.col=col1
			children.append(new_node1)
		new2, index2, row2, col2=move2(i+1,state,carDir,carLen)			
		if new2 != 'none':
			new_node2 = Node(current_node, new2)
			new_node2.index=index2
			new_node2.row=row2
			new_node2.col=col2
			children.append(new_node2)
		
		
	for child in children:
		if child not in idastarPath:
		
			#update value of f,g,h	
			child.g = current_node.g+1
			#Heuristics
			redcar=False
			h_value=0
			for i in range(24,36,2):
				if child.state[i]=='0' and child.state[i+1]=='1':
					redcar=True
				else:
					if not redcar:
						continue
					else:
						if int(child.state[i:i+2]) != 0:
							h_value+=1
					
			child.h = h_value
			#print('h', h_value)
			child.f = child.g + child.h
			
			#if success, return answer
			#otherwise, find minimum
			path.append(child)
			idastarPath.append(child.state)
			tmp = IDAstar(path, bound)
			if tmp == True:
				return True
			if tmp < minimum:
				minimum = tmp
			path.pop()
			idastarPath.pop()
				
	return minimum
				
			

with open('output.txt', 'w') as f:		
	if algorithm == 1:
		BFS(initial)
	elif algorithm == 2:
		DFS(initial, 0)
	elif algorithm == 3:
		#IDS
		limit=1
		while True:
			#print(limit)
			idsPath.clear()
			idsPath[initial]=['', -1, -1, -1]
			find=IDS(initial, 0, limit)			
			if find == True:
				break
			else:
				limit+=1
			
			
	elif algorithm == 4:
		Astar(initial)
	elif algorithm == 5:
		#IDAstar
		#create start node
		Start_node = Node(None, initial)	
		Start_node.g = 0
		#Heuristics
		Redcar=False
		H_value=0
		for i in range(24,36,2):
			if Start_node.state[i]=='0' and Start_node.state[i+1]=='1':
				Redcar=True
			else:
				if not Redcar:
					continue
				else:
					if int(Start_node.state[i:i+2]) != 0:
						H_value+=1		
		Start_node.h = H_value
		#print('h', h_value)
		Start_node.f = Start_node.g + Start_node.h
		Start_node.index=Start_node.row=Start_node.col = -1
		#initial bound is start_node of h value
		bound=Start_node.h
		path = [Start_node]
		while True:
			search=IDAstar(path, bound)
			#print(search)
			if search == True:
				print('depth:')
				print(bound)
				break
			elif search == float('inf'):
				print('False')
			else:
				bound = search

	
print('TIME: ', now() - start)	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	

