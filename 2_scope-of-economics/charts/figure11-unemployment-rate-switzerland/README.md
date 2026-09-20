# Abbildung 11 — Arbeitslosigkeit in der Schweiz

CDE-Style-Grafik für `2_gegenstandsbereich/2_intro.qmd`, Abbildung 11. Zeigt **zwei Reihen auf zwei unabhängigen y-Achsen**: die Arbeitslosenquote (%, linke Achse) und die absolute Zahl registrierter Arbeitsloser (rechte Achse).

Kein Standard-`cde-charts`-Template: `line_chart.py` unterstützt nur eine y-Achse mit bis zu 4 Reihen in derselben Einheit. Für diesen Fall wurde ein eigenständiges `dual_axis_chart.py` in diesem Ordner geschrieben, das dieselben `cde_style.py`-Bausteine (Farben, Schrift, Footer, PNG/GIF-Export) verwendet, aber `ax.twinx()` für die zweite Achse einsetzt.

## Datenquellen

1. **1920–1995**: **Historische Statistik der Schweiz (HSSO)**, Tab. F.18a „Stellensuchende und Arbeitslosenquote nach Geschlecht im Jahresmittel 1913–1995".
   - Spalte „Total" (Ganzarbeitslose + Übrige, Total) → registrierte Arbeitslose (Anzahl).
   - Spalte „Arbeitslosenquote (4)", Total → Arbeitslosenquote (%).
   - Quelle: `https://hsso.ch/de/2012/f/18a`, XLSX-Download `https://hsso.ch/get/F.18a.xlsx`, heruntergeladen am 2026-08-17.
2. **1996–2025**: **SNB-Datenportal**, Cube `amarbma` (Arbeitsmarkt) — Serie „Registrierte Arbeitslose – Total" (Anzahl) und Serie „Arbeitslosenquote – Total" (%, nicht saisonbereinigt); beides von SECO erhoben, von der SNB weiterveröffentlicht.
   - Quelle: `https://data.snb.ch/api/cube/amarbma/data/json/de`, heruntergeladen am 2026-08-17.
   - Aus den Monatswerten wurde pro Jahr das arithmetische Mittel der 12 Monatswerte gebildet (Jahresdurchschnitt). 2025 ist bereits ein vollständiges Jahr (12 Monate) und wurde einbezogen; 2026 (bisher nur 6 Monate) wurde nicht verwendet, um nur vollständige Jahresdurchschnitte zu zeigen.

## Transparenzhinweis

Diese Grafik wurde mit Unterstützung von Claude Code (Anthropic) erstellt — Transparenzhinweis gem. Art. 50 EU AI Act.

## Dateien

- `abbildung11-arbeitslosenquote-schweiz.png` — eingebunden als `../../images/abb16.png` im qmd.
- `abbildung11-arbeitslosenquote-schweiz.gif` — animierte Variante für eine Präsentation, falls gebraucht.
- `abbildung11-arbeitslosenquote-schweiz.csv` — alle 106 geplotteten Werte (Quote + Anzahl, 1920–2025, ungekürzt) mit Quellenspalte pro Zeile — das ist jetzt identisch mit dem, was tatsächlich im Chart steht.
- `hsso_f18a_full_1913-1995.csv` — Rohauszug direkt aus der HSSO-Quelldatei (1913–1995, weiter zurückreichend als der Chart), zur unabhängigen Prüfung gegen die Originalquelle.
- `seco_amarbma_full_1984-2025.csv` — Rohauszug direkt aus der SNB-Quelldatei (1984–2025, weiter zurückreichend als der Chart), zur unabhängigen Prüfung gegen die Originalquelle.
- `dual_axis_chart.py` + `cde_style.py` — das Skript, das die Grafik erzeugt (liest die beiden Rohauszüge oben direkt ein).
