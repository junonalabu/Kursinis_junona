# Kursinis darbas "Tic-Tac-Toe"
## 1. Introduction
Šis projektas – tai klasikinio žaidimo **Kryžiukai-Nuliukai** („Tic-Tac-Toe“) realizacija Python programavimo kalba, naudojant **objektinio programavimo (OOP)** principus.
### Tikslas
Norėjau pademonstruoti visus pagrindinius objektinio programavimo principus, taip pat pirmą kartą išbandyti suprogramuoti paprastą žaidimą pythono kalba. 
Pagrindiniai objektinio programavimo principai: 
- Inkapsuliacija (Encapsulation)
- Abstrakcija (Abstraction)
- Paveldėjimas (Inheritance)
- Polimorfizmas (Polymorphism)
Taip pat:
- Naudojamas dizaino šablonas (Singleton)
- Kompozicija ir/arba agregacija
- Duomenų skaitymas ir rašymas į failus
- Testavimas su `unittest`

### Kaip paleisti programą

1. Įsitikinkite, kad turite Python 3.x versiją.
2. Atsisiųskite failą `tic_tac_toe.py`.
3. Terminale paleiskite komandą:
   ```bash
   python tic_tac_toe.py

## Kaip naudotis programa?
1. Paleidus programą, bus paprašyta įvesti pirmojo žaidėjo vardą.
2. Tada galite pasirinkti, ar žaisite prieš kompiuterį ("y"), ar prieš kitą žaidėją ("n").
3. Jei renkatės žaisti prieš kitą žaidėją, bus paprašyta įvesti antrojo žaidėjo vardą.
4. Žaidimo metu žaidėjai paeiliui įveda skaičių nuo 1 iki 9, atitinkantį lentos laukelį.
5. Žaidimas baigiasi, kai vienas žaidėjas suformuoja tris savo simbolius iš eilės arba kai visi laukeliai užpildyti (lygiosios).
6. Po kiekvieno žaidimo bus išsaugomas rezultatas ir galėsite pasirinkti, ar žaisti dar kartą.

# Programos analizė

## 1. Inkapsuliacija (Encapsulation)

### Kas tai yra?
Inkapsuliacija yra principas, kuris slepia objekto vidinę būseną ir leidžia prie jos prieiti tik per apibrėžtus metodus.

### Kaip panaudota?

```python
class Player:
    def __init__(self, name, symbol):
        self._name = name
        self._symbol = symbol

    @property
    def name(self):
        return self._name
```
## Kodėl būtent taip?
Kintamieji pažymėti _ yra laikomi „protected“. Protected (_) prieiga padeda kode apsaugoti vidinius kintamuosius, tokius kaip žaidėjo vardas ar simbolis, nuo tiesioginio keitimo iš išorės, taip užtikrinant, kad jie būtų valdomi tik per saugius metodus arba paveldėtas klases.
`name` ir `symbol` saugomi kaip apsaugoti atributai. 
 Jie yra apsaugoti nuo atsitiktinio pakeitimo.  

## 2. Abstrakcija (Abstraction)
Abstrakcija yra į objekto orientuoto programavimo sąvoka, kuri parodo tik esminius atributus ir slepia nereikalingą informaciją. Ji leidžia išryškinti tik tai, kas yra svarbu naudotojui ir dirbti su bendrais metodais, nesigilinant į konkrečias implementacijas. Tai padeda sumažinti programavimo sudėtingumą. 
```python
from abc import ABC, abstractmethod

class Player(ABC):
    @abstractmethod
    def make_move(self, board):
        pass
```
`Player` klasė  apibrėžia abstraktų metodą `make_move`, kurį turi įgyvendinti visi paveldėtojai.
Konkrečios klasės `HumanPlayer` ir `ComputerPlayer` pačios apibrėžia, kaip įgyvendinamas šis metodas. Tai padeda užtikrinti, kad kiekvienas žaidėjas turės tą patį funkcionalumą ir leidžia programuoti bendrai, be žinių apie konkretaus žaidėjo veikimo principus. 

## 3. Paveldėjimas
Paveldėjimas - tai objektinio programavimo principas, kuris leidžia klasei perimti savybes ir metodus iš kitos klasės. Bendresnė klasė vadinama tėvine klase, o paveldėjusi klasė - dukterine klase. 
```python
class HumanPlayer(Player):
    def make_move(self, board):

class ComputerPlayer(Player):
    def make_move(self, board):
```
Abi klasės paveldi `Player` struktūrą ir privalo įgyvendint `make_move`.
Skirtingi žaidėjų tipai veikia nepriklausomai, bet laikosi bendros struktūros.

## 4. Polimorfizmas 
Polimorfizmas leidžia skirtingiems objektams naudoti tą patį metodą, bet įgyvendinti jį skirtingai. Metodas gali būti vykdoma skirtingai, priklausomai nuo konkrečios klasės realizacijos. 
```python
class Player(ABC):
    def __init__(self, name, symbol):
        self._name = name
        self._symbol = symbol
    def make_move(self, board):
        pass
