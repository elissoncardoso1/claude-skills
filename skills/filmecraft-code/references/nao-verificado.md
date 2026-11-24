# Não verificado

O que está aqui vem da documentação oficial, do `describe`, do código-fonte ou da análise estática, mas
**não** foi executado na 0.19.0 durante a verificação desta skill. Trate como hipótese: rode num
projeto de teste e confira com `inspect`/render antes de usar no trabalho do usuário.

## Comandos e opções

| Item | Fonte | Observação |
|---|---|---|
| `sequence.applyAudioTransition` | `describe` | mesma forma da transição de vídeo |
| `timeline.move {moves:[{clip,track,time}], insert, linked, copy}` | docs/control-protocol.md | aceita `time` como objeto `{"seconds":…}` segundo a doc; confirme antes |
| `effects.setInterpolation`, `effects.moveKeyframe`, `effects.addKeyframe` (alterna) | `describe`, docs/agents.md | |
| `graphics.setCharStyle`, `graphics.setRoll`, `graphics.newShape`, `graphics.template.*` | `describe` | |
| `lumetri.*`, `lut.*`, `sequence.colorSettings` (correção de cor) | docs/control-protocol.md | |
| `mixer.*`, `essentialSound.*` (ducking automático, presets de voz) | docs/control-protocol.md | |
| `multicam.*`, `transcript.*`, `tts.*` | catálogo | |
| `file.importAaf`, importar OTIO/FCPXML/EDL de volta | catálogo | só a exportação foi testada |
| `file.exportInterchange` com `xml`, `aaf`, `omf` | `describe` | |
| `export.queue.*` além de `--queue` | docs | |
| `--gpu-rendering off`, `hardwareEncoding:"auto"`, `loudnessLufs`, `alpha` | `--help`, `describe` | |
| Progresso (`_meta.progressToken`) e cancelamento MCP de export | docs/agents.md | |
| `chave.aninhada=valor` na CLI | `--help` | prefira `'{json}'` |
| `--data-dir` da CLI para presets do usuário | `--help` | |

## App desktop / bridge

| Item | Fonte |
|---|---|
| `ui_drag`, `ui_type`, `ui.scroll`, `ui.move`, `ui.resize`, `ui.focus`, `ui.panel.show/close`, `ui.timeline.hit` | docs/control-protocol.md |
| `--control-input-only` (só aceita entrada pelo canal) | `--help` |
| `--graphics <modo>`, `--recover` | `--help` |
| `FILMCRAFT_CPU_COMPOSITE` | string no binário (REA); sem documentação encontrada |
| Bridge com o app já aberto pelo usuário (token definido antes de abrir o app) | docs; aqui o app sempre foi aberto pelo script |
| Abrir projeto do usuário no app via `file.open {path}` | docs/project-files.md |

## Plataforma

- Windows e Linux: caminhos de instalação da CLI (`%LOCALAPPDATA%\Programs\ArtCraft\FilmCraft\filmcraft-cli.exe`,
  `/usr/bin/filmcraft-cli`) vêm da documentação; só macOS arm64 foi testado.
- Asset `filmcraft-cli-<versão>-macos-<arch>.zip` da release: não baixado; a CLI testada foi compilada do
  código-fonte no commit da release 0.19.0.
