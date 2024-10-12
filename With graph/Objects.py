

class Voznik:
    def __init__(self, voznik_atts, Ckm):
        self.ID = voznik_atts.setdefault("ID", -1)
        self.LVi = voznik_atts["LVi"]
        self.Ki = voznik_atts["Ki"]
        self.MVi = voznik_atts["MVi"]
        self.Ckm = Ckm
        
        self.time = 0
        self.barrels = 0
        self.LVi_start = voznik_atts["LVi"]
        self.LVi_before = None
        
        self.voznja = {
			"VVi" : 0, #(številka voznika; od 1 do V);
			"LZi" : 0, #(lokacija začetka vožnje; od 1 do L);
			"LKi" : 0, #(lokacija konca vožnje; od 1 do L);
			"TVi" : 0, #(čas začetka vožnje; od 0 do 1440);
			"DZi" : 0, #(sprememba v številu sodov na začetku vožnje, lahko tudi 0);
			"DKi" : 0  #(sprememba v številu sodov na koncu vožnje, lahko tudi 0).
		}
        
        self.voznje = []
    
    
    def __repr__(self) -> str:
        return (f"{Voznik.__name__} {self.LVi_start}")
        

class Stranka:
    def __init__(self, stranka_atts):
        self.ID = stranka_atts.setdefault("ID", -1)
        self.LSi = stranka_atts["LSi"]
        self.Ni = stranka_atts["Ni"]
        self.MSi = stranka_atts["MSi"]
        self.CSi = stranka_atts["CSi"]
    
    def __repr__(self) -> str:
        return (f"{Stranka.__name__} {self.ID}")
        
        
class Odlagalisce:
    def __init__(self, lokacija):
        self.LOi = lokacija
        
    def __repr__(self) -> str:
        return (f"{Odlagalisce.__name__}")