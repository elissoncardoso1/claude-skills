---
name: after-effects-applescript
description: Controla o Adobe After Effects aberto no macOS pelo servidor MCP ae-applescript-mcp (ferramentas ae_*, via AppleScript/DoScript, sem plugin no AE). Cria e lê composições, adiciona camadas de texto, sólido, shape, null e ajuste, define propriedades e keyframes em lote, aplica efeitos, enfileira render e salva projetos. Use quando o usuário pedir algo no After Effects ou AE, como criar ou editar composição/comp, camada, texto animado, fade, keyframe, lower third, motion, motion graphics, vinheta, efeito, render, fila de render, exportar vídeo ou salvar .aep, ou quando as ferramentas ae_* estiverem disponíveis. Também serve para diagnosticar erros do servidor (After Effects fechado, Automação negada, -1743, -1712, "recusou o script").
---

# After Effects via AppleScript (ae_*)

O servidor envia ExtendScript ao AE já aberto e lê o resultado de volta. Todo comando roda num undo group `MCP: …`, então o usuário desfaz com Cmd+Z.

## 1. Antes de tudo

1. Se uma ferramenta falhar com "não está aberto", "Automação" ou "recusou", **execute** (não leia) `bash scripts/doctor.sh`, no diretório desta skill, e siga a seta `→` da linha FALHA.
2. Chame `ae_get_project_overview`. Anote:
   - `unsaved_changes: true` ou `project_file` preenchido significa que o projeto é do usuário: só adicione, não descarte nada;
   - os nomes das comps existentes.
3. **Identifique comps sempre por `comp_name`.** O `comp_index` segue a ordem do painel Projeto (alfabética) e muda sempre que um item novo aparece: outra comp, ou a pasta "Solids" que o AE cria ao adicionar um sólido. Dê nomes únicos às camadas, porque os sólidos também viram itens com esse nome no painel.

## 2. Modelo mental que evita erros

