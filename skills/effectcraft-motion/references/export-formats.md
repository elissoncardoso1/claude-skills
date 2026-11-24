# Exportação: formatos, alpha e Lottie

## Render de vídeo/imagem (`effectcraft-cli render`)
`render P --comp C --out FILE --format F [--channels rgb|rgba] [--prores PROFILE] [--webm-codec vp9|av1] [--start S --end S] [--fps N] [--resolution full|half|third|quarter|K] [--quality best|draft] [--bitrate KBPS] [--video-quality N] [--progress]`.
Wrapper com verificação: `scripts/render.sh P C OUT FORMAT [args…]` (recusa sobrescrever, confere tamanho, duração e alpha com ffprobe).

| Entrega | Comando verificado | ffprobe (lab/09) |
|---|---|---|
| MP4 H.264 (redes, web) | `--format h264` | h264 High, yuv420p, fps da comp |
| ProRes 4444 **com alpha** | `--format prores --prores 4444 --channels rgba` | prores 4444, `yuva444p12le` |
| WebM VP9 **com alpha** (web) | `--format webm --webm-codec vp9 --channels rgba` | vp9, tag `alpha_mode=1` (decodificar com `ffmpeg -c:v libvpx-vp9 -i …` para ver o alpha) |
| Sequência PNG com alpha | `--out 'frames/f_[#####].png' --format png --channels rgba` | N PNGs `srgba`, numerados a partir de 00000 |
| GIF (com transparência) | `--format gif [--channels rgba]` | gif `bgra` |
| HEVC / AV1 / TIFF / EXR / JPEG / uncompressed / WAV / AIFF | `--format hevc\|av1\|tiff\|exr\|jpeg\|uncompressed\|wav\|aiff` | listados no código (`render_queue.rs:607-625`); não exercitados no lab |

- **Alpha**: só existe se a comp não tiver uma layer de fundo opaca (a cor de fundo da comp não entra no alpha). Pedir `--channels rgba` em h264 → `H.264 has no alpha channel` (exit 1); em webm AV1 → `AV1 WebM has no alpha channel (VP9 WebM has)`.
- H.264/HEVC arredondam largura e altura para baixo até o par.
- **O render sobrescreve sem perguntar** um arquivo de saída existente (exit 0). Escolha nomes novos ou use `scripts/render.sh`.
- Velocidade (M-series, 720p, 3 s): h264/prores/gif/png ≈ 0,4 s; WebM VP9 ≈ 5,7 s (o mais lento).
- GIF grande fica pesado: renderize um comp menor ou use `--resolution half` (e `--fps 15` para loops). Opção não exercitada no lab: `--fps`.
- Fila de render (alternativa via comandos): `renderQueue.add {comp, format, channels:"rgba", proresProfile:"4444", output}` → `renderQueue.render {"wait":true}` (doc agents.md:297; não exercitado no lab).
- Conhecido (docs/gaps.md #10): ProRes 4444 sai marcado bt709 mas codificado em sRGB (#340); se a cor exata importa, confira no destino.

## Lottie
`exec file.exportLottie '{"comp":"C","path":"/abs/out.json"}' P --json` (`.lottie` no path → arquivo dotLottie: zip com `manifest.json` + `animations/<nome>.json`).
Opções: `"textAsShapes":true` (texto vira glifos; Source Text keys e animadores **congelam em t=0**) · `"includeExpressions":true` (vão como `x`; a maioria dos players ignora).
Resposta: `{path, bytes, warnings:[…]}`. **Leia sempre `warnings`** e repasse ao usuário.

Suportado (sem warning, verificado): shape layers com group/rect/ellipse/star/path/fill/stroke/gfill/gstroke/**trim**/**repeater**/round/offset/pucker/twist/zigzag/merge; texto com **um** animador/selector; transform com keys e ease; parenting; opacidade/escala/posição.
Efeitos exportáveis: **apenas** Gaussian Blur, Tint, Tritone, Drop Shadow, Fill e Slider/Angle/Color/Point/Checkbox Control (`crates/lottie/src/export.rs:45-81`).

Warnings reais (lab/09):
- `T ▸ Glow: effect not supported by Lottie (skipped)`; idem `Fractal Noise`, `CC Particle World` e qualquer efeito fora da lista acima;
- `T: layer styles are not exported`;
- `X ▸ Transform ▸ Position: expression not exported (enable includeExpressions to export it as \`x\`)`;
- `Word: text exported as static glyph shapes (Source Text keys and animators are baked at time 0)` (com `textAsShapes`).

Também gera warning (código, crates/lottie/src): mask feather; 3D (`ddd:1`); adjustment layer, áudio, vídeo/sequência de imagens, câmera, luz, modelo 3D (viram null); stretch reverso; blend modes sem equivalente; track matte que não está logo acima ou visível; markers de layer; Preserve Transparency; texto: só o 1º selector, fontes por caractere, text on path, expressão no Source Text, propriedades de animador sem suporte.

Comportamento num player real (lottie-web 5.12.2 no Chrome; `scripts/lottie_preview.sh`):
- O Lottie **não leva a cor de fundo da comp**: fundo transparente.
- Texto vivo usa a fonte **pelo nome** (`Inter`); se o navegador não a tem, cai para uma serifada. Para fidelidade sem servir fontes, use `textAsShapes:true` (quando o texto não tem animadores) ou distribua a fonte junto.
- Verifique em 3 frames: `scripts/lottie_preview.sh out.json check 20 60 120`.
- Reimportar no EffectCraft (`exec file.importLottie '{"path":"/abs/out.json"}' --empty --save-as rt.ecproj`) é uma segunda checagem barata.
