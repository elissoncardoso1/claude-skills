# Formatos de redes sociais e anúncios (peça estática)

> Consulta das páginas oficiais em 4 nov. 2026 (via mapa de referências). Especificações de plataforma mudam: quando a peça for para veiculação paga ou o usuário pedir precisão, **reconfirme na página oficial** (WebSearch/WebFetch) antes de fechar o arquivo e diga a data da conferência.
> Use `scripts/formatos.py` para obter dimensões, zonas seguras em px e gerar um overlay-guia PNG.

## Índice
1. Tabela de especificações
2. Regras de produção por formato
3. Zona segura vertical (Stories/Reels)
4. Carrossel
5. Thumbnail
6. Atenção em feed: o que a evidência permite dizer
7. Mitos de formato

---

## 1. Tabela de especificações

| Plataforma / posicionamento | Proporção | Resolução de produção | Limites | Observação | Status |
|---|---|---|---|---|---|
| Meta Feed (FB/IG) — imagem | 4:5 | 1440×1800 (master); 1080×1350 aceitável | JPG/PNG ≤ 30 MB | Texto principal 50–150 caracteres, título 27 | Oficial |
| Meta Feed — objetivo Tráfego | 1.91:1 a 4:5 | 1:1 = 1440×1440; 4:5 = 1440×1800 | Largura mín. 600 px; tolerância 3% | — | Oficial |
| Instagram Reels / Stories — imagem | 9:16 | 1440×2560 (ou 1080×1920) | JPG/PNG | Zona livre ≈ 14% topo, 35% base, 6% laterais | Oficial (Reels) |
| Carrossel Meta Feed | 1:1 ou 4:5 | ≥ 1080×1080 | 2–10 cartões; ≤ 30 MB cada | Mesma proporção em todos | Oficial |
| Carrossel Meta Stories | 9:16 | 1080×1920 | até 3 cartões | — | Oficial |
| Facebook coluna direita | 1:1 | ≥ 1080×1080 | mín. 254×133 | Meta recomenda evitar texto na imagem | Oficial |
| LinkedIn imagem única | 1.91:1 | 1200×627 | PNG/JPG < 5 MB | 1:1 (1200×1200) e 4:5 (720×900) só em fontes secundárias | Oficial / secundário |
| LinkedIn carrossel | 1:1 | 1080×1080 | 2–10 cartões; ≤ 10 MB | — | Oficial |
| YouTube thumbnail | 16:9 | 1280×720 (mín. 640 larg.) | 2 MB celular / 50 MB computador | Resolução não aparece no trecho oficial; 3840×2160 só em uma fonte secundária | Proporção oficial; px secundário |

**Não verificados:** posts orgânicos do Instagram (perfil/grid), TikTok, Pinterest, X, WhatsApp Status. Para esses, use a proporção nativa mais comum (9:16 vertical; 2:3 Pinterest) e declare que é suposição.

## 2. Regras de produção por formato

1. **Produza um master e derive.** Para Feed, faça o master em 4:5 (1440×1800 ou 1080×1350) e mantenha título + marca dentro do quadrado central 1:1, porque o grid de perfil e alguns posicionamentos recortam (Meta Feed; prática).
2. **Texto longo vai na legenda**, não na arte. A arte carrega o gancho (até ~7 palavras no título) e a marca.
3. **Teste em miniatura real**: reduza a peça para ~25% (≈ 270 px de largura) e veja se título e elemento dominante sobrevivem. Para leitura no celular, o corpo mínimo útil em post de 1080 px fica em torno de 36–40 px; títulos para sobreviver ao grid do perfil, ≥ ~110 px (cálculo a partir de Legge & Bigelow, 2011 — ver `tipografia-legibilidade.md` §13).
4. **Versões horizontais** (LinkedIn 1.91:1, thumbnails 16:9) não são cortes do 4:5: recomponha (elemento dominante à esquerda/direita, texto no lado oposto).
5. **Exporte sRGB.** JPG qualidade alta para foto; PNG para tipografia/chapado (evita artefato em bordas de letra).

## 3. Zona segura vertical (Stories/Reels, 9:16)

Em 1080×1920: topo livre ≈ 269 px, base livre ≈ 672 px, laterais ≈ 65 px. Área útil ≈ 950×979 px centrada um pouco acima do meio.
- Nunca coloque CTA, logo, preço ou data nos 35% inferiores: a interface (legenda, botões, CTA nativo) cobre.
- O elemento dominante pode sangrar para fora da zona; a **informação** não.

## 4. Carrossel

- Mesma proporção em todos os cartões (Meta).
- **Primeiro cartão autônomo**: precisa funcionar sozinho como post (gancho + promessa), porque é o único que a maioria vê.
- Induza o deslize com continuidade gráfica (elemento que atravessa a borda entre cartões, grid compartilhado, numeração "1/7").
- Último cartão: conclusão + CTA + marca.
- Um grid único para todos os cartões (ver `composicao-gestalt-grid.md` §6) — é o que faz a série parecer sistema.

## 5. Thumbnail (YouTube)

- 16:9, ≥ 1280×720.
- Desenhe para o tamanho de celular: um rosto ou objeto + até 3–4 palavras grandes, alto contraste de valor.
- Evite o canto inferior direito (selo de duração).

## 6. Atenção em feed: o que a evidência permite dizer

A base empírica mais sólida (Pieters & Wedel, 2004) vem de **anúncios de revista**, não de feeds: imagem capta atenção independentemente do tamanho; texto capta em proporção à área; marca transfere atenção. Use como hipótese de trabalho para feeds, não como fato. Detalhes em `conceito-retorica-atencao.md` §5. Lacuna: estudos com peças estáticas em feeds móveis (ponto de partida: *Journal of Advertising*, 2025, doi:10.1080/00913367.2025.2524186 — não lido).

## 7. Mitos de formato

- **"Regra dos 20% de texto da Meta"**: as páginas oficiais atuais falam de proporção, resolução e zona segura, não de limite de 20%. Trate como heurística antiga — texto enxuto continua sendo boa prática, por legibilidade, não por regra de veiculação.
- **"Resolução 72 dpi para redes"**: dpi é irrelevante em tela; o que importa é a dimensão em pixels.
