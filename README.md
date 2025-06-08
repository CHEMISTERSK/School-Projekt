# Tank Game Project 🎮

Koncoročný projekt vytvorený dvoma študentmi s pomocou AI.

## 👥 Autori
- **Tomáš Vavro**
- **Radoslav Blecha**

**Škola:** SPŠE Karla Adlera 5

---

## 📖 Popis projektu

Tank Game je 2D akčná hra vytvorená v Pythone s použitím knižnice Pygame. Hra obsahuje:

- 🚗 **Ovládanie tanku** s realistickou fyzikou
- 💥 **Rôzne typy projektílov** (zelené, oranžové, červené)
- 🌊 **Systém vĺn nepriateľov**
- 💾 **Ukladanie/načítavanie hry**
- 🗄️ **Databázové pripojenie** pre štatistiky
- 🎵 **Zvukové efekty a hudba**
- ⚙️ **Konfigurovateľné nastavenia**
- 📊 **Logovanie a konzola pre debug**

---

## 🛠️ Inštalácia a spustenie

### Požiadavky na systém
- **Python 3.8+**
- **Windows** (odporúčané)

### Krok 1: Klonovanie projektu
```bash
git clone <repository-url>
cd School_Project
```

### Krok 2: Inštalácia Python knižníc
```bash
pip install pygame
pip install sqlite3  # Obvykle súčasť Pythonu
```

### Krok 3: Spustenie hry
```bash
python game.pyw
```

