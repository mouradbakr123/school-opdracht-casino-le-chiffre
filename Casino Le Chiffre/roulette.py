"""
Casino Le Chiffre - Europese roulette
Speel met:  python roulette.py

De rekenfuncties in dit bestand worden getest door test_roulette.py.
"""

import os
import random
import sys
import time

# Europese roulette: 37 vakjes, 0 tot en met 36, met één groene nul.
ROOD = (1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36)
ZWART = (2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35)

# De volgorde waarin de nummers fysiek op het wiel staan.
WIELVOLGORDE = (
    0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23,
    10, 5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26,
)

COUPURES = (100, 25, 10, 5, 1)

# Wat elke inzetsoort uitbetaalt, inclusief de eigen inzet.
# "rood" met 10 fiches inzet levert bij winst 2 x 10 = 20 fiches op.
UITBETALINGSFACTOR = {
    "rood": 2,
    "zwart": 2,
    "even": 2,
    "oneven": 2,
    "laag": 2,        # 1 tot en met 18
    "hoog": 2,        # 19 tot en met 36
    "dozijn1": 3,     # 1 tot en met 12
    "dozijn2": 3,     # 13 tot en met 24
    "dozijn3": 3,     # 25 tot en met 36
    "nummer": 36,     # één enkel nummer
}


# ==================================================================
# Rekenfuncties. Deze zijn objectief te controleren met unit tests.
# ==================================================================

def euro_naar_fiches(bedrag):
    """Wisselt een bedrag in hele euro's om naar zo min mogelijk fiches.

    Geeft een dictionary terug met per coupure het aantal fiches:
    euro_naar_fiches(137) geeft {100: 1, 25: 1, 10: 1, 5: 0, 1: 2}
    """
    if not isinstance(bedrag, int) or isinstance(bedrag, bool):
        raise ValueError("Wisselen kan alleen met hele euro's.")
    if bedrag < 0:
        raise ValueError("Je kunt geen negatief bedrag wisselen.")

    fiches = {}
    rest = bedrag
    for coupure in COUPURES:
        fiches[coupure] = rest // coupure
        rest = rest % coupure
    return fiches


def kleur_van(nummer):
    """Geeft de kleur van een vakje: "rood", "zwart" of "groen"."""
    if nummer not in WIELVOLGORDE:
        raise ValueError("Dit vakje bestaat niet op een Europees wiel: " + str(nummer))
    if nummer == 0:
        return "groen"
    if nummer in ROOD:
        return "rood"
    return "zwart"


def is_winnende_inzet(soort, nummer, uitkomst):
    """Bepaalt of een inzet wint.

    soort    is bijvoorbeeld "rood", "even", "dozijn2" of "nummer"
    nummer   is het gekozen nummer bij soort "nummer", anders None
    uitkomst is het nummer waar de bal op is gevallen
    """
    if soort not in UITBETALINGSFACTOR:
        raise ValueError("Onbekende inzetsoort: " + str(soort))
    if uitkomst == 0:
        return soort == "nummer" and nummer == 0

    if soort == "rood":
        return kleur_van(uitkomst) == "rood"
    if soort == "zwart":
        return kleur_van(uitkomst) == "zwart"
    if soort == "even":
        return uitkomst % 2 == 0
    if soort == "oneven":
        return uitkomst % 2 == 1
    if soort == "laag":
        return 1 <= uitkomst <= 18
    if soort == "hoog":
        return 19 <= uitkomst <= 36
    if soort == "dozijn1":
        return 1 <= uitkomst <= 12
    if soort == "dozijn2":
        return 13 <= uitkomst <= 24
    if soort == "dozijn3":
        return 25 <= uitkomst <= 36
    return nummer == uitkomst


def bereken_uitbetaling(soort, nummer, inzet, uitkomst):
    """Geeft het aantal fiches dat de speler terugkrijgt.

    Bij verlies is dat 0. Bij winst is dat de inzet plus de winst,
    dus bereken_uitbetaling("rood", None, 10, 3) geeft 20.
    """
    if inzet <= 0:
        raise ValueError("Een inzet moet groter dan 0 zijn.")
    if not is_winnende_inzet(soort, nummer, uitkomst):
        return 0
    return inzet * UITBETALINGSFACTOR[soort]


