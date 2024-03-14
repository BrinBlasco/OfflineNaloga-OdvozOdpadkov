from DataParser import DataProcessor
from pprint import pprint
from typing import List

data = DataProcessor.loadFile("Data/testodvoz01.json")

pprint(data)


def find_closest(voznik: int, entity: str, mx: List[List[int]], o_mx):

    current = voznik["LVi"]

    match entity:
        case "smetisce":
            smetisca_lokacije = []

            for idx, el in enumerate(data["smetisce"]):
                if el == 1:
                    smetisca_lokacije.append(idx+1)

            i, closest = 0, float('inf')
            for idx, lokacija in enumerate(smetisca_lokacije):
                closest = min(closest, mx[current-1][lokacija-1])
                i = idx if closest == mx[current-1][lokacija-1] else i
            

            dest = {
                "Smetisce" : smetisca_lokacije[i],
                "distance_to_node" : closest,
                "time_to_node" : o_mx[current][smetisca_lokacije[i]]
            }

            
        case "stranka":
            lokacije = []
            for stranka in data["stranke"]:
                if stranka["Ni"] == 0: continue
                lokacije.append(list(stranka.values())[0])
            
            i, closest = 0, float('inf')
            for idx, lokacija in enumerate(lokacije):
                closest = min(closest, mx[current-1][lokacija-1])
                i = idx if closest == mx[current-1][lokacija-1] else i
            
            dest = {
                "Stranka" : lokacije[i],
                "distance_to_node" : closest,
                "time_to_node" : o_mx[current][lokacije[i]],
                "barrels_count" : 
            }
    
    return dest


vozniki = data["vozniki"]
razdalje = data["razdalje"]
casovne_razdalje = data["casovne_razdalje"]


for voznik in vozniki:
    time = 480
    zacetna = voznik["LVi"]
    print("Zacetna voznika", zacetna)
    while time <= 960:

        closest_node = find_closest(voznik, "stranka", razdalje, casovne_razdalje)
        print("Do stranke: ")
        print(voznik["LVi"], "->", closest_node, end="\n\n")
        voznik["LVi"] = closest_node["Stranka"]
        time+=closest_node["time_to_node"]
        

        closest_node = find_closest(voznik, "smetisce", razdalje, casovne_razdalje)
        print("Do smetisca: ")
        print(voznik["LVi"], "->", closest_node, end="\n\n")
        voznik["LVi"] = closest_node["Smetisce"]
        time += closest_node["time_to_node"]

    closest_node = {
        "Node" : zacetna,
        "distance_to_node" : razdalje[voznik["LVi"]][zacetna],
        "time_to_node" : casovne_razdalje[voznik["LVi"]][zacetna]
    }

    print("Nazaj na zacetno lokacijo: ")
    print(voznik["LVi"], "->", closest_node)
    voznik["LVi"] = zacetna
    time += closest_node["time_to_node"]

    print("Time at the end of driving", time, "\n")
    print("Cost of overtime", time*voznik["MVi"])
    


	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	