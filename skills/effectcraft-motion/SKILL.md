---
name: effectcraft-motion
description: Create motion graphics and animations with EffectCraft (effectcraft-cli 0.17.0, open-source After Effects-style compositor) through its CLI or MCP server, and export them to MP4/H.264, ProRes 4444 with alpha, WebM VP9 with alpha, PNG sequence, GIF or Lottie (.json/.lottie). Use when the user asks to create motion graphics, animate text or a logo, make a lower third, title card, kinetic typography, logo reveal, text reveal, shape write-on, transition, looping background, vinheta, animação para vídeo/redes sociais (Reels, TikTok, Shorts, 9:16, 1:1, 4:5), exportar Lottie, or mentions EffectCraft, effectcraft-cli, .ecproj, criar motion graphics, animar texto/logo, lower third, vinheta, kinetic type.
---

# EffectCraft motion graphics

EffectCraft é um compositor estilo After Effects em Rust. Tudo é um **comando** com id e parâmetros JSON (734 no 0.17.0). CLI, MCP e canal de controle chamam os mesmos ids. Esta skill foi construída e testada contra o **effectcraft-cli 0.17.0** no macOS arm64. Toda afirmação aqui foi verificada (evidências no `ec-lab/EVIDENCE.md` do projeto de origem).

## 0. Pré-voo (uma vez por sessão)

```bash
effectcraft-cli --version            # esperado: effectcraft-cli 0.17.0; outra versão → confira ids com `commands`
```
- Ferramentas `mcp__effectcraft__*` disponíveis? → via **MCP** (preferida para criar e iterar). Senão → **CLI**.
- Para verificação visual são necessários `magick` (contact sheets) e `ffprobe` (checagem dos renders). Os scripts degradam sem eles, mas avise o usuário.
- `SK=~/.claude/skills/effectcraft-motion`: os scripts e receitas usam caminhos relativos a ele. Trabalhe na pasta do usuário, nunca dentro da skill.

## 1. Workflow obrigatório

1. **Entender o briefing.** Fixe e repita ao usuário: formato e resolução (16:9 1920×1080 · 9:16 1080×1920 · 1:1 1080×1080 · 4:5 1080×1350), duração, fps (padrão 30), paleta (hex), **texto exato** (com acentos), fonte, entrega (MP4, ProRes alpha, WebM alpha, GIF, Lottie). Pergunte só o que for ambíguo e mudar o resultado; o resto, defina e diga qual padrão usou.
2. **Escolher a via.**
   - MCP: criar/iterar (`render_frame` devolve a imagem; `add_keyframe {interpolation:"easyEase"}`; `add_effect {values}`; `batch` com undo atômico).
   - CLI one-shot (`exec`/`run`/`set`/`render`): tarefas pontuais em um `.ecproj` existente.
   - CLI `run --args-file` em shell script: lotes e variações (as receitas são assim).
   - `script --eval` / `run_script`: lógica com laços (cuidado: o `setValueAtTime` usa tempo de comp).
   - Detalhes: `references/mcp-tools.md`, `references/cli-reference.md`.
   - **Partiu de uma receita?** Rode o `.sh` dela (seção 4) e ajuste; é o caminho mais curto e testado.
3. **Construir incrementalmente e salvar.**
   - Comp nova sempre com `width`, `height`, `frameRate`, `duration` explícitos. Pelo CLI, **sempre `--empty`** (sem projeto, o CLI abre o DEMO).
   - Dê `name` a toda layer criada e endereçe por nome.
   - Depois de cada bloco: salve (`--save` / `save_project`) e rode `exec expr.errors '{"comp":"C"}'` (erro de expressão **não** falha o comando).
