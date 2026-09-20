# Sustainable-Economics

Quarto book source code for **"Introduction to Sustainable Economics"**, the accompanying script for the course of the same name at the University of Bern. This is the English translation of the German original ([Nachhaltig-Wirtschaften](https://github.com/CDEteaching/Nachhaltig-Wirtschaften), "Einführung Nachhaltige Ökonomie").

## 🎓 About the Course

*Introduction to Sustainable Economics* is a lecture at the University of Bern in an **inverted-classroom format**: students work through the course content in self-study phases using this accompanying script and additional materials on [ILIAS](https://ilias.unibe.ch/go/crs/3443640); in-person time is used for deepening, discussion, and application.

In six chapters, the script introduces a sustainable, pluralist perspective on economics:

1. How can we think about economics?
2. Scope of economics
3. Problem analysis: What ails our economy?
4. Strategies for a sustainable economy: efficiency, consistency, sufficiency
5. The role of the state and economic policy guiding models
6. Sustainable economics: synthesis

## 📚 CDE Open Educational Resources

This course is part of the Open Educational Resources of the [Centre for Development and Environment (CDE)](https://www.cde.unibe.ch/) at the University of Bern. An overview of all freely accessible CDE teaching materials can be found at [CDEteaching](https://cdeteaching.github.io/CDEteaching/). The structure and tooling of this repo are modelled on [CDEteaching/Basics-of-sustainability](https://github.com/CDEteaching/Basics-of-sustainability).

## 📜 Licence

Unless otherwise stated, all materials are licensed under the [CC-BY-NC-SA 4.0 Int License](https://creativecommons.org/licenses/by-nc-sa/4.0/). Built with [Quarto](https://quarto.org/).

## 📖 Citation

Bader, C., Bezzola, N., Brülisauer, S. (eds.). (2026). Introduction to Sustainable Economics [Accompanying script]. CDE, University of Bern.

## 🧩 Contribution Matrix (CRediT Taxonomy)

| Name | Affiliation | ORCID | Roles (CRediT) |
|------------------|------------------|------------------|------------------|
| Christoph Bader | CDE, University of Bern | [0000-0002-8991-353X](https://orcid.org/0000-0002-8991-353X) | Conceptualization, Software, Supervision, Writing – original draft, Writing – review & editing, Project administration |
| Nicolà Bezzola | CDE, University of Bern | — | Writing – original draft, Writing – review & editing |
| Samuel Brülisauer | CDE, University of Bern | [0000-0002-2196-1922](https://orcid.org/0000-0002-2196-1922) | Writing – original draft, Writing – review & editing |

## Structure

- `_quarto.yml` — Quarto book configuration (title, chapter list, theme, sidebar).
- `index.qmd` — Preface.
- `1_thinking-economics/` … `6_synthesis/` — the six chapters, each with one `_intro.qmd` plus `images/`.
- `references.qmd` / `references.bib` — Bibliography.
- `theme.scss`, `theme.css`, `webex.css`, `webex.js` — Theme and self-check quiz assets, taken over from the reference repo.
- `_extensions/coatless-quarto/custom-callout/` — Callout extension, taken over from the reference repo.

## Translation notes

- Figures in the `images/` folders (and `2_scope-of-economics/charts/`) are copied unchanged from the German original and still carry German labels.
- The source `.bib` file is unchanged; some references are German-language sources.
- Video and ILIAS links point to German-language material unless stated otherwise.
