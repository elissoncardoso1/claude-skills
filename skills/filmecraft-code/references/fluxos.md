# Receitas verificadas (FilmCraft 0.19.0)

Todas rodaram no sandbox com mídia sintética e tiveram o resultado conferido (inspect, PNG ou ffprobe).
`C=filmcraft-cli`, `S=${CLAUDE_SKILL_DIR}/scripts`. Use caminhos absolutos para mídia e saídas.
Os ids mostrados são os da execução de teste; os seus virão nos retornos.

## 1. Montar N clipes em sequência e exportar MP4 1080p (CLI, passo a passo)

```sh
$C --save-as /abs/p.fcproj exec file.newSequence name=Main width=1920 height=1080 fps=30   # {"sequence":7}
$C --project /abs/p.fcproj --save import /abs/a.mp4 /abs/b.mp4 /abs/c.mp4                # {"items":[8,9,10]}
$C --project /abs/p.fcproj --save exec timeline.place '{"items":[8,9,10],"track":"V1","seconds":0}'
python3 $S/fc_check.py /abs/p.fcproj                                                      # timeline em segundos
$C --project /abs/p.fcproj render --seconds 5 --out /abs/f5.png --scale 0.5               # olhe o PNG
$C --project /abs/p.fcproj export /abs/out.mp4                                            # h264+aac 1920x1080
ffprobe -v error -show_entries stream=codec_name,width,height,r_frame_rate:format=duration -of compact /abs/out.mp4
```

`timeline.place` com `items` põe os clipes colados, vídeo em V1 e áudio em A1, numa etapa de undo, e
devolve `placed: [[vídeo, áudio], …]`. Se os clipes não tiverem o tamanho da sequência, rode
`exec clip.fitToFrame '{"clips":[<ids de vídeo>]}'` (ou use `"matchSequence": true` numa sequência vazia).

## 2. A mesma montagem numa sessão MCP, com ids encadeados

`calls.json`:

```json
[
 {"tool":"command_run","args":{"id":"file.newSequence","params":{"name":"Promo","width":1920,"height":1080,"fps":30}}},
 {"tool":"media_import","args":{"paths":["/abs/a.mp4","/abs/b.mp4","/abs/c.mp4"]}},
 {"tool":"command_run","args":{"id":"timeline.place","params":{"items":"$1.items","track":"V1","seconds":0}}},
 {"tool":"render_frame","args":{"seconds":1,"max_side":960}},
 {"tool":"command_run","args":{"id":"file.save","params":{"path":"/abs/promo.fcproj"}}}
]
```

```sh
python3 $S/fc_mcp.py calls.json            # projeto vazio; --project P para abrir um existente
```

Um `"$N.chave"` vira o valor da chamada N, contando a partir de **0** (no exemplo, `"$1.items"` é o
retorno do `media_import`, a segunda chamada). Índices de lista também: `"$1.items.0"`,
`"$2.placed.1.0"` (vídeo do segundo clipe colocado). Se a
chamada N falhou, o script para ali sem enviar o resto. Termine sempre com `file.save {path}`: a sessão
é descartada quando o script acaba.

## 3. Título centralizado com fade-in

```json
[
 {"tool":"command_run","args":{"id":"graphics.newText","params":{"text":"Olá FilmCraft","size":120,"seconds":3,"time":0}}},
 {"tool":"command_run","args":{"id":"graphics.set","params":{"clip":"$0.clip","layer":0,"props":{"align":"center","fill_color":"#ffcc00","font_style":"Bold","stroke":true,"stroke_width":6,"stroke_color":"#000000"}}}},
 {"tool":"command_run","args":{"id":"graphics.align","params":{"clip":"$0.clip","layers":[0],"align":"hcenter"}}},
 {"tool":"command_run","args":{"id":"graphics.align","params":{"clip":"$0.clip","layers":[0],"align":"vcenter"}}},
 {"tool":"command_run","args":{"id":"effects.setParam","params":{"clip":"$0.clip","effect":"opacity","param":"opacity","value":0,"seconds":0,"keyframe":true}}},
 {"tool":"command_run","args":{"id":"effects.setParam","params":{"clip":"$0.clip","effect":"opacity","param":"opacity","value":100,"seconds":1,"keyframe":true}}},
 {"tool":"render_frame","args":{"seconds":1.5,"max_side":960}}
]
```

Junte a um projeto existente com `--project` (é preciso uma sequência aberta; sem ela o comando
responde `no sequence is open`). O texto vai para a primeira trilha de vídeo livre (V2) começando em
`time` (ticks); em `graphics.newText`, `seconds` é a **duração**. Padrão sem `graphics.set`: Inter
Regular, branco, 100 px, 5 s.