4. **Preview antes do render final.** Rode `$SK/scripts/preview.sh P.ecproj COMP 6` (com `TIMES="0.3 0.8"` para os momentos-chave) e **olhe** o `sheet.png` (ou use `render_frame` no MCP). Confira: entra/sai no tempo certo? texto legível e dentro da safe area? nada cortado? frame vazio onde não devia?
5. **Renderizar e verificar.** Rode `$SK/scripts/render.sh P.ecproj COMP OUT FORMAT [args]`. Ele recusa sobrescrever (o CLI sobrescreve sem avisar) e confere existência, tamanho, duração e alpha via ffprobe. Lottie: `$SK/recipes/lottie-web-export.sh` (warnings + player real). Ver `references/export-formats.md`.
6. **Informar limitações.** Repasse todos os `warnings` do Lottie, efeitos descartados, recursos não suportados e qualquer item marcado UNVERIFIED que você usou. Ver `references/known-gaps.md`.

## 2. Regras que evitam os erros mais comuns (todas reproduzidas no laboratório)

- **Ids e parâmetros só do catálogo**: `references/command-catalog.md` (gerado do binário) ou `commands --filter X` / `describe_command`. Chave desconhecida dá erro com a lista aceita: leia a mensagem.
- **Tempo:**
  - `prop.addKey`, `add_keyframe` e `set --time` usam **tempo de layer**; leituras e `render_frame` usam **tempo de comp**.
  - Em layer deslocada, passe `"timeBase":"comp"`.
  - Último frame = `duration − 1/fps`.
- **Ease pelo CLI**: `prop.addKey` cria keys **lineares**. Aplique no mesmo `run`: `keys.selectAll {"layers":[…]}` + `keys.easyEase {}`.
- **Presets** (`anim.applyBuiltinPreset`, `layer.applyTextPreset`) criam keys a partir do **CTI**: `time.set {"time":T}` antes.
- **Precompor antes de parentear.** Precompor layers parenteadas a um null que fica de fora quebra o layout, sem erro.
- **Valores**: vec3 para position/scale/anchor (`[x,y,z]`); cores em `"#hex"`; enums são índices 0-based (rótulos em `references/property-paths.md` / `effects-catalog.md`).
- Parâmetro com **tipo** errado (`"width":"wide"`) é ignorado sem aviso, e a comp cai em 1920×1080 @ 29,97 fps. Confira com `exec comp.info` após criar.
- **Texto**: `layer.newText {position}` centra em x e põe a **baseline** em y; `justify:"left"` alinha à esquerda. Fontes embutidas (portáteis): Inter (Regular/Medium/SemiBold/Bold/Italic), JetBrains Mono, Noto Serif.
- **Shapes**: `layer.newShape {position}` = centro do shape. Para crescer de uma borda, mova o `transform/anchor`.
- **Alpha** só sem layer de fundo opaca. h264 e webm-AV1 recusam `--channels rgba` (erro explícito).
- Não edite `.ecproj` à mão: tempos são Tick (254 016 000 000/s). Valide com `$SK/scripts/validate_ecproj.py F --engine`.

## 3. O que NÃO fazer

- Inventar ids de comando, nomes de efeito, paths ou parâmetros. O que não estiver no catálogo/nas referências, descubra com `commands`, `describe_command`, `props --flat` ou `effect.list`.
- Assumir compatibilidade com After Effects: **não abre `.aep`/`.aepx`/`.mogrt`/`.ffx`**, **não roda plug-ins** (Trapcode, Element, Saber, Optical Flares…), presets do AE não existem. Expressões e scripting seguem o modelo do AE, mas teste cada uma.
- Pular a verificação visual ou a do arquivo final. A fidelidade com o AE não é medida (alpha); só os frames provam o resultado.
- Prometer recursos no Lottie sem ler `warnings`: Glow, Fractal Noise, partículas, Linear Wipe, layer styles, blur de animador de texto e expressões **não** vão para o Lottie.
- Trabalhar no projeto demo por engano (CLI sem `--project`/`--empty`).

## 4. Receitas testadas (`$SK/recipes/`)

Cada `X.sh` gera um `.ecproj` validado; `X.md` explica as técnicas e traz o frame de referência (`recipes/frames/X.png`). Templates prontos (saídas validadas) em `templates/`; troque textos com `layer.setText {"layer","text"}`.

