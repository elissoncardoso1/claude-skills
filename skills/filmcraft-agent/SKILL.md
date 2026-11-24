---
name: filmcraft-agent
description: Edita, inspeciona, renderiza e exporta projetos de vídeo do FilmCraft (editor não linear open source; projetos .fcproj) pelo filmcraft-cli (headless ou --bridge com o app aberto) e pelo servidor MCP `filmcraft-cli mcp` (ferramentas command_run, command_batch, sequence_inspect, render_frame, ui_*). Use quando o usuário pedir para montar, cortar ou aparar um vídeo, colocar clipes na timeline, títulos, legendas (SRT/VTT), transições, efeitos com keyframes, trilha sonora e ganho, mudar a velocidade, exportar MP4/MOV/ProRes/HEVC/WAV/GIF/sequência PNG, exportar EDL/OTIO/FCPXML, revincular mídia offline, gerar quadros de prévia, automatizar edições em lote ou diagnosticar um .fcproj. Gatilhos: FilmCraft, FilmeCraft, filmcraft-cli, .fcproj, mcp__filmcraft__, editar vídeo, montar vídeo, timeline, razor, render, exportar vídeo, legenda, video editing, edit video, export video, NLE.
---

# filmcraft-agent

Toda edição no FilmCraft é um **comando do motor** (718 ids, ex.: `timeline.place`). O CLI e o MCP são duas portas para os mesmos
comandos. Verificado em filmcraft-cli **0.19.0** (app 0.20.1). Antes de assumir um parâmetro, confira com
`filmcraft-cli describe <id>`.

## 0. Pré-checagem (sempre)

```
bash <skill>/scripts/doctor.sh                       # headless
bash <skill>/scripts/doctor.sh --bridge 127.0.0.1:PORTA   # se for usar o app aberto
```
Execute o script, não o leia. Saída 1 = problema bloqueante, e a linha `FAIL` diz o que fazer. Trabalhe num diretório temporário
(`mktemp -d`) ou na pasta que o usuário indicar.

## 1. CLI ou MCP?

| Situação | Use |
|---|---|
| Scripts, lotes, CI, edição reproduzível, o resultado precisa ficar em disco | **CLI headless**: `filmcraft-cli --project P.fcproj --save …` |
| Várias edições em sequência num projeto, com JSONL | CLI `run script.jsonl` (atômico: falhou, não grava) |
| Você já está numa sessão MCP com as ferramentas `mcp__filmcraft__*` | **MCP**: `command_run`/`command_batch`, e salve com `file.save`/`file.saveAs` |
| Precisa ver o quadro (PNG) sem escrever arquivo | MCP `render_frame`, ou CLI `render --out x.png` |
| Controlar o app aberto na tela (clicar, arrastar, screenshot) | MCP com `--bridge` e as ferramentas `ui_*` (exige confirmação, ver §4) |

Diferenças que importam:
- O CLI faz `file.exportMedia` **esperar** sozinho. No MCP, passe **`"wait": true`**: sem isso, o job roda em segundo plano e o arquivo
  se perde quando a sessão termina.
- `filmcraft-cli import` torna os caminhos absolutos. O MCP `media_import` grava o caminho como veio: use **sempre caminhos absolutos**.
- Cada execução do CLI é um processo novo: os ids persistem no `.fcproj` salvo, mas o undo não persiste.
- Os argumentos das ferramentas MCP são estritos (`-32602`). Os `params` dos comandos **não são validados** (chave errada é ignorada).

## 2. Regras de ouro

1. **Descubra antes de usar:** `filmcraft-cli commands <trecho>` → `filmcraft-cli describe <id>` (MCP: `command_list {filter}`).
2. **Tempo no nível de cima:** `seconds=6` ou `timecode=00:00:06:00`. Nunca `time={"seconds":6}` no topo do comando
   (`markers.add`, `timeline.razor`, `effects.setParam`…): o objeto é ignorado e vira 0. No topo, `time` aceita só ticks
   (254016000000 por segundo). **Exceção:** dentro de `moves[]` do `timeline.move`, use `"time":{"seconds":1}` (ou ticks); ali
   `seconds` solto é rejeitado. Na dúvida, siga o `describe` do comando.
