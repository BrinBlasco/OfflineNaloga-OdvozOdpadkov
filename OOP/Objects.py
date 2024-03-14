
import typing
from DataParser import DataProcessor

data = DataProcessor.loadFile("Data/testodvoz01.json")
COST_PER_KILOMETER = data["Ckm"]

class Stranka:

    def __init__(self, dictionary) -> None:
        self.dictionary = dictionary

        self.ID = dictionary.get("ID", None)
        self.LSi = dictionary["LSi"]
        self.Ni = dictionary["Ni"]
        self.MSi = dictionary["MSi"]
        self.CSi = dictionary["CSi"]

    def __str__(self) -> dict:
        return f"""
        Dict: {self.dictionary},
        Lokacija: {self.LSi}, 
        Stevilo Sodov: {self.Ni},
        Cena na neodpeljan sod: {self.CSi}, 
        Cena izven Delovnega Casa: {self.MSi}
        """

class Voznik:

    def __init__(self, dictionary) -> None:


        self.ID = None

        self.LVi = dictionary["LVi"]
        self.LVi_next = None

        self.Ki = dictionary["Ki"]
        self.MVi = dictionary["MVi"]

        self.barrels = 0
        self.barrels_next = None

        self.time = 0
        self.time_next = None


        self.dictionary = dictionary

    def best_client(self, stranke, d_mtx, t_mtx):
        
        best_time_distance_ratio = float('inf')
        max_barrel_picked_up = 0

        for ID, stranka in enumerate(stranke):
            
            client = Stranka(stranka)
            client.ID = ID

            travel_distance = d_mtx[self.LVi - 1][client.LSi - 1]
            travel_cost = d_mtx[self.LVi - 1][client.LSi - 1] * COST_PER_KILOMETER
            
            travel_time = t_mtx[self.LVi - 1][client.LSi - 1]

            time_distance_ratio = travel_time / (travel_cost / COST_PER_KILOMETER)

            barrels_picked_up = min(client.Ni, self.Ki)

            if time_distance_ratio < best_time_distance_ratio or (time_distance_ratio == best_time_distance_ratio and barrels_picked_up > max_barrels_picked_up):
                best_client = client
                best_time_distance_ratio = time_distance_ratio
                max_barrels_picked_up = barrels_picked_up
        
        return client.dictionary


    def next(self, next_location):

        # VVi (številka voznika; od 1 do V);
        # LZi (lokacija začetka vožnje; od 1 do L);
        # LKi (lokacija konca vožnje; od 1 do L);
        # TVi (čas začetka vožnje; od 0 do 1440);
        # DZi (sprememba v številu sodov na začetku vožnje, lahko tudi 0);
        # DKi (sprememba v številu sodov na koncu vožnje, lahko tudi 0).
        ...
        

    def __repr__(self):
        return f"""
        Dict: {self.dictionary}
        Lokacija: {self.LVi}, 
        Kapaciteta: {self.Ki}, 
        Cena izven Delovnega Casa: {self.MVi}
        """

#print(voznik.LVi.__dict__["dictionary"])


vozniki = data["vozniki"]
stranke = data["stranke"]
d_mtx = data["razdalje"]
t_mtx = data["casovne_razdalje"]

for voznikID, voznik in enumerate(vozniki, start=1):
    sofer = Voznik(voznik)
    sofer.ID = voznikID
    print(sofer.__dict__)
    sofer.zacetna_lokacija = sofer.LVi

    #print(sofer.best_client(stranke, d_mtx, t_mtx))




