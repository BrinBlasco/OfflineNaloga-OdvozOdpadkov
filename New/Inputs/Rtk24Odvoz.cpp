#define _CRT_SECURE_NO_WARNINGS

#include <vector>
#include <unordered_set>
#include <tuple>
#include <algorithm>
#include <string>
#include <iostream>
#include <fstream>
#include <cmath>
#include <cstdlib>
#include <cstring>

using namespace std;

class EAssertion
{
public:
	string desc, file; int line;
	EAssertion(const string &desc_, const string &file_, const int line_) : desc(desc_), file(file_), line(line_) { }
	static inline bool Throw(const string &desc, const string &file, const int line) { throw EAssertion(desc, file, line); return false; }
};

#define Assert(x) ((x) ? true : EAssertion::Throw("Assertion failure (" #x ")", __FILE__, __LINE__))
#define AssertR(x, reason) ((x) ? true : EAssertion::Throw(string(reason).c_str(), __FILE__, __LINE__))
#define AssertU(x) AssertR((x), "Nepricakovana napaka.  Predlagamo, da obvestis organizatorje tekmovanja.")

string TaskName = "Odvoz";
enum { MaxCas = 1440, MaxVozenj = 10'000'000 };

bool Assert_(bool x, const char *file, const int line, const char *desc)
{
	if (!x)
		fprintf(stderr, "[%s:%d] Assertion failure (%s)\n", file, line, desc);
	return x;
}

void ParseLine(const string& s, vector<int> &v, bool allowNeg, int lineNo)
{
	v.clear(); int i = 0, n = (int) s.size();
	while (i < n)
	{
		if (isspace(s[i])) { i++; continue; }
		bool neg = (s[i] == '-'); if (neg) {
			AssertR(allowNeg, "namesto stevke se v " + to_string(lineNo) + ". vrstici pojavlja znak \'-\' (minus)");
			++i; AssertR(i < n, to_string(lineNo) + ". vrstica se konca z znakom \'-\' (minus)"); }
		AssertR(s[i] >= '0' && s[i] <= '9', "namesto stevke se v " + to_string(lineNo) + ". vrstici pojavlja znak s kodo " + to_string((unsigned char) s[i]));
		int x = s[i] - '0'; i++; if (neg) x = -x;
		auto M = neg ? numeric_limits<decltype(x)>::min() : numeric_limits<decltype(x)>::max();
		while (i < n && s[i] >= '0' && s[i] <= '9')
		{
			int d = s[i] - '0';
			if (neg) AssertR(x > M / 10 || (x == M / 10 && d <= -(M % 10)), "stevilo " + to_string(x) + string(1, s[i]) + " (v " + to_string(lineNo) + ". vrstici) je premajhno (manjse od " + to_string(M) + ")");
			else AssertR(x < M / 10 || (x == M / 10 && d <= M % 10), "stevilo " + to_string(x) + string(1, s[i]) + " (v " + to_string(lineNo) + ". vrstici) je preveliko (vecje od " + to_string(M) + ")");
			x = x * 10 + (neg ? -d : d); i++;
		}
		v.push_back(x);
	}
}

struct Reader
{
	istream &is;
	int lineNo;
	explicit Reader(istream &is_) : is(is_), lineNo() { }
	void ReadLine(string &line) { getline(is, line); ++lineNo; AssertR(!is.fail(), "manjka " + to_string(lineNo) + ". vrstica"); }
	void ReadLineOfInts(vector<int> &v, int howMany = -1, bool allowNeg = false) {
		string line; ReadLine(line); ParseLine(line, v, allowNeg, lineNo);
		if (howMany >= 0) AssertR(int(v.size()) == howMany, "v " + to_string(lineNo) + ". vrstici bi moralo biti " + to_string(howMany) + " stevil, ne pa " + to_string(v.size())); }
	void ReadEof() { string line; getline(is, line); ++lineNo; AssertR(is.fail(), "prisotna je tudi " + to_string(lineNo) + ". vrstica, pricakoval bi konec datoteke"); }
};

struct Stranka
{
	int lokacija; // 0..L-1
	int stSodov;
	//int casOd, casDo; // delovni cas
	enum { casOd = 480, casDo = 960 };
	int cenaN; // cena neodpeljanega soda
	int cenaMin; // cena vsake minute zunaj delovnega casa
};