3. **Uma chave errada não dá erro:** depois de editar, **sempre** verifique com `inspect sequence` (ou `sequence_inspect`). Vários
   comandos (`timeline.delete`, `timeline.setTrack`, `graphics.set`) devolvem só `null` quando dão certo. O JSON é grande (~10 KB):
   resuma assim:
   `filmcraft-cli --project $P inspect sequence --compact | python3 -c 'import json,sys;j=json.load(sys.stdin);[print(t["name"],[(c["clip"],c["name"],c["start"]/254016000000,c["duration"]/254016000000) for c in t["items"]]) for t in j["video"]+j["audio"] if t["items"]]'`
   Legendas não aparecem ali: use `exec captions.list`.
4. **Ids vêm dos resultados:** `import` → `{"items":[8,9]}`; `timeline.place` → `{"clips":[13,14,…]}`; `inspect project` lista os itens.
5. **Salve:** `--save` (no `--project`) ou `--save-as P`. No MCP: `command_run file.save` / `file.saveAs {path}`.
6. **Use o `path` do resultado do export:** se o formato não bater com a extensão, ela é acrescentada (`b.mov` + hevc → `b.mov.mp4`).
7. **Confira `errors[]` no import:** uma falha parcial sai com 0.

## 3. Receitas

Convenções: `P=proj.fcproj`; `T=254016000000` (ticks por segundo). Os ids nos exemplos são os de uma execução real e
**vão mudar**: leia-os da saída.

### R1. Montar um vídeo do zero
```
filmcraft-cli exec file.newSequence name=Main width=1920 height=1080 fps=30 --save-as $P      # {"sequence":7}
filmcraft-cli --project $P --save import /abs/a.mp4 /abs/b.mp4 /abs/musica.wav                # {"errors":[],"items":[8,9,10]}
cat > monta.jsonl <<'J'
{"id":"timeline.place","params":{"items":[8,9],"track":"V1","seconds":0}}
{"id":"timeline.place","params":{"item":10,"track":"A2","seconds":0}}
J
filmcraft-cli --project $P --save run monta.jsonl
```
`items` coloca os clipes um depois do outro; o áudio vinculado vai junto para A1. Música em A2 para não colidir.
**Verificar:** `filmcraft-cli --project $P inspect sequence --compact` → `video[0].items[].start/duration` (em ticks) e `audio[1]`.
Se a sequência deve herdar o tamanho e a taxa do clipe, use `"matchSequence":true` no primeiro `timeline.place`. Clipes de tamanho
diferente do da sequência ficam a 100% (cortados ou com borda). Veja o tamanho da mídia com `filmcraft-cli probe <arquivo>` e ajuste com
`exec clip.fitToFrame 'clips=[13,16,19]'` (cabe inteiro, pode sobrar borda) ou `exec clip.fillFrame 'clips=[…]'` (preenche, pode
cortar). Confira com `render`.

### R2. Cortar e remover um trecho, fechando o buraco (ripple)
Ex.: remover 5–7 s da imagem (V1) e do som vinculado (A1), deixando a música em A2 intacta. São **dois cortes** (início e fim) em
**cada** faixa afetada. `timeline.razor` sem `track` corta **todas** as faixas, inclusive a música, então indique a faixa:
```
cat > corta.jsonl <<'J'
{"id":"timeline.razor","params":{"seconds":5,"track":"V1"}}
{"id":"timeline.razor","params":{"seconds":5,"track":"A1"}}
{"id":"timeline.razor","params":{"seconds":7,"track":"V1"}}
{"id":"timeline.razor","params":{"seconds":7,"track":"A1"}}
J
filmcraft-cli --project $P --save run corta.jsonl
filmcraft-cli --project $P inspect sequence --compact    # (resumo da regra 3) ids das peças que COMEÇAM em 5 s em V1 e A1, ex. 26 e 28
cat > ripple.jsonl <<'J'
{"id":"timeline.setTrack","params":{"track":"A2","syncLock":false}}
{"id":"timeline.delete","params":{"clips":[26,28],"ripple":true}}
{"id":"timeline.setTrack","params":{"track":"A2","syncLock":true}}
J
filmcraft-cli --project $P --save run ripple.jsonl
```
Sem desligar o sync-lock, o ripple falha ("A2 is sync-locked and has a clip in the way"). Desligue só nas faixas que devem ficar
intactas e religue depois.
**Verificar:** V1 e A1 terminam 2 s mais cedo; A2 continua com a mesma peça (início e duração iguais).

