# Figure 11 — Unemployment in Switzerland

CDE-style chart for `2_scope-of-economics/2_intro.qmd` (unemployment section). Shows **two series on two independent y-axes**: the unemployment rate (%, left axis) and the number of registered unemployed (right axis).

Not a standard `cde-charts` template: `line_chart.py` only supports one y-axis with up to 4 series in the same unit. A stand-alone `dual_axis_chart.py` was therefore written for this chart. It uses the same `cde_style.py` building blocks (colours, font, footer, PNG/GIF export) but adds a second axis with `ax.twinx()`.

English version of the chart in the German script (`Nachhaltig-Wirtschaften`, `abbildung11-arbeitslosenquote-schweiz`), same data, labels translated on 2026-10-07.

## Data sources

1. **1920–1995**: **Historical Statistics of Switzerland (HSSO)**, table F.18a "Job seekers and unemployment rate by sex, annual mean 1913–1995".
   - Column "Total" (fully unemployed + others, total) → registered unemployed (number).
   - Column "Unemployment rate (4)", total → unemployment rate (%).
   - Source: `https://hsso.ch/de/2012/f/18a`, XLSX download `https://hsso.ch/get/F.18a.xlsx`, downloaded 2026-08-17.
2. **1996–2025**: **SNB data portal**, cube `amarbma` (labour market): series "Registered unemployed – total" (number) and "Unemployment rate – total" (%, not seasonally adjusted); both collected by SECO and republished by the SNB.
   - Source: `https://data.snb.ch/api/cube/amarbma/data/json/de`, downloaded 2026-08-17.
   - Annual values are the arithmetic mean of the 12 monthly values. 2025 is a complete year (12 months) and is included; 2026 (only 6 months at download) is not used, so that only complete annual means are shown.

## Transparency notice

This chart was created with the assistance of Claude Code (Anthropic) — transparency notice per EU AI Act Art. 50.

## Files

- `figure11-unemployment-rate-switzerland.png` — embedded directly in the qmd.
- `figure11-unemployment-rate-switzerland.gif` — animated version for a presentation, if needed.
- `figure11-unemployment-rate-switzerland.csv` — all 106 plotted values (rate + number, 1920–2025) with a source column per row.
- `hsso_f18a_full_1913-1995.csv` — raw extract from the HSSO source file (1913–1995), for independent checking against the original.
- `seco_amarbma_full_1984-2025.csv` — raw extract from the SNB source file (1984–2025), for independent checking against the original.
- `dual_axis_chart.py` + `cde_style.py` — the script that produces the chart (reads the two raw extracts above).
