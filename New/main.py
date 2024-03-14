from DataParser import DataProcessor
from pprint import pprint
from typing import List, Dict, Optional

data = DataProcessor.loadFile("Data/odvoz01.json")

#pprint(data)

COST_PER_KILOMETER = data["Ckm"]

def update_driver(driver: Dict[str, int], new_location: int, barrels: int, time, path):

    old_location = driver["LVi"]
    old_barrels = driver.get("barrels", 0)
    start = time
    change_barrels = barrels - old_barrels

    path = [driver["id"], old_location, new_location, start, old_barrels, change_barrels]
    print(" ".join(map(str, path)))

    driver["LVi"] = new_location
    driver["barrels"] = barrels

        
    


    # VVi (številka voznika; od 1 do V);
    # LZi (lokacija začetka vožnje; od 1 do L);
    # LKi (lokacija konca vožnje; od 1 do L);
    # TVi (čas začetka vožnje; od 0 do 1440);
    # DZi (sprememba v številu sodov na začetku vožnje, lahko tudi 0);
    # DKi (sprememba v številu sodov na koncu vožnje, lahko tudi 0).

def gap(mx, start, end):
    return mx[start][end]

def find_closest(voznik: Dict[str,int], entity: str, d_mx: List[List[int]], t_mx: List[List[int]]) -> Dict[str, int]:

    current = voznik["LVi"]
    match entity:
        case "smetisce":
            smetisca_lokacije = []

            for idx, el in enumerate(data["smetisce"]):
                if el == 1:
                    smetisca_lokacije.append(idx+1)

            i, d_closest = 0, float('inf')
            for idx, lokacija in enumerate(smetisca_lokacije):
                distance = gap(d_mx, current-1, lokacija-1)
                d_closest = min(d_closest, distance)
                i = idx if d_closest == distance else i
            
            return {
                "location": smetisca_lokacije[i], 
                "distance" : d_closest, 
                "time_required": t_mx[current-1][smetisca_lokacije[i]] # PLAC, POT, CAS
            } 
            
        # case "stranka":
        #     lokacije = []

        #     for stranka in data["stranke"]:
        #         if stranka["Ni"] == 0: continue
        #         lokacije.append( (list(stranka.values())[0], stranka) )
            
        #     i, closest = 0, float('inf')
        #     for idx, (lokacija, _) in enumerate(lokacije):
        #         closest = min(closest, d_mx[current-1][lokacija-1])
        #         i = idx if closest == d_mx[current-1][lokacija-1] else i

        #     dest = lokacije[i][0], lokacije[i][1]



def find_best(voznik: dict, stranke: List[Dict[str, int]], d_mx: List[List[int]], t_mx: List[List[int]]) -> Dict[int, int]:
    
 
    best_time_distance_ratio = float('inf')
    max_barrels_picked_up = 0

    for i, stranka in enumerate(stranke):
        travel_cost = d_mx[voznik['LVi'] - 1][stranka['LSi'] - 1] * COST_PER_KILOMETER
        
        travel_time = t_mx[voznik['LVi'] - 1][stranka['LSi'] - 1]

        time_distance_ratio = travel_time / (travel_cost / COST_PER_KILOMETER)

        barrels_picked_up = min(stranka['Ni'], voznik['Ki'])

        if time_distance_ratio < best_time_distance_ratio or (time_distance_ratio == best_time_distance_ratio and barrels_picked_up > max_barrels_picked_up):
            best_client = stranka
            best_time_distance_ratio = time_distance_ratio
            max_barrels_picked_up = barrels_picked_up

    return {
        "client": best_client, 
        "barrels": max_barrels_picked_up, 
        "time_required": travel_time
    }

def main():

    vozniki = data["vozniki"]
    stranke = data["stranke"]
    razdalje = data["razdalje"]
    casovne_razdalje = data["casovne_razdalje"]

    ZACETEK_VOZENJ = 480

    for i, voznik in enumerate(vozniki, start=1):
        voznik["id"] = i
        startVoznik = voznik["LVi"]

        best = find_best(voznik, stranke, razdalje, casovne_razdalje)

        update_driver(voznik, best["client"]["LSi"], best["barrels"], 480+best["time_required"], path=[])
        ZACETEK_VOZENJ += best["time_required"]

        disposal = find_closest(voznik, "smetisce", razdalje, casovne_razdalje)
        update_driver(voznik, disposal["location"], 0, disposal["time_required"], path=[])
        ZACETEK_VOZENJ += disposal["time_required"]

        update_driver(voznik, startVoznik, 0, gap(casovne_razdalje, voznik["LVi"], startVoznik), path=[])
        ZACETEK_VOZENJ = 480
        # write down first disposal location, we need it for the solution

if __name__ == "__main__":
    main()