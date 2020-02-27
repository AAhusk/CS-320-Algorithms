'''
This is an implementation of the adjacency-list representation of a graph
where the vertices are numbered from 0 through n-1.

The class has integer variables recording the number n of vertices
and number m of edges.  It has a list ._verts of length n of lists of integers.
The list that appears in position i of this list is the list of neighbors
of vertex i.  For example, if ._verts is [[1,2], [], [0]], then
there are three vertices, since there are three lists in it.  Vertex 0
has neighbors 1 and 2, vertex 1 has no neighbors, and vertex has 0 as
its only neighbor.
'''

class Graph(object):

  # return number of vertices
  def getn(self):
     return len(self._verts)

  # return number of edges
  def getm(self):
     return self._m

  # Return a reference to the list of neighbors of vertex i
  def neighbors(self, i):
    return self._verts[i]

  # return a list of ordered pairs giving the edges of the graph
  def getEdges(self):
     edgeList = []
     for i in range(self.getn()):
        for j in self.neighbors(i):
           edgeList.append((i,j))
     return edgeList
        
  ''' constructor.  __init__ is a reserved keyword identifying it
      as a constructor.  numVerts tells how many vertices it should have.  
      edgeList is a list of ordered pairs, one for each edge, in any order.
      Example: numVerts = 3 and edgeList = [(0,1), (1,2), (0,2), (2,0)]'''
  def __init__ (self, numVerts, edgeList):
    self._m = len(edgeList)
    self._verts = [[] for i in range(numVerts)]
    for u, v in edgeList:
      self.neighbors(u).append(v)  # works because neighbors returns a reference
                                   #  to the neighbor list

  # add an edge from tail to head.  No checking for duplicate edges
  def addEdge(self, tail, head):
    self.neighbors(tail).append(head)
    self._m += 1
  
  ''' Return the transpose of the graph, that is, the result of reversing
      all the edges '''
  def transpose (self):
    other = Graph(self.getn(), [])
    edgeList = self.getEdges()
    for u,v in edgeList:
      other.addEdge(v,u)
    return other

  ''' String representation of the graph.  If G is an instance of the class,
      this is called with str(G).  It is called implicitly when a string
      is expected, e.g. in a call to print(G) '''
  def __str__(self):
     return 'n = ' + str(self.getn()) + ' m = ' + str(self.getm()) + '\n' + str(self._verts)


  '''
  Version of dfs that labels each vertex with its parent in the dfs forest, or
  -1 if it is the root of one of the trees in the forest.  In the main
  call of dfs, the loop traverses the vertices in ascending order,
  unless a list of vertices in another order is supplied as a list of
  length n in the second parameter.

  (You can assign labels to vertices with an array L, where L[i] gives the
  label of vertex i.)  In the returned list, parent, parent[i] gives
  the vertex number of the parent of vertex i, or -1 if i is the root of
  a tree in the dfs forest.
  '''
  def dfs(self, vertOrder = None):
      if vertOrder == None:
         vertOrder = range(self.getn())
      colored = [False for i in range(self.getn())] #label vertices as uncolored
      parent = [-1 for i in range(self.getn())] #vertices start out with no parent
      for j in range(self.getn()):
          if colored[vertOrder[j]] == False:
              self.dfsVisit(vertOrder[j], colored, parent)
      return parent


  ''' DFSVisit.  colored[j] = True if vertex j is colored, and it's False if j is 
      white.  The parameter i is the vertex number of the vertex to start 
      at, and it must be white.  parent is a list of parent labels that have
      been assigned so far.  '''
  def dfsVisit(self, i, colored, parent):
    colored[i] = True
    for j in self.neighbors(i):
      if not colored[j]:
          parent[j] = i
          self.dfsVisit(j, colored, parent)

  ''' 
  This is a version of DFS that assigns discovery and finishing times to
  vertices.  The vertOrder parameter gives the order in which to cycle
  through the vertices in the main loop of DFS.  If none is given,
  they are traversed in ascending order of vertex number.  It should
  return two lists, discovery and finish, where discovery[i] and finish[i]
  give the discovery and finishing times of vertex i.
  '''
  def timestamp(self, vertOrder = None):  
      time = 0
      if vertOrder == None:
          vertOrder = range(self.getn())
      discovery = [-1 for i in range(self.getn())]
      finish = [-1 for i in range(self.getn())]
      for j in range(self.getn()):
          if discovery[vertOrder[j]] == -1:
              time = self.timestampVisit(vertOrder[j], time, discovery, finish)
      return discovery, finish

  '''
  Version of dfsVisit to go with timestamp.  It increments the time
  variable each time a label is applied, and returns the updated time variable.
  Since discovery and finish are passed by reference, new timestamps
  will be reflected in them when the method returns.
  '''
  def timestampVisit(self, i, time, discovery, finish):
    discovery[i] = time
    time += 1
    for child in self.neighbors(i):
        if (discovery[child] == -1):
            time = self.timestampVisit(child, time, discovery, finish)
    finish[i] = time
    time += 1
    return time


  '''  Determine whether the graph is strongly connected.  Return True
  if it is strongly connected and False if it is not.'''
  def stronglyConnected(self):
    #  Fill in code here.  The challenge is to solve it with two calls
    #  to dfsVisit, examining the state of the 'colored' list after each
    #  of the calls.
    visited_vertices = [False for vertex in range(self.getn())]
    parent = [-1 for vertex in range(self.getn())]

    self.dfsVisit(0, visited_vertices, parent)
    for v in visited_vertices:
      if (v == False):                         #this means not every vertex was visited and the graph can't possibly be strongly connected
        return False
    
    transpose = self.transpose()
    visited_transpose = [False for vertex in range(transpose.getn())]
    transpose.dfsVisit(0, visited_transpose, parent)
    for v in visited_transpose:
      if (v == False):
        return False
    
    return True

  ''' Go through each vertex in the graph in the order given by vertOrder,
      calling DFS on the vertex if it's still white.  If no vertOrder
      parameter is given, then go through them in ascending order of
      vertex number.   Return a list L of lists, where each list in L
      is the vertices colored by one of the calls to DFS generated
      from finishOrder.  Each list should appear in descending order
      of finishing time.  In the list of lists, the lists should appear
      in descending order of finishing time.  
  '''
  def finishOrder(self, vertOrder = None):
    #  Fill in code here
    size = self.getn()
    colored = [False for i in range(size)]
    finished = []
    if vertOrder == None:
      vertOrder = range(size)
    for i in range(self.getn()):
      vertex = vertOrder[i]
      if (colored[vertex] == False):
        sublist = self.finishOrderVisit(vertex, colored, finished)
        sublist.reverse()
        finished.insert(0, sublist)
    
    return finished

  ''' This is a varant on dfsVisit that returns a list of vertices that
      were colored during the call, in *ascending* order of finishing
      time.  This allows you to append a finished vertex to the list
      in O(1) time.  (When a list of size k is returned by the root
      (top) call, it can be reversed in O(k) time to get it into
      descending order of finishing time.)  '''
  def finishOrderVisit(self, i, colored, finished):
    #  Fill in code here
    colored_this_call = []
    colored[i] = True
    for neighbor in self.neighbors(i):
      if (colored[neighbor] == False):
        colored_in_rec_call = self.finishOrderVisit(neighbor, colored, finished)
        for vertex_colored in colored_in_rec_call:  
          colored_this_call.append(vertex_colored)
    colored_this_call.append(i)
    return colored_this_call


  ''' Return the strongly-connected components, as a list L of lists of 
      integers.  Each list in L has the vertices in one strongly-connected
      components.  One step is to pass in the vertices in descending order
      of finishing time from a first call.  This list can be obtained with
      a call to 'finishOrder()' and then concatenating the lists in the
      list of lists that it returns.  (Be sure to perform this concatenation
      in O(n) time.)
  '''
  def scc(self):
    #  Fill in code here
    strong_components = []
    finishing_times = []
    finish_list_of_lists = self.finishOrder()
    finishing_times = [element for sublist in finish_list_of_lists for element in sublist]
    visited = [False for i in range(self.getn())]
    transpose = self.transpose()
    for vertex in finishing_times:
      if (visited[vertex] == False):
        scc = transpose.finishOrderVisit(vertex, visited, finishing_times)
        strong_components.append(scc)
    return strong_components

  '''
  Determine whether a graph is a DAG, using a call to a variant of DFS that may 
  halt early if it determines if the graph is not a DAG.  If the graph is a DAG,
  it should return two values, True and a list giving a topological sort.
  If it is not, it should return False and a list giving the vertices of a directed
  cycle in order.
  '''
  def isDag(self):
      # Fill in code here
      visited = [False for i in range(self.getn())]
      visited_in_current_recur = [False for i in range(self.getn())]
      topological_order = []
      for i in range(self.getn()):
        if(visited[i] == False) :
          in_subgraph = []
          top_sort = []
          cyclic = self.isCyclic(i, visited, in_subgraph, top_sort, visited_in_current_recur)
          if (cyclic == True):
            cycle_vertex = in_subgraph[len(in_subgraph)-1]                                 #gets the last element from the list, the vertex that was started and ended on in a cycle        
            cycle_start_index = in_subgraph.index(cycle_vertex)                                                 #gets the first occurence of the vertex that was started and ended on
            return False, in_subgraph[cycle_start_index : (len(in_subgraph)-1)]             #exclude the last element
          else:
            for vertex in top_sort:
              topological_order.append(vertex)
      
      topological_order.reverse()
      return True, topological_order                                          

  def isCyclic(self, v, visited, in_subgraph, top_sort, visited_in_current_recur):
      in_subgraph.append(v)
      visited[v] = True
      visited_in_current_recur[v] = True
      for neighbor in self.neighbors(v):
            if (visited[neighbor] == False):
                if (self.isCyclic(neighbor, visited, in_subgraph, top_sort, visited_in_current_recur) == True):
                    return True
            elif (visited_in_current_recur[neighbor] == True):
                in_subgraph.append(neighbor)
                return True                                       
      top_sort.append(v)
      in_subgraph.pop()
      visited_in_current_recur[v] = False                                                                 #find out how to actually get the cycle

  '''
  Test whether an alleged topological sort really is one.  
  The parameters are a graph and a list of the integers from 0 to n-1 in some order.
  It should output True if it is a topological sort, and False and an edge (i,j)
  that points the wrong way, showing that it is not a topological sort.
  '''
  def testTopSort(self, Tsort):
      # Fill in code here
      inverse_Tsort = [-1 for vertex in range(self.getn())]                    #inverse_Tsort holds the place vertex v has in Tsort at inverse_Tsort[v]
      for i in range(len(Tsort)):
        inverse_Tsort[Tsort[i]] = i
      
      for vertex in Tsort:
        for neighbor in G.neighbors(vertex):
          if (inverse_Tsort[neighbor] < inverse_Tsort[vertex]):
            return False, (vertex, neighbor)
      return True
'''  Read a graph in from a file.  The format of the file is as follows:
     The first line gives the number of vertices.
     Each subsequent line gives an ordered pair of vertices, separated by
     a comma, indicating a directed edge.

     Example:
     ----
     3
     0,1
     1,2
     0,2
     2,0
     ----

     This gives a graph with three vertices and four directed edges,
     (0,1), (1,2), (0,2), (2,0)
'''

def readGraph(filename):
  edgeList = []
  fp = open(filename, 'r')
  n = int(fp.readline())
  for line in fp:
     u,v  = [int(x) for x in line.split(',')]
     edgeList.append((u,v))
  return Graph(n, edgeList)
    
