# `.ecproj`: estrutura (schema 2, EffectCraft 0.17.0)

**Regra prática: não edite o `.ecproj` à mão.** Crie e altere tudo por comandos (CLI/MCP); leia o JSON só para inspecionar ou validar (`scripts/validate_ecproj.py`). Os tempos ficam em **Tick** (254 016 000 000 por segundo), não em segundos, e cada valor carrega um tag de tipo.

Fontes: `crates/project/src/lib.rs` (Project/Item/Comp/Layer; `SCHEMA_VERSION = 2` na linha 35), `crates/project/src/props.rs` (PropGroup/Property/paths), `crates/keyframe/src/{lib.rs,value.rs}` (Keyframe/Ease/Value). Exemplo abaixo: arquivo real gerado pelo CLI 0.17.0, resumido.

```jsonc
{
  "savedBy": "0.17.0", "activeComp": 1,
  "schema": 2,                         // um schema maior que o suportado → "project schema N is newer than this version supports"
  "settings": { /* bitDepth, colorEngine, workingSpace… (file.projectSettings) */ },
  "items": {                           // objeto indexado pelo id do item (string)
    "1": { "id": 1, "name": "Min", "label": "Sandstone", "comment": "", "parent": null,
      "kind": {
        "type": "Comp",                // Folder | Comp | Footage | Solid
        "width": 1280, "height": 720, "pixel_aspect": 1.0,
        "frame_rate": { "num": 30, "den": 1 },          // 29.97 = 30000/1001
        "duration": 508032000000,                       // 2 s em Tick
        "background": [0.0, 0.0, 0.0],                  // RGB 0..1
        "work_area": [0, 508032000000], "renderer": "Classic3D",
        "shutter_angle": 180.0, "motion_blur_samples": 16, "markers": [],
        "layers": [                                     // o primeiro é a layer #1 (topo)
          { "id": 4, "name": "Red",
            "source": { "type": "Solid", "item": 3 },   // Footage{item} | Comp{item} (precomp) | Solid{item} | Text | Shape | Null | Camera | Light{kind} | Model{item} | Primitive{kind}
            "start_time": 0, "in_point": 0, "out_point": 508032000000,   // Tick, em tempo de comp
            "stretch": 100.0,
            "switches": { "video": true, "three_d": false, "motion_blur": false, "adjustment": false, "…": "…" },
            "blend_mode": "Normal", "track_matte": null,        // {"layer": <id>, "kind": "Alpha|AlphaInverted|Luma|LumaInverted"}
            "parent": null,                                     // id de outra layer da MESMA comp
            "props": { "uid": 5, "match": "…", "children": [
              { "node": "Group", "match": "transform", "name": "Transform", "children": [
                { "node": "Prop", "uid": 15, "match": "opacity", "name": "Opacity",
                  "value": { "t": "Scalar", "v": 100.0 },       // valor estático (sem keys)
                  "keys": [
                    { "time": 0, "value": { "t": "Scalar", "v": 0.0 },
                      "in_interp": "Linear", "out_interp": "Linear",   // Linear | Bezier | Hold
                      "in_ease": [], "out_ease": [],                   // por dimensão: [{"speed": u/s, "influence": 0..1}]
                      "continuous": false, "auto_bezier": false, "roving": false,
                      "spatial_in": [0,0,0], "spatial_out": [0,0,0], "spatial_auto": true },
                    { "time": 254016000000, "value": { "t": "Scalar", "v": 100.0 }, "…": "…" } ],
                  "expr": { "text": "wiggle(2,30)", "enabled": true },  // opcional
                  "ui": { "kind": "Slider", "min": 0.0, "max": 100.0 } } ] } ] } } ] } },
    "2": { "id": 2, "name": "Solids", "kind": { "type": "Folder" } },
    "3": { "id": 3, "name": "Red", "parent": 2, "kind": { "type": "Solid", "color": [1,0,0], "width": 200, "height": 200, "pixel_aspect": 1.0 } }
  },
  "next_id": 30
}
```

## Tipos de valor (`value.t`)
`Scalar` (número) · `Vec2` `[x,y]` · `Vec3` `[x,y,z]` (position, scale, anchor de layer são Vec3) · `Color` `[r,g,b,a]` 0..1 straight · `Bool` · `Enum` (índice 0-based; os rótulos estão em `crates/project/src/build.rs` e, para efeitos, em `effects-catalog.md`) · `Path` (`{closed, vertices, in_tangents, out_tangents}`) · `Text` (TextDoc) · `Layer` (id) · `Gradient` · `Str`.

Ao **escrever** por comando, use JSON simples: `50`, `[960,540,0]`, `"#ff5a36"` (cores aceitam hex), `true`. Os comandos convertem para o tipo.

## Keyframes e ease
- Easy Ease = `Bezier` com `speed 0`, `influence 1/3` (33,33%) dos dois lados (`crates/keyframe/src/lib.rs:53`). Ease padrão de um Bezier novo: `influence 1/6`.
- Easy Ease In/Out = só o lado `in` ou `out`. Hold = `Hold`.
- Propriedades espaciais (position, anchor, pontos de efeito) têm `spatial_in/out` (tangentes do motion path) e o ease temporal é **um só valor** ao longo do caminho.

## Validar
`python3 scripts/validate_ecproj.py F.ecproj --engine`: checa schema, tipos, Tick inteiros, ordem dos keys, referências de parent/track matte/source e, com `--engine`, abre no loader real. O loader real **não** pega parent pendente (layer inexistente); o script pega.
