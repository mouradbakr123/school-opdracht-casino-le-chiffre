# Casino Le Chiffre

Een roulettespel voor in de terminal, met unit tests en een monte-carlosimulatie.
Dit project hoort bij opdracht 2 over geautomatiseerd testen.

## Het spel spelen

Je hebt Python 3.10 of hoger nodig.

    python roulette.py

Je wisselt eerst euro's om naar fiches en zet daarna in op rood, zwart, even,
oneven, hoog, laag, een dozijn of een enkel nummer. Het spel is Europese
roulette: 37 vakjes, van 0 tot en met 36, met een enkele groene nul.

| Inzet             | Uitbetaling | Kans      |
|-------------------|-------------|-----------|
| Rood of zwart     | 1 op 1      | 18 op 37  |
| Even of oneven    | 1 op 1      | 18 op 37  |
| Hoog of laag      | 1 op 1      | 18 op 37  |
| Een dozijn        | 2 op 1      | 12 op 37  |
| Een enkel nummer  | 35 op 1     | 1 op 37   |

Door die groene nul is elke inzet in het voordeel van het huis.
Op de lange termijn houdt het casino 1/37 van alles wat er ingelegd wordt,
oftewel 2,70 procent.

## De tests draaien

    pip install -r requirements.txt
    pytest -v

De tests staan in `test_roulette.py` en controleren de rekenfuncties:

- `euro_naar_fiches()` wisselt een bedrag in hele euro's om naar zo min
  mogelijk fiches.
- `kleur_van()` geeft de kleur van een vakje.
- `is_winnende_inzet()` bepaalt of een inzet wint.
- `bereken_uitbetaling()` rekent uit hoeveel fiches de speler terugkrijgt.
- `nieuw_saldo()` berekent het saldo na een ronde.
- `simuleer()` speelt heel veel rondes achter elkaar.

## De simulatie draaien

    python simulatie.py

Standaard speelt de simulatie een miljoen rondes per inzetsoort. Wil je het
sneller, geef dan een kleiner aantal mee:

    python simulatie.py 10000

Hoe meer rondes, hoe dichter het gemeten huisvoordeel bij de theoretische
2,70 procent komt te liggen. Bij een inzet op een enkel nummer duurt dat het
langst, want die wint maar 1 op de 37 keer.
