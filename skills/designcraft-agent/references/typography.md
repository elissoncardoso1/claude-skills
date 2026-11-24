# Text and typography

## Stories and frames [O]
- A text frame holds a **story**; threaded frames share one story. `frame.create {content:"text", text}`
  returns `{id, story}`.
- Replace all text: `story.setText {story, text}` (MCP `set_story_text`) — keeps the formatting of
  the first paragraph/character and applies it to the new text [O t06].
- Read: `story.get {story | frame}` → `text, frames, paragraphs, lines, overset, oversetChars`
  (`overset`/`oversetChars` are `null` when everything fits; `document.inspect.stories[].overset` is a bool).
- Insert at a point: `text.placeCaret {frame, point:[x,y]}` → `{pos}`; then `text.insert {text}`;
  finish with `text.release {}`. Range replace: `story.replaceRange {story, start, end, text}`.
- Offsets (`anchor`, `focus`, `start`, `end`, `pos`, `length`) are **UTF-8 byte offsets**:
  `"Relatório"` is 10 bytes. Compute with `len(s.encode("utf-8"))`.
- `\n` = new paragraph, `\u2028` forced line break, `\t` tab, `\ue000` page number.

## Targeting formatting (the #1 pitfall) [O t06, tc]
`type.char`, `type.para`, `type.align`, `style.paragraph.apply`, `style.character.apply` act on:
1. the **text selection** — `text.select {story, anchor, focus}` (caret = anchor==focus selects that
   paragraph for paragraph-level commands), `text.selectStory {frame}`, `text.selectParagraph`; or
2. **selected text frames** — `selection.set {"ids": [frameId]}` → whole story.

Immediately after `frame.create` neither is set for that frame, and these commands change
**nothing** — and still return `null`, exactly like a successful call. Verify formatting with
`type.selectionAttrs {}` after a `text.select`: it returns `paragraphStyle`, `characterStyle`,
`ownChars` (local overrides), `paraOverrides`, and the resolved `chars`/`para` (e.g. `chars.size`) [O].
`document.inspect` and `style.list` give style **names** only. Recipe per frame:
```
frame.create {"rect": [...], "content": "text", "text": "Title\nBody..."}
selection.set {"ids": ["$0.id"]}
style.paragraph.apply {"name": "Body"}                 # whole story
text.select {"story": "$0.story", "anchor": 0, "focus": 0}
style.paragraph.apply {"name": "H1"}                   # first paragraph only
```
Character style on a range: `text.select {story, anchor, focus}` then `style.character.apply {name}`.

## Character attributes — `type.char {attrs}` [O]
`fontFamily, fontStyle, size, leading: {kind:"auto"} | {kind:"points", value}, tracking, kerning,
hScale, vScale, baselineShift, fill (swatch name), capitalization, underline, …` (`describe type.char`).
Unnamed colour on text: `object.color {color:"#hex", text:true}` with the text selected [D].

## Paragraph attributes — `type.para {attrs}` [O]
`align: left|center|right|leftJustified|centerJustified|rightJustified|fullyJustified|towardsSpine|awayFromSpine`,
`leftIndent, firstLineIndent, spaceBefore, spaceAfter, dropCapLines, dropCapChars, hyphenate (default true),
ruleAbove/ruleBelow {on, weight, color, offset…}, tabs` (`describe type.para`).
Wrong enum → error listing the valid variants. `describe type.para` truncates its key list with `…`;
other keys exist, e.g. `keepWithNext: n` (keep with the next n lines — avoids headings stranded at
a column bottom; accepted by the engine [O], attribute in source `ParaAttrs.keep_with_next` [S],
visual effect reported but not isolated [U]). Read the full attribute set of a paragraph with
`text.select` + `type.selectionAttrs` (keys of `para`).

## Styles [O]
```
style.paragraph.create {"name": "H1", "basedOn"?: "...", "nextStyle"?: "...",
   "chars": {"fontFamily": "Source Sans 3", "fontStyle": "Bold", "size": 28,
             "leading": {"kind": "points", "value": 32}, "fill": "[Black]"},
   "para": {"spaceAfter": 10, "align": "left"}}
style.character.create {"name": "Accent", "chars": {"fontStyle": "Bold", "fill": "Brand Red"}}
style.paragraph.apply {"name": "H1", "clearOverrides"?: true}
style.paragraph.edit / style.paragraph.redefine / style.list
```
Built-ins: `[No Paragraph Style]`, `[Basic Paragraph]`, `[None]` (character). Create styles first,
then apply — consistent hierarchy across pages comes from styles, not local overrides.
`style.paragraph.create` does **not** warn about missing fonts; check with `font.list`.

## Fonts [O t02]
- Bundled (always available): **Inter** Regular/Medium/SemiBold (no Bold, no Italic),
  **Source Sans 3** `Regular` `Italic` `Semibold` `Bold` (no Bold Italic), **Source Serif 4** `Regular` `Italic`
  `Semibold` `Bold` `Bold Italic`,
  **JetBrains Mono** Regular. Default text font: Source Serif 4 Regular.
- Use these exact `fontStyle` names. `It`/`BoldIt` (PostScript suffixes) are substituted; `Semibold`
  and `SemiBold` both resolve [O `evidence` font-styles test, 19 combinations].
- System-installed fonts are usable (`source: installed`); availability varies per machine —
  verify with `font.list` after applying.
- A missing style is silently substituted (Inter Bold → Inter SemiBold, `matchStatus:"styleSubstitute"`),
  a missing family is `missing:true`. `type.char` returns `{warnings}` on a family/style change to an
  unavailable font [D]. `scripts/dc_check.py` turns both into errors.
- There is no command listing every installed font on 0.17.2 [O: registry search]; test a family by
  applying it and reading `font.list`.

## Threading and overset [O t03, t04]
- Overset: `story.get` → `overset` (byte offset) / `oversetChars`; `document.inspect.stories[].overset` (bool).
- Thread to a new frame: `text.thread {from: frameId, rect: [...], spread?}` → `{story, to, overset}`.
- Fill the document: `text.thread {from, rect, spread, autoflow: true}` threads a frame per column on
  following pages and **adds pages** until the story fits (`pagesAdded`). The target spread must exist
  (insert a page first). `text.thread` requires two of `from`, `to`, `rect`.
- Columns inside one frame: `object.textFrameOptions {columns, gutter, ids}`.
- Text wrap around an image: `object.textWrap {mode:"boundingBox", offset, ids:[imageId]}`.

## Long-document features (exercised once) [O t07]
- TOC: `toc.generate {styles:["H1","H2"], page: <1-based>, createBookmarks: true}` → new frame
  with entries and page numbers. Refresh with `toc.update`.
- Footnotes, cross-references, index, variables, conditions, data merge exist (`commands footnote` …)
  [D: docs/agents.md] — not exercised here; `describe` before use.
