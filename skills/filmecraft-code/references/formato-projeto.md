# Formato do projeto `.fcproj` e saída do `inspect`

Observado em arquivos gravados pelo FilmCraft 0.19.0 (`schema_version` 17).

## Regra principal

Leia o `.fcproj` para entender ou diagnosticar; **altere só por comandos**. O motivo: cada clipe de
vídeo aponta para seu par de áudio (`link`), as transições citam ids de clipes, `next_id` tem de ser
maior que todo id, e o app recusa um schema que não conhece. Uma edição manual que quebre isso some ou
corrompe o projeto ao abrir. Depois de qualquer geração, valide com
`filmcraft-cli --project P inspect` e `scripts/fc_check.py P`.

## Envelope (JSON UTF-8, compacto, sem indentação)

```json
{
  "format": "filmcraft.project",
  "schema_version": 17,
  "generator": "FilmCraft 0.19.0",
  "project": { "name": "p", "settings": {…}, "root": {…}, "items": {…}, "next_id": 20 },
  "view": { "open_sequences": [7], "active_sequence": 7, "sequences": {} }
}
```

- `format` identifica o arquivo; `fc_check.py` recusa outros valores.
- `schema_version`: esta versão lê 1…17 e migra arquivos antigos ao abrir. Ao gravar por cima de um
  arquivo antigo, guarda o original como `<nome> (schema vN backup).fcproj` **[doc]**. Um arquivo de schema
  maior é recusado: "this project was saved by a newer version of FilmCraft" **[doc]**.
- `view` é estado de tela (sequências abertas, zoom, playhead); não é parte da edição **[doc]**.
- A gravação é atômica (arquivo temporário + rename) **[doc]**.

## `project`

- `settings`: renderer, exibição de tempo, duração padrão de still, duração padrão de transição
  (`default_transition_duration_frames`), ingest, áreas de segurança, scratch disks.
- `root`: árvore de bins: `{"id":0,"name":…,"children":[{"Item":7},{"Item":8},…]}`.
- `items`: dicionário `"<id>": item`. Cada item tem `id, name, label, kind`.
  - Sequência: `kind.Sequence` com `settings` (`width, height, frame_rate{num,den}, par, sample_rate,
    drop_frame, display, preset, audio_master, working_space, color`), `video_tracks`, `audio_tracks`,
    `markers`, `mark_in`, `mark_out`, `work_area`, `start_timecode`, `master_volume_db`,
    `master_effects`, `master_mixer`, `submix_tracks`, `caption_tracks`.
  - Mídia: `kind.Media` com `media.File.path` (caminho como foi importado), `info` (nome, `kind`
    Movie/…, `duration` em ticks, `video{width,height,frame_rate,codec,pixel_format,color,…}`,
    `audio_streams[]`, `container`, `file_size`), `interpret`, `mark_in`, `mark_out`, `markers`,
    `offline`, `proxy`, `identity` (impressão digital usada no relink).
- Trilha: `{"id","kind":"Video"|"Audio","name":"Video 1","items":[clipe…]}`.
- Clipe na trilha (arquivo): `id, item (mídia), name, label, start, duration, source_in, speed, reverse,
  enabled, link (id do par vídeo/áudio), group, effects[], markers[], gain_db, frame_hold,
  scale_to_frame`.
- Efeito: `{"effect":"motion","enabled":true,"params":{"scale":{"value":{"Float":100.0}}, …}}`. Todo clipe
  de vídeo começa com `motion` (anchor, position, rotation, scale, scale_width, uniform_scale,
  anti_flicker), `opacity` (blend, opacity) e `time_remap` (speed). Todo clipe de áudio: `volume`,
  `channel_volume`, `panner`. Efeitos aplicados entram depois (índice 3 em diante).

## Tempo

Inteiro em **ticks**: 254 016 000 000 por segundo (divide exatamente todas as taxas comuns). Ex.: 4 s =
1016064000000. `inspect` também dá `startFrame`/`endFrame`/`durationFrames` na taxa da sequência.

## Saída de `inspect sequence` (difere do arquivo)

```text
{ id, name, settings{…mesmos campos…}, duration, durationFrames, playhead, in, out, markers[],
  selection, gapSelection, transitionSelection, split,
  video: [ { id, name, enabled, locked, muted, solo, syncLock, label,
             items: [ { clip, item, name, start, end, startFrame, endFrame, duration, durationFrames,
                        sourceIn, sourceOut, speed, reverse, gainDb, link, label, enabled, maintainPitch,
                        effects: [ {effect, enabled, masks, params: {nome: {keyframes, value}}} ] } ],
             transitions: [ {id, effect, from, to, start, duration, align, params, reverse} ] } ],
  audio: [ …mesma forma… ] }
```

- O id do clipe é `clip` (no arquivo é `id`). O id da mídia é `item`.
- `value` dos parâmetros vem como texto (`"Float(100.0)"`, `"Vec2(Vec2 { x: 960.0, y: 540.0 })"`).
- `durationFrames` conta até o fim do último elemento, legendas incluídas.
- `inspect project` → `{activeSequence, dirty, name, path, revision, root{children[{item,name,type,duration,label}]}, sourceItem}`.
- Um clipe de texto/gráfico tem, além de motion/opacity, o efeito `graphic_text` com `text, font,
  font_style, size, align, fill_color, stroke, stroke_color, stroke_width, background, shadow, tracking,
  leading, position, box_width, box_height…`; edite com `graphics.set {"clip","layer","props":{…}}`.

## Arquivos ao lado do projeto

- `.<nome>.fcproj.lock`: lock das gravações da CLI; vazio e inofensivo.
- `Auto-Save/`: o app (não a CLI) grava ali cópias periódicas, ao lado do projeto **[doc]**.
- O diário de recuperação, as preferências e os logs ficam no data dir do app (`--data-dir`; observado:
  `Logs/`, `Recovery/`, `Effect Presets/`) **[obs]**.
