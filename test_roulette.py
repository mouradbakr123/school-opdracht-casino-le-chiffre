"""
Unit tests voor Casino Le Chiffre.

Draai de tests met:   pytest -v
"""

import pytest

from roulette import (
    bereken_uitbetaling,
    euro_naar_fiches,
    is_winnende_inzet,
    kleur_van,
    nieuw_saldo,
    simuleer,
)


# ------------------------------------------------------------------
# euro_naar_fiches
# ------------------------------------------------------------------

def test_wisselen_van_137_euro():
    assert euro_naar_fiches(137) == {100: 1, 25: 1, 10: 1, 5: 0, 1: 2}


def test_wisselen_van_nul_euro():
    assert euro_naar_fiches(0) == {100: 0, 25: 0, 10: 0, 5: 0, 1: 0}


def test_wisselen_gebruikt_zo_min_mogelijk_fiches():
    fiches = euro_naar_fiches(99)
    assert sum(fiches.values()) == 9


def test_wisselen_van_negatief_bedrag_mag_niet():
    with pytest.raises(ValueError):
        euro_naar_fiches(-5)


def test_wisselen_van_halve_euro_mag_niet():
    with pytest.raises(ValueError):
        euro_naar_fiches(12.50)


# ------------------------------------------------------------------
# kleur_van
# ------------------------------------------------------------------

def test_nul_is_groen():
    assert kleur_van(0) == "groen"


def test_zeventien_is_zwart():
    assert kleur_van(17) == "zwart"


def test_zesendertig_is_rood():
    assert kleur_van(36) == "rood"


def test_er_zijn_achttien_rode_en_achttien_zwarte_vakjes():
    kleuren = [kleur_van(nummer) for nummer in range(37)]
    assert kleuren.count("rood") == 18
    assert kleuren.count("zwart") == 18
    assert kleuren.count("groen") == 1


def test_vakje_37_bestaat_niet():
    with pytest.raises(ValueError):
        kleur_van(37)


# ------------------------------------------------------------------
# is_winnende_inzet
# ------------------------------------------------------------------

def test_rood_wint_bij_een_rood_nummer():
    assert is_winnende_inzet("rood", None, 3) is True


def test_rood_verliest_bij_een_zwart_nummer():
    assert is_winnende_inzet("rood", None, 2) is False


def test_alle_kansen_verliezen_bij_nul():
    for soort in ("rood", "zwart", "even", "oneven", "laag", "hoog",
                  "dozijn1", "dozijn2", "dozijn3"):
        assert is_winnende_inzet(soort, None, 0) is False


def test_inzet_op_nul_wint_wel_bij_nul():
    assert is_winnende_inzet("nummer", 0, 0) is True


def test_tweede_dozijn_wint_bij_vierentwintig():
    assert is_winnende_inzet("dozijn2", None, 24) is True


def test_tweede_dozijn_verliest_bij_vijfentwintig():
    assert is_winnende_inzet("dozijn2", None, 25) is False


# ------------------------------------------------------------------
# bereken_uitbetaling
# ------------------------------------------------------------------

def test_winst_op_rood_verdubbelt_de_inzet():
    assert bereken_uitbetaling("rood", None, 10, 3) == 20


def test_verlies_levert_niets_op():
    assert bereken_uitbetaling("rood", None, 10, 2) == 0


def test_winst_op_een_dozijn_verdrievoudigt_de_inzet():
    assert bereken_uitbetaling("dozijn1", None, 10, 7) == 30


def test_winst_op_een_nummer_levert_zesendertig_keer_de_inzet_op():
    assert bereken_uitbetaling("nummer", 17, 5, 17) == 180


def test_inzet_van_nul_mag_niet():
    with pytest.raises(ValueError):
        bereken_uitbetaling("rood", None, 0, 3)


# ------------------------------------------------------------------
# nieuw_saldo
# ------------------------------------------------------------------

def test_saldo_na_winst():
    assert nieuw_saldo(100, 10, 20) == 110


def test_saldo_na_verlies():
    assert nieuw_saldo(100, 10, 0) == 90


def test_meer_inzetten_dan_je_saldo_mag_niet():
    with pytest.raises(ValueError):
        nieuw_saldo(50, 60, 0)


# ------------------------------------------------------------------
# simuleer
# ------------------------------------------------------------------

def test_simulatie_met_dezelfde_seed_geeft_dezelfde_uitkomst():
    eerste = simuleer(5000, "rood", 10, seed=42)
    tweede = simuleer(5000, "rood", 10, seed=42)
    assert eerste == tweede


def test_simulatie_legt_het_juiste_bedrag_in():
    uitkomst = simuleer(1000, "rood", 5, seed=1)
    assert uitkomst["ingelegd"] == 5000


def test_huisvoordeel_ligt_rond_de_twee_komma_zeven_procent():
    uitkomst = simuleer(300000, "rood", 10, seed=7)
    assert 1.5 < uitkomst["huisvoordeel_procent"] < 4.0
