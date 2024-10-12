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

1. **Ustvarjanje virtualnega okolja:** Priporočljivo je ustvariti virtualno okolje za ločevanje knjižnic projekta. To naredite z naslednjim ukazom:

   ```bash
   python -m venv venv
   ```

   To omogoča, da so knjižnice specifične za ta projekt, kar preprečuje konflikte z drugimi projekti.
2. **Aktivacija virtualnega okolja:** Aktivirajte virtualno okolje:

   - Na Windows:

     ```bash
     venv\Scripts\activate
     ```
   - Na MacOS/Linux:

     ```bash
     source venv/bin/activate
     ```
3. **Namestitev zahtev:** Za namestitev vseh knjižnic zaženite naslednji ukaz:

   ```bash
   pip install -r requirements.txt
   ```
4. **Zagon glavnega skripta:** Zaženite glavni skript, ki vas bo vodil skozi nadaljnje korake:

   ```bash
   python main.py
   ```
5. **Lokacija izhoda:** Vsi rezultati bodo shranjeni v mapi `./Testing/`.

### Ocenjevanje:

Cena rešitve temelji na prevoženih kilometrih, neodpeljanih sodih, in kaznih za prekoračen delovni čas.