def nieuw_saldo(saldo, inzet, uitbetaling):
    """Berekent het saldo na een ronde."""
    if inzet > saldo:
        raise ValueError("Je kunt niet meer inzetten dan je saldo.")
    return saldo - inzet + uitbetaling


def draai_wiel(generator=None):
    """Laat de bal vallen en geeft het winnende nummer terug."""
    if generator is None:
        generator = random
    return generator.choice(WIELVOLGORDE)


def simuleer(aantal_rondes, soort="rood", inzet=10, seed=None):
    """Speelt aantal_rondes keer dezelfde inzet en geeft de uitkomst terug.

    Dit is de monte-carlosimulatie. Hoe meer rondes, hoe dichter het
    huisvoordeel bij de theoretische 2,70 procent komt te liggen.
    """
    if aantal_rondes <= 0:
        raise ValueError("Het aantal rondes moet groter dan 0 zijn.")

    generator = random.Random(seed)
    ingelegd = 0
    uitbetaald = 0
    gewonnen_rondes = 0

    for _ in range(aantal_rondes):
        uitkomst = draai_wiel(generator)
        ingelegd = ingelegd + inzet
        opbrengst = bereken_uitbetaling(soort, None if soort != "nummer" else 17,
                                        inzet, uitkomst)
        uitbetaald = uitbetaald + opbrengst
        if opbrengst > 0:
            gewonnen_rondes = gewonnen_rondes + 1

    resultaat = uitbetaald - ingelegd
    return {
        "rondes": aantal_rondes,
        "soort": soort,
        "inzet": inzet,
        "ingelegd": ingelegd,
        "uitbetaald": uitbetaald,
        "resultaat": resultaat,
        "gewonnen_rondes": gewonnen_rondes,
        "huisvoordeel_procent": round(-resultaat / ingelegd * 100, 4),
    }


# ==================================================================
# Alles hieronder is het spel zelf.
# ==================================================================

KLEURCODE = {"rood": "\033[91m", "zwart": "\033[97m", "groen": "\033[92m"}
RESET = "\033[0m"


def _zet_kleuren_aan():
    if os.name == "nt":
        os.system("")


def _gekleurd(nummer):
    return KLEURCODE[kleur_van(nummer)] + str(nummer) + RESET


