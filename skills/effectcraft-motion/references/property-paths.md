# Endereçamento de comps, layers e propriedades

## Comp
Nome ou id (`"Main"`, `1`); no CLI, `-` = comp ativa; no MCP, omitir = comp ativa. Comp inexistente → `no composition "X"`.

## Layer
- **Nome** (recomendado: sempre passe `name` ao criar: `layer.newText {…,"name":"Title"}`).
- **id** (o número devolvido por `layer.new*`: `{"layer": 27}`); uma string só de dígitos que não bate com nenhum nome vira id.
- **`"#n"`**: posição na pilha, 1 = topo. Muda quando layers são criadas ou movidas (layers novas entram no topo).
- Referência inexistente é sempre erro (`no layer "Ghost"`), nunca no-op.

## Path de propriedade (crates/project/src/props.rs:309-341)
Segmentos separados por `/` (ou `.`). Cada segmento é:
- `match`: o id estável da propriedade/grupo (`transform`, `position`, `blurriness`); equivale a `match#1`;
- `match#n`: a n-ésima ocorrência daquele match entre irmãos (`contents/rect#2/size`, `text/animators/animator#2/…`);
- `#n`: o n-ésimo filho, 1-based (`effects/#1/blurriness` = 1º efeito);
- `@uid`: por uid, também como path inteiro (`@57`).

Descubra paths com `effectcraft-cli props COMP LAYER P --flat` (ou MCP `get_layer {layer, flat:true}`). **Prefira os paths que as respostas devolvem** (`add_effect` → `effects/#1/...`; `layer.addShapeItem` → `{uid, path}`). Path de grupo em `get`/`set` → erro `` `effects/#1` is a property group; use layer.tree ``.

## Paths verificados (0.17.0)

| O quê | Path |
|---|---|
| Transform | `transform/anchor` · `transform/position` · `transform/scale` · `transform/rotation` · `transform/opacity` (3D: `transform/orientation`, `rotationX`, `rotationY`) |
| Texto | `text/sourceText` |
| Text animator (1º) | `text/animators/animator/properties/{opacity,position,scale,rotation,blur,tracking,fillColor,…}` |
| Range selector (1º) | `text/animators/animator/selectors/rangeSelector/{start,end,offset}` · `…/advanced/{units,basedOn,mode,amount,shape,smoothness,easeHigh,easeLow,randomize}` |
| 2º animator | `text/animators/animator#2/...` |
| Shape (de `layer.newShape`) | `contents/group/contents/{rect\|ellipse\|star\|polygon\|path}/{size,position,…}` · `contents/group/contents/fill/{color,opacity}` · `contents/group/contents/stroke/{color,width,opacity,cap,join,dashes/*,taper/*}` · `contents/group/transform/*` |
| Trim Paths (de `layer.addShapeItem kind:trim`) | `contents/trim/{start,end,offset,mode}` |
| Repeater (`kind:repeater`) | `contents/repeater/{copies,offset}` · `contents/repeater/transform/{position,scale,rotation,startOpacity,endOpacity}` |
| Efeito n | `effects/#n/<paramId>` (ids em `effects-catalog.md`; grupos: `effects/#1/evolutionOptions/cycle`, `effects/#1/transform/scale`) |
| Máscara | `masks/#1/feather` (doc: `layer.addMask {layer, shape: rect\|ellipse, rect}` + `layer.mask.set {field, value}`; UNVERIFIED no lab) |

Enums: `stroke/cap` 0 Butt · 1 Round · 2 Projecting; `stroke/join` 0 Miter · 1 Round · 2 Bevel (`build.rs:442-443`); `rangeSelector/advanced/shape` 0 Square · 1 Ramp Up · 2 Ramp Down · 3 Triangle · 4 Round · 5 Smooth; `basedOn` 0 Characters · 1 Characters Excluding Spaces · 2 Words · 3 Lines (`crates/project/src/build.rs:175-187`).

## Coordenadas
- `layer.newText {position}`: o texto fica **centrado em x** (justify padrão center) com a **baseline em y**. Para centrar na vertical, some ~0,35×size ao y. `justify:"left"` alinha a borda esquerda em x.
- `layer.newShape {position}`: o **centro** do shape; o conteúdo fica centrado na origem da layer (anchor `[0,0]`). Para escalar a partir da borda esquerda: `anchor [-w/2,0,0]` e `position [x_esq, y, 0]`.
- `shape.newPath {space:"comp", vertices}`: vértices em coordenadas da comp; o path é guardado centrado no espaço da layer.
- Pontos de efeito (Gradient Ramp `start/end`…): pixels em effect space; para shape/texto, o centro da comp é a origem do conteúdo.
- `layer.setParent` compensa a posição: o filho passa a guardar posição relativa ao pai.
