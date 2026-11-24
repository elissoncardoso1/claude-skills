---
name: filmecraft-code
description: Cria, edita, inspeciona, renderiza e exporta projetos de vídeo do FilmCraft (FilmeCraft, editor não linear open source em Rust, arquivos .fcproj) pelo shell com filmcraft-cli, pelo servidor MCP (headless ou bridge) ou pelo canal de controle do app aberto. Use quando o usuário pedir para montar ou cortar um vídeo, editar a timeline, colocar clipes, títulos, legendas, transições, efeitos, keyframes, trilha sonora, ajustar velocidade ou volume, exportar MP4/ProRes/WAV/GIF/sequência de imagens, exportar EDL/OTIO/FCPXML, revincular mídia offline, automatizar edições em lote ou diagnosticar um .fcproj. Gatilhos - FilmCraft, FilmeCraft, filmcraft-cli, .fcproj, editar vídeo, montar vídeo, timeline, render, exportar vídeo, legenda, video editing, edit video, export video, NLE, cut, trim, captions.
---

# FilmCraft pelo Claude Code

Verificado em **FilmCraft 0.19.0 / filmcraft-cli 0.19.0**, macOS arm64, 2026-11-09. Cada regra abaixo
foi observada nessa versão. Uma CLI compilada da branch `main` na mesma data se identifica como
**0.17.0** e tem o mesmo catálogo (718 comandos, parâmetros idênticos): funciona igual. Para outra
versão, confira com `filmcraft-cli commands --json` e confie no binário instalado mais do que neste texto.

FilmCraft é um editor de vídeo não linear (modelo de painéis e atalhos de NLE profissional). Tudo o que a
interface faz é um **comando** com id e parâmetros (718 na 0.19). O mesmo comando roda pela CLI, pelo MCP
e pelo canal de controle do app.

## 0. Localize e descubra antes de agir

```sh
C=$(command -v filmcraft-cli || echo ~/.local/bin/filmcraft-cli)   # o .app do macOS não traz a CLI
"$C" --version                            # use "$C" no lugar de filmcraft-cli nos exemplos se não estiver no PATH
/Applications/FilmCraft.app/Contents/MacOS/FilmCraft --version  # versão do app (não abre janela)
filmcraft-cli commands <palavra>          # busca ids por id, rótulo ou menu
filmcraft-cli describe <id>               # parâmetros, menu, atalho, se está habilitado agora
```

Se não houver CLI, veja "Instalação" em [references/cli.md](references/cli.md). Leia o `describe` de todo
comando antes do primeiro uso: parâmetros desconhecidos **não** dão erro (regra 3.1). `"enabled": false`
no `describe` é normal sem projeto aberto ou sem seleção; o comando roda quando recebe o alvo explícito.

## 1. Escolha a interface

| Necessidade | Use | Por quê |
|---|---|---|
| Passos isolados, reproduzíveis, que gravam no arquivo | `filmcraft-cli --project P --save exec ID '{json}'` | cada chamada abre, edita e salva |
| Vários passos que dependem de ids devolvidos | `python3 ${CLAUDE_SKILL_DIR}/scripts/fc_mcp.py --project P calls.json` | uma única sessão; `"$N.chave"` reaproveita resultados |
| Lote fixo de comandos sem ids novos | `filmcraft-cli --project P --save run script.jsonl` | uma linha `{"id","params"}` por comando |
| Exportar | `filmcraft-cli --project P export out.mp4` | espera o fim e verifica mídia offline |
| Ver o app ao vivo, clicar, capturar a janela | `scripts/fc_bridge_session.sh -- …` com MCP `--bridge` | só quando o usuário quer a janela |

Não edite o `.fcproj` à mão: os ids, os vínculos áudio/vídeo e as transições são coerentes entre si e o
app recusa ou corrompe arquivos inconsistentes. Gere e altere projetos sempre por comandos.

## 2. Fluxo: INSPECIONAR → PLANEJAR → EDITAR → RENDERIZAR → CHECAR → EXPORTAR → VERIFICAR

1. **Inspecionar.** `filmcraft-cli --project P inspect project` (bins, itens, ids) e `inspect sequence`
   (trilhas `video[]`/`audio[]`, cada uma com `items[]`, `transitions[]`; marcadores; configurações).
2. **Planejar.** Defina tamanho, fps e a ordem dos clipes. Converta tempos para segundos.
3. **Editar.** Novo projeto: `filmcraft-cli --save-as P.fcproj exec file.newSequence name=Main width=1920 height=1080 fps=30`.
   Depois `import` (caminhos absolutos), `timeline.place`, títulos, transições e efeitos.
4. **Renderizar.** `filmcraft-cli --project P render --seconds S --out f.png --scale 0.5` e **olhe** o PNG.
   Comando aceito não prova resultado certo.
5. **Checar.** `python3 ${CLAUDE_SKILL_DIR}/scripts/fc_check.py P.fcproj` lista a timeline em segundos
   (clipes, transições, keyframes) e sai com 1 se houver mídia offline ou clipe com tamanho diferente da
   sequência sem ajuste. Ele lê o arquivo: salve antes.