def teken_wiel(winnend=None):
    """Bouwt een ASCII-tekening van het roulettewiel."""
    import math

    breedte, hoogte = 68, 23
    raster = [[" "] * breedte for _ in range(hoogte)]

    midden_x, midden_y = breedte // 2, hoogte // 2
    straal_x, straal_y = 31.0, 10.5

    def schrijf(x, y, tekst):
        for verschuiving, teken in enumerate(tekst):
            kolom = x + verschuiving
            if 0 <= kolom < breedte and 0 <= y < hoogte:
                raster[y][kolom] = teken

    for index, nummer in enumerate(WIELVOLGORDE):
        hoek = -math.pi / 2 + 2 * math.pi * index / len(WIELVOLGORDE)
        x = int(round(midden_x + straal_x * math.cos(hoek)))
        y = int(round(midden_y + straal_y * math.sin(hoek)))
        if nummer == winnend:
            schrijf(x - 1, y, "[" + str(nummer) + "]")
        else:
            schrijf(x, y, "{:>2}".format(nummer))

    if winnend is None:
        regels_midden = ["CASINO LE CHIFFRE", "Europese roulette"]
    else:
        regels_midden = ["De bal ligt op", "{}  ({})".format(winnend, kleur_van(winnend))]

    start_y = midden_y - (len(regels_midden) - 1) // 2 - 1
    for verschuiving, regel in enumerate(regels_midden):
        schrijf(midden_x - len(regel) // 2, start_y + verschuiving * 2, regel)

    return "\n".join("".join(rij).rstrip() for rij in raster)


def draai_animatie(winnend):
    print()
    stappen = 14
    startindex = random.randrange(len(WIELVOLGORDE))
    for stap in range(stappen):
        nummer = WIELVOLGORDE[(startindex + stap * 7) % len(WIELVOLGORDE)]
        print("   De bal rolt ...  " + _gekleurd(nummer) + "    ", end="\r")
        sys.stdout.flush()
        time.sleep(0.06 + stap * 0.015)
    print("   De bal valt in vakje " + _gekleurd(winnend) + "        ")
    print()
    print(teken_wiel(winnend))
    print()


def toon_inzetmenu():
    print()
    print("  Waarop zet je in?")
    print("   1. Rood            (1 op 1)")
    print("   2. Zwart           (1 op 1)")
    print("   3. Even            (1 op 1)")
    print("   4. Oneven          (1 op 1)")
    print("   5. Laag, 1 t/m 18  (1 op 1)")
    print("   6. Hoog, 19 t/m 36 (1 op 1)")
    print("   7. Eerste dozijn, 1 t/m 12   (2 op 1)")
    print("   8. Tweede dozijn, 13 t/m 24  (2 op 1)")
    print("   9. Derde dozijn, 25 t/m 36   (2 op 1)")
    print("  10. Eén nummer      (35 op 1)")
    print("   S. Stoppen en je fiches inwisselen")


MENUKEUZES = {
    "1": "rood", "2": "zwart", "3": "even", "4": "oneven",
    "5": "laag", "6": "hoog", "7": "dozijn1", "8": "dozijn2",
    "9": "dozijn3", "10": "nummer",
}


def vraag_geheel_getal(vraag, minimum, maximum):
    while True:
        antwoord = input(vraag).strip()
        try:
            waarde = int(antwoord)
        except ValueError:
            print("  Vul een heel getal in.")
            continue
        if waarde < minimum or waarde > maximum:
            print("  Kies een getal van {} tot en met {}.".format(minimum, maximum))
            continue
        return waarde


def main():
    _zet_kleuren_aan()
    print()
    print(teken_wiel())
    print()
    print("  Welkom bij Casino Le Chiffre.")

    bedrag = vraag_geheel_getal("  Voor hoeveel hele euro's wissel je fiches? ", 1, 10000)
    fiches = euro_naar_fiches(bedrag)
    print()
    print("  Je krijgt:")
    for coupure in COUPURES:
        if fiches[coupure] > 0:
            print("   {:>3} fiches van {:>3}".format(fiches[coupure], coupure))
    saldo = bedrag
    print("  Je saldo is {} fiches.".format(saldo))

    while saldo > 0:
        toon_inzetmenu()
        print("  Saldo: {} fiches".format(saldo))
        keuze = input("  Keuze: ").strip()

        if keuze.upper() == "S":
            break
        if keuze not in MENUKEUZES:
            print("  Dat is geen geldige keuze.")
            continue

        soort = MENUKEUZES[keuze]
        nummer = None
        if soort == "nummer":
            nummer = vraag_geheel_getal("  Op welk nummer zet je in (0 t/m 36)? ", 0, 36)

        inzet = vraag_geheel_getal("  Hoeveel fiches zet je in? ", 1, saldo)

        uitkomst = draai_wiel()
        draai_animatie(uitkomst)

        uitbetaling = bereken_uitbetaling(soort, nummer, inzet, uitkomst)
        saldo = nieuw_saldo(saldo, inzet, uitbetaling)

        if uitbetaling > 0:
            print("  Gewonnen. Je krijgt {} fiches uitbetaald.".format(uitbetaling))
        else:
            print("  Verloren. Je bent {} fiches kwijt.".format(inzet))
        print("  Nieuw saldo: {} fiches.".format(saldo))

    print()
    if saldo == 0:
        print("  Je fiches zijn op. Het huis wint altijd.")
    else:
        print("  Je wisselt {} fiches in voor EUR {},00.".format(saldo, saldo))
    print("  Tot ziens.")
    print()


if __name__ == "__main__":
    main()
