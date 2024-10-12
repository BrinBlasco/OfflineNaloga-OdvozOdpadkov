import heapq

class Node:
    def __init__(self, node_id):
        self.id = node_id

class Graph:
    def __init__(self, data):
        self.nodes = {}
        self.locations = data["L"]
        self.time_matrix = data["casovne_razdalje"]
        self.distance_matrix = data["razdalje"]
        self.Ckm = data["Ckm"]  # Assuming you have this value in your data

        for i in range(1, self.locations + 1):
            self.nodes[i] = Node(i)

    def cost(self, current_id, next_id):
        # Cost function: Distance to travel between nodes
        return self.distance_matrix[current_id - 1][next_id - 1] * self.Ckm

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
                total_distance = sum(self.cost(path[i], path[i + 1]) for i in range(len(path) - 1)) // self.Ckm
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

# Example usage:
data = {
    "L": 5,
    "casovne_razdalje": [
        [0, 2, 4, 0, 0],
        [2, 0, 1, 5, 0],
        [4, 1, 0, 8, 2],
        [0, 5, 8, 0, 3],
        [0, 0, 2, 3, 0]
    ],
    "razdalje": [
        [0, 10, 15, 0, 0],
        [10, 0, 20, 25, 0],
        [15, 20, 0, 30, 5],
        [0, 25, 30, 0, 10],
        [0, 0, 5, 10, 0]
    ],
    "Ckm": 10
}

graph = Graph(data)
path, total_time, total_distance = graph.astar(1, 5)
print("Path:", path)
print("Total Time:", total_time)
print("Total Distance:", total_distance)