**Keyframes usam tempo da sequência.** O `seconds` de `effects.setParam` é o instante na timeline; o
arquivo guarda relativo ao clipe. Título de 5 s a 7 s com fade-in de 0,5 s (verificado):

```json
{"tool":"command_run","args":{"id":"graphics.newText","params":{"text":"Capítulo 2","seconds":2,"time":1270080000000}}},
{"tool":"command_run","args":{"id":"effects.setParam","params":{"clip":"$0.clip","effect":"opacity","param":"opacity","value":0,"seconds":5,"keyframe":true}}},
{"tool":"command_run","args":{"id":"effects.setParam","params":{"clip":"$0.clip","effect":"opacity","param":"opacity","value":100,"seconds":5.5,"keyframe":true}}}
```

`time` = segundos × 254016000000 (5 s = 1270080000000). Grave o projeto e rode `fc_check.py`: ele lista
os keyframes em segundos da sequência (`opacity.opacity@5.0s=0.0,5.5s=100.0`); `inspect` só dá a contagem. Sem `graphics.set align` e `graphics.align`, o texto começa no
centro e fica deslocado para a direita. `graphics.newText` → `{"clip","layer"}`.

## 4. Transição entre dois clipes

```json
{"tool":"command_run","args":{"id":"sequence.applyVideoTransition","params":{"clip":<clipe da direita>,"effect":"Cross Dissolve","frames":30,"edge":"in","align":"center"}}}
```

Aplique no clipe que **entra** com `edge:"in"`. Funcionou mesmo sem sobra de mídia (handles) nos
clipes: com `align:"center"` e 30 frames, a dissolve ficou em 3,5–4,5 s. Resultado `{"transition": id}`; aparece em
`inspect sequence` → `video[i].transitions`. Aplique depois de todos os `place` e cortes: um `place`
que sobrescreve o corte apaga a transição. Para áudio: `sequence.applyAudioTransition` (mesmos
parâmetros; não testado). Nomes: `exec effects.list '{"kind":"VideoTransition"}'`.

## 5. Efeito com parâmetro

```json
{"tool":"command_run","args":{"id":"effects.apply","params":{"clips":[14],"effect":"Gaussian Blur"}}},
{"tool":"command_run","args":{"id":"effects.setParam","params":{"clip":14,"effect":3,"param":"blurriness","value":40}}}
```

`effects.apply` → `{"applied":[{"clip","effect":"gaussian_blur","index":3}]}`; use esse `index` em
`effect`. Sem `clips`, o comando exige seleção (`select clips first`). Nomes e parâmetros dos efeitos:
`exec effects.list '{"kind":"Video","detail":true}'` e `inspect sequence` (efeitos do clipe).

## 6. Trilha sonora em A2 com volume reduzido

```json
[
 {"tool":"media_import","args":{"paths":["/abs/music.wav"]}},
 {"tool":"command_run","args":{"id":"timeline.place","params":{"items":"$0.items","track":"A2","seconds":0}}},
 {"tool":"command_run","args":{"id":"clip.audioGain","params":{"clips":"$1.clips","mode":"set","db":-12}}}
]
```

Um arquivo só de áudio com `track:"A2"` fica só em A2 e não toca no áudio dos clipes (A1). Para tirar o
áudio dos clipes de vídeo ao colocá-los, use `"audio": false` no `timeline.place`.

## 7. Cortar e remover um trecho fechando o buraco

```sh
$C --project P --save exec timeline.razor seconds=6                    # sem track: corta todas as trilhas → {"cuts":2}
python3 $S/fc_check.py P                                               # lista os pedaços com início/fim
$C --project P --save exec timeline.delete '{"clips":[22],"ripple":true}'   # devolve null
```

Para tirar o trecho de A a B: corte em A e em B (`timeline.razor seconds=A`, depois `seconds=B`); o
pedaço a remover é o clipe de vídeo que começa exatamente em A. Basta apagar esse clipe: o par de áudio
vai junto. Exemplo testado: 3 clipes de 4 s, remover 5–7 s deixa 10 s (verde 4–6 s, azul 6–10 s).

Vários trechos: faça **todos** os cortes primeiro (os tempos ainda são os originais), anote os ids dos
pedaços e apague do **último para o primeiro** (assim os tempos anotados não andam). Testado: remover
2–3 s e 9–10 s de 12 s (cortes em 2, 3, 9, 10; apagar o pedaço de 9 s e depois o de 2 s) deu 10 s.

`timeline.razor` com `"track":"V1"` corta só aquela trilha. `timeline.delete` com ripple remove também o
par vinculado (vídeo+áudio) e puxa o resto para trás.

## 8. Velocidade

```json
{"tool":"command_run","args":{"id":"clip.speedDuration","params":{"clips":[15],"speed":200,"ripple":true}}}
```

