import json
class DataProcessor:
    
    #? ime_naloge, stevilka_testa, L, S, V, Ckm, casovne_razdalje, razdalje, smetisce, stranke, vozniki
    
    @staticmethod
    def loadFile(path_to_file):
        with open(f"{path_to_file}", 'r') as f:
            data = json.load(f)
            return data
    
    @staticmethod
    def parseInput(path_to_input):
        with open(f"{path_to_input}", 'r') as f:
        
            #data[0] = ime
            #data[1] = st naloge
            #data[2] = L, S, V, Ckm
            #data[3:3+L] = casovne razdalje (od 3 dalje do 3+L)
            #data[3+L:3+L*2] = razdalje (od 3+L dalje do 3+L*2)
            #data[3+L*2] = smetisca (na indeksu 3+2*L, takoj po razdaljah)
            #data[4+L*2:4+L*2+S] = stranke (od 4+L*2 dalje do 4+L*2+S)
            #data[5+2*L+S:5+2*L+S+V] = vozniki (od 5+L*2+S dalje do 5+2*L+S+V, takoj po strankah)
            
            data = [d.strip('\n') for d in f.readlines()]
            ime_naloge = data[0]
            stevilka_testa = int(data[1])
            L, S, V, Ckm = map(int, data[2].split())
            casovne_razdalje = [list(map(int, line.split())) for line in data[3:3+L]]
            razdalje = [list(map(int, line.split())) for line in data[3+L:3+2*L]]
            smetisca = list(map(int, data[3+2*L].split()))
            strankePos = [tuple(map(int, line.split())) for line in data[4+2*L:4+2*L+S]]
            voznikiPos = [tuple(map(int, line.split())) for line in data[4+2*L+S:]]

            stranke = [None for i in range(S)]
            vozniki = [None for i in range(V)]

            for i in range(S):
                stranke[i] = {
                    "LSi" : strankePos[i][0],
                    "Ni" : strankePos[i][1], 
                    "CSi" : strankePos[i][2],
                    "MSi" : strankePos[i][3] 
                }

            for i in range(V):
                vozniki[i] = {
                    "LVi" : voznikiPos[i][0],
                    "Ki" : voznikiPos[i][1], 
                    "MVi" : voznikiPos[i][2]
                }
        


        processed_data = {
            "ime_naloge": ime_naloge,
            "stevilka_testa": stevilka_testa,
            "L": L,
            "S": S,
            "V": V,
            "Ckm": Ckm,
            "casovne_razdalje": casovne_razdalje,
            "razdalje": razdalje,
            "smetisca": smetisca,
            "stranke" : stranke,
            "vozniki" : vozniki
        }
        
        newOut = path_to_input[:-3].split("/")[1]
        with open(f"Data/{newOut}.json", "x") as f:
            json.dump(processed_data, f)
        
