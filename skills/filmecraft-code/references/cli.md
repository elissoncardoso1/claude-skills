# Superfícies de automação do FilmCraft 0.19.0

Marcação: **[obs]** = executado e observado na 0.19.0; **[doc]** = documentação oficial / `--help` /
código-fonte, não executado aqui.

## Instalação da CLI

O `.app` do macOS traz só o app. A CLI vem do asset `filmcraft-cli-<versão>-macos-<arch>.zip` da
release **[doc]** ou do código-fonte **[obs]**:

```sh
git clone https://github.com/storytold/filmcraft.git && cd filmcraft
git checkout <commit da release>   # o Info.plist do app traz FilmCraftBuildCommit
cargo build --release -p filmcraft-cli
rm -f ~/.local/bin/filmcraft-cli && cp target/release/filmcraft-cli ~/.local/bin/
```

Ao atualizar, apague antes de copiar: no macOS, copiar por cima de um `filmcraft-cli` existente
reaproveita o arquivo e o sistema mata o binário novo (exit 137, sem saída nenhuma) **[obs]**.

Para alinhar a CLI ao app: `plutil -p /Applications/FilmCraft.app/Contents/Info.plist | grep -E 'FilmCraftVersion|BuildCommit'`.

## CLI: subcomandos [obs]

```text
filmcraft-cli [OPÇÕES] <SUBCOMANDO>
  exec <id> [chave=valor ...]  | exec <id> '<json>'    um comando, resultado JSON
  run <script.jsonl | ->                                um {"id","params"} por linha; # comenta
  commands [filtro] [--json]                            lista comandos
  describe <id>                                         um comando: menu, atalho, params, habilitado
  inspect [project|sequence]                            JSON (padrão: os dois)
  import <arquivo>...                                   importa mídia
  export <saída> [--preset nome] [--format f] [--range entire|inOut|workArea]
         [--start s --end s] [--settings json] [--scale f] [--quality 0-100]
         [--no-audio] [--queue] [--allow-offline] [--gpu-rendering auto|off]
  export --list-presets [busca]
  render --seconds S --out f.png [--scale 0.5] [--allow-offline]
  probe <mídia> [--image-sequence]
  mcp                                                    servidor MCP em stdio
Opções: --project p.fcproj | --demo | --save | --save-as p.fcproj | --bridge 127.0.0.1:PORTA
        --data-dir DIR | --keep-going | --compact
```

- `chave=valor` é lido como JSON quando possível (`3.5`, `true`, `[1,2]`), senão como texto; chaves com
  ponto aninham (`color.r=1`) **[doc]**. Para objetos e listas prefira `'{json}'` **[obs]**.
- Sem `--project` a sessão começa com um projeto vazio **[obs]**. `--demo` abre o projeto de demonstração
  embutido **[obs]**.
- Códigos de saída **[obs]**: 0 sucesso; 1 comando falhou, ou export/render com mídia offline sem
  `--allow-offline`; 2 erro de uso (ex.: `--bogus` → `missing subcommand`).
- `run`: imprime `{"line","id","ok","result"|"error"}` por linha. Não há referência entre linhas: use
  `fc_mcp.py` quando um passo precisa do id criado por outro **[obs]**.

### Exportação [obs]

- Formato pela extensão: `.mp4` → H.264 High + AAC; `.mov` com `--format prores` → ProRes 422 HQ +
  PCM; `.wav` → PCM. `--scale 0.5` → metade da resolução. `--start/--end` em segundos.
- Presets: `export --list-presets <busca>` devolve `name, category, format, frameSize, extension`.
  Exemplo verificado: `"YouTube 1080p Full HD"` (H.264 1920×1080 VBR 16 Mbps).
- Resultado: `{"job","offlineMedia":[],"path","result":{"bytes","frames","render_fps","seconds"},"warnings":[]}`.
- Formatos aceitos pelo comando `file.exportMedia` **[doc, `describe`]**: h264, hevc, prores, dnxhr,
  apv, mjpeg, mxf-op1a, mxf-opatom, png, tiff, bmp, jpg, tga, dpx, exr, gif, wav, aiff, aac, mp3, flac.
  Verificados **[obs]**: mp4 (h264), `--format hevc`, `--format prores`, `--format dnxhr` (.mov), `.gif`,
  `.wav`, `.png` (sequência: `seq.png` vira `seq000.png`…`seq005.png`).
