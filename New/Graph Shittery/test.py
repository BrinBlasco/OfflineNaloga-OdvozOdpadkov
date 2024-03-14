from DataParser import DataProcessor

def calculate_best_client(driver, clients, time_matrix, distance_matrix, cost_per_km):
    # Initialize variables to keep track of the best client and its time/cost ratio
 
    best_time_cost_ratio = float('inf')
    max_barrels_picked_up = 0

    # Iterate through each client
    for i, client in enumerate(clients):
        # Calculate cost for traveling to the client
        travel_cost = distance_matrix[driver['LVi'] - 1][client['LSi'] - 1] * cost_per_km
        
        # Calculate time for traveling to the client
        travel_time = time_matrix[driver['LVi'] - 1][client['LSi'] - 1]

        # Calculate time/cost ratio
        time_cost_ratio = travel_time / travel_cost

        # Calculate how many barrels can be picked up
        barrels_picked_up = min(client['Ni'], driver['Ki'])

        # Update best client if the current client has a better time/cost ratio and picks up more barrels
        if time_cost_ratio < best_time_cost_ratio or (time_cost_ratio == best_time_cost_ratio and barrels_picked_up > max_barrels_picked_up):
            best_client = client
            best_time_cost_ratio = time_cost_ratio
            max_barrels_picked_up = barrels_picked_up

    # Return the index of the best client and its time/cost ratio
    return best_client, max_barrels_picked_up


data = DataProcessor.loadFile("Data/odvoz01.json")

# Example usage:
driver = data["vozniki"][2]
clients = data["stranke"]
time_matrix = data["casovne_razdalje"]
distance_matrix = data["razdalje"]

best_client, best_time_cost_ratio = calculate_best_client(driver, clients, time_matrix, distance_matrix, data["Ckm"])
if best_client is not None:
    print(f"The best client to move to from {driver} is at location {best_client} with a time/cost ratio of {best_time_cost_ratio}.")
else:
    print("No feasible client found.")