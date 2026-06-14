# Zvonko – pametno školsko zvono

# Napomena o testnoj verziji

Aplikacija je izrađena kao studentski prototip za potrebe kolegija Projektiranje informacijskih sustava.  
Korisničko ime i lozinka služe samo za demonstraciju rada aplikacije i nisu namijenjeni za stvarnu produkcijsku upotrebu.

U stvarnoj verziji sustava bilo bi potrebno implementirati sigurniju autentikaciju, spremanje lozinki u zaštićenom obliku i naprednije korisničke uloge.

**Zvonko** je web aplikacija za upravljanje školskim zvonom. Aplikacija omogućuje administratoru škole pregled rasporeda, ručno i automatsko zvonjenje, uključivanje i isključivanje sustava, rad s osnovnom i srednjom školom te rad u jednoj ili dvije smjene.

Projekt je izrađen kao praktični rad za kolegij **Projektiranje informacijskih sustava**.

---

## Opis projekta

Cilj projekta je izraditi jednostavan informacijski sustav za upravljanje školskim zvonom putem web preglednika.

Aplikacija omogućuje:

* prijavu administratora
* uključivanje i isključivanje sustava zvonjenja
* ručno aktiviranje zvona
* automatsko zvonjenje prema rasporedu
* pregled tjednog rasporeda
* odabir pojedinog dana
* skraćeni raspored za odabrani dan
* rad s osnovnom i srednjom školom
* rad u jednoj ili dvije smjene
* evidenciju zvonjenja u JSON datoteci

---

## Tehnologije

U projektu su korištene sljedeće tehnologije:

* Python
* Flask
* HTML
* CSS
* JavaScript
* JSON
* GitHub

---

## Funkcionalnosti aplikacije

### Prijava u sustav

Aplikacija ima jednostavnu administratorsku prijavu.

Testni podaci za prijavu:

```text
Korisničko ime: admin
Lozinka: Skzvono.26
```

---

### Globalne postavke

Administrator može kroz web sučelje podesiti:

* tip škole
* uključivanje ili isključivanje sustava zvonjenja
* rad u jednoj ili dvije smjene

Aplikacija razlikuje:

* osnovnu školu
* srednju školu

Kod osnovne škole generira se **6 nastavnih sati**, dok se kod srednje škole generira **7 nastavnih sati**.

---

### Smjene

Aplikacija podržava rad u jednoj ili dvije smjene.

* prva smjena počinje u 08:00
* druga smjena počinje u 14:00

Ako je odabrana jedna smjena, prikazuje se samo raspored prve smjene.

Ako su odabrane dvije smjene, aplikacija prikazuje raspored prve i druge smjene.

---

### Skraćeni raspored

Za pojedini dan moguće je uključiti skraćeni raspored.

Kod normalnog rasporeda nastavni sat traje 45 minuta.

Kod skraćenog rasporeda nastavni sat traje 30 minuta.

U trenutnoj verziji skraćeni raspored vrijedi za cijeli odabrani dan. Odvojeno skraćivanje prve i druge smjene predviđeno je kao moguća buduća nadogradnja.

---

### Veliki odmor

Nakon drugog sata aplikacija računa veliki odmor.

Nakon velikog odmora sustav generira:

* zvono za ulazak nakon velikog odmora
* zvono za početak sljedećeg sata nakon 5 minuta

Primjer za prvu smjenu:

```text
09:35 - kraj 2. sata
09:50 - ulazak nakon velikog odmora
09:55 - početak 3. sata
```

---

### Ručno zvonjenje

Administrator može ručno aktivirati zvono klikom na gumb **Pozvoni!**.

Ručno zvonjenje se evidentira u datoteci:

```text
data/bell_log.json
```

---

### Automatsko zvonjenje

Aplikacija provjerava trenutno vrijeme i uspoređuje ga s rasporedom zvonjenja.

Ako se trenutno vrijeme poklapa s nekim vremenom iz rasporeda, sustav automatski aktivira zvono.

Sustav sprječava višestruko automatsko zvonjenje u istoj minuti.

---

## Struktura projekta

Primjer strukture projekta:

```text
school_bell_app/
│
├── app.py
├── requirements.txt
├── README.md
│
├── models/
│   ├── day_schedule.py
│   └── week_schedule.py
│
├── managers/
│   ├── settings_manager.py
│   ├── schedule_manager.py
│   └── bell_log_manager.py
│
├── templates/
│   ├── login.html
│   └── dashboard.html
│
├── static/
│   ├── style.css
│   ├── bell.svg
│   └── bell.mp3
│
└── data/
    ├── settings.json
    ├── schedule.json
    └── bell_log.json
```

---

## Opis važnijih datoteka

### app.py

Glavna Flask aplikacija.
Sadrži rute za prijavu, dashboard, ručno zvonjenje, provjeru statusa zvona i odjavu.

Glavne rute:

```text
/              - prijava korisnika
/dashboard     - glavna nadzorna ploča
/ring_bell     - ručno zvonjenje
/bell_status   - provjera statusa zvona
/logout        - odjava korisnika
```

---