- `--settings` e `settings` **são validados**: chave errada → `settings: unknown key \`height\``. As chaves
  de settings são as de `exec export.presets.get name="<preset>"` (`frameSize`, `frameRate`, `bitrateKbps`,
  `crf`, `includeAudio`…) **[obs]**. Para tamanho, prefira `file.exportMedia {"width":1280,"height":720}` **[obs]**.
- `--range entire`, `--no-audio`, `--quality 80`, `--queue` (passa pela fila e espera) **[obs]**.
- Via comando (MCP/`exec`) o formato **não** vem da extensão **[obs]**: sem `format`, `file.exportMedia`
  gera H.264 e acrescenta `.mp4` (`mix.wav` → `mix.wav.mp4`). Passe `"format":"wav"|"prores"|"gif"|…`.
  `export.presets.list {query}` → `{default, presets:[…]}`.
- Exemplo via comando **[obs]**:
  `file.exportMedia {"path":"/abs/out.mp4","range":"entire","burnCaptions":true,"captionSidecar":"vtt","wait":true}`
  queima as legendas e grava `out.vtt` ao lado. Sem `"wait": true` volta na hora com
  `{job, poll:"jobs.list", cancel:"jobs.cancel"}` (com `wait:true` essas chaves também aparecem, junto
  com o `result` já pronto); acompanhe com `jobs.list` (`progress`, `finished`,
  `result`). Se a sessão MCP terminar antes, o arquivo **não** é gravado **[obs]**: use `wait:true`.
- Outras chaves de `file.exportMedia` (do `describe`, não testadas uma a uma): `preset, settings, format, audioCodec, width, height, fps,
  bitrateKbps, bitrateMode (cbr|vbr1Pass|vbr2Pass|crf), crf, hardwareEncoding (off|auto), scale, audio,
  quality, alpha, loudnessLufs, proresProfile, dnxProfile, h264Profile, sequence, range, startSeconds,
  endSeconds`. Leia `describe file.exportMedia` antes de usar.

### Quadro e intercâmbio [obs]

```sh
filmcraft-cli --project P render --seconds 2 --out f.png --scale 0.5      # monitor Programa → PNG
filmcraft-cli --project P exec file.exportFrame '{"path":"/abs/still.png","time":508032000000}'
filmcraft-cli --project P exec file.exportInterchange '{"format":"otio","path":"/abs/seq.otio"}'   # também edl, fcpxml
filmcraft-cli --project P exec markers.exportCsv path=/abs/review.csv          # CSV com cabeçalho Sequence,Marker ID,Name,…
```

`file.exportInterchange` aceita `edl|xml|fcpxml|otio|aaf|omf`; só edl, otio e fcpxml foram testados.

## Servidor MCP [obs]

```sh
filmcraft-cli mcp                       # headless, projeto vazio
filmcraft-cli mcp --project p.fcproj    # headless, abre o projeto
filmcraft-cli mcp --demo
filmcraft-cli mcp --bridge 127.0.0.1:9876   # app aberto com --control 9876 (token no ambiente)
claude mcp add -s user filmcraft -- "$HOME/.local/bin/filmcraft-cli" mcp
```

Ferramentas (argumentos exatos de `tools/list`):

| Ferramenta | Argumentos | Modo |
|---|---|---|
| `command_list` | `filter`, `enabled_only` | ambos |
| `command_run` | `id`, `params` | ambos |
| `command_batch` | `steps:[{id,params}]`, `stop_on_error` | ambos; devolve `{completed, failed, results}` e `isError` se algum falhou |
| `doc_inspect`, `project_inspect`, `sequence_inspect` | — | ambos |
| `media_import` | `paths` (absolutos), `bin`, `image_sequence` | ambos |
| `render_frame`, `render_preview` | `seconds`, `max_side` | headless renderiza; bridge captura o monitor Programa |
| `ui_inspect`, `ui_elements {prefix}`, `ui_click {id\|x,y,button,count,modifiers}`, `ui_drag {from,to,steps,modifiers}`, `ui_key {key}`, `ui_type {text}`, `ui_screenshot {panel,max_side}`, `ui_control {method,params}` | | só bridge |