### R3. Título legível e centralizado
```
filmcraft-cli --project $P --save --compact exec graphics.newText text="Meu título" seconds=3 track=2   # {"clip":23,"layer":0}
filmcraft-cli --project $P --save --compact exec graphics.set clip=23 \
  'props={"font":"Inter","font_style":"Bold","size":90,"fill_color":"#ffcc00","align":"center","position":[960,980]}'
filmcraft-cli --project $P render --seconds 1 --out titulo.png --scale 0.5
```
`seconds` em `newText` é a **duração** (começa em `time`/playhead = 0). `track` é um **índice a partir de 0** (2 = V3). `position`
está em **pixels da sequência** (`[960,980]` = centro-baixo em 1920×1080; em 1280×720, use `[640,650]`). Sem `align:center`, `position` é a
ponta **esquerda** do texto. As propriedades do texto **não** aparecem no `inspect`.
**Verificar:** abra o PNG (ferramenta de leitura de imagem) e confirme o texto, a cor e a posição.

### R4. Transição e trilha sonora com ganho
```
filmcraft-cli --project $P --save --compact exec sequence.applyVideoTransition clip=13 edge=out effect="Cross Dissolve" frames=15
filmcraft-cli --project $P --save --compact exec clip.audioGain 'clips=[21]' mode=set db=-12
```
Transições disponíveis: `filmcraft-cli --project $P exec effects.list kind=VideoTransition`.
**Verificar:** `inspect sequence` → `video[0].transitions[]` (`effect`, `from`, `to`, `duration`); o resultado do ganho traz
`gainDb`.

### R5. Efeito com keyframes
```
filmcraft-cli --project $P --save --compact exec effects.apply 'clips=[19]' effect="Gaussian Blur"   # {"applied":[{"clip":19,"index":3,…}]}
filmcraft-cli --project $P --save --compact exec effects.setParam clip=19 effect=3 param=blurriness value=0  seconds=8  keyframe=true
filmcraft-cli --project $P --save --compact exec effects.setParam clip=19 effect=3 param=blurriness value=40 seconds=10 keyframe=true
```
`effect` = o `index` devolvido por `effects.apply`. `seconds` (ou `frame=`, só nos params do `exec`) = **tempo da sequência** em que o
keyframe é criado. O keyframe fica guardado relativo ao clipe e o acompanha se o clipe for movido (verificado). O "kept there even
outside the clip" do `describe` só quer dizer que um keyframe pode ficar fora do intervalo visível do clipe. "Fim do clipe" = último quadro: `início + duração - 1 quadro`.
Os nomes dos parâmetros aparecem em `inspect sequence` → `effects[i].params`, que mostra só **quantos** keyframes há (`{"keyframes":2}`).
**Verificar:** `render --seconds 8.1` e `--seconds 9.9` produzem quadros visivelmente diferentes. O `render` só aceita
`--seconds`: um `--frame N` é **ignorado em silêncio** (renderiza 0 s). Para o último quadro, use `--seconds` um pouco antes do fim
(ex.: fim − 0,5 quadro).

### R5b. Mover um clipe (e o áudio vinculado) sem destruir nada
```
filmcraft-cli --project $P --save --compact exec timeline.move \
  'moves=[{"clip":16,"track":"V2","time":{"seconds":1}},{"clip":17,"track":"A3","time":{"seconds":1}}]' linked=false
```
Uma entrada por clipe. Para levar o áudio a **outra** faixa, liste-o também e passe `linked=false`; sem isso, o áudio vinculado segue
o vídeo na mesma faixa de áudio. Mover **sobrescreve** o destino: o resultado traz `overwritten[]`, que precisa vir vazio. Escolha
faixas e tempos livres, ou `"track":"new"`. Efeitos e keyframes acompanham o clipe.
**Verificar:** `overwritten` vazio; o resumo do `inspect` mostra os outros clipes com início e duração inalterados.

### R6. Velocidade
```
filmcraft-cli --project $P --save --compact exec clip.speedDuration 'clips=[16]' speed=200 ripple=true
```
**Verificar:** a `duration` do clipe caiu pela metade, e os seguintes andaram para trás (com `ripple=true`).

### R7. Exportar e conferir
```
filmcraft-cli --project $P export out/final.mp4 --compact                    # formato pela extensão (mp4→h264, mov→prores, wav, png…)
filmcraft-cli --project $P export out/trecho.mp4 --start 0 --end 2           # faixa custom: sempre os dois limites
filmcraft-cli --project $P export out/s.mp4 --preset "YouTube 1080p Full HD"  # presets: export --list-presets youtube
filmcraft-cli --project $P export out/x.mov --format hevc --scale 0.5 --no-audio   # grava out/x.mov.mp4 (veja "path")
```
**Verificar:** a saída é 0; o `path` do JSON é o arquivo real; `offlineMedia` está vazio; depois
`ffprobe -v error -show_entries stream=codec_name,width,height:format=duration -of compact=p=0 <path>` (ou
`filmcraft-cli probe <path>`). Saída 1 com "placeholder frames for offline media" → R8.

### R8. Mídia offline → revincular
```
filmcraft-cli --project $P --save --compact exec media.relink item=8 path=/abs/novo.mp4            # nome/tamanho iguais
filmcraft-cli --project $P --save --compact exec media.relink item=8 path=/abs/outro.mp4 force=true  # arquivo diferente
```
**Verificar:** `{"relinked":[…],"remaining":[]}`, e o export seguinte sai com 0 e `offlineMedia: []`.

### R9. Legendas e intercâmbio
```
filmcraft-cli --project $P --save --compact exec captions.import path=/abs/legenda.srt     # {"captions":N,"track":…}
filmcraft-cli --project $P --compact exec captions.export path=/abs/out/legenda.vtt         # formato pela extensão
filmcraft-cli --project $P --compact exec file.exportInterchange format=otio path=/abs/out/seq.otio   # edl|xml|fcpxml|otio|aaf|omf
```
`captions.import` aceita `language="pt-BR"` (o padrão é `en`). Confira as legendas com `exec captions.list` (elas não aparecem no
`inspect sequence`).
**Verificar:** leia o arquivo gerado; veja `report[]` no resultado (ex.: "EDLs hold one video track; only V1 was exported"). O OTIO
**não leva as legendas** e não avisa: exporte-as à parte com `captions.export`.

### R10. Pelo MCP (mesma lógica, uma sessão)
Com as ferramentas `mcp__filmcraft__*` (servidor iniciado sem projeto, ou com `--project`):
1. `command_run {"id":"file.open","params":{"path":"/abs/P.fcproj"}}`, ou `file.newSequence` + `media_import {"paths":["/abs/…"]}`.
2. `command_batch {"steps":[{"id":"timeline.place","params":{…}}, …]}`. Leia `failed` e `results[].error`.
3. `sequence_inspect` para conferir; `render_frame {"seconds":5,"max_side":480}` para ver.
4. `command_run {"id":"file.saveAs","params":{"path":"/abs/P.fcproj"}}`.
5. `command_run {"id":"file.exportMedia","params":{"path":"/abs/out.mp4","format":"h264","wait":true}}`: **sempre `format` e
   `wait:true`**. Sem `format`, um `.wav` vira `.wav.mp4`.

O resultado do export com `wait:true` ainda traz `job`/`poll`, mas também `result {bytes, frames, path}`: é o `result` que indica o fim.

Fora de uma sessão MCP (ex.: no shell), use `python3 <skill>/scripts/fc_mcp.py [--project P] chamadas.json`, em que `chamadas.json`
é `[{"tool":…, "args":{…}}]`. Use `"$0.items.0"` para reaproveitar o resultado da chamada 0. O script não tem `--data-dir`:
exporte `FILMCRAFT_DATA_DIR=<temp>` antes.

## 4. O que exige confirmação do usuário

Peça confirmação antes de:
- **sobrescrever** um `.fcproj` ou arquivo de mídia **do usuário** (refazer um arquivo que você mesmo gerou na tarefa é livre) (`--save` no original, `file.saveAs`/export para um caminho que já
  existe). Por padrão, trabalhe numa cópia (`--save-as nova.fcproj`) e exporte para um arquivo novo;
- apagar arquivos, ou rodar `timeline.delete` em grande quantidade num projeto que não seja cópia;
- **abrir o app** (`FilmCraft --control …`) ou usar qualquer `ui_*`/`ui_control` (agem na tela do usuário); `ui_control app.quit`
  fecha o app **sem perguntar** e descarta as alterações não salvas (elas vão para Recovery);
- gravar no diretório de dados real (`export.presets.save`, `--data-dir` omitido). Prefira `--data-dir <temp>`;
- instalar ou atualizar o filmcraft-cli, ou alterar a configuração do cliente MCP.

Livre: `--version`, `commands`, `describe`, `inspect`, `probe`, `render`/export para arquivos novos numa pasta de trabalho, e edições
em cópias.