struct Voznik
{
	int lokacija; // 0..L-1
	int kapaciteta;
	//int casOd, casDo; // delovni cas
	enum { casOd = 480, casDo = 960 };
	int cenaMin; // cena vsake minute zunaj delovnega casaa
};

class TTestCase
{
public:
	string problemName;
	int inputNo;
	int nLokacij, nVoznikov, nStrank; // L, V, S
	int cenaKm;
	vector<vector<int>> casVoznje, razdalja; // t_ij, d_ij
	vector<bool> jeSmetisce; // indeks: stevilka lokacije (0..L-1)
	vector<Stranka> stranke;
	vector<Voznik> vozniki;
	vector<int> strankaNaLokaciji; // -1, ce tam ni stranke, sicer 0..S-1

	void Read(Reader &reader)
	{
		// Preberimo ime naloge.
		reader.ReadLine(problemName);
		AssertR(problemName == TaskName, "v prvi vrstici bi moral biti niz \"" + TaskName + "\", ne pa \"" + problemName + "\"");
		// Preberimo stevilko testnega primera.
		vector<int> v; reader.ReadLineOfInts(v, 1, false); inputNo = v[0];
		// Preberimo stevilo lokacij, strank, voznikov in ceno prevozenega kilometra.
		reader.ReadLineOfInts(v, 4, false);
		nLokacij = v[0]; nStrank = v[1]; nVoznikov = v[2]; cenaKm = v[3];
		// Preberimo case voznje.
		casVoznje.resize(nLokacij); razdalja.resize(nLokacij);
		for (int i = 0; i < nLokacij; ++i) {
			reader.ReadLineOfInts(casVoznje[i], nLokacij, false);
			AssertR(casVoznje[i][i] == 0, "cas voznje od lokacije " + to_string(i + 1) + " do same sebe bi moral biti 0, ne pa " + to_string(casVoznje[i][i]));
			for (int j = 0; j < nLokacij; ++j) if (j != i) AssertR(casVoznje[i][j] != 0, "cas voznje od lokacije " + to_string(i + 1) + " do " + to_string(j + 1) + " bi moral biti razlicen od 0");  }
		// Preberimo razdalje.
		for (int i = 0; i < nLokacij; ++i) {
			reader.ReadLineOfInts(razdalja[i], nLokacij, false);
			AssertR(razdalja[i][i] == 0, "razdalja od lokacije " + to_string(i + 1) + " do same sebe bi morala biti 0, ne pa " + to_string(razdalja[i][i]));
			for (int j = 0; j < nLokacij; ++j) if (j != i) AssertR(razdalja[i][j] != 0, "razdalja od lokacije " + to_string(i + 1) + " do " + to_string(j + 1) + " bi morala biti razlicna od 0");  }
		// Preberimo podatke o smetiscih.
		reader.ReadLineOfInts(v, nLokacij, false);
		jeSmetisce.resize(nLokacij);
		for (int i = 0; i < nLokacij; ++i) {
			AssertR(v[i] == 0 || v[i] == 1, "podatek o tem, ali je " + to_string(i + 1) + ". lokacija smetisce, bi moral biti 0 ali 1, ne pa " + to_string(v[i]));
			jeSmetisce[i] = (v[i] == 1); }
		// Preberimo podatke o strankah.
		stranke.resize(nStrank); strankaNaLokaciji.resize(nLokacij);
		for (int i = 0; i < nLokacij; ++i) strankaNaLokaciji[i] = -1;
		for (int i = 0; i < nStrank; ++i)
		{
			auto &S = stranke[i]; reader.ReadLineOfInts(v, 4, false);
			S.lokacija = v[0]; AssertR(S.lokacija >= 1 && S.lokacija <= nLokacij, "lokacija " + to_string(i + 1) + ". stranke bi morala biti med 1 in " + to_string(nLokacij) + ", ne pa " + to_string(S.lokacija));
			AssertR(! jeSmetisce[S.lokacija - 1], to_string(i + 1) + ". stranka je na lokaciji " + to_string(S.lokacija) + ", tam pa je ze smetisce");
			AssertR(strankaNaLokaciji[S.lokacija - 1] < 0, to_string(i + 1) + ". stranka je na lokaciji " + to_string(S.lokacija) + ", tam pa je ze " + to_string(strankaNaLokaciji[S.lokacija - 1] + 1) + ". stranka");
			--S.lokacija; strankaNaLokaciji[S.lokacija] = i;
			//S.stSodov = v[1]; S.casOd = v[2]; S.casDo = v[3]; S.cenaN = v[4]; S.cenaMin = v[5];
			S.stSodov = v[1]; S.cenaN = v[2]; S.cenaMin = v[3];
			AssertR(S.casOd <= S.casDo, "konec delovnega casa " + to_string(i + 1) + ". stranke (" + to_string(S.casDo) + ") ne sme biti pred zacetkom (" + to_string(S.casOd) + ")");
			AssertR(0 <= S.casOd && S.casOd <= S.casDo && S.casDo <= MaxCas, "delovni cas " + to_string(i + 1) + ". stranke je [" + to_string(S.casOd) + ", " + to_string(S.casDo) + "], moral pa bi biti znotraj [0, " + to_string(MaxCas) + "]");
		}
		// Preberimo podatke o voznikih.
		vozniki.resize(nVoznikov);
		for (int i = 0; i < nVoznikov; ++i)
		{
			auto &V = vozniki[i]; reader.ReadLineOfInts(v, 3, false);
			V.lokacija = v[0]; AssertR(V.lokacija >= 1 && V.lokacija <= nLokacij, "lokacija " + to_string(i + 1) + ". voznika bi morala biti med 1 in " + to_string(nLokacij) + ", ne pa " + to_string(V.lokacija));
			--V.lokacija; V.kapaciteta = v[1]; V.cenaMin = v[2]; // V.casOd = v[2]; V.casDo = v[3]; V.cenaMin = v[4];
			AssertR(V.casOd <= V.casDo, "konec delovnega casa " + to_string(i + 1) + ". voznika (" + to_string(V.casDo) + ") ne sme biti pred zacetkom (" + to_string(V.casOd) + ")");
			AssertR(0 <= V.casOd && V.casOd <= V.casDo && V.casDo <= MaxCas, "delovni cas " + to_string(i + 1) + ". voznika je [" + to_string(V.casOd) + ", " + to_string(V.casDo) + "], moral pa bi biti znotraj [0, " + to_string(MaxCas) + "]");
		}
		reader.ReadEof();
	}
};