- Argumento de ferramenta errado → erro `-32602` que lista os aceitos. `params` de `command_run` não é
  validado (veja SKILL.md, regra 1).
- A sessão headless vive enquanto o processo vive: grave com `file.save {"path":"/abs/p.fcproj"}` (devolve
  `{bytes, path, backup}`) antes de encerrar.
- Imagens voltam como conteúdo `image` (PNG). `fc_mcp.py` as grava como `mcp_<i>.png`.
- Recursos **[obs]**: `filmcraft://document`, `filmcraft://commands` (`application/json`).
- Exportação longa com `wait:true` aceita `_meta.progressToken` e cancelamento MCP **[doc]**.

### `scripts/fc_mcp.py` (execute)

```sh
python3 fc_mcp.py [--cli PATH] [--project P | --demo | --bridge 127.0.0.1:PORTA] [--list] calls.json
```

`calls.json` é uma lista `[{"tool": "...", "args": {...}}]`. Um texto `"$N.chave"` em qualquer argumento é
trocado pela chave do resultado da chamada N, contando de 0 (ex.: `"items": "$1.items"`,
`"item": "$1.items.0"`). `fc_mcp.py --help` mostra o uso.
Imprime uma linha JSON por chamada e sai com 1 se alguma falhou.

## App desktop e canal de controle

Flags do app **[obs, `--help`]**: `--control <porta>` (ou `FILMCRAFT_CONTROL_PORT`), `--control-input-only`,
`--demo`, `--empty`, `--recover`, `--no-recover`, `--data-dir <dir>` (ou `FILMCRAFT_DATA_DIR`; isola
preferências, auto-save, recuperação e logs), `--graphics <modo>`, `--version`, `-h`.

Regras do canal **[obs]**:
- Escuta só em `127.0.0.1`. Exige `FILMCRAFT_CONTROL_TOKEN` com 64 caracteres hex no ambiente do app; o
  cliente (CLI `--bridge`, MCP `--bridge`) herda a mesma variável. Token errado → `control authentication
  failed; closing the connection`.
- A porta abre antes do app aceitar comandos: as primeiras respostas são `FilmCraft is still starting;
  send the request again`. Repita até `ok: true`.
- Não ponha o token em argumentos, logs ou arquivos versionados **[doc]**.

`scripts/fc_bridge_session.sh` (execute) faz tudo isso: gera o token só no ambiente, abre o app com
`--empty --no-recover` e o `--data-dir` dado, espera ficar pronto, roda o comando e fecha o app com
`app.quit` (sem pedir para salvar; a recuperação fica no `--data-dir`).

Protocolo bruto (uma requisição JSON por linha, uma resposta por linha) **[obs]**:

```json
{"id":1,"token":"<TOKEN>","method":"engine.execute","params":{"command":"project.inspect"}}
{"id":1,"ok":true,"result":{...}}
```

Métodos verificados **[obs]**: `engine.execute {command, params}`, `engine.commands` (718), `ui.inspect`,
`ui.elements {prefix}`, `ui.click {id}`, `ui.key {key}` (`"C"` ativa a Razor, `"V"` a Selection),
`ui.set {"workspace":"Editing"}`, `ui.playback {"action":"stop"}`, `ui.screenshot`, `app.quit`.
`ui.timeline.locate {clip}` responde `clip not visible in the timeline` para id inexistente ou fora da tela.
Os demais métodos estão em [nao-verificado.md](nao-verificado.md).

Ids de elementos **[obs]**: `tools.<Ferramenta>` (`tools.Selection`, `tools.Razor`…),
`timeline.clip.<id>`, `timeline.clip.<id>.volume`. Liste com `ui_elements {"prefix":"…"}` em vez de adivinhar. `ui_inspect` → `result.ui.tool`, `.workspace`, `.focused`, `.mode`.
A interface segue o idioma do sistema (pt-BR observado); ids não mudam com o idioma.

Exemplo verificado (CLI contra o app):

```sh
fc_bridge_session.sh --port 9876 --data-dir /tmp/fc-data -- \
  filmcraft-cli --bridge 127.0.0.1:9876 exec window.workspace.color      # → {"workspace":"Color"}
```