6. **Exportar.** `filmcraft-cli --project P export out.mp4` (formato pela extensão) ou `--preset "…"`.
7. **Verificar.** `ffprobe` no arquivo (codec, tamanho, fps, duração) se disponível; senão `filmcraft-cli probe out.mp4`.

Receitas completas e testadas: [references/fluxos.md](references/fluxos.md).

## 3. Regras críticas (todas observadas em teste)

1. **Parâmetros desconhecidos são ignorados em silêncio.** `timeline.place {"item":8,"trak":"V1"}`
   foi aceito, usou os padrões (V1 em 0 s) e sobrescreveu clipes que já estavam lá. Copie os nomes do
   `describe` (mais `seconds`/`timecode`, regra 2) e confira com `inspect sequence` depois de cada edição. Só os argumentos das *ferramentas*
   MCP são validados (`-32602`); o conteúdo de `params` vai direto ao comando.
2. **Tempo vai em chave de topo.** Onde o `describe` mostra `"time": ticks`, os comandos também aceitam
   `"seconds": 6` e `"timecode": "00:00:06:00"`, mesmo sem listá-los (verificado em `timeline.place`,
   `timeline.razor`, `markers.add`, `effects.setParam`, `captions.add`). Um objeto `"time": {"seconds": 6}`
   virou 0 em `markers.add`, não cortou nada em `timeline.razor` e, em `effects.setParam`, sobrescreveu o
   keyframe de 0 s. Exceção: em `graphics.newText` (e nos outros `graphics.new*`), `seconds` é a
   **duração** do clipe; o início vai em `"time"` em ticks. Keyframes (`effects.setParam`) usam tempo da
   **sequência**, não do clipe. 1 s = 254016000000 ticks; os resultados vêm em ticks.
3. **Use os ids devolvidos.** `file.newSequence` → `{"sequence": id}`; `import` → `{"items": [...]}`;
   `timeline.place` → `{"clips": [...], "placed": [[vídeo, áudio], ...]}` (só vídeo com `"audio": false`);
   `graphics.newText` → `{"clip", "layer"}`. Os ids dependem do que já existe no projeto (o mesmo import
   deu 8 depois de `file.newSequence` e 1 num projeto vazio): nunca presuma, leia o retorno.
4. **`timeline.place` sobrescreve o destino.** Clipes já existentes no intervalo são cortados ou
   substituídos (e transições ali somem). Para empurrar o resto, passe `"insert": true`. `"items":[a,b,c]`
   coloca em sequência numa só etapa de undo.
5. **Clipe de outro tamanho não é ajustado.** Um 1080p numa sequência 720p fica cortado (escala 100 %).
   Use `exec clip.fitToFrame '{"clips":[id]}'`, ou, numa sequência vazia, `"matchSequence": true` no
   primeiro `timeline.place` (a sequência adota tamanho e fps do clipe).
6. **Texto novo começa no centro, não centralizado.** `graphics.newText` põe o ponto de alinhamento no
   meio do quadro, então o texto começa ali. Para centralizar:
   `graphics.set {"clip":C,"layer":0,"props":{"align":"center"}}` e depois
   `graphics.align {"clip":C,"layers":[0],"align":"hcenter"}` e `"vcenter"`. O título vai para a primeira
   trilha de vídeo livre acima (V2).
7. **Cada chamada `exec` é uma sessão nova.** Sem `--save`/`--save-as` nada é gravado. O histórico não
   vai para o arquivo: `edit.undo` numa chamada seguinte responde `nothing to undo`. Para desfazer passo a
   passo, trabalhe numa sessão MCP (`edit.undo`, `history.list`), ou guarde uma cópia do `.fcproj` antes.
8. **`run` não salva quando falha.** Sem `--keep-going`, ele para na primeira linha com erro, sai com 1 e
   não grava nada. Com `--keep-going`, grava as linhas que funcionaram e ainda sai com 1.
9. **Mídia offline bloqueia export e render.** O arquivo sai com quadros "media not found" e o exit é 1.
   Antes: `exec media.status`. Corrija com `media.relink {"item":id,"path":"/novo/caminho","force":true}`
   (`force` é necessário se o nome do arquivo mudou). `--allow-offline` só quando o usuário aceitar.
10. **Caminhos sempre absolutos.** O projeto guarda o caminho como foi passado: a CLI gravou
    `cwd/../x.mp4` e o MCP gravou `../x.mp4` literalmente, que fica offline se o projeto for aberto de
    outro diretório.
11. **Uma sessão por projeto.** Chamadas da CLI com `--save` se revezam com um lock `.<nome>.lock`, mas o
    app e o MCP não pegam esse lock. Não grave por CLI um projeto que está aberto no app.
