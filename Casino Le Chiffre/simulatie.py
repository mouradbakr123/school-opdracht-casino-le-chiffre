"""
Monte-carlosimulatie voor Casino Le Chiffre.

Deze simulatie speelt heel veel rondes roulette achter elkaar en kijkt
hoeveel het huis daaraan verdient. Theoretisch is dat bij Europese
roulette 1/37, oftewel 2,70 procent van alles wat er ingelegd wordt.

Draai met:   python simulatie.py
Of met een eigen aantal rondes:   python simulatie.py 2000000
"""

import sys
from datetime import datetime

from roulette import simuleer

STANDAARD_RONDES = 1000000
INZETSOORTEN = ("rood", "even", "dozijn1", "nummer")


def main():
    if len(sys.argv) > 1:
        rondes = int(sys.argv[1])
    else:
        rondes = STANDAARD_RONDES

    print("=" * 66)
    print("  MONTE-CARLOSIMULATIE - CASINO LE CHIFFRE")
    print("  Datum: " + datetime.now().strftime("%d-%m-%Y %H:%M"))
    print("  Rondes per inzetsoort: {:,}".format(rondes).replace(",", "."))
    print("=" * 66)
    print()
    print("  {:<10} {:>14} {:>14} {:>12}".format(
        "inzet", "ingelegd", "resultaat", "huisvoordeel"))
    print("  " + "-" * 52)

    for soort in INZETSOORTEN:
        uitkomst = simuleer(rondes, soort=soort, inzet=10)
        print("  {:<10} {:>14} {:>14} {:>11.2f}%".format(
            uitkomst["soort"],
            uitkomst["ingelegd"],
            uitkomst["resultaat"],
            uitkomst["huisvoordeel_procent"],
        ))

    print()
    print("  Theoretisch huisvoordeel bij Europese roulette: 2,70%")
    print("  Een inzet op een enkel nummer wint maar 1 op de 37 keer.")
    print("  Die rij schommelt daarom veel sterker dan de rest.")
    print("=" * 66)


if __name__ == "__main__":
    main()