| Fato | Consequência |
|---|---|
| Camada nova entra no **topo** (`layer_index` 1) e empurra as outras +1 | crie primeiro o que fica **atrás** (fundo) e por último o que fica na frente. Depois de cada `ae_add_layer`, use o `layer_index` que ele devolveu |
| `layer_index` é contado de cima para baixo, começando em 1 | confira com `ae_inspect_comp` antes de editar uma comp que você não criou |
| Tempos em segundos; o último frame de uma comp de 10 s a 30 fps está em 9,967 s | para "termina invisível no último frame", ponha o keyframe final em `duration - 1/fps` |
| Texto nasce com a âncora na linha de base | centralizar = `justification:"center"` + `center_anchor:true` + `position:[w/2, h/2]`, tudo no mesmo `ae_set_layer_properties` |
| `color` em `ae_add_layer` pinta o sólido, a shape **ou o preenchimento do texto** | sempre passe `color` no texto; sem ele, a cor vem do último uso no AE (ex.: #EBEBEB) |
| `font_size` padrão é pequeno (~36 px) | comece em ~9% da **menor** dimensão da comp (1080x1920 → 96; 1920x1080 → 96) e ajuste pela largura: no `detailed`, `size[0]` deve ficar entre 70% e 90% de `width` para "grande", e abaixo de 60% para "discreto". Leia, ajuste o `font_size` proporcionalmente e leia de novo |
| Tingir ou sobrepor cor = efeito Fill (`ADBE Fill`) com `Opacity` de 0 a 1 | "levemente" → 0.2–0.3; "tingido" → 0.4–0.5; "forte" → 0.6–0.8; "trocar a cor" → 1. Outros efeitos também usam escala interna; confira em `effects[].params` |
| Fade de N s no fim | o keyframe final vai em `duration - 1/fps` (último frame) e o inicial em `duration - N`. Ex.: 4 s a 30 fps, meio segundo → 3.5 e 3.967 |
| Numa propriedade animada, o campo `opacity` (ou `position`) do inspect é o valor no tempo atual | confira a animação em `animated[].keyframes`, não nesses campos |
| Caminhos em /tmp voltam como /private/tmp | é o mesmo lugar no macOS; compare pelo nome do arquivo |
| Propriedade com keyframes não aceita valor estático | use `ae_set_keyframes`. Por padrão ele **acrescenta** (keyframes no mesmo tempo são sobrescritos). `replace_existing:true` apaga todos os anteriores; só use em animação criada nesta conversa ou com confirmação |
| O render **nunca** é iniciado pelo servidor | depois de `ae_queue_render`, diga ao usuário para clicar em Render no AE |

## 3. Receitas

Mais receitas em [references/receitas.md](references/receitas.md).

**Texto centralizado com fade sobre fundo**, comp 1080x1920 de 10 s. No passo 5, inclua só os fades pedidos: o fade-in são os dois primeiros keyframes, e o fade-out são os dois últimos.
1. `ae_create_comp {name:"Story", width:1080, height:1920, duration:10}`
2. `ae_add_layer {comp_name:"Story", layer_type:"solid", color:"#26326E", name:"Fundo"}`: o fundo vai primeiro
3. `ae_add_layer {comp_name:"Story", layer_type:"text", text:"…", color:"#F05378", name:"Título"}`: entra como camada 1
4. `ae_set_layer_properties {comp_name:"Story", changes:[{layer_index:1, justification:"center", font_size:96, center_anchor:true, position:[540,960]}]}`
5. `ae_set_keyframes {comp_name:"Story", tracks:[{layer_index:1, property:"opacity", easing:"ease", keyframes:[{time:0,value:0},{time:1,value:100},{time:9,value:100},{time:9.967,value:0}]}]}`
6. Verifique (seção 4).

**Animar efeito:** `ae_apply_effect` devolve `parameters`. Use o caminho `"Effects/<nome do efeito>/<parâmetro>"` em `ae_set_keyframes`. Ex.: `"Effects/Gaussian Blur/Blurriness"`.

**Parentesco:** crie os filhos, depois o null (ele fica no topo, índice 1); em seguida `changes:[{layer_index:2,parent_index:1},{layer_index:3,parent_index:1}]`.

**Render:** `ae_queue_render {comp_name, output_path:"/abs/saida.mp4"}`. O template padrão do AE 2027 gera **.mp4**. Para `.mov`, passe `output_module_template` com um template QuickTime. Se errar, o erro lista os templates disponíveis e nada fica na fila.

## 4. Verifique sempre

Depois de editar, chame `ae_inspect_comp {comp_name, response_format:"detailed"}` e confira cada requisito do pedido:

| Requisito | Campo |
|---|---|
| tamanho e duração | `width`, `height`, `duration`, `frame_rate` |
| ordem (frente e fundo) | ordem de `layers` (o primeiro está na frente) |
| texto, cor, centralização | `text`, `fill_color`, `justification:"center"` e `position` = centro da comp. A âncora fica no centro visual do texto, então ela não é [0,0] |
| cor do sólido | `color` (só no `detailed`) |
| animação | `animated[].keyframes[{time,value}]` |
| efeitos e seus valores | `effects[].params` (no `detailed`; no `concise` vem só o nome) |
| texto cabe na tela | `size` ≤ `width` / `height` da comp |
| janela de tempo | `in_point`, `out_point` |
| fila de render | `ae_get_project_overview` → `render_queue[].status == "QUEUED"` e `output` com a extensão certa |

Relate ao usuário o que foi conferido, não só o que foi chamado.

## 5. Peça confirmação ao usuário antes de

- `ae_save_project_as` com `overwrite:true`;
- `ae_new_project` ou `ae_open_project` com `discard_unsaved_changes:true`, que perde trabalho não salvo;
- `ae_remove_layers` em camadas que você não criou nesta conversa;
- `ae_queue_render` com `overwrite:true`.

Sem confirmação, chame sem esses flags. O servidor recusa com uma mensagem, e você repassa a pergunta ao usuário.
`ae_run_extendscript` vem desligada; só o usuário pode ligá-la (`AE_MCP_ENABLE_RUN_EXTENDSCRIPT=1`). Não proponha contorná-la.

## 6. Erros frequentes

| Mensagem contém | Causa | O que fazer |
|---|---|---|
| "não está aberto" | AE fechado | peça ao usuário para abrir o AE e esperar a tela inicial |
| "Automação" / -1743 | macOS bloqueou | o usuário libera em Ajustes › Privacidade e Segurança › Automação |
| "recusou o script" | diálogo ou alerta aberto no AE | peça ao usuário para fechar a janela no AE; não repita em loop |
| "ainda está processando" | timeout, mas o script segue no AE | espere 5–10 s e repita **uma** vez |
| "Comp '…' não encontrada" | nome errado | `ae_get_project_overview` e use o nome exato |
| "layer_index … inválido" | índice mudou | `ae_inspect_comp` e use o índice atual |
| "tem keyframes" | valor estático numa propriedade animada | `ae_set_keyframes` |
| "Efeito … não reconhecido" | nome localizado ou errado | nome em inglês ou matchName (`ADBE Gaussian Blur 2`) |
| "gera '.mp4', não '.mov'" | template de saída | repita com um template da lista ou mude a extensão |

Nunca chame ferramentas ae_* em paralelo: o AE executa um script por vez.

Limites (o que não dá para fazer por aqui) estão em [references/limitacoes.md](references/limitacoes.md).

## 7. Este servidor ou o EffectCraft?

Os dois imitam o After Effects, mas não trocam arquivos (`.aep` × `.ecproj`). Use **ae_*** quando:
- o resultado precisa ser um `.aep`;
- o usuário já tem o projeto no AE;
- a peça depende de plug-ins da Adobe.

Use o **EffectCraft** (`mcp__effectcraft__*`, skill `effectcraft-motion`) quando:
- o agente precisa ver frames;
- a entrega é o vídeo renderizado, com alpha, ou em Lottie;
- não há AE disponível.

Comparação completa: `docs/comparacao-effectcraft.md` do repositório.
