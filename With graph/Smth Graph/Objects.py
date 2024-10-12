

from typing import Dict, List, Tuple, Optional 
# from main import t_mx, COST_PER_KILOMETER

class Stranka:

    def __init__(self, podatki: Dict[str,int]) -> None:

        self.ID = podatki.setdefault("ID", -1)
        
        self.LSi = podatki["LSi"]
        self.Ni = podatki["Ni"]
        self.MSi = podatki["MSi"]
        self.CSi = podatki["CSi"]
        

class Voznik:

    def __init__(self, podatki, Ckm) -> None:

        self.ID = podatki.setdefault("ID", -1)
        
        self.LVi_start = podatki["LVi"]

        self.LVi_before = None
        self.LVi = podatki["LVi"]
  
        self.Ki = podatki["Ki"]
        self.MVi = podatki["MVi"]

        self.barrels = 0

        self.time = 0

        self.voznja = {
			"VVi" : 0, #(številka voznika; od 1 do V);
			"LZi" : 0, #(lokacija začetka vožnje; od 1 do L);
			"LKi" : 0, #(lokacija konca vožnje; od 1 do L);
			"TVi" : 0, #(čas začetka vožnje; od 0 do 1440);
			"DZi" : 0, #(sprememba v številu sodov na začetku vožnje, lahko tudi 0);
			"DKi" : 0  #(sprememba v številu sodov na koncu vožnje, lahko tudi 0).
		}
        
        self.voznje = []
        
        self.COST_PER_KILOMETER = Ckm

    # def best_client(self, stranke: List[Dict[str, int]], d_mtx: List[List[int]], t_mtx: List[List[int]]) -> Tuple[int, Stranka]:
        
    #     """_summary_

    #     Args:
    #         stranke (List[Dict[str, int]]): _description_
    #         d_mtx (List[List[int]]): _description_
    #         t_mtx (List[List[int]]): _description_

    #     Returns:
    #         Tuple[int, Stranka]: _description_
    #     """
        
    #     # for ID, stranka in stranke.items():
            
    #     #     client = Stranka(stranka)
    #     #     client.ID = ID
        
    #     best_time_distance_ratio = float('inf')
    #     max_barrels_picked_up = 0
        
    #     best_client = None

    #     for ID, stranka in stranke.items():
            
    #         client = Stranka(stranka)
    #         client.ID = ID
            
    #         travel_distance = self.get_gap(self.LVi, client.LSi, d_mtx)
    #         travel_cost = self.get_gap(self.LVi, client.LSi, t_mtx) * self.barrelsCOST_PER_KILOMETER
            
    #         travel_time = self.get_gap(self.LVi, client.LSi, t_mtx)
    #         time_distance_ratio = travel_time / travel_cost

    #         barrels_picked_up = min(client.Ni, self.Ki)

    #         if time_distance_ratio < best_time_distance_ratio or (time_distance_ratio == best_time_distance_ratio and barrels_picked_up > max_barrels_picked_up):
    #             best_client = client
    #             best_client.ID = ID
    #             best_time_distance_ratio = time_distance_ratio
    #             max_barrels_picked_up = barrels_picked_up
                
    #     try:
    #         return best_client.ID, best_client
    #     except Exception as e:
    #         print(e)
    #         exit()
    
    # def best_garbage_dump(self, smetisca: List[int], mtx: List[List[int]]) -> int:
        
    #     """_summary_

    #     Args:
    #         smetisca (List[int]): _description_
    #         d_mtx (List[List[int]]): _description_
    #         t_mtx (List[List[int]]): _description_

    #     Returns:
    #         int: _description_
    #     """


    #     idc ,closest = 0, float("inf")
    #     for idx, smetisce in enumerate(smetisca):
    #         gap = self.get_gap(self.LVi, smetisce, mtx) 
    #         if gap < closest: 
    #             closest = gap
    #             idc = idx
            
    #     return smetisca[idc]

    # def next(self, next_location: int, d_mtx, t_mtx, maximum_possible_barrels: Optional[int] = 0):
     
    #     voznja = []
    #     voznja.append(self.ID)

    #     time_next = self.get_gap(self.LVi, next_location, t_mtx)

    #     self.LVi_before = self.LVi
    #     voznja.append(self.LVi_before)

    #     self.LVi = next_location
    #     voznja.append(self.LVi)

    #     voznja.append(self.time)
    #     self.time += time_next


    #     #=========================== BARRELS ===========================#

    #     self.barrels_before = self.barrels
    #     voznja.append(0)

    #     self.barrels += min(self.Ki, maximum_possible_barrels)
    #     voznja.append(self.barrels-self.barrels_before)

    #     self.voznje.append(voznja)

    #     # VVi (številka voznika; od 1 do V);
    #     # LZi (lokacija začetka vožnje; od 1 do L);
    #     # LKi (lokacija konca vožnje; od 1 do L);
    #     # TVi (čas začetka vožnje; od 0 do 1440);
    #     # DZi (sprememba v številu sodov na začetku vožnje, lahko tudi 0);
    #     # DKi (sprememba v številu sodov na koncu vožnje, lahko tudi 0).

    # def get_gap(self, current: int, dest: int, mx: List[ List[int] ]):
        
    #     """
    #     Args:
    #         * takes in i for current
    #         * takes in j for next
    #         * takes in the matrix

    #     Returns:
    #         * The time or distance depending on the matrix that was passed in 
    #     """
    #     try:
    #         return mx[current-1][dest-1]
        
    #     except Exception as e:
            
    #         print(e, "Max index of the matrix: ", len(mx)-1, len(mx[0])-1)
    #         print("Index called i called:", current-1)
    #         print("Index called j called:", dest-1)
            
    #         print(">=====================================================<")
    #         print(e.with_traceback)
    #         exit() 
            