### models/day_schedule.py

Sadrži klasu `DaySchedule`.

Ova klasa generira dnevni raspored sati i vremena zvonjenja.

Podržava:

* normalni raspored
* skraćeni raspored
* prvu smjenu
* drugu smjenu
* posebno zvono nakon velikog odmora

---

### models/week_schedule.py

Sadrži logiku za tjedni prikaz rasporeda.

Koristi se za prikaz radnih dana i navigaciju kroz tjedne.

---

### managers/settings_manager.py

Upravlja globalnim postavkama aplikacije.

Postavke se spremaju u:

```text
data/settings.json
```

Primjer postavki:

```json
{
    "system_enabled": true,
    "school_type": "secondary",
    "shift_mode": "double",
    "shortened_days": []
}
```

---

### managers/schedule_manager.py

Upravlja dnevnim postavkama rasporeda.

Primjer dnevne postavke je informacija je li za određeni dan uključen skraćeni raspored.

---

### managers/bell_log_manager.py

Upravlja evidencijom zvonjenja.

Događaji zvonjenja spremaju se u:

```text
data/bell_log.json
```

Primjer događaja:

```json
{
    "timestamp": "2026-06-13 18:07:27",
    "event_type": "manual",
    "label": "Ručno zvonjenje",
    "user": "Administrator"
}
```

---

## Pokretanje aplikacije

### 1. Kloniranje repozitorija

```bash
git clone https://github.com/USERNAME/NAZIV-REPOZITORIJA.git
```

Ulazak u folder projekta:

```bash
cd NAZIV-REPOZITORIJA
```

---

### 2. Kreiranje virtualnog okruženja

```bash
python -m venv venv
```

---

### 3. Aktiviranje virtualnog okruženja

Na Windows sustavu:

```bash
venv\Scripts\activate
```

Ako PowerShell blokira aktivaciju, može se koristiti:

```bash
cmd /k .\venv\Scripts\activate.bat
```

---

### 4. Instalacija potrebnih paketa

```bash
pip install -r requirements.txt
```

---

### 5. Pokretanje aplikacije

```bash
python app.py
```

---

### 6. Otvaranje aplikacije u pregledniku

Nakon pokretanja aplikacija je dostupna na adresi:

```text
http://127.0.0.1:5000
```

---

## requirements.txt

Datoteka `requirements.txt` treba sadržavati:

```text
Flask
```

---

## Testiranje

Tijekom testiranja provjerene su sljedeće funkcionalnosti:

| Test                             | Očekivani rezultat                                 |
| -------------------------------- | -------------------------------------------------- |
| Prijava s ispravnim podacima     | Otvara se dashboard                                |
| Prijava s pogrešnim podacima     | Prikazuje se poruka o pogrešci                     |
| Odabir osnovne škole             | Sustav prikazuje 6 sati                            |
| Odabir srednje škole             | Sustav prikazuje 7 sati                            |
| Odabir jedne smjene              | Prikazuje se samo prva smjena                      |
| Odabir dvije smjene              | Prikazuju se prva i druga smjena                   |
| Uključivanje skraćenog rasporeda | Sati traju 30 minuta                               |
| Ručno zvonjenje                  | Zvono se aktivira i zapisuje u log                 |
| Automatsko zvonjenje             | Sustav zvoni prema rasporedu                       |
| Navigacija po tjednima           | Moguće je pregledavati prethodni i sljedeći tjedan |

---

## Trenutna ograničenja

Aplikacija je izrađena kao studentski prototip i ima neka ograničenja:

* postoji samo jedan administratorski korisnik
* lozinka je definirana u kodu
* podaci se spremaju u JSON datoteke
* početak prve i druge smjene trenutno je definiran u kodu
* skraćeni raspored vrijedi za cijeli dan, a ne zasebno po smjenama
* fizičko zvono nije povezano u ovoj verziji

---

## Moguće nadogradnje

Moguće buduće nadogradnje sustava:

* ručni unos početka prve i druge smjene kroz web sučelje
* zasebno skraćivanje prve i druge smjene
* povezivanje s Raspberry Pi uređajem i relejem
* korištenje baze podataka umjesto JSON datoteka
* dodavanje više korisničkih uloga
* sigurnije spremanje korisničkih podataka
* pregledniji prikaz evidencije zvonjenja
* izvoz izvještaja u PDF ili Excel
* dodavanje kalendara praznika i neradnih dana
* automatska sinkronizacija vremena putem NTP-a

---

## Zaključak

Zvonko je web aplikacija koja prikazuje primjer jednostavnog informacijskog sustava za upravljanje školskim zvonom.

Projekt ima frontend i backend dio. Frontend omogućuje korisniku rad kroz web preglednik, dok backend obrađuje prijavu, postavke, generiranje rasporeda, ručno i automatsko zvonjenje te spremanje podataka.

Iako je aplikacija izrađena kao prototip, ona pokazuje kako se stvarni školski proces može digitalizirati i automatizirati. Uz dodatne nadogradnje sustav bi se mogao povezati s fizičkim zvonom i koristiti u stvarnom školskom okruženju.