**Dôležité:** Pre zabránenie problémom s cestami k súborom umiestnite projekt do `C:\` namiesto používateľského priečinka.

---

## 📦 Požadované Python knižnice

```txt
pygame>=2.0.0
sqlite3 (built-in)
json (built-in)
os (built-in)
datetime (built-in)
threading (built-in)
math (built-in)
random (built-in)
```

### Inštalácia cez pip:
```bash
pip install pygame
```

---

## 🔧 Štruktúra projektu

```
School_Project/
├── game.pyw              # Hlavný spúšťací súbor
├── files/
│   ├── Game_Main.py      # Hlavná herná logika
│   ├── data/             # Konfiguračné súbory
│   │   ├── settings.json
│   │   ├── default_data.json
│   │   └── avdata.dat
│   ├── functions/        # Pomocné funkcie
│   │   ├── data.py       # Načítanie dát
│   │   ├── func.py       # Všeobecné funkcie
│   │   ├── save.py       # Ukladanie/načítanie
│   │   ├── console.py    # Debug konzola
│   │   ├── logging.py    # Logovanie
│   │   └── db/           # Databázové funkcie
│   ├── mechanics/        # Herné mechaniky
│   │   ├── menu.py       # Menu systém
│   │   └── generation.py # Generovanie obsahu
│   ├── textures/         # Obrázky a textúry
│   ├── sounds/           # Zvukové efekty
│   ├── fonts/            # Fonty
│   ├── saves/            # Uložené hry
│   └── logs/             # Log súbory
```

---

## 🎮 Ovládanie

| Klávesa | Akcia |
|---------|-------|
| `W/S` | Pohyb dopredu/dozadu |
| `A/D` | Otáčanie tanku |
| `Space` | Streľba |
| `R` | Nabíjanie |
| `F11` | Prepnutie fullscreen |
| `ESC` | Menu/Pauza |
| `F12` | Debug konzola |

---

## ⚙️ Konfigurácia

### Nastavenia hry (`files/data/settings.json`)
```json
{
    "player_name": "HRÁČ",
    "password": "heslo123",
    "fov": 0.75,
    "volume": 0.5,
    "default_fullscreen": false,
    "server_ip_address": "localhost",
    "server_port": 5432
}
```

### Herné hodnoty (`files/data/default_data.dat`)
Obsahuje predvolené hodnoty pre:
- Pozíciu a vlastnosti tanku
- Štatistiky projektílov
- FPS a rozlíšenie
- Herné flagy

---

## 🔌 Odporúčané VS Code rozšírenia

### 🐍 Python Development:
- **Python** (`ms-python.python`) - Základná podpora pre Python
- **Pylance** (`ms-python.vscode-pylance`) - Pokročilý IntelliSense pre Python
- **Python Debugger** (`ms-python.debugpy`) - Debugging nástroje
- **Black Formatter** (`ms-python.black-formatter`) - Automatické formátovanie
- **Flake8** (`ms-python.flake8`) - Linting a kontrola kvality kódu
- **isort** (`ms-python.isort`) - Organizovanie importov

### 🎨 Formátovanie a kvalita kódu:
- **Prettier** (`esbenp.prettier-vscode`) - Formátovanie JSON/Markdown/CSS
- **EditorConfig** (`EditorConfig.EditorConfig`) - Konzistentné nastavenia
- **Error Lens** (`usernamehw.errorlens`) - Inline zobrazenie chýb
- **Indent Rainbow** (`oderwat.indent-rainbow`) - Farebné odsadenie

### 🔄 Git a verziovanie:
- **GitLens** (`eamodio.gitlens`) - Rozšírené Git funkcie
- **Git Graph** (`mhutchie.git-graph`) - Vizuálna Git história
- **Git History** (`donjayamanne.githistory`) - História súborov

### 🎮 Herný vývoj:
- **Hex Dump** (`ms-vscode.hexdump`) - Prezeranie binárov
- **Bookmarks** (`alefragnani.Bookmarks`) - Označovanie dôležitých miest
- **Code Runner** (`formulahendry.code-runner`) - Rýchle spúšťanie kódu

### 🎯 Produktivita:
- **TODO Highlight** (`wayou.vscode-todo-highlight`) - Zvýraznenie TODO komentárov
- **Path Intellisense** (`christian-kohler.path-intellisense`) - Autocomplete pre cesty
- **Material Icon Theme** (`PKief.material-icon-theme`) - Krásne ikony súborov

### 📚 Dokumentácia:
- **Markdown All in One** (`yzhang.markdown-all-in-one`) - Markdown podpora
- **Markdown Lint** (`DavidAnson.vscode-markdownlint`) - Markdown linting

### 🧪 Testovanie:
- **Test Explorer** (`hbenl.vscode-test-explorer`) - Rozhranie pre testy
- **Python Test Adapter** (`littlefoxteam.vscode-python-test-adapter`) - Python testy

### 🎨 Témy a vzhľad:
- **GitHub Theme** (`GitHub.github-vscode-theme`) - GitHub téma
- **Live Server** (`ms-vscode.live-server`) - Lokálny web server
- **TODO Highlight** (`wayou.vscode-todo-highlight`) - Zvýraznenie TODO komentárov

---

## 🖥️ Vývojové nástroje

### Automatické formátovanie kódu

Projekt používa automatické formátovanie kódu:

#### Pre Python súbory:
- **Black** formatter je nakonfigurovaný pre Python súbory
- Súbory sa automaticky formátujú pri uložení
- Manuálne formátovanie: `Ctrl+Shift+P` → "Format Document"

#### Pre JavaScript/JSON/HTML/CSS súbory:
- **Prettier** je nakonfigurovaný pre automatické formátovanie
- Súbory sa automaticky formátujú pri uložení
- Manuálne formátovanie: `Ctrl+Shift+P` → "Format Document"

### VS Code Tasks:
- `Ctrl+Shift+P` → "Tasks: Run Task" → "Format All Files"
- `Ctrl+Shift+P` → "Tasks: Run Task" → "Check Formatting"
- `Ctrl+Shift+P` → "Tasks: Run Task" → "Format Python Files"

### Konfiguračné súbory:
- `.editorconfig` - Editor konfigurácia pre konzistentné kódovacie štýly
- `.prettierrc` - Prettier konfigurácia
- `.prettierignore` - Súbory na ignorovanie pri formátovaní
- `pyproject.toml` - Black formatter konfigurácia
- `.vscode/settings.json` - VS Code formátovacie nastavenia

### EditorConfig:
- Zabezpečuje konzistentný kódovací štýl vo všetkých editoroch
- Automaticky nastavuje odsadenie, kódovanie a konce riadkov
- Funguje s VS Code, IntelliJ, Sublime Text a inými editormi

---

## 🐛 Riešenie problémov

### Bežné problémy:

1. **Hra sa nespustí**
   - Skontrolujte, či máte nainštalovanú knižnicu Pygame
   - Ubezpečte sa, že používate Python 3.8+

2. **Chýbajúce textúry/zvuky**
   - Skontrolujte súbor `files/data/avdata.dat`
   - Overte, že súbory existujú v priečinkoch `textures/` a `sounds/`

3. **Databázové chyby**
   - Skontrolujte pripojenie v `files/functions/db/db.py`
   - Overte nastavenia v `settings.json`

4. **Problémy s cestami**
   - Umiestnite projekt do `C:\` namiesto používateľského priečinka
   - Skontrolujte relatívne cesty v kóde

### Logy a debugging:
- **Error logy:** `files/logs/error_log.log`
- **Running logy:** `files/logs/running_log.log`
- **Temp logy:** `files/logs/temp.log`
- **Debug konzola:** Stlačte `F12` v hre

---

## 📄 Licencia

Tento projekt je vytvorený pre školské účely na SPŠE Karla Adlera 5.

---

## 📞 Kontakt

Pre otázky a problémy kontaktujte autorov:
- Tomáš Vavro
- Radoslav Blecha

**Škola:** SPŠE Karla Adlera 5
