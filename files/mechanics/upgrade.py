import random

# Štatistiky hráča
default_stats = {
    "poškodenie": 10,
    "výdrž": 100,
    "pohyblivosť": 5
}

# Upgrady
def upgrade_poškodenie(stats):
    stats["poškodenie"] += 5
    print("Zvýšené poškodenie!")

def upgrade_vydrz(stats):
    stats["výdrž"] += 20
    print("Zvýšená výdrž!")

def upgrade_pohyblivost(stats):
    stats["pohyblivosť"] += 1
    print("Zvýšená pohyblivosť!")

# Názvy funkcií
UPGRADY = {
    "Poškodenie": upgrade_poškodenie,
    "Výdrž": upgrade_vydrz,
    "Pohyblivosť": upgrade_pohyblivost
}

def zobraz_upgrade_menu(stats):
    print("\n--- Výber upgradu ---")
    moznosti = random.sample(list(UPGRADY.keys()), 3)
    
    for i, moznost in enumerate(moznosti, 1):
        print(f"{i}. {moznost}")

    vyber = 0
    while vyber not in [1, 2, 3]:
        try:
            vyber = int(input("Vyber upgrade (1-3): "))
        except ValueError:
            continue

    vybrany = moznosti[vyber - 1]
    print(f"Zvolený upgrade: {vybrany}")
    UPGRADY[vybrany](stats)

# Príklad
if __name__ == "__main__":
    stats = default_stats.copy()
    print("Štartovacie štatistiky:", stats)
    zobraz_upgrade_menu(stats)
    print("Aktualizované štatistiky:", stats)