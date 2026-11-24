# Produção gráfica e pré-impressão

> Para PDFs paginados (e-book, relatório, catálogo) e preflight detalhado, a skill `design-pdf` é a especialista; este arquivo cobre o fechamento de **peças avulsas** (cartaz, flyer, folder, cartão, banner).
> Normas citadas: ISO 15930-7:2010 (PDF/X-4); ISO 12647-2:2013 (offset, FOGRA51/52); perfis ECI PSO Coated v3; dados Fogra (2020). Sangria, margem de segurança e 300 ppi são prática consagrada **sem fonte normativa verificada**. Acabamentos não têm referência verificada.

## Índice
1. Perguntas obrigatórias à gráfica
2. Cor para impressão
3. Arquivo final (PDF/X-4)
4. Sangria, segurança e resolução
5. Formatos de papel e tamanhos comuns
6. Checklist de fechamento

---

## 1. Perguntas obrigatórias à gráfica (antes de converter qualquer coisa)

1. Processo (offset, digital, grande formato, serigrafia)?
2. Condição de impressão / perfil de saída (ex.: PSO Coated v3 / FOGRA51; não revestido FOGRA52)? Há laminação?
3. PDF/X-4 aceito? Ou exigem PDF/X-1a (fluxos antigos, sem transparência)?
4. Sangria exigida (3 mm é o comum; grande formato varia) e marcas de corte?
5. Cores especiais (Pantone), verniz localizado, faca especial? Como querem as camadas/separações?

Se o usuário não sabe, entregue com os padrões abaixo e **diga explicitamente quais suposições fez**.

## 2. Cor para impressão

- **Projete em RGB, converta para CMYK só com o perfil da condição da gráfica** (ISO 12647-2:2013; ECI). Converter cedo, com perfil errado, perde gamut à toa.
- Condição de referência atual para couché premium: **PSO Coated v3 (FOGRA51)**, TAC (cobertura total de tinta) **300%**, preto máximo 96% (ECI). Não use FOGRA39 se a gráfica segue a norma de 2013.
- Papel não revestido: FOGRA52 (PSO Uncoated v3). Com laminação fosca/brilhante: FOGRA56/57 (Fogra, 2020).
- **Preto de texto**: 100% K puro (evita registro desalinhado em letra pequena). **Preto de massa** para grandes áreas: preto rico (ex.: C40 M30 Y30 K100 — dentro do TAC), nunca em texto pequeno. (prática consagrada)
- Faça **soft-proof** com o perfil de saída antes de aprovar; cores neon/RGB saturadas (verde-limão, azul elétrico, laranja vivo) caem em CMYK — avise o cliente ou indique Pantone.
- Cor é relativa ao entorno e à luz de observação (Albers; Pedrosa): aprove a prova sob luz padrão (D50) quando possível.

## 3. Arquivo final (PDF/X-4)

- **PDF/X-4** (ISO 15930-7:2010): mantém transparência ativa e camadas, aceita dados RGB/CMYK gerenciados com OutputIntent. Entregue com o **OutputIntent da gráfica**.
- **Não achate transparências manualmente**: o RIP moderno resolve.
- **Incorpore todas as fontes** (e verifique licença para incorporação).
- Imagens vinculadas embutidas; sem RGB "solto" se a gráfica pedir CMYK.
- PDF/X-6 (ISO 15930-9:2020) existe, mas só foi encontrado em fonte secundária — não recomende sem conferir com a gráfica.

## 4. Sangria, segurança e resolução (prática consagrada)

| Item | Padrão |
|---|---|
| Sangria | 3 mm por lado (offset/digital); grande formato: conforme gráfica |
| Margem de segurança (nada de texto/logo) | ≥ 3–5 mm da linha de corte; ≥ 8–10 mm em peças dobradas ou encadernadas |
| Resolução de imagem | 300 ppi no tamanho final (offset); 150 ppi costuma bastar em banner visto a > 2 m |
| Traço/linha fina | ≥ 0,25 pt; texto vazado (branco sobre cor) ≥ 8 pt e peso regular ou mais |

## 5. Formatos comuns (mm)

A6 105×148 · A5 148×210 · A4 210×297 · A3 297×420 · A2 420×594 · A1 594×841 · A0 841×1189 · cartão de visita BR 90×50 · flyer comum 100×150 / 148×210 · cartaz lambe 297×420 ou 460×640.
Para dimensionar letra pela distância de leitura (cartaz, banner, sinalização), use `scripts/legibilidade.py`.

## 6. Checklist de fechamento

- [ ] Condição de impressão confirmada (ou suposição declarada)
- [ ] Documento no tamanho final + sangria; elementos de fundo sangrando
- [ ] Texto e logos dentro da margem de segurança
- [ ] Imagens ≥ 300 ppi efetivos (ou justificativa para menos)
- [ ] CMYK com perfil correto; TAC ≤ 300% nas áreas escuras; texto preto 100K
- [ ] Fontes incorporadas e licenciadas; sem falso negrito/itálico
- [ ] PDF/X-4 com OutputIntent; marcas de corte se pedidas
- [ ] Prova (ou soft-proof) aprovada; ortografia revisada (PT-BR, acentos e cedilha visíveis no tamanho final)