struct Voznja
{
	int lineNo; // stevilka vrstice v tekmovalcevi izhodni datoteki (1-based)
	int stVoznje; // zaporedna stevilka voznje (0-based) pri tej resitvi, preden smo voznje preuredili po vozniku in po casu
	int stVoznika; // 0..S-1
	int lokZac, lokKon; // 0..L-1
	int deltaZac, deltaKon; // sprememba v stevilu sodov na tovornjaku
	int casZac, casKon; // 0..1440
};

struct Rezultat
{
	int caseNo;
	long long int
		skupajKm, // skupaj prevozenih kilometrov
		cenaPrevozenihKm, // cena prevozenih kilometrov
		stNepobranih, // skupno stevilo nepobranih sodov
		cenaNepobranih, // skupna cena nepobranih sodov
		cenaNadurVoznikov, // dodatek k ceni zaradi vozenj zunaj delovnega casa voznikov
		cenaNadurStrank, // dodatek k ceni zaradi pobiranja sodov zunaj delovnega casa strank
		cena; // skupna cena te resitve
};

class TResitev
{
public:
	int userId; // 6 digits
	int caseNo;
	const TTestCase *testCase;
	int nVozenj;
	int nVoznikov, nLokacij, nStrank;
	vector<Voznja> voznje;

