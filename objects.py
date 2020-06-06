#superclass for directed graphs with weighted edges.
class Graph():
	def __init__(self, matrix):
		self.data = matrix
	
	#use slices to get weights along a path:	
	def __getitem__(self, path):
		i = 0
		result = []
		while i+1 < len(path):
			result.append(self.data[path[i]][path[i+1]])
			i = i+1
		return result
		
	def __setitem__(self, path, values):
		i = 0
		while i+1 < len(path):
			self.data[path[i]][path[i+1]] = values[i]
			i = i+1
	
	def link(self, from_node, to_node, weight = 1):
		self.data[from_node][to_node] = weight
	
	def get_outflow(self, node):
		return self.data[node]
		
	def get_inflow(self, node):
		return [each_row[node] for each_row in self.data]
		
	def add_node(self, loc):
		filler = [0 for _ in self.data]
		self.data.insert(loc,filler)
		for each_row in self.data:
			each_row.insert(loc,0)
	
	def get_dim(self):
		return len(self.data)


#Network tracks both routes and flow, each of which are instances of Graph.
class Network():
	def __init__(self, matrix, starts, ends):
		self.data = Graph(matrix)
		self.starts = starts
		self.ends = ends
		self.augment()
		
		#initialize zero matrix for tracking flow through network:
		self.flow = Graph([[0 for _ in self.data.get_dim()] for _ in self.data.get_dim()])
		
	def augment(self):
		self.start = 0
		self.end = len(self.data)
		
		self.data.add_node(self.start)
		self.data.add_node(self.end)
		
		#all node labels are now off by 1:
		self.starts = self.starts + 1
		self.ends = self.ends + 1
		
		starts_outflow = []
		for each in self.starts:
			m = max(self.data.get_outflow(each))
			starts_outflow.append(m)
		m = max(starts_outflow)
		
		ends_inflow = []
		for each in self.ends:
			n = max(self.data.get_inflow(each))
			ends_inflow.append(n)
		n = max(ends_inflow)
		
		for each in starts:
			self.data.link(self.start,each,m)
			
		for each in ends:
			self.data.link(each,self.end,n)

	def flow_thru_path(self, path):
		f = min(self.get_residual_flow(path))
		self.update_flow(path, f)

	# def get_residual_flow(self):
	# 	#self.data - self.flow
	# 	neg_flow = [[-x for x in each] for each in self.flow]
	# 	#matrix addition:
	# 	return [[sum(i) for i in zip(each[0], each[1])] for each in zip(self.data, neg_flow)]

	def get_residual_flow(self, path):
		#self.data[path] - self.flow[path]
		return [x-y for (x,y) in zip(self.data[path], self.flow[path])]

	def update_flow(self, path, water):
		#flow water down the path
		#self.flow[path] += self.flow[path] + water
		stream = [water] * len(path)
		self.flow[path] = [x+y for (x,y) in zip(self.flow[path], stream)]
		
		
		