## 5. Erros frequentes

| Mensagem / sintoma | Causa | Correção |
|---|---|---|
| `… is not available right now: no sequence is open` (saída 1) | sem projeto ou sem sequência ativa | `--project P.fcproj`, ou `exec file.newSequence … --save-as P` |
| `unknown command 'x'` (1) | id errado | `filmcraft-cli commands <trecho>` |
| `expected key=value, got 'x'` / `params JSON: …` (2) | sintaxe do `exec` | `chave=valor`; objetos e listas entre aspas simples: `'clips=[19]'` |
| a edição caiu em 0 s / no lugar errado, sem erro | chave inexistente ou `time:{"seconds":…}` | `seconds=`/`timecode=` no topo; `describe <id>`; confira com `inspect` |
| `edit failed: this edit would break sync: A2 is sync-locked…` | o ripple esbarra noutra faixa | `timeline.setTrack track=A2 syncLock=false`, ou faça o razor/delete nas faixas certas (R2) |
| `no track V9 in this sequence` | a faixa não existe | `inspect sequence` → `video[].name`; `"track":"new"` cria uma |
| `export: give --preset or --format (unknown extension)` (2) | extensão desconhecida | `--format h264` etc. |
| `custom range: need end …` (1) | só `--start` | passe `--start` **e** `--end` |
| `no export preset named 'X'` (1) | nome errado, ou preset do usuário noutro diretório de dados | `export --list-presets X` com o mesmo `--data-dir` |
| saída 1 + `has placeholder frames for offline media` (o arquivo foi gravado) | mídia ausente | R8 (`media.relink`), ou `--allow-offline` se o usuário aceitar |
| `media.relink: … doesn't match …` | nome ou tamanho diferente | `force=true` (confirme com o usuário) |
| arquivo exportado "sumiu" / nome com extensão dupla | o formato acrescentou a extensão | use o `path` do resultado |
| MCP: export devolveu `{job, poll:"jobs.list"}` **sem `result`**, e não há arquivo | faltou `wait:true` e a sessão terminou | `"wait": true` |
| `timeline.move` devolveu `overwritten:[…]` | mover **sobrescreve** o que está no destino, inclusive na faixa de áudio vinculada | mova para uma faixa ou um tempo livre (`"track":"new"`), ou `"insert":true`; confira com `inspect` |
| mídia offline não aparece no `inspect` | o status offline só aparece em export/render (`offlineMedia`) | rode um export curto (`--start 0 --end 0.1`) ou um `render` para detectar |
| projeto aberto noutra pasta com mídia offline | caminho relativo gravado pelo MCP | caminhos absolutos; `media.relink` |
| `edit.undo`: `nothing to undo` | undo não atravessa processos do CLI | faça a edição inversa, ou use `run` numa única execução |
| `filmcraft-cli: waiting for another run saving P` | outra execução `--save` em andamento | normal: ela espera a vez |
| sobram arquivos `.<nome>.fcproj.lock` | trava das execuções `--save`; o arquivo é mantido de propósito | inofensivos: não apague com execuções em andamento |
| `exported … in Ns` mesmo com `--compact` | é a linha de diagnóstico do export, no **stderr** | ignore, ou leia só o stdout (`2>/dev/null`) |
| `control authentication failed` | token ausente ou diferente | o mesmo `FILMCRAFT_CONTROL_TOKEN` (64 hex) no app e no CLI/MCP |
| `cannot connect to 127.0.0.1:PORTA` | o app não foi aberto com `--control` | `FILMCRAFT_CONTROL_TOKEN=… /Applications/FilmCraft.app/Contents/MacOS/FilmCraft --control PORTA` |
| `ui_*`: `this tool drives the live app` | MCP headless | iniciar `filmcraft-cli mcp --bridge …` (ver §4) |
| `--bridge drives the running app…` (2) | `--bridge` junto com `--project` | no bridge, abra com `exec file.open path=/abs/P.fcproj` |
| `--version` sai 137 sem nada | binário copiado por cima no macOS | `rm` o arquivo e copie de novo |

## Referências (carregue quando precisar)
- `references/cli.md`: todos os subcomandos, opções, códigos de saída e o mapa extensão→formato.
- `references/mcp.md`: as 17 ferramentas, schemas, respostas, bridge e o canal de controle.
- `references/limitacoes.md`: o que não foi verificado, as diferenças de versão e os comportamentos frágeis.
