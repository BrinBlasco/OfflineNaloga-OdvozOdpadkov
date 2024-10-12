import os
import time
import heapq
import functools
import numpy as np  # Import NumPy
from collections import deque
from typing import List, Tuple
from other import pprint, timer
from DataParser import DataProcessor
from Objects import Voznik, Stranka, Odlagalisce

class Graph:
    def __init__(self, data):
        self.locations = data["L"]
        self.time_matrix = np.array(data["casovne_razdalje"])  # Convert to NumPy array
        self.distance_matrix = np.array(data["razdalje"])  # Convert to NumPy array and apply multiplier

    def print_graph(self):
        for node in self.nodes.values():
            print(node.__dict__)

    def cost(self, current_id, next_id):
        return self.distance_matrix[current_id - 1][next_id - 1]

    def heuristic(self, current_id, target_id):
        return self.time_matrix[current_id - 1][target_id - 1]

    @functools.cache
    def astar(self, start_id, target_id) -> Tuple[List[int], int, int]:
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

def load(voznik: Voznik, stranka: Stranka):
    remainingKi = voznik.Ki - voznik.barrels
    to_load = min(stranka.Ni, remainingKi)
    
    voznik.barrels += to_load
    stranka.Ni -= to_load
    
    voznik.voznja["DKi"] = to_load
    
def unload(voznik: Voznik):
    voznik.voznja["DKi"] = -voznik.barrels
    voznik.barrels = 0



def move_to_location(voznik, location, t_mtx): # only for calling to move to single locations, but mostly for functionallity of move_through_path
    voznik.LVi_before = voznik.LVi
    voznik.LVi = location
    
    voznik.voznja["VVi"] = voznik.ID
    voznik.voznja["LZi"] = voznik.LVi_before
    voznik.voznja["LKi"] = voznik.LVi 
    voznik.voznja["TVi"] = voznik.time
    
    voznik.time += get_gap(voznik.LVi_before, voznik.LVi, t_mtx)
    
def move_through_path(voznik, path, t_mtx, graph) -> None: # we dont include last for reasons i cant explain reallly
    if len(path) == 1: pass
    for v in path[:len(path)-1]:
        voznik.voznja["DKi"] = 0
        move_to_location(voznik, v, t_mtx)
        voznik.voznje.append(voznik.voznja.copy())
    



def closest_stranka(voznik, stranke, graph):
    
    lowest_time = float('inf')
    best_stranka = None
    best_path = None
    
    for stranka in stranke:
        # path, time, distance
        if stranka.Ni == 0: continue
        path, time, dist = graph.astar(voznik.LVi, stranka.LSi)
        if time < lowest_time:
            lowest_time = time
            best_stranka = stranka
            best_path = path
            
    return best_stranka, best_path
   
def closest_smetisce(voznik, smetisca, graph):
    lowest_time = float('inf')
    best_smetisce = None
    best_path = None
    
    for smetisce in smetisca:
        # path, time, distance
        path, time, _ = graph.astar(voznik.LVi, smetisce.LOi)
        #print(path, time, _)
        if time < lowest_time:
            lowest_time = time
            best_smetisce = smetisce
            best_path = path
            
    return best_smetisce, best_path
    
def barrels_left(stranke: List[Stranka]) -> bool:
    
    for stranka in stranke:
        if stranka.Ni > 0: return True
    return False

def voznik_next_sequence(voznik, stranke, smetisca, t_mx, graph):
    originalLVi = voznik.LVi
    time_spent = 0
    
    best_stranka, _ = closest_stranka(voznik, stranke, graph)
    if best_stranka == None:
        return float("inf")
    _, time, _ = graph.astar(voznik.LVi, best_stranka.LSi)
    time_spent += time
    
    voznik.LVi = best_stranka.LSi
    
    best_smetisce, _ = closest_smetisce(voznik, smetisca, graph)
    _, time, _ = graph.astar(voznik.LVi, best_smetisce.LOi)
    time_spent += time
    
    voznik.LVi = best_smetisce.LOi
    
    _, time, _ = graph.astar(voznik.LVi, voznik.LVi_start)
    time_spent += time
    
    voznik.LVi = originalLVi
    
    return time_spent
    
