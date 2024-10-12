import heapq
from typing import List
from other import pprint
from collections import deque
from DataParser import DataProcessor
from Objects import Voznik, Stranka, Odlagalisce



class Node:
    def __init__(self, location):
        self.location = location
        self.resident = None
        self.occupant = None  # No occupant initially

class Graph:
    def __init__(self, data):
        self.nodes = {}
        
        self.locations =       data["L"]
        self.time_matrix =     data["casovne_razdalje"]
        self.distance_matrix = data["razdalje"]
        
        for i in range(1, self.locations+1):
            self.nodes[i] = Node(i)
            
    def add_vozniki(self, vozniki):
        for voznik in vozniki:
            self.nodes[voznik.LVi].occupant = voznik
        
    def add_stranke(self, stranke):
        for stranka in stranke:
            self.nodes[stranka.LSi].resident = stranka
        
    def add_smetisca(self, smetisca):
        for smetisce in smetisca:
            self.nodes[smetisce.LOi].resident = smetisce
    
    def update_voznik(self, current_location, new_location):
        self.nodes[new_location].occupant = self.nodes[current_location].occupant
        self.nodes[current_location].occupant = None
    
    def print_graph(self):
    
        for node in self.nodes.values():
            print(node.__dict__)
            
    
    def cost(self, current_id, next_id):
        # Cost function: Distance to travel between nodes
        return self.distance_matrix[current_id - 1][next_id - 1] * data["Ckm"]

    def heuristic(self, current_id, target_id):
        # Example heuristic: Euclidean distance between nodes
        return self.distance_matrix[current_id - 1][target_id - 1]

    def astar(self, start_id, target_id):
        visited = set()
        heap = [(0, start_id)]  # (f-score, node_id)
        parent = {}
        g_score = {node_id: float('inf') for node_id in range(1, self.locations + 1)}
        g_score[start_id] = 0

        while heap:
            f_score, current_id = heapq.heappop(heap)

            if current_id == target_id:
                path = [current_id]
                while current_id in parent:
                    current_id = parent[current_id]
                    path.append(current_id)
                path.reverse()

                # Calculate total distance and time
                total_distance = sum(self.cost(path[i], path[i + 1]) for i in range(len(path) - 1)) // data["Ckm"]
                total_time = sum(self.time_matrix[path[i] - 1][path[i + 1] - 1] for i in range(len(path) - 1))

                return path[1:], total_time, total_distance

            if current_id in visited:
                continue

            visited.add(current_id)

            for next_id, cost in enumerate(self.distance_matrix[current_id - 1]):
                if cost == 0 or next_id + 1 in visited:
                    continue

                tentative_g_score = g_score[current_id] + self.cost(current_id, next_id + 1)

                if tentative_g_score < g_score[next_id + 1]:
                    parent[next_id + 1] = current_id
                    g_score[next_id + 1] = tentative_g_score
                    f_score = tentative_g_score + self.heuristic(next_id + 1, target_id)
                    heapq.heappush(heap, (f_score, next_id + 1))

        return None, None, None  # No path found
    
   
            
            
def sort_vozniki_by_capacity(vozniki: List[Voznik]) -> List[Voznik]:
    
    return sorted(vozniki, key=lambda x: x.Ki, reverse=True)

            
def get_gap(loc1: int, loc2: int, mx: List[List[int]]):
    return mx[loc1-1][loc2-1]


def move_to_location(voznik, location, t_mtx):
    voznik.LVi_before = voznik.LVi
    voznik.LVi = location
    
    voznik.voznja["VVi"] = voznik.ID
    voznik.voznja["LZi"] = voznik.LVi_before
    voznik.voznja["LKi"] = voznik.LVi 
    voznik.voznja["TVi"] = voznik.time
    print("voznik voznja tvi",voznik.voznja["TVi"])
    
    
    print("Voznik lvi before",voznik.LVi_before)
    print("Voznik lvi",voznik.LVi)
    print("Voznik from before to now", get_gap(voznik.LVi_before, voznik.LVi, t_mtx))
    voznik.time += get_gap(voznik.LVi_before, voznik.LVi, t_mtx)
            
def main(data, vozniki, stranke, smetisca):
    
    d_mx = data["razdalje"]
    t_mx = data["casovne_razdalje"]
    
    graph = Graph(data)
    graph.add_vozniki(vozniki)
    graph.add_stranke(stranke)
    graph.add_smetisca(smetisca)

    vozniki_by_capacity = sort_vozniki_by_capacity(vozniki)

    
    for voznik in vozniki_by_capacity:
        voznik.TIME = 0
        
        while voznik.time < 1440:
            voznik.voznja["VVi"] = voznik.ID
            voznik.voznja["TVi"] = voznik.time
            
            
            
    voznik1 = vozniki[0]
    stranka1 = stranke[0]
    
    path = graph.astar(voznik1.LVi, stranka1.LSi)[0]
    
    voznik_before_path = voznik1.LVi 
    print("starting time",voznik1.time)
    for v in path:
        move_to_location(voznik1, v, t_mx)
        print("voznja",voznik1.voznja)
        voznik1.voznje.append(voznik1.voznja)
    graph.update_voznik(voznik_before_path, voznik1.LVi)
    
    print("voznik1 time after path",voznik1.time)
    print("voznik1 with direct time", get_gap(44,49,t_mx))
    print("voznik1 with direct distance", get_gap(44,49,d_mx))
    #graph.print_graph()
    
    
    
    
    
    


if __name__ == "__main__":
    
    data = DataProcessor.loadFile("./Data/odvoz01.json")

    Ckm = data["Ckm"]
    smetisca_bin = data["smetisca"]

    smetisca = []
    for i, smetisce in enumerate(smetisca_bin, start=1):
        if smetisce == 1: smetisca.append(i)

        
    vozniki = [Voznik(voznik, Ckm) for voznik in data["vozniki"]]
    stranke = [Stranka(stranka) for stranka in data["stranke"]]
    smetisca = [Odlagalisce(smetisce) for smetisce in smetisca]


    for vID, voznik_fill_ids in enumerate(vozniki, start=1):
        voznik_fill_ids.ID = vID

    for sID, stranka_fill_ids in enumerate(stranke, start=1):
        stranka_fill_ids.ID = sID
    
    main(data, vozniki, stranke, smetisca)


    
    