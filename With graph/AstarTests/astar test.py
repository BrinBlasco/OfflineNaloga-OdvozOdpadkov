import heapq

from DataParser import DataProcessor

class Graph:
    def __init__(self, distance_matrix, time_matrix):
        self.distance_matrix = distance_matrix
        self.time_matrix = time_matrix
        self.Ckm = 100
        
    def cost(self, current_id, next_id):
        # Cost function: Distance to travel between nodes
        return self.distance_matrix[current_id][next_id] * self.Ckm
    
    def heuristic(self, current_id, target_id):
        # Example heuristic: Euclidean distance between nodes
        return self.time_matrix[current_id][target_id]
    
    def astar(self, start_id, target_id):
        visited = set()
        heap = [(0, start_id)]  # (f-score, node_id)
        parent = {}
        g_score = {node_id: float('inf') for node_id in range(len(self.distance_matrix))}
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
                total_distance = sum(self.cost(path[i], path[i + 1]) for i in range(len(path) - 1)) // self.Ckm
                total_time = sum(self.time_matrix[path[i]][path[i + 1]] for i in range(len(path) - 1))

                return path, total_time, total_distance

            if current_id in visited:
                continue

            visited.add(current_id)

            for next_id, cost in enumerate(self.distance_matrix[current_id]):
                if cost == 0 or next_id in visited:
                    continue

                tentative_g_score = g_score[current_id] + self.cost(current_id, next_id)

                if tentative_g_score < g_score[next_id]:
                    parent[next_id] = current_id
                    g_score[next_id] = tentative_g_score
                    f_score = tentative_g_score + self.heuristic(next_id, target_id)
                    heapq.heappush(heap, (f_score, next_id))

        return None, None, None  # No path found

# Example usage:
if __name__ == "__main__":
    
    data = DataProcessor.loadFile("./Data/odvoz01.json")

    distance_matrix = data["razdalje"]  # Example distance matrix
    time_matrix = data["casovne_razdalje"] 
    Ckm = data["Ckm"]  # Example price per kilometer
    
    graph = Graph(distance_matrix,time_matrix)

    # Define your start and target nodes
    start_id = 44  # Example start node ID
    target_id = 49 # Example target node ID

    path, time, distance = graph.astar(start_id, target_id)
    if path:
        print("Best path:", path)
        print("Time spent:", time)
        print("Distance traveled:", distance)
        print(f"Time Normally from {path[0]} to {path[-1]} is", time_matrix[path[0]][path[-1]])
        print(f"Distance Normally from {path[0]} to {path[-1]} is", distance_matrix[path[0]][path[-1]])
    else:
        print("No path found")