@timer
def main(data, vozniki: List[Voznik], stranke: List[Stranka], smetisca: List[Odlagalisce], start_time, end_time, ime) -> None:
    
    d_mx = data["razdalje"]
    t_mx = data["casovne_razdalje"]
    
    graph = Graph(data)
    # graph.add_vozniki(vozniki)
    # graph.add_stranke(stranke)
    # graph.add_smetisca(smetisca)
    
    resitev = []

    vozniki_by_capacity = sort_vozniki_by_capacity(vozniki)
    
    for voznik in vozniki_by_capacity:
        voznik.time = start_time
        
        if voznik.Ki < 10:
            voznik.time = 480
            end_time = 960
            
        
        
        if not barrels_left(stranke): break
        
        while (voznik.time + voznik_next_sequence(voznik, stranke, smetisca, t_mx, graph) <= end_time):       #voznik.time < END_TIME:
            
            best_stranka, path_to_best_stranka = closest_stranka(voznik, stranke, graph)
            if path_to_best_stranka == None: break
            
            move_through_path(voznik, path_to_best_stranka, t_mx, graph)
            move_to_location(voznik, path_to_best_stranka[-1], t_mx)
            load(voznik, best_stranka)
            voznik.voznje.append(voznik.voznja.copy())
            
            if voznik.barrels < (voznik.Ki*0.66):
                best_stranka, path_to_best_stranka = closest_stranka(voznik, stranke, graph)
                if path_to_best_stranka != None:
                    
                    move_through_path(voznik, path_to_best_stranka, t_mx, graph)
                    move_to_location(voznik, path_to_best_stranka[-1], t_mx)
                    load(voznik, best_stranka)
                    voznik.voznje.append(voznik.voznja.copy())
                
            best_smetisce, path_to_best_smetisce = closest_smetisce(voznik, smetisca, graph)
            
            move_through_path(voznik, path_to_best_smetisce, t_mx, graph)
            move_to_location(voznik, path_to_best_smetisce[-1], t_mx)
            unload(voznik)
            voznik.voznje.append(voznik.voznja.copy())
            
        best_path_home, _, _ = graph.astar(voznik.LVi, voznik.LVi_start)
        move_through_path(voznik, best_path_home, t_mx, graph)
        move_to_location(voznik, best_path_home[-1], t_mx)
        voznik.voznja["DKi"] = 0
        voznik.voznje.append(voznik.voznja)

        for voznja in voznik.voznje:
            resitev.append(" ".join(map(str, list(voznja.values()))))
        
        
    with open(f"{ime}.txt", "w", encoding="utf-8") as f:
        f.write(f"{428802}\n")
        f.write(f"{data["ime_naloge"]}\n\n")
        f.write(f"{data["stevilka_testa"]}\n")
        f.write(f"{len(resitev)}\n")
        for r in resitev:
            f.write(f"{r}\n")


    
    
    
    

if __name__ == "__main__":
    
    st_naloge = input("St naloge: ")
    START_TIME = int(input("Start time: "))
    END_TIME = int(input("End time: "))  
    
    data = DataProcessor.loadFile(f"Data/odvoz0{st_naloge}.json")
    
    
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
        
    start_time = START_TIME
    end_time = END_TIME #1280 => 55.0 
    
    timer(main(data, vozniki, stranke, smetisca, start_time, end_time, "output"))
    
    stream = os.popen(rf".\Rtk24Odvoz.exe eval .\Inputs\odvoz0{data["stevilka_testa"]}.in output.txt report.txt")
    print(stream.read())
    


    
    