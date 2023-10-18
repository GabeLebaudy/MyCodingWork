#This file will be used to demonstrate the graph data structure


class Graph:
    #Constructor
    def __init__(self, edges):
        self.edges = edges
        self.graphDict = {}
        for start, end in self.edges:
            if start in self.graphDict:
                self.graphDict[start].append(end)
            else:
                self.graphDict[start] = [end]

        #print("Graph Dictionary", self.graphDict)

    #Get all paths given a start and end point on the graph
    def getPaths(self, start, end, path = []):
        path = path + [start]

        if start == end:
            return [path]
        
        if start not in self.graphDict:
            return []
        
        paths = []

        for node in self.graphDict[start]:
            if node not in path:
                newPaths = self.getPaths(node, end, path)
                for p in newPaths:
                    paths.append(p)


        return paths
    

    #Get the shortest path
    def getShortestPath(self, start, end, path = []):
        path = path + [start]
        
        if start == end:
            return path
        
        if start not in self.graphDict:
            return None
        
        shortestPath = None
        for node in self.graphDict[start]:
            if node not in path:
                curSp = self.getShortestPath(node, end, path)
                if curSp:
                    if shortestPath is None or len(curSp) < len(shortestPath):
                        shortestPath = curSp

        return shortestPath
    
#Main Method
if __name__ == "__main__":
    routes = [
        ("Mumbai", "Paris"),
        ("Mumbai", "Dubai"),
        ("Paris", "Dubai"),
        ("Paris", "New York"),
        ("Dubai", "New York"),
        ("New York", "Toronto")
    ]

    routeGraph = Graph(routes)
    
    start = "Paris"
    end = "New York"

    print(routeGraph.getShortestPath(start, end))