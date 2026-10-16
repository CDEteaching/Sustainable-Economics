# Sustainable-Economics

Quarto book source code for **"Introduction to Sustainable Economics"**, a self-paced e-learning course at the University of Bern.

## 🎓 About the Course

*Introduction to Sustainable Economics* is based on the German original **"Einführung in Nachhaltige Ökonomie"** ([Nachhaltig-Wirtschaften](https://github.com/CDEteaching/Nachhaltig-Wirtschaften)), a full-fledged lecture in an inverted-classroom format at the University of Bern. The English edition adapts its accompanying script into an e-learning course and is used for **additional attainments in the Master's in Sustainability Transformations**: students who need to catch up on the economic dimension of sustainability work through the course at their own pace, with no in-person sessions. Assessment consists of a written exam on Chapters 1 to 3 and a reflection paper (see the preface).

In seven chapters, the course introduces a sustainable, pluralist perspective on economics:

1. How Can We Think About Economics?
2. Scope of Economics
3. Problem Analysis: What Is Going Wrong?
4. Strategies for a Sustainable Economy: Efficiency, Consistency, Sufficiency
5. Role of the State and Policy Paradigm for Sustainability
6. Sustainable Economics: A Synthesis
7. Approaches to Sustainable Economics

Chapters 1 to 5 end with an ungraded self-test quiz, and interactive H5P exercises are embedded throughout.

## 📚 CDE Open Educational Resources

This course is part of the Open Educational Resources of the [Centre for Development and Environment (CDE)](https://www.cde.unibe.ch/) at the University of Bern. An overview of all freely accessible CDE teaching materials can be found at [CDEteaching](https://cdeteaching.github.io/CDEteaching/). The structure and tooling of this repo are modelled on [CDEteaching/Basics-of-sustainability](https://github.com/CDEteaching/Basics-of-sustainability).

## 📜 Licence

Unless otherwise stated, all materials are licensed under the [CC-BY-NC-SA 4.0 Int License](https://creativecommons.org/licenses/by-nc-sa/4.0/). Built with [Quarto](https://quarto.org/).

## 📖 Citation

Bader, C., Bezzola, N., Brülisauer, S. (eds.). (2026). Introduction to Sustainable Economics [E-learning course]. CDE, University of Bern.

## 🧩 Contribution Matrix (CRediT Taxonomy)

| Name | Affiliation | ORCID | Roles (CRediT) |
|------------------|------------------|------------------|------------------|
| Christoph Bader | CDE, University of Bern | [0000-0002-8991-353X](https://orcid.org/0000-0002-8991-353X) | Conceptualization, Software, Supervision, Writing – original draft, Writing – review & editing, Project administration |
| Nicolà Bezzola | CDE, University of Bern | — | Writing – original draft, Writing – review & editing |
| Samuel Brülisauer | CDE, University of Bern | [0000-0002-2196-1922](https://orcid.org/0000-0002-2196-1922) | Writing – original draft, Writing – review & editing |

## Structure

- `_quarto.yml` — Quarto book configuration (title, chapter list, theme, sidebar).
- `index.qmd` — Preface.
- `1_thinking-economics/` … `7_approaches/` — the seven chapters, each with one `_intro.qmd` plus `images/` (Chapters 1 to 5 also include a generated `_quiz.qmd`).
- `quizzes/` — source and generator of the self-test quizzes; `h5p/` and `_extensions/h5p/` — interactive H5P exercises (see below).
- `references.qmd` / `references.bib` — Bibliography.
- `theme.scss`, `theme.css`, `webex.css`, `webex.js` — Theme and self-check quiz assets, taken over from the reference repo.
- `_extensions/coatless-quarto/custom-callout/` — Callout extension, taken over from the reference repo.

## Self-test quizzes

Chapters 1 to 5 end with an ungraded self-test quiz (40 questions in total). The questions live in `quizzes/quizzes.yml` (field descriptions at the top of the file). Each chapter's quiz is generated as `<chapter folder>/_quiz.qmd` and pulled in with `{{< include _quiz.qmd >}}` at the end of the chapter.

1. Edit `quizzes/quizzes.yml`.
2. Run `python quizzes/build_quizzes.py` (needs PyYAML) to regenerate the `_quiz.qmd` files. Do not edit those by hand.
3. Render. The HTML shows interactive questions checked by `webex.js`, and the PDF shows the questions followed by an answer key.

Convention: no questions on excursus boxes.

## Interactive H5P elements

H5P content is authored in [Lumi](https://app.lumi.education/) (free desktop editor) and played by a self-hosted copy of [h5p-standalone](https://github.com/tunapanda/h5p-standalone) v3.8.2 (MIT licence) in `h5p/player/`, so no H5P server or LMS is needed.

1. In Lumi, create the element and save it as `h5p/source/<name>.h5p` (lower case, hyphens, e.g. `circular-flow.h5p`). Lumi `.h5p` files include all libraries the player needs.
2. Run `powershell -ExecutionPolicy Bypass -File h5p\extract-h5p.ps1` to extract it to `h5p/content/<name>/`.
3. Place `{{< h5p circular-flow >}}` in the `.qmd` where the element should appear (optional: `title="..."`, used in the PDF). Convention: put each element in a closed callout box, like this:

   ```
   ::: {.callout-caution collapse="true"}
   #### Interactive exercise -- Label the circular flow

   {{< h5p circular-flow title="Label the circular flow" >}}
   :::
   ```

   The player inside a closed box only starts when the box is first opened (see `_extensions/h5p/h5p-loader.html`).
4. Render. The HTML shows the element; the PDF shows a note pointing to the online version.
5. To test locally, do not open `docs/*.html` by double-clicking (browsers block the player on `file://`). Use `quarto preview`, or run `python -m http.server 8000 --directory docs` from the repo root and open <http://localhost:8000/>. Do not start the server from inside `docs/`: Windows then locks the folder and the next render fails with "os error 32". Stop the server (Ctrl+C) before rendering.

The font files in `h5p/player/fonts/` were renamed to short names (e.g. `open-sans-600italic.woff2`, references updated in `styles/h5p.css` and `styles/h5p-fonts.css`), because the original names exceeded the Windows path-length limit and Git could not add them. Repeat this if the player is ever updated.

Keep the `.h5p` file in `h5p/source/` so the element can be reopened and edited in Lumi; repeat step 2 after every edit. Results are not tracked (no LMS), so use H5P for self-tests and exploration only.

## Translation notes

- Figures in the `images/` folders (and `2_scope-of-economics/charts/`) are copied unchanged from the German original and still carry German labels.
- The source `.bib` file is unchanged; some references are German-language sources.
- Video and ILIAS links point to German-language material unless stated otherwise.
