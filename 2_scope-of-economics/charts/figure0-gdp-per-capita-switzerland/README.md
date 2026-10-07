# Figure 0 — GDP per capita in Switzerland

CDE-style chart for `2_scope-of-economics/2_intro.qmd` (`@fig-GDP-CH`), copied into `images/fig0.png`.

English version of the chart in the German script (`Nachhaltig-Wirtschaften`, `abbildung6-bip-pro-kopf-schweiz`), same data, labels translated on 2026-10-07.

## Data source

**Maddison Project Database, Release 2020** (Bolt, J. & van Zanden, J. L., 2020), Groningen Growth and Development Centre, University of Groningen.
- File `mpd2020.xlsx`, sheet "Full data", column `gdppc` (real GDP per capita in 2011 US dollars, PPP-adjusted), country "Switzerland".
- Downloaded 2026-08-17 from `https://www.rug.nl/ggdc/historicaldevelopment/maddison/data/mpd2020.xlsx` (release page `https://www.rug.nl/ggdc/historicaldevelopment/maddison/releases/maddison-project-database-2020`), the version the caption refers to.
- MPD2020 has continuous annual values for Switzerland from 1851 to 2018 (a single, very rough estimate for year 1 was not used).

## Transformation

No calculation: all plotted values are unchanged `gdppc` values from the source, rounded to whole US dollars.

The chart shows a ten-year selection (1851, 1860, 1870, …, 2010, 2018) of the 168 annual values, so that the line chart template (marker per data point) stays readable. The full annual series is in `che_mpd2020_full_1851-2018.csv`.

## Transparency notice

This chart was created with the assistance of Claude Code (Anthropic) — transparency notice per EU AI Act Art. 50.

## Files

- `figure0-gdp-per-capita-switzerland.png` — for the book, copied to `../../images/fig0.png`.
- `figure0-gdp-per-capita-switzerland.gif` — animated version for a presentation, if needed.
- `figure0-gdp-per-capita-switzerland.csv` — the 18 plotted values (ten-year selection).
- `che_mpd2020_full_1851-2018.csv` — all 168 annual values 1851–2018.
- `line_chart.py` + `cde_style.py` — the script that produces the chart.