class HumanPlayer(Player):
    def make_move(self, board):
def make_move(self, board):
        while True:
            try:
                move = input(f"{self._name}, enter your move (1-9): ")
                position = int(move) - 1
                if 0 <= position < 9 and board.is_position_empty(position):
                    return position
                print("Invalid move, try again!")
            except ValueError:
                print("Please enter a number between 1 and 9.")
        
class ComputerPlayer(Player):
    def make_move(self, board):
```
`make_move` metodas kviečiamas vienodai, nepriklausomai nuo to, ar tai žmogus ar kompiuteris.
Žaidimo logika paprastesnė, nes dirbama su bendru tipu `Player`.

## Singleton dizaino šablonas
Singleton šablonas užtikrina, kad egzistuoja tik vienas egzempliorius. Tai programavimo būdas, kai sukuriamas tik vienas konkrečios klasės objektas, ir visi programos komponentai naudoja tą patį objektą.
```python
class Board:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.reset()
        return cls._instance
```
Lenta yra vienintelė žaidimo erdvė, todėl visi žaidėjai turi dirbti su ta pačia objekto būsena. Jei kiekvienas žaidėjas turėtų savo lentos kopiją, jų matoma būsena skirtųsi, o tai prieštarautų žaidimo logikai.

Naudojant Singleton šabloną, garantuojama, kad žaidimo metu egzistuoja tik viena lentos kopija, kurią valdo visi žaidimo komponentai.

Tai leidžia išvengti situacijų, kuriose būtų keletas lentų ir skirtingi rezultatai. Singleton užtikrina vieningą ir nuoseklią žaidimo eigą.
# Nauda
Lenta kuriama tik vieną kartą ir naudojama visame žaidime.
Užtikrinama, kad visi žaidėjai dirba su ta pačia būsena.
Pagerina atminties naudojimą.

## Kompozicija
Kompozicija - tai objektinio programavimo principas, kai viena klasė turi kitų klasių objektus kaip savo dalis, ir šie objektai negali egzistuoti be ją turinčios klasės.
```python
self.board = Board()
self.players = [player1, player2]
```
`TicTacToeGame` klasė kuria ir valdo `Board` objektą savo viduje. Tai reiškia, kad lenta egzistuoja tol, kol gyvas žaidimo objektas.

`players` objektai taip pat priskiriami `TicTacToeGame` kaip jo vidinės dalys. Nors jie sukurti anksčiau, jie perduodami žaidimui, kuris valdo jų naudojimą žaidimo metu.

Objektų gyvavimo ciklai yra glaudžiai susiję – tai atitinka kompozicijos požymius.
# Nauda
Leidžia kurti aiškią, modulinę struktūrą.
Užtikrina, kad kiekvienas komponentas būtų tiesiogiai susietas su žaidimo eiga.

## Failų skaitymas ir rašymas 
```python
with open("praeitas.txt", "r") as f:
    paskutinis = f.read().strip()

with open("praeitas.txt", "w") as f:
    f.write(result_text + "\n")

with open("dabar.txt", "w") as f:
    f.write(result_text + "\n")
```
## Paaiškinimas:
Programa nuskaito paskutinį žaidimo rezultatą iš `praeitas.txt` ir parodo jį vartotojui prieš naują žaidimą.
Pasibaigus žaidimui, naujas rezultatas įrašomas tiek į `praeitas.txt`, tiek į `dabar.txt`.
Tokiu būdu `praeitas.txt` visada rodo naujausią rezultatą prieš kitą žaidimą, o `dabar.txt` saugo dabartinio žaidimo rezultatą.
## Nauda:
Leidžia rodyti naudotojui ankstesnio žaidimo rezultatą.
Sudaro galimybę sukurti žaidimo rezultatų istoriją arba statistiką ateityje.
# Rezultatai

Sukurtas pilnai veikiantis OOP pagrįstas kryžiukų-nuliukų žaidimas.
Įgyvendinti visi pagrindiniai OOP principai ir panaudota kompozicija.
Naudotas Singleton dizaino šablonas.
Duomenys saugomi ir nuskaitomi iš failų.
Įtraukti automatiniai vieneto testai.

# Išvados 

- Objektinis programavimas padėjo sukurti aišką, struktūruotą, lengvai plėtojamą ir prižiūrimą programinę sistemą.

- Naudojant abstrakciją ir paveldėjimą, supaprastinama skirtingų žaidėjų logika.

- Polimorfizmas leido rašyti bendresnį kodą, kuris veikia nepriklausomai nuo objekto tipo.

- Inkapsuliacija apsaugojo duomenis nuo netinkamo naudojimo.

- Singleton užtikrino, kad visi komponentai naudotų vieną bendrą lentą.

- Kompozicija padėjo suvaldyti objekto gyvavimo ciklą bei priklausomybes.

- Ateityje žaidimą galima išplėsti.