| Pedido | Receita | Formato | Lottie |
|---|---|---|---|
| lower third, nome + cargo | `lower-third` | 16:9, 6 s | sim |
| título, kinetic type, palavras em sequência | `title-card-kinetic-type` | 16:9, 4 s | sim |
| logo reveal, vinheta de marca | `logo-reveal` (trim + Glow) | 16:9, 4 s | parcial (sem Glow) |
| texto letra a letra / por palavra, stories | `text-reveal-per-character` | 9:16, 4 s | parcial (sem blur) |
| traço que se desenha, assinatura, linha | `shape-write-on` | 16:9, 3 s | sim |
| fundo animado em loop | `looping-background` (Fractal Noise + expressão) | qualquer, 10 s | não |
| transição entre cenas | `transition-wipe` (Linear Wipe) | 16:9, 4 s | não |
| entrega web/app em Lottie | `lottie-web-export` | — | é a receita |

Os scripts aceitam variáveis de ambiente (`NAME=`, `TITLE=`, `ACCENT=`, `W=`/`H=`…) e o caminho do `.ecproj` de saída como argumento.

## 5. Checklist de motion design (aplique antes do preview)

- [ ] **Easing**: nada linear em UI, títulos e logos sem motivo. Easy Ease no mínimo; para "snap", influence 70–85% (`keys.velocity`). Linear só em loops contínuos e rotações constantes.
- [ ] **Timing**:
  - entradas e saídas de 0,3–0,8 s;
  - stagger de 0,05–0,2 s entre elementos;
  - texto parado legível por ~0,3 s/palavra + 1 s;
  - saída mais curta que a entrada.
- [ ] **Hierarquia**: um elemento principal por vez; o secundário entra depois (stagger) e é menor ou mais leve; no máximo 2 pesos de fonte.
- [ ] **Safe areas** (convenções de mercado; confira a plataforma de destino):
  - 16:9: title-safe 10% (texto dentro de 192–1728 px em x), action-safe 5%;
  - 9:16 (Reels/TikTok/Shorts): texto fora dos ~14% de cima e ~20% de baixo, margens laterais ≥ 8%;
  - 1:1 e 4:5: margem ≥ 8% em todos os lados.
- [ ] **Contraste e legibilidade**:
  - texto com contraste ≥ 4.5:1 contra o fundo (use painel/sombra se o fundo variar);
  - corpo ≥ 34 px em 1080p e ≥ 48 px em 9:16;
  - sem texto fino sobre ruído.
- [ ] **Fim limpo**: a última posição fica estável ou sai da tela; loops voltam ao estado inicial em t=duration.

## 6. Referências (carregue sob demanda)

| Arquivo | Quando |
|---|---|
| `references/cli-reference.md` | sintaxe do CLI, padrões de `run`, exit codes |
| `references/mcp-tools.md` | as 27 (+9 bridge) tools MCP; MCP × CLI × script |
| `references/command-catalog.md` | **todos** os 734 ids com params (grep por namespace: `` grep -n '^| `keys\.' ``) |
| `references/effects-catalog.md` | os 307 efeitos com ids de parâmetros e enums (`grep -n -i 'glow'`) |
| `references/property-paths.md` | endereçamento de comp/layer/propriedade, paths verificados, coordenadas |
| `references/keyframes-easing.md` | interpolação, ease, velocity, tempo de layer × comp, presets |
| `references/expressions.md` | padrões testados (wiggle, loopOut, ligação, parâmetros de efeito), `expr.errors` |
| `references/export-formats.md` | formatos, alpha, GIF, Lottie (suporte e warnings reais) |
| `references/ecproj-schema.md` | estrutura do `.ecproj` com exemplo real comentado |
| `references/known-gaps.md` | limitações da versão alpha e armadilhas |
| `references/troubleshooting.md` | mensagens de erro reais → correção; falhas silenciosas |

Scripts: `scripts/preview.sh` (frames + contact sheet), `scripts/render.sh` (render verificado), `scripts/validate_ecproj.py` (schema + engine), `scripts/lottie_preview.sh` (Lottie no lottie-web via Chrome headless).