12. **Proteja os projetos do usuário.** Antes de alterar um `.fcproj` do usuário (mesmo a pedido), faça
    `cp P P.bak`, mantenha o `.bak` e diga ao usuário onde ele ficou; não apague backups. Para testar,
    use uma cópia ou `--save-as`. Não rode o app com o `--data-dir` padrão em testes; use uma pasta própria.

## 4. Exportação em uma linha

```sh
filmcraft-cli --project P export out.mp4                                 # H.264 + AAC, tamanho da sequência
filmcraft-cli --project P export out.mp4 --preset "YouTube 1080p Full HD" --start 0 --end 10
filmcraft-cli --project P export master.mov --format prores            # ProRes 422 HQ
filmcraft-cli --project P export mix.wav                                # só áudio
filmcraft-cli --project P export prev.mp4 --scale 0.5                   # metade da resolução
filmcraft-cli export --list-presets youtube                             # presets embutidos e do usuário
```

A CLI `export` deduz o formato pela extensão. O comando `file.exportMedia` (via `exec` ou MCP) não:
sem `"format"` ele gera H.264 e grava `nome.wav.mp4`. Legendas queimadas, `.srt`/`.vtt` ao lado, perfis,
CRF e bitrate: [references/cli.md](references/cli.md).

## 5. App ao vivo (bridge)

Só quando o usuário quer ver ou operar a janela. O app precisa de `--control PORT` e de
`FILMCRAFT_CONTROL_TOKEN` (64 hex) no ambiente, e o cliente herda o mesmo token. O script abaixo gera o
token, abre o app isolado, espera ficar pronto, roda o comando e fecha o app:

```sh
${CLAUDE_SKILL_DIR}/scripts/fc_bridge_session.sh --port 9876 --data-dir /tmp/fc-data -- \
  python3 ${CLAUDE_SKILL_DIR}/scripts/fc_mcp.py --bridge 127.0.0.1:9876 calls.json
```

Ferramentas só do bridge: `ui_inspect`, `ui_elements`, `ui_click`, `ui_drag`, `ui_key`, `ui_type`,
`ui_screenshot`, `ui_control`. Detalhes e protocolo bruto: [references/cli.md](references/cli.md).

## 6. Erros comuns e como resolver

| Sintoma | Causa | Solução |
|---|---|---|
| Comando aceito mas nada mudou, ou mudou no lugar errado | nome de parâmetro errado ou tempo como objeto | `describe <id>`; use `seconds` no topo; confira com `inspect sequence` |
| `select clips first` / `is not available right now` | o comando age sobre a seleção (ou não há o que desfazer) | passe o alvo explícito (`"clips":[id]` ou `"item":id`) |
| `unknown command \`x\`` | id inventado | `filmcraft-cli commands <palavra>` |
| Export sai com exit 1 e aviso `placeholder frames` | mídia offline | `exec media.status`; `media.relink … force:true` |
| `media.relink: … doesn't match … file name differs` | arquivo renomeado | repita com `"force": true` |
| Imagem cortada ou com bordas | clipe com tamanho diferente da sequência | `clip.fitToFrame` |
| Título deslocado para a direita | ponto de alinhamento no centro | `graphics.set align:center` + `graphics.align hcenter/vcenter` |
| Transição sumiu | um `place` posterior sobrescreveu o corte | reaplique `sequence.applyVideoTransition` depois das edições |
| Sequência mais longa que os clipes | legenda ou marcador além do último clipe | ajuste as legendas ou exporte com `--start/--end` |
| `-32602 unknown argument` no MCP | argumento de ferramenta errado | a mensagem lista os aceitos |
| Título com duração errada | `seconds` em `graphics.newText` é duração | início em `"time"` (ticks) |
| Depois do relink o item mantém o nome antigo | o nome exibido não muda | confira `status: online` em `media.status` |
| `timeline.delete`, `clip.speedDuration`, `graphics.set` devolvem `null` | é o retorno normal | confira com `inspect sequence` |
| Bridge responde `still starting` | a porta abre antes do app aceitar comandos | repita após 0,5 s (o script já espera) |
| Bridge: `control authentication failed` | token diferente entre app e cliente | inicie os dois no mesmo ambiente (use o script) |
| `this project was saved by a newer version` | schema maior que o suportado | atualize o FilmCraft; não edite o número do schema |

## 7. Arquivos desta skill

- [references/cli.md](references/cli.md): CLI, opções, códigos de saída, MCP, bridge, protocolo, instalação.
- [references/formato-projeto.md](references/formato-projeto.md): o `.fcproj` e a saída do `inspect`.
- [references/fluxos.md](references/fluxos.md): receitas testadas (montagem, títulos, legendas, áudio, export, intercâmbio, relink).
- [references/nao-verificado.md](references/nao-verificado.md): o que não foi testado; trate como hipótese.
- `scripts/fc_mcp.py` (execute): uma sessão MCP com vários passos e `"$N.chave"`; salva imagens como PNG.
- `scripts/fc_check.py` (execute): resumo e checagem do projeto antes do export.
- `scripts/fc_bridge_session.sh` (execute): abre o app com canal de controle, roda um comando, fecha.