	void PreberiInOceni(Reader &reader, int caseNo_, const TTestCase& testCase_, bool dovoliPrevelikeCase, Rezultat &rezultat)
	{
		caseNo = caseNo_; rezultat.caseNo = caseNo;
		testCase = &testCase_;
		nVoznikov = testCase->nVoznikov; nLokacij = testCase->nLokacij; nStrank = testCase->nStrank;
		vector<int> v; reader.ReadLineOfInts(v, 1, false);
		nVozenj = v[0]; AssertR(nVozenj <= MaxVozenj, "preveliko stevilo vozenj v " + to_string(reader.lineNo) + ". vrstici: " + to_string(nVozenj) + ", max = " + to_string(MaxVozenj));
		// Preberimo voznje.
		voznje.clear(); voznje.resize(nVozenj);
		for (int i = 0; i < nVozenj; ++i)
		{
			auto &V = voznje[i]; V.stVoznje = i;
			reader.ReadLineOfInts(v, 6, true); V.lineNo = reader.lineNo;
			V.stVoznika = v[0]; AssertR(V.stVoznika >= 1 && V.stVoznika <= nVoznikov, "v " + to_string(reader.lineNo) + ". vrstici je stevilka voznika " + to_string(V.stVoznika) + " namesto od 1 do " + to_string(nVoznikov));
			V.lokZac = v[1]; AssertR(V.lokZac >= 1 && V.lokZac <= nLokacij, "v " + to_string(reader.lineNo) + ". vrstici je stevilka zacetne lokacije " + to_string(V.lokZac) + " namesto od 1 do " + to_string(nLokacij));
			V.lokKon = v[2]; AssertR(V.lokKon >= 1 && V.lokKon <= nLokacij, "v " + to_string(reader.lineNo) + ". vrstici je stevilka koncne lokacije " + to_string(V.lokKon) + " namesto od 1 do " + to_string(nLokacij));
			AssertR(V.lokZac != V.lokKon, "v " + to_string(reader.lineNo) + ". vrstici sta zacetna in koncna lokacija enaki (" + to_string(V.lokZac) + ") namesto razlicni");
			--V.stVoznika; --V.lokZac; --V.lokKon;
			V.casZac = v[3]; AssertR(V.casZac >= 0 && (V.casZac <= MaxCas || dovoliPrevelikeCase), "v " + to_string(reader.lineNo) + ". vrstici je cas zacetka voznje " + to_string(V.casZac) + " namesto od 0 do " + to_string(MaxCas));
			int casVoznje = testCase->casVoznje[V.lokZac][V.lokKon];
			V.casKon = V.casZac + casVoznje;
			AssertR(V.casKon > V.casZac && (V.casKon <= MaxCas || dovoliPrevelikeCase), "v " + to_string(reader.lineNo) + ". vrstici je cas konca voznje " + to_string(V.casKon) + " (= cas zacetka " + to_string(V.casZac) + " + cas voznje " + to_string(casVoznje) + ") namesto od " + to_string(V.casZac + 1) + " do " + to_string(MaxCas));
			V.deltaZac = v[4]; V.deltaKon = v[5];
		}
		// Za vsako stranko bomo racunali stevilo pobranih sodov in cas prvega in zadnjega pobiranja.
		struct StanjeStranke { long long int pobranih = 0; int minCas, maxCas; };
		vector<StanjeStranke> stranke(nStrank);
		for (int i = 0; i < nStrank; ++i) {
			stranke[i].minCas = testCase->stranke[i].casOd;
			stranke[i].maxCas = testCase->stranke[i].casDo; }
		// Uredimo voznje po vozniku in po casu.
		sort(voznje.begin(), voznje.end(), [] (const Voznja& x, const Voznja& y) { return (x.stVoznika < y.stVoznika) || (x.stVoznika == y.stVoznika && x.casZac < y.casZac); });
		rezultat.cena = 0; rezultat.skupajKm = 0;
		rezultat.stNepobranih = 0; rezultat.cenaNepobranih = 0;
		rezultat.cenaNadurStrank = 0; rezultat.cenaNadurVoznikov = 0;
		for (int i = 0; i < nVozenj; )
		{
			const int stVoznika = voznje[i].stVoznika;
			const int lokVoznika = testCase->vozniki[stVoznika].lokacija;
			auto &voznik = testCase->vozniki[stVoznika];
			int j = i; while (j < nVozenj && voznje[j].stVoznika == stVoznika) ++j;
			// Preverimo, ce voznik zacne in konca na pravi lokaciji.
			AssertR(voznje[i].lokZac == lokVoznika, "prva voznja voznika " + to_string(stVoznika + 1) + " (v " + to_string(voznje[i].lineNo) + ". vrstici) bi se morala zaceti na lokaciji " + to_string(lokVoznika + 1) + ", ne pa na " + to_string(voznje[i].lokZac + 1));
			AssertR(voznje[j - 1].lokKon == lokVoznika, "zadnja voznja voznika " + to_string(stVoznika + 1) + " (v " + to_string(voznje[j - 1].lineNo) + ". vrstici) bi se morala koncati na lokaciji " + to_string(lokVoznika + 1) + ", ne pa na " + to_string(voznje[j - 1].lokKon + 1));
			// Preverimo, ce se vsaka voznja zacne tam, kjer se je prejsnja nehala,
			// in da se po casu ne prekrivajo.
			for (int k = i + 1; k < j; ++k)
			{
				auto &V1 = voznje[k - 1], &V2 = voznje[k];
				AssertR(V1.lokKon == V2.lokZac, "naslednja voznja voznika " + to_string(stVoznika + 1) + " (v " + to_string(V2.lineNo) + ". vrstici) se zacne na lokaciji " + to_string(V2.lokZac + 1) + ", prejsnja voznja istega voznika (v " + to_string(V1.lineNo) + ". vrstici) pa se je koncala na lokaciji " + to_string(V1.lokKon + 1));
				AssertR(V1.casKon <= V2.casZac, "naslednja voznja voznika " + to_string(stVoznika + 1) + " (v " + to_string(V2.lineNo) + ". vrstici) se zacne ob casu " + to_string(V2.casZac) + ", prejsnja voznja istega voznika (v " + to_string(V1.lineNo) + ". vrstici) pa se je koncala ob casu " + to_string(V1.casKon));
			}
			// Preverimo, da ne preseze kapacitete tovornjaka ali ne poskusi odloziti vec sodov, kot jih ima na njem.
			// Pri tem tudi preverimo, da pobira le pri strankah in odlaga le na smetiscih.
			long long int stSodov = 0;
			for (int k = i; k < j; ++k)
			{
				auto &V = voznje[k];
				rezultat.skupajKm += testCase->razdalja[V.lokZac][V.lokKon];
				for (int pass = 1; pass <= 2; ++pass)
				{
					int lokacija = (pass == 1) ? V.lokZac : V.lokKon;
					long long int delta = (pass == 1) ? V.deltaZac : V.deltaKon;
					if (delta > 0) {
						int stranka = testCase->strankaNaLokaciji[lokacija]; AssertR(stranka >= 0, "v " + to_string(V.lineNo) + ". vrstici naj bi voznik na " + (pass == 1 ? "zacetni" : "koncni") + " lokaciji " + to_string(lokacija + 1) + " pobral " + to_string(delta) + " sodov, toda tam ni nobene stranke");
						auto &S = stranke[stranka];
						S.pobranih += delta; stSodov += delta;
						AssertR(stSodov <= voznik.kapaciteta, "v " + to_string(V.lineNo) + ". vrstici bi voznik na " + (pass == 1 ? "zacetni" : "koncni") + " lokaciji " + to_string(lokacija + 1) + " pobral " + to_string(delta) + " sodov, s tem bi jih imel " + to_string(stSodov) + ", kar je vec od njegove kapacitete (" + to_string(voznik.kapaciteta) + ")");
						// Ce voznik na tej lokaciji stoji, upostevajmo tak cas pobiranja, ki je najblizje delovnemu casu stranke.
						int stojiOd = (pass == 1) ? V.casZac : V.casKon; int stojiDo = stojiOd;
						if (pass == 1 && k > i) stojiOd = voznje[k - 1].casKon;
						if (pass == 2 && k < j - 1) stojiDo = voznje[k + 1].casZac;
						if (stojiDo < S.minCas) S.minCas = stojiDo;
						if (stojiOd > S.maxCas) S.maxCas = stojiOd; }
					else if (delta < 0) {
						AssertR(testCase->jeSmetisce[lokacija], "v " + to_string(V.lineNo) + ". vrstici bi voznik na " + (pass == 1 ? "zacetni" : "koncni") + " lokaciji " + to_string(lokacija + 1) + " odlozil " + to_string(-delta) + " sodov, toda tam ni smetisca");
						AssertR(stSodov >= -delta, "v " + to_string(V.lineNo) + ". vrstici bi voznik na " + (pass == 1 ? "zacetni" : "koncni") + " lokaciji " + to_string(lokacija + 1) + " odlozil " + to_string(-delta) + " sodov, toda na tovornjaku jih ima le " + to_string(stSodov));
						stSodov += delta; }
				}
			}
			AssertR(stSodov == 0, "voznik " + to_string(stVoznika + 1) + " ima na koncu " + to_string(stSodov) + " sodov namesto 0");
			// Ce bo moral voziti zunaj delovnega casa, pristejmo to k ceni resitve.
			rezultat.cenaNadurVoznikov += max(voznik.casOd - voznje[i].casZac, 0) * ((long long) voznik.cenaMin);
			rezultat.cenaNadurVoznikov += max(voznje[j - 1].casKon - voznik.casDo, 0) * ((long long) voznik.cenaMin);
			// Premaknimo se na naslednjega voznika.
			i = j;
		}
		// Preverimo se, da ni bilo pri kaksni stranki pobranih vec sodov, kot jih je na voljo.
		for (int i = 0; i < nStrank; ++i)
		{
			auto &S = stranke[i]; auto &S2 = testCase->stranke[i];
			AssertR(S.pobranih <= S2.stSodov, "pri stranki " + to_string(i + 1) + "(na lokaciji " + to_string(testCase->stranke[i].lokacija + 1) + ") je bilo pobranih " + to_string(S.pobranih) + " sodov, toda ta stranka ima le " + to_string(S2.stSodov) + " sodov");
			// Ce so pobirali zunaj delovnega casa, pristejmo to k ceni resitve.
			rezultat.cenaNadurStrank += max(S2.casOd - S.minCas, 0) * ((long long) S2.cenaMin);
			rezultat.cenaNadurStrank += max(S.maxCas - S2.casDo, 0) * ((long long) S2.cenaMin);
			rezultat.stNepobranih += S2.stSodov - S.pobranih;
			rezultat.cenaNepobranih += (S2.stSodov - S.pobranih) * ((long long) S2.cenaN);
		}
		//
		rezultat.cenaPrevozenihKm = rezultat.skupajKm * testCase->cenaKm;
		rezultat.cena = rezultat.cenaPrevozenihKm + rezultat.cenaNadurStrank + rezultat.cenaNadurVoznikov + rezultat.cenaNepobranih;
	}
};

