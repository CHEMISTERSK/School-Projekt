# Inštalačný návod - Tank Game Project

## 🔧 Kroky pre inštaláciu

### 1. Predpoklady
- **Python 3.8 alebo vyšší** - [Stiahnuť Python](https://www.python.org/downloads/)
- **Git** (voliteľné) - [Stiahnuť Git](https://git-scm.com/downloads)
- **VS Code** (odporúčané) - [Stiahnuť VS Code](https://code.visualstudio.com/)

### 2. Overenie Python inštalácie
Otvorte terminál/príkazový riadok a zadajte:
```bash
python --version
```
Ak sa zobrazí verzia 3.8+, môžete pokračovať.

### 3. Získanie projektu

#### Metóda A: Git Clone (odporúčané)
```bash
git clone <repository-url>
cd School_Project
```

#### Metóda B: Manuálne stiahnutie
1. Stiahnite projekt ako ZIP súbor
2. Rozbaľte do `C:\School_Project\`
3. Otvorte terminál v tomto priečinku

### 4. Inštalácia Python knižníc

#### Automatická inštalácia (odporúčané):
```bash
pip install -r requirements.txt
```

#### Manuálna inštalácia:
```bash
pip install pygame
```

### 5. Overenie inštalácie
```bash
python -c "import pygame; print('Pygame verzia:', pygame.version.ver)"
```

### 6. Spustenie hry
```bash
python game.pyw
```

---

## 🛠️ Nastavenie VS Code

### 1. Inštalácia odporúčaných rozšírení
Po otvorení projektu vo VS Code:
1. Stlačte `Ctrl+Shift+P`
2. Zadajte "Extensions: Show Recommended Extensions"
3. Nainštalujte všetky odporúčané rozšírenia

### 2. Automatická inštalácia rozšírení
```json
{
    "recommendations": [
        "ms-python.python",
        "ms-python.vscode-pylance",
        "ms-python.debugpy",
        "ms-python.black-formatter",
        "esbenp.prettier-vscode",
        "EditorConfig.EditorConfig"
    ]
}
```

### 3. Spustenie z VS Code
1. Otvorte súbor `game.pyw`
2. Stlačte `F5` alebo `Ctrl+F5` pre spustenie

---

## 🐛 Riešenie problémov

### Python nie je rozpoznaný
```bash
# Windows - pridajte Python do PATH
# Alebo použite:
py --version
py -m pip install pygame
```

### Pygame sa nedá nainštalovať
```bash
# Aktualizujte pip
python -m pip install --upgrade pip

# Potom skúste znovu
pip install pygame
```

### Chyba s cestami k súborom
```bash
# Presúvajte projekt do C:\
# Nie do C:\Users\[username]\
```

### ModuleNotFoundError
```bash
# Overte, že ste v správnom priečinku
cd C:\School_Project

# Overte Python cestu
python -c "import sys; print(sys.path)"
```

### Chýbajúce súbory
```bash
# Overte štruktúru projektu
dir files\data\
dir files\textures\
dir files\sounds\
```

---

## 📋 Checklist pre úspešnú inštaláciu

- [ ] Python 3.8+ je nainštalovaný
- [ ] Projekt je v `C:\School_Project\`
- [ ] Pygame je nainštalovaný (`pip list | grep pygame`)
- [ ] Súbory `files/data/settings.json` existujú
- [ ] Priečinky `textures/` a `sounds/` obsahujú súbory
- [ ] `python game.pyw` spustí hru bez chýb

---

## 🔄 Aktualizácia projektu

```bash
# Git pull (ak používate Git)
git pull origin main

# Aktualizácia knižníc
pip install -r requirements.txt --upgrade
```

---

## 💡 Tipy pre vývojárov

### Virtuálne prostredie (odporúčané)
```bash
# Vytvorenie virtuálneho prostredia
python -m venv tank_game_env

# Aktivácia
# Windows:
tank_game_env\Scripts\activate
# Linux/Mac:
source tank_game_env/bin/activate

# Inštalácia knižníc
pip install -r requirements.txt
```

### Debug režim
```bash
# Spustenie s verbose logovaním
python game.pyw --debug
```

### Formátovanie kódu
```bash
# Black formatter
black .

# Kontrola formátovania
black --check .
```

---

## 📞 Pomoc

Ak máte problémy s inštaláciou:

1. **Skontrolujte logs:** `files/logs/error_log.log`
2. **Debug konzola:** Stlačte `F12` v hre
3. **Kontaktujte autorov:** Tomáš Vavro, Radoslav Blecha
4. **Škola:** SPŠE Karla Adlera 5
