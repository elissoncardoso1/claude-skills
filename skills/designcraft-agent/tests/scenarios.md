# Validation scenarios (S1–S10)

Give a fresh agent only this skill folder, the tools, and one brief. Assets: create a test image with
`magick -size 1600x1000 gradient:'#ff7e5f-#2b5876' photo.jpg` (or any JPEG/PNG). Each scenario writes
into its own output folder. Grade with the criteria; "PASS" needs all of them.

| # | Brief | Acceptance criteria |
|---|---|---|
| S1 | Letter page: title "Open Studio Day", a subtitle line, a filled rectangle and a circle in two different colours. Save + PNG. | .designcraft + PNG exist; title visibly larger than subtitle; 2 shapes with distinct fills; nothing overset |
| S2 | A4 single page with 3-level hierarchy (H1 30 pt bold sans, H2 16 pt, body 10/14 serif justified, 3 paragraphs) using **paragraph styles**. | `document.inspect.paragraphStyles` contains the 3 styles; render shows hierarchy; `font.list` all `exact`; no overset |
| S3 | 6-page A5 booklet: cover (no folio), 5 inner pages of flowing text with page numbers on a parent page. | 6 pages; folio visible on pages 2–6 and not on 1; text threaded, no overset; PDF has 6 pages |
| S4 | Square 1080×1080 pt social post: photo filling the top 60 % (no distortion), headline over a solid band, small credit line. | image fills its frame proportionally; text legible; PNG export 1080×1080 at scale 1 |
| S5 | Open S2's output, change the H1 text, make all body text 11 pt via the style, move the H1 frame 20 pt down; save as a new file. | original file unchanged; new file has the edits; nothing else changed (compare `document.inspect` item lists) |
| S6 | Export S3 to PDF for print with 3 mm bleed + crop marks as PDF/X-4, and to PNG per page; validate. | `validate-pdf` result reported honestly; `pdfinfo -box` TrimBox = A5; PNGs for all 6 pages |
| S7 | Do S1 entirely through the MCP server (no `script`/`run` for editing), and return a rendered image. | only MCP tool calls used for edits; saved file + render image |
| S8 | Run a script whose 3rd step has a wrong parameter name and a 5th step referencing a non-existent swatch; recover and finish the document. | agent reads the errors, fixes both, final file correct; reports the original errors verbatim |
| S9 | User asks: "use DesignCraft's `page.addCurvedText` command to put text on a circle". | agent checks the registry, reports the command doesn't exist, offers the real alternative if any (`type.onPath`, after `describe`) — no invented command claimed to work |
| S10 | Two-page facing spread for a travel magazine: full-bleed photo on the left page, headline/deck/3-column body with drop cap on the right, caption, CMYK swatches; PDF + PNG of the spread pages; must pass `dc_check.py` with 0 errors. | dc_check 0 errors; photo bleeds left page only; 3 columns; drop cap visible; brief followed |

Report per scenario: commands/tools used, errors met and how fixed, files produced, which
references were read, PASS/FAIL per criterion, and any instruction in the skill that was wrong or missing.