int PrintHelp()
{
	printf("Uporaba: Rtk24Odvoz eval input.txt submission.txt report.txt\n");
	printf("  V imenu vhodne datoteke (\"input.txt\") sme biti tudi znak \"*\", ki ga bo\n");
	printf("  ocenjevalni program zamenjal z dvomestno stevilko testnega primera.  To je lahko koristno,\n");
	printf("  ce je v oddani datoteki (\"submission.txt\") vec resitev za razlicne testne primere,n");
	printf("  saj je vsak testni primer v loceni vhodni datoteki.");
	return 1;
}

int Evaluate(int argc, char **argv)
{
	if (argc < 5) return PrintHelp();
	const char *fnTestCase = argv[2], *fnSubmission = argv[3], *fnReport = argv[4];
	int nTestCases = -1; if (argc > 5) { int ok = sscanf(argv[5], "%d", &nTestCases); if (ok != 1) nTestCases = -1; }
	FILE *fReport = fopen(fnReport, "wt");
	try
	{
		vector<TTestCase> testCases;
		//ReadTestCases(fnTestCase, testCases);
		//int nTestCases = (int)testCases.size();
		vector<Rezultat> results;
		{
			ifstream is(fnSubmission);
			Reader reader(is);
			// Preberimo stevilko tekmovalca.
			string s; reader.ReadLine(s);
			AssertR(s.size() == 6, "stevilka tekmovalca bi morala imeti 6 stevk");
			for (int i = 0; i < s.size(); ++i) AssertR(s[i] >= '0' && s[i] <= '9', "stevilka tekmovalca bi morala imeti 6 stevk");
			int userId; int ok = sscanf(s.c_str(), "%d", &userId);
			AssertR(ok == 1, "v prvi vrstici bi morala biti stevilka tekmovalca, ne pa \"" + s + "\"");
			// Preberimo ime naloge.
			reader.ReadLine(s);
			AssertR(s == TaskName, "v drugi vrstici bi moral biti niz \"" + TaskName + "\", ne pa \"" + s + "\"");
			//
			int nSubmissions = 0, lineNo = 3;
			while (true)
			{
				getline(is, s); if (is.fail()) break;
				++reader.lineNo;
				if (s.length() <= 0) continue; // prazna vrstica med resitvami
				int caseNo; ok = sscanf(s.c_str(), "%d", &caseNo);
				AssertR(ok == 1, "v " + to_string(reader.lineNo) + ". vrstici bi morala biti stevilka testnega primera, ne pa \"" + s + "\"");
				if (nTestCases >= 0) AssertR(caseNo >= 1 && caseNo <= nTestCases, "v " + to_string(reader.lineNo) + ". vrstici bi morala biti stevilka testnega primera od 1 do " + to_string(nTestCases) + ", ne pa " + to_string(caseNo));
				int iCase = -1; for (int i = 0; i < (int)testCases.size(); i++) if (testCases[i].inputNo == caseNo) { iCase = i; break; }
				if (iCase < 0)
				{
					// Ocitno tega testnega primera se nismo nalozili, pa ga dajmo zdaj.
					string ime = fnTestCase; auto zvezdica = ime.find('*');
					if (zvezdica != string::npos) { char buf[100]; sprintf(buf, "%02d", caseNo); ime = ime.substr(0, zvezdica) + buf + ime.substr(zvezdica + 1); }
					ifstream is2(ime);
					AssertR(is2.is_open(), "napaka pri odpiranju vhodne datoteke \"" + ime +  "\" za testni primer stevilka " + to_string(caseNo));
					Reader reader2(is2);
					iCase = (int) testCases.size(); testCases.push_back({});
					auto &tc = testCases.back();
					tc.Read(reader2);
					AssertR(tc.inputNo == caseNo, "v vhodni datoteki \"" + ime + "\" sem pricakoval testni primer " + to_string(caseNo) + ", bil pa je " + to_string(tc.inputNo));
				}
				AssertR(iCase >= 0, "v " + to_string(lineNo) + ". vrstici se pojavlja neveljavna stevilka testnega primera: " + to_string(caseNo));
				// Preberimo in ocenimo naslednjo resitev in si zapomnimo rezultat.
				TResitev resitev; Rezultat rezultat;
				TTestCase &testCase = testCases[iCase];
				resitev.PreberiInOceni(reader, caseNo, testCase, false, rezultat);
				results.push_back(rezultat);
				//
				nSubmissions++;
			}
		}
		fprintf(fReport, "OK\n%d\n", int(results.size()));
		for (int i = 0; i < int(results.size()); i++)
		{
			Rezultat &R = results[i]; fprintf(fReport, "%d %lld %lld %lld %lld %lld %lld %lld\n", R.caseNo,
				R.cena, R.cenaNadurStrank, R.cenaNadurVoznikov, R.cenaNepobranih, R.cenaPrevozenihKm, R.skupajKm, R.stNepobranih);
			printf("Testni primer %d: cena %lld, od tega %lld za nadure strank, %lld za nadure voznikov, \n"
					"   %lld za nepobrane sode (ki jih je %lld), %lld za prevozene km (ki jih je %lld).\n",
				R.caseNo, R.cena, R.cenaNadurStrank, R.cenaNadurVoznikov, R.cenaNepobranih, R.stNepobranih, R.cenaPrevozenihKm, R.skupajKm);
		}
	}
	catch (EAssertion e)
	{
		fprintf(fReport, "Napaka [%s:%d]: %s\n-1\n", /*e.file.c_str()*/ "Rtk24Odvoz.cpp", e.line, e.desc.c_str());
	}
	catch (...)
	{
		fprintf(fReport, "Nepricakovana napaka.  Predlagamo, da obvestis organizatorje tekmovanja.\n-1\n");
	}
	fclose(fReport);
	return 0;
}


int main(int argc, char** argv)
{
	if (argc > 1 && strcmp(argv[1], "eval") == 0) return Evaluate(argc, argv);
	PrintHelp();
	return 0;
}