`speed` em porcentagem; `ripple:true` puxa os clipes seguintes (o clipe de 4 s passou a 2 s e o próximo
começou 2 s antes). Devolve `null`; confira em `inspect sequence` (`speed: 2.0`).

## 9. Legendas: importar, adicionar, exportar, queimar

```json
[
 {"tool":"command_run","args":{"id":"captions.import","params":{"path":"/abs/in.srt","language":"pt-BR"}}},
 {"tool":"command_run","args":{"id":"captions.add","params":{"track":"C1","text":"Terceira","seconds":9,"durationSeconds":2}}},
 {"tool":"command_run","args":{"id":"captions.export","params":{"path":"/abs/out.srt"}}},
 {"tool":"command_run","args":{"id":"file.exportMedia","params":{"path":"/abs/burn.mp4","range":"entire","burnCaptions":true,"captionSidecar":"vtt","wait":true}}}
]
```

`captions.import` cria a trilha C1 se não houver. Uma legenda depois do último clipe aumenta a duração da
sequência (o export usa quadros pretos até ela); exporte com `--start/--end` se não quiser isso.

## 10. Marcadores e relatório de revisão

```sh
$C --project P --save exec markers.add target=program seconds=6 name=Revisar comment="cor da cena"
$C --project P exec markers.exportCsv path=/abs/review.csv
```

Tempo em `seconds`, `timecode` ou `time` (ticks). `time: {"seconds": …}` vira 0.

## 11. Exportações variadas

```sh
$C --project P export /abs/yt.mp4 --preset "YouTube 1080p Full HD" --start 0 --end 30
$C --project P export /abs/master.mov --format prores
$C --project P export /abs/dnx.mov --format dnxhr
$C --project P export /abs/h265.mp4 --format hevc
$C --project P export /abs/mix.wav
$C --project P export /abs/anim.gif --scale 0.25 --start 0 --end 3
$C --project P export /abs/frames/f.png --start 0 --end 1          # f000.png … f0NN.png
$C --project P exec file.exportMedia '{"path":"/abs/720.mp4","width":1280,"height":720,"wait":true}'
$C --project P exec file.exportFrame '{"path":"/abs/still.png","time":508032000000}'   # 2 s
```

## 12. Intercâmbio com outros editores

```sh
$C --project P exec file.exportInterchange '{"format":"otio","path":"/abs/seq.otio"}'
$C --project P exec file.exportInterchange '{"format":"edl","path":"/abs/seq.edl"}'
$C --project P exec file.exportInterchange '{"format":"fcpxml","path":"/abs/seq.fcpxml"}'
```

`report` lista o que o formato não guarda. O EDL grava caminhos relativos ao arquivo `.edl`.

## 13. Diagnosticar e revincular mídia offline

```sh
$C --project P exec media.status          # status: online | missing | offline | unreadable
$C --project P --save exec media.relink '{"item":8,"path":"/abs/novo.mp4","force":true}'
python3 $S/fc_check.py P                  # exit 0 quando tudo está online e enquadrado
```

Sem `force`, o relink recusa arquivo com outro nome (`file name differs`). `relinkOthers` (padrão true)
tenta achar as outras mídias perdidas na mesma pasta.

## 14. Lote: o mesmo ajuste em vários projetos

```sh
for p in /abs/projetos/*.fcproj; do
  cp "$p" "$p.bak"                                       # o undo não sobrevive entre chamadas
  $C --project "$p" --save run /abs/ajuste.jsonl || { echo "falhou: $p"; mv "$p.bak" "$p"; }
  $C --project "$p" export "${p%.fcproj}.mp4" || echo "export falhou: $p"
done
```

`ajuste.jsonl` contém uma linha `{"id":…,"params":…}` por comando (linhas `#` são comentários). Sem
`--keep-going`, uma linha com erro faz o `run` parar sem gravar nada.

## 15. Operar o app aberto (bridge)

```json
[
 {"tool":"command_run","args":{"id":"window.workspace.color","params":{}}},
 {"tool":"ui_elements","args":{"prefix":"timeline.clip."}},
 {"tool":"ui_key","args":{"key":"C"}},
 {"tool":"ui_inspect","args":{}},
 {"tool":"ui_screenshot","args":{"panel":"Timeline","max_side":1200}}
]
```

```sh
$S/fc_bridge_session.sh --port 9876 --data-dir /tmp/fc-data -- \
  python3 $S/fc_mcp.py --bridge 127.0.0.1:9876 calls.json
```

`ui_key "C"` ativa a Razor e `"V"` a Selection; confira em `ui_inspect` → `result.ui.tool`. O app sobe
com projeto vazio e é fechado no fim; salve antes com `file.save {path}` se quiser manter o trabalho.
