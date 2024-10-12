## README

### Odvoz odpadkov - ACM Tekmovanje

Ta projekt rešuje problem optimizacije odvoza odpadkov, kjer je cilj minimizirati skupno ceno razporeda voženj. Cena vključuje prevoženo razdaljo, neodpeljane odpadke, in kazni za vožnje izven delovnega časa.

### Vhod:

- Lokacije strank, smetišč, voznikov
- Razdalje in časi med lokacijami
- Število sodov pri strankah in kapaciteta tovornjakov

### Izhod:

- Optimalen razpored voženj voznikov, ki minimizira ceno glede na dane kriterije.

### Postopek namestitve

1. **Namestitev zahtev:**
   Za namestitev vseh knjižnic zaženite naslednji ukaz:

   ```bash
   pip install -r requirements.txt
   ```
2. **Zagon glavnega skripta:**
   Zaženite glavni skript, ki vas bo vodil skozi nadaljnje korake:

   ```bash
   python main.py
   ```
3. **Lokacija izhoda:**
   Vsi rezultati bodo shranjeni v mapi `./Testing/`.

### Ocenjevanje:

Cena rešitve temelji na prevoženih kilometrih, neodpeljanih sodih, in kaznih za delovni čas.
