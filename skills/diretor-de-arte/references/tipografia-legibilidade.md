# Tipografia e legibilidade — referência operacional

Escopo: peças estáticas (cartaz, post, carrossel, capa, flyer, anúncio, infográfico, impresso). Tudo aqui é paráfrase; citações literais só quando indicado.
Níveis de evidência: **[F]** forte (empírico controlado/convergente); **[M]** moderada (empírico limitado, amostra pequena ou relato indireto); **[PC]** prática consagrada (tradição tipográfica); **[O]** opinião de especialista. **[Cálc.]** = cálculo nosso a partir de dado publicado.
Fontes: Bringhurst (2005), *Elementos do estilo tipográfico* v3.0, Cosac Naify — citado por seção (§) e página; Lupton (2006), *Pensar com tipos*, Cosac Naify; Farias (2013), *Tipografia digital*, 2AB — e-book sem paginação, citado por capítulo/seção; Legge & Bigelow (2011), *J. Vision* 11(5):8, p. 1–22; Arditi & Cho (2005), *Vision Research* 45, p. 2926–2933; Dogusoy, Cicek & Cagiltay (2016), LNCS 9747, p. 578–586; Martins (2008), *InfoDesign* 5(3), p. 57–61; Farias & Landim (2020), *InfoDesign* 17(2), p. 99–116.

## Índice
1. Ordem de decisão (atalho)
2. Escolha de família
3. Pareamento
4. Escala tipográfica e hierarquia (exemplos para post 1080×1350 px e A3)
5. Entrelinha
6. Medida (comprimento de linha)
7. Espacejamento, tracking e kerning
8. Alinhamento e hifenização
9. Viúvas, órfãs e quebras
10. Detalhes: aspas, travessões, números, versaletes, espaços
11. Tipografia expressiva com camada legível
12. Dimensionamento por distância (fórmula e tabela)
13. Tamanho em tela de celular (cálculo)
14. Serifa vs. sem serifa: o que a evidência diz
15. Legibilidade vs. leiturabilidade
16. Idosos e baixa visão
17. Defeitos frequentes → correção
18. Checklist tipográfico final

---

## 1. Ordem de decisão (atalho)

1. **Defina distância e condição de leitura antes da fonte** (celular a ~35 cm? cartaz a 3 m? sala mal iluminada?). O tamanho angular manda mais que o desenho da letra (Legge & Bigelow, 2011, p. 1, 6–7) [F].
2. **Fixe o tamanho mínimo pela altura-x** (§12–13), depois escolha família, escala, entrelinha e medida.
3. **Escolha a família por tom, contexto e funcionalidade técnica**, não pelo mito da serifa (§14).
4. **Teste em condição real** (impressão em escala 1:1, celular na mão, miniatura do feed). Pesquisas de laboratório nem sempre valem fora dele (Martins, 2008, p. 59–60) [PC].

## 2. Escolha de família

- **Comece pelo tom, mas sem literalismo.** Leitores, mesmo leigos, atribuem significados convergentes (elegância, precisão, dignidade) a classes tipográficas diferentes (experimento de Linkens relatado por Blanchard, via Farias, 2013, cap. 3.3) [M — relato indireto]. Porém, não escolha a fonte "temática" que ilustra o assunto: o melhor tipo é primeiro intrinsecamente bom, depois adequado à leitura, e só então simpático ao tema (Bringhurst, 2005, §6.2.1, p. 103–104) [O].
- **Escolha pelo contexto de uso.** Para texto corrido: desenho calmo, contraformas abertas, peso regular. Para título e display: a família pode ter mais personalidade, desde que reforce a estrutura da fonte de texto (Bringhurst, 2005, §6.5.4, p. 117) [PC].
- **Prefira altura-x generosa para tamanhos pequenos e leitura à distância.** No mesmo corpo em pontos, fontes de altura-x maior parecem maiores; o tamanho efetivo é a altura-x, não o corpo (Lupton, 2006, p. 37; Legge & Bigelow, 2011, p. 3–4) [F]. A fração altura-x/corpo varia de 0,28 a 0,58 (média 0,46) em 1.049 romanas; em fontes de livros e jornais, 0,36–0,55 (Legge & Bigelow, 2011, p. 4). Por isso, **"12 pt" não é um tamanho; é uma caixa**. Jornais usam fontes de altura-x maior quanto menor o corpo (correlação inversa 0,71; p. 12) [F].
- **Exija a família completa que o trabalho pede:** itálico verdadeiro, pesos suficientes (regular, semibold, bold no mínimo), versaletes se houver siglas, algarismos de texto e tabulares se houver números (Bringhurst, 2005, §6.2.2, p. 104–105) [PC].
- **Verifique suporte a PT-BR no tamanho de uso.** Teste a string `AÇÃO À VÉSPERA — ÓTIMO, PÃO, VOCÊ, coração, ônibus, “aspas”, 1–2` em caixa-alta e baixa. Confira: til e cedilha desenhados (não compostos de forma tosca), acentos de maiúscula que não colidem com a linha de cima em entrelinha apertada, aspas curvas e travessões presentes [PC].
- **Verifique a licença antes do uso comercial.** Confirme se cobre o uso pretendido (impressão, web, app, logotipo, embutir em PDF). Fontes sob SIL Open Font License (a maioria do Google Fonts) permitem uso comercial; fontes de sistema e "grátis para uso pessoal" frequentemente não [PC — nenhuma das fontes lidas trata de licença; Farias, 2013, trata de formato/tecnologia, não de licenciamento].
- **Não falsifique estilos.** Pseudo-itálico (inclinação), pseudo-bold (contorno) e pseudo-versalete (maiúscula reduzida) são "crimes tipográficos" (Lupton, 2006, p. 44–45). Não comprima nem expanda horizontalmente: escolha uma variante estreita ou larga desenhada para isso (Lupton, 2006, p. 36; Bringhurst, 2005, §2.1.9, p. 42–43) [PC].

## 3. Pareamento

> Opções concretas de fontes gratuitas e pareamentos prontos: `catalogo-fontes.md`.

- **Comece com uma família só.** A maioria das páginas se resolve com uma família e suas variações (Bringhurst, 2005, §6.5.1, p. 114) [PC]. Em post e flyer, uma superfamília (serifa + sem serifa do mesmo projeto, como Thesis; Lupton, 2006, p. 46) resolve quase tudo.
- **Se parear, escolha entre dois caminhos:**
  - **Parentesco:** mesma estrutura interna (eixo, proporções, origem histórica). Exemplos: uma sem serifa humanista com uma romana renascentista (Syntax + Minion); uma geométrica com uma didona (Futura + Bodoni) (Bringhurst, 2005, §6.5.5, p. 117–118) [PC].
  - **Contraste claro de papel:** fontes estruturalmente diferentes, mas com funções nítidas (uma só para títulos, outra só para texto) (Bringhurst, 2005, §6.5, p. 116–117) [PC].
- **Evite a quase-semelhança.** Duas sem serifa parecidas, mas não iguais, parecem erro, não escolha [O].
- **Iguale a altura-x ao misturar famílias na mesma linha.** Ajuste os corpos até as alturas-x casarem (Lupton, 2006, p. 95) [PC].
- **Limite: 2 famílias por peça; 3 só com justificativa** (por exemplo, uma display de assinatura de marca) [O].

## 4. Escala tipográfica e hierarquia

- **Não componha sem escala.** Use poucos tamanhos com relações consistentes. A escala clássica (6, 7, 8, 9, 10, 11, 12, 14, 16, 18, 21, 24, 36, 48, 60, 72 pt) é o equivalente tipográfico da escala diatônica; comece de um tamanho base e suba por intervalos (Bringhurst, 2005, §3.1.1, p. 54) [PC].
- **Em leitura rápida, dê saltos grandes.** Em jornais, cada categoria (texto → intertítulo → título menor → manchete) é cerca de **2×** a anterior, o que maximiza a diferença perceptiva entre funções (Legge & Bigelow, 2011, p. 13) [M — descritivo]. Em peça de rolagem rápida, use razões entre 1,5 e 2 entre níveis; reserve razões menores (1,2–1,33) para material de leitura contínua.
- **Máximo de 3 níveis visíveis em peça rápida**, e **no máximo 3 sinais por nível** (tamanho, peso, cor, caixa, espaço). Para ênfase em texto corrido basta **uma** mudança, normalmente o itálico (Lupton, 2006, p. 94–95) [PC].
- **Exemplo — post 1080×1350 px (base 40 px, razão ~1,5):**

| Papel | px | Peso | Observação |
|---|---|---|---|
| Nota/legal/crédito | 30–32 | regular | só texto que não precisa ser lido rapidamente; abaixo de ~36 px fica no limite crítico no celular (§13) |
| Texto de apoio | 40–44 | regular | até 3–4 linhas |
| Subtítulo / chamada | 60–64 | semibold | |
| Título | 90–100 | bold | |
| Destaque/número-herói | 140–200 | bold/black | 1–3 palavras; precisa sobreviver à miniatura da grade (§13) |

- **Exemplo — cartaz A3 (297×420 mm) lido a 1–3 m:**

| Papel | pt | Distância-alvo |
|---|---|---|
| Rodapé/realização/logos | 9–12 | lido de perto (40–60 cm) |
| Informação prática (data, local, horário) | 24–36 | legível a ~1–1,5 m |
| Subtítulo | 48–60 | ~2–3 m |
| Título | 96–144 | 3–5 m |
| Palavra-gancho (opcional) | 200–300 | visível a 6–10 m |

  A escala segue a série clássica estendida (12, 24, 36, 48, 72, 96, 144); confira cada nível na tabela do §12.

## 5. Entrelinha

- **Ajuste a entrelinha ao tipo, ao texto e à medida.** Valores rotineiros para texto: 9/11, 10/12, 11/13, 12/15. Colunas largas, fontes pesadas, fontes de altura-x grande e **sem serifa pedem mais entrelinha** (Bringhurst, 2005, §2.2.1, p. 44–45) [PC].
- **Padrão de software ≈ 120% do corpo.** Em texto corrido, use **120–145%**. Aumentar demais transforma o bloco em linhas soltas, não em textura (Lupton, 2006, p. 83) [PC].
- **Títulos: 90–110%.** Entrelinha negativa (ex.: 18/15) é aceitável em título curto ou texto publicitário, desde que ascendentes e descendentes não colidam (Bringhurst, 2005, §2.2.1, p. 44). Título só em caixa-alta tolera ~85–95%, pois não há descendentes; **confira os acentos das maiúsculas** (Á, Ã, Ç) contra a linha de cima [PC].
- **Respeite o ritmo vertical.** Espaços entre blocos devem ser múltiplos da entrelinha base: em 11/13, os desvios somam 13, 26, 39 pt... (Bringhurst, 2005, §2.2.2, p. 46) [PC]. Em post, use um módulo vertical (ex.: 8 ou 10 px) e múltiplos dele.
- **Texto com muitas maiúsculas, números ou acentos pede um pouco mais de entrelinha** (Bringhurst, 2005, p. 46) [PC].

## 6. Medida (comprimento de linha)

- **Texto contínuo em uma coluna: 45–75 caracteres** (com espaços); ~66 é o ideal clássico. **Múltiplas colunas: 40–50** (Bringhurst, 2005, §2.1.2, p. 33) [PC].
- **Em português, o mínimo prático para texto justificado é ~48 caracteres** (nota da tradução; o inglês fica em 40), porque a palavra média portuguesa é mais longa: ~6 caracteres, contra 5 no inglês (Bringhurst, 2005, p. 33 e nota à p. 46–47) [PC]. Abaixo disso, alinhe à esquerda.
- **Atalho de cálculo:** a coluna costuma ter 20–40 vezes o corpo (típico: 30×). Exemplo: corpo 10 pt × 30 = 300 pt ≈ 65 caracteres (Bringhurst, 2005, p. 34) [PC].
- **Peças rápidas (post, cartaz):** use linhas de 20–40 caracteres. Blocos com menos de ~30 caracteres por linha parecem magros em texto longo; em trechos pequenos e isolados, até 12–15 caracteres são aceitáveis (Bringhurst, 2005, p. 33) [PC].

## 7. Espacejamento, tracking e kerning

- **Caixa-alta e versaletes: sempre espacejar.** Abra o tracking em +5% a +10% do corpo (+50 a +100 unidades/1000 em). Em versais justificadas tradicionais, chega a 20–25%. O equilíbrio óptico importa mais que o valor: LA e AVA quase não pedem espaço; NN e HIH pedem muito (Bringhurst, 2005, §2.1.6, p. 36–37; Lupton, 2006, p. 81) [PC].
- **Minúsculas em texto: tracking 0.** Não espaceje minúsculas sem necessidade, porque isso prejudica a leitura. Exceção: subtítulos curtos em sem serifa estreita e pesada podem ganhar abertura modesta (Bringhurst, 2005, §2.1.7, p. 38–39) [PC].
- **Títulos grandes: reduza levemente o tracking (−1% a −3%) e faça kerning manual.** Os vazios entre letras crescem com o corpo e ficam óbvios em display (Lupton, 2006, p. 80) [PC].
- **Nunca use tracking negativo para "caber o texto"**: ajuste o sapato, não o pé (Lupton, 2006, p. 82). Também não comprima letras para ajustar espaço (Bringhurst, 2005, §2.1.9, p. 42) [PC]. Corte o texto ou mude o layout.
- **Não aperte texto pequeno.** Letras próximas demais elevam o limiar de reconhecimento (efeito de *crowding*), um efeito grande e sistemático (Arditi & Cho, 2005, p. 2929) [F]. **Também não espere ganho com espacejamento extra-largo**: ele não aumenta o *span* visual nem a velocidade de leitura (Yu et al., 2007, via Legge & Bigelow, 2011, p. 10–11) [F]. Use o espacejamento de fábrica em texto.
- **Agrupe números longos.** Sequências de 3+ dígitos (telefone, protocolo) ficam mais legíveis em grupos com pequeno espaço (Bringhurst, 2005, p. 37) [PC]. Em PT-BR: `(98) 9 8765-4321`.

## 8. Alinhamento e hifenização

- **Padrão para peças: alinhado à esquerda (bandeira).** Evita os "rios" da justificação em colunas estreitas. Um bom desalinhamento não forma cunhas, luas ou degraus (Lupton, 2006, p. 84; Bringhurst, 2005, §2.1.3, p. 35) [PC]. Muitas sem serifa ficam melhores desalinhadas em qualquer medida (Bringhurst, 2005, p. 35).
- **Justifique só com medida ≥ ~48 caracteres** (PT-BR) e hifenização ativa em português [PC].
- **Centralizado:** só em blocos curtos e formais (convite, certificado, capa), quebrando a linha **pelo sentido** (Lupton, 2006, p. 85) [PC].
- **Alinhado à direita:** só em blocos pequenos (legenda, nota, olho) (Lupton, 2006, p. 85) [PC].
- **Hifenização (Bringhurst, 2005, §2.4, p. 51–53) [PC]:** deixe ≥ 2 letras antes e leve ≥ 3 para a linha seguinte; não termine parágrafo com fragmento hifenizado nem com palavra de menos de 3 letras; no máximo 3 hífens consecutivos; hifenize nomes próprios só em último caso; siga a silabação portuguesa (na-tu-ral).
- **Em títulos, chamadas e CTAs: zero hifenização.** Quebre as linhas manualmente, por unidade de sentido [PC].
- **Use espaço inseparável** para manter juntos `R$ 47`, `10 mm`, `p. 3`, `4 × 4` e iniciais (Bringhurst, 2005, §2.4.6, p. 51) [PC].
- **Evite hífen perto de interrupção** (imagem, olho, caixa) (Bringhurst, 2005, §2.4.10, p. 53) [PC].

## 9. Viúvas, órfãs e quebras

- **Atenção à terminologia:** Bringhurst chama de "órfã" a primeira linha de parágrafo isolada no pé da página e de "viúva" a última linha isolada no topo da seguinte. A nota da tradução avisa que, no meio editorial brasileiro, "viúva" também designa a palavra sozinha na última linha do parágrafo, e "linha enforcada/forca" designa linha isolada (Bringhurst, 2005, §2.4.8, p. 52) [PC]. **Na skill, descreva o defeito, não só o nome.**
- **Regras operacionais [PC]:**
  - nenhuma palavra sozinha (ou sílaba) na última linha de parágrafo, título ou legenda; reescreva ou reequilibre a quebra;
  - nenhuma linha isolada de parágrafo no topo de coluna/página (Bringhurst, 2005, §2.4.8);
  - não comece duas ou mais linhas seguidas com a mesma palavra (§2.4.7);
  - em títulos de 2–3 linhas, equilibre as larguras e quebre pelo sentido, nunca separando artigo/preposição do seu nome ("de / São Luís").
- **Não "conserte" viúvas com tracking ou entrelinha extra.** Mova linhas, edite o texto ou mude a medida (Bringhurst, 2005, §2.4.9, p. 52–53) [PC].

## 10. Detalhes: aspas, travessões, números, versaletes, espaços

- **Aspas curvas** (“ ” e ‘ ’), nunca retas (" '). Use aspas com parcimônia (Bringhurst, 2005, §5.4.1, p. 96–97) [PC]. Em título display, prefira aspas "penduradas" fora da margem (pontuação suspensa) para preservar o alinhamento óptico [PC].
- **Hífen, meia-risca e travessão não são intercambiáveis** (Bringhurst, 2005, §5.2, p. 90–92) [PC]:
  - intervalos numéricos: **meia-risca (–) sem espaços**: `3–6 de novembro`, `14h–18h`;
  - inciso no texto: Bringhurst recomenda meia-risca com espaços (– assim –); o uso editorial brasileiro consagra o travessão (—). **Escolha um padrão e mantenha-o na peça inteira**;
  - diálogo: travessão (—) (§5.2.3);
  - nunca use dois hifens (--) como travessão;
  - dimensões: sinal de multiplicação (×), não a letra x: `1080 × 1350` (§5.2.6).
- **Algarismos:** use **titulares (alinhados)** com caixa-alta e em tabelas, e **de texto (estilo antigo)** dentro de texto corrido em caixa-baixa (Bringhurst, 2005, §3.2.1, p. 55). Use **tabulares** em colunas de números e preços (Lupton, 2006, p. 44) [PC]. Em post, número-herói em titular, com kerning manual.
- **Siglas:** em texto corrido, use versaletes **genuínos** e levemente espacejados para siglas de 3+ letras. Use versaletes em fontes de altura-x pequena e versais em fontes de altura-x grande (Bringhurst, 2005, §3.2.2, p. 56–57) [PC]. Sem versaletes verdadeiros, use versais com +5% de tracking, não versalete falso.
- **Um só espaço entre frases** (Bringhurst, 2005, §2.1.4) [PC]. **Reticências** como caractere da fonte (…) (§5.2.7). **Ligaduras** padrão ativas em texto; desligue-as em texto espacejado (Bringhurst, 2005, p. 39) [PC].
- **Datas e horas PT-BR:** `10/11/2026`, `9h30`, `14h` (sem "hs") [PC — norma de uso, não das fontes].

## 11. Tipografia expressiva com camada legível

- **Separe duas camadas:** (a) **expressiva** — distorção controlada, sobreposição, escala extrema, letra como imagem; (b) **informativa** — o quê, quando, onde, quem e CTA, em tipo legível, contraste alto e tamanho acima do mínimo do §12 [O — princípio da Área 2 do mapa; ver também Lupton, 2006, sobre hierarquia, p. 94–95].
- **A expressão pode desafiar a leitura, mas não a informação crítica.** A tipografia experimental das décadas de 1980–1990 forçou os limites da legibilidade e exigiu "chaves" do leitor; a aceitação cresceu com a familiaridade do público (caso de David Carson, em Farias, 2013, cap. 1) [O]. Pergunte: o público-alvo tem essas chaves? Para público amplo, idoso ou institucional, presuma que não.
- **Ilegibilidade é uma escolha de público.** As letras "excêntricas" funcionam como código para iniciados (Farias, 2013, cap. 1) [O]. Use quando o objetivo for pertencimento ou atitude, não informação.
- **Teste de sobrevivência:** reduza a peça a 25% (ou miniatura do feed). Se a camada informativa some, ela está errada; a expressiva pode sumir [PC].
- **Acima de ~2° de altura-x a leitura não acelera** (Legge & Bigelow, 2011, p. 7). Ganhe impacto com peso, contraste, cor e corte, não só com tamanho. A queda acima de 2° é suave e irrelevante para 1–6 palavras (p. 13) [F]. Uma palavra gigante é legítima; um parágrafo gigante, não.

## 12. Dimensionamento por distância

**Dado de base (Legge & Bigelow, 2011, p. 1, 6–7) [F]:** a velocidade de leitura é máxima numa **faixa fluente de altura-x entre ~0,2° e ~2° de ângulo visual**. Abaixo do **tamanho crítico de impressão (~0,2°)** a velocidade cai bruscamente. A 40 cm, isso corresponde a altura-x de 1,4 mm (~4 pt de altura-x) a 14 mm. Times New Roman a 9 pt, lida a 40 cm, fica exatamente no limite crítico (p. 6). Texto corrido de jornais e livros fica em 0,2°–0,28° (p. 11–12). Ou seja, a prática editorial trabalha **logo acima** do limite, para leitores com boa visão e boa luz.

**Fórmula [Cálc.]:** altura-x mínima ≈ distância × tan(0,2°) ≈ **0,0035 × distância**. Limite superior útil para texto corrido ≈ **0,035 × distância** (2°).
**Do mínimo ao corpo:** corpo ≈ altura-x ÷ fração de altura-x da fonte. **Suposição da tabela: fração = 0,5**, que vale para sem serifa e serifadas modernas de olho grande (Lupton, 2006, p. 37; faixa real 0,36–0,55, segundo Legge & Bigelow, 2011, p. 4). **Com fonte de olho pequeno (fração ~0,4), multiplique o corpo por 1,25.** Meça a fração: digite "x" e "H" no corpo 100 e meça a altura do x. 1 pt = 0,3528 mm.

| Distância | Altura-x mínima (0,2°) | Corpo mínimo (fração 0,5) | Corpo recomendado (×2, margem de segurança) | Altura-x no teto fluente (2°) |
|---|---|---|---|---|
| 40 cm (impresso na mão) | 1,4 mm | ~8 pt | ~16 pt p/ público geral em peça rápida; 10–12 pt em texto corrido | 14 mm |
| 1 m (balcão, mural próximo) | 3,5 mm | ~20 pt | ~40 pt | 35 mm |
| 3 m (cartaz na parede) | 10,5 mm | ~60 pt | ~120 pt | 105 mm |
| 5 m (banner, sala) | 17,5 mm | ~100 pt | ~200 pt | 175 mm |
| 10 m (fachada, palco) | 35 mm | ~200 pt | ~400 pt (≈ 14 cm de corpo) | 350 mm |

- **Por que dobrar ("×2")? [Cálc./O]** O mínimo da tabela é o **limiar** para leitores com boa visão, boa luz e alto contraste. O tamanho crítico é pelo menos o dobro da acuidade de letras e cresce muito com baixa visão (Legge & Bigelow, 2011, p. 7). Baixo contraste estreita a faixa fluente (p. 7). Idosos perdem mais com pouca luz, ofuscamento e baixo contraste (p. 14). Cartaz é lido de relance, em movimento e sob luz ruim. Use o mínimo só para texto secundário.
- **A "aposta" do cartaz:** o título deve ser lido da maior distância de abordagem; a informação prática, da distância de parada (~1–1,5 m); o rodapé, de perto [PC].
- **Nunca confunda acuidade com leitura fluente:** ver que há letras ≠ ler com velocidade. Dimensionar pelo limite de acuidade torna a leitura lenta e penosa (Legge & Bigelow, 2011, p. 7) [F].

## 13. Tamanho em tela de celular [Cálc.]

- **Premissas:** post de 1080 px de largura exibido na largura total de um celular de ~6,1–6,7" (~65–72 mm úteis) → 1 px ≈ 0,065 mm; distância de uso ~30–35 cm (Legge & Bigelow, 2011, p. 5, relatam ~36 cm para livros e ~50 cm para leitores eletrônicos).
- **Limite crítico a 33 cm:** altura-x ≈ 1,15 mm ≈ **18 px** → corpo ≈ **36 px** (fração 0,5). Daí: **texto de apoio ≥ 40 px; texto importante ≥ 48 px; abaixo de 36 px, só crédito ou nota legal.**
- **Miniatura da grade do perfil (~1/3 da largura):** tudo encolhe ~3×. Para o título ser lido na grade, use corpo ≥ ~110–120 px. Para o 1º card de carrossel, teste a leitura na grade [Cálc.].
- **Títulos on-line são muito menores que os impressos** (média de 0,31° na home de portais, contra 1,71° na manchete impressa; Legge & Bigelow, 2011, p. 18). No feed, o título funciona como anzol; trate-o como manchete impressa, não como título de portal [M].

## 14. Serifa vs. sem serifa: o que a evidência diz

- **Experimento controlado (Arditi & Cho, 2005) [F para o recorte estudado]:** fontes idênticas exceto a serifa (0%, 5% e 10% da altura de maiúscula). Serifa de 5% deu ganho mínimo de acuidade **perto do limite visual**, explicado em grande parte pelo espaço extra que a serifa impõe. **Velocidade de leitura (RSVP e contínua, em papel): nenhum efeito**, com visão normal e com 2 leitores com DMRI (p. 2926, 2931–2932). Os autores concluem que o efeito é improvável em tamanhos típicos e condições normais (p. 2932). Limite: uma única fonte paramétrica e amostra pequena.
- **Eye tracking em tela (Dogusoy et al., 2016) [M — fraca]:** 10 pós-graduandos, revisão de texto em Times New Roman vs. Arial 12 pt. Arial foi mais rápida e mais precisa (p. 578). Limites: n = 10, tarefa de achar erros (não leitura), fontes que diferem em muito mais que a serifa.
- **Idosos brasileiros (Farias & Landim, 2020) [M]:** traço homogêneo (Arial, Trebuchet, Gill Sans) teve menos erros e mais preferência que traço modulado (Times, Bodoni, Book Antiqua), **sem diferença significativa de tempo** (p. 106–107). O fator decisivo é **modulação e diferenciação**, não a serifa em si.
- **Spencer (1969, via Farias, 2013, cap. 3.3) [M — relato indireto]:** palavras só em maiúsculas são bem menos legíveis que em caixa-baixa; itálico reduz a legibilidade; negrito com contraformas abertas, não; seminegrito é preferido e essencial para quem tem problema de visão.
- **Regra:** **escolha serifa ou sem serifa por tom e contexto.** Para legibilidade, controle o que pesa: altura-x, espacejamento, peso (evite light/thin em texto), contraste figura-fundo, modulação baixa em tamanhos pequenos, tamanho angular [F/M].

## 15. Legibilidade vs. leiturabilidade

- **Legibilidade (*legibility*):** clareza de caracteres isolados; medida pela velocidade/precisão de reconhecimento. **Leiturabilidade (*readability*):** conforto de leitura sustentada; medida por quanto tempo se lê sem cansaço (Tracy, 1986, via Farias, 2013, cap. 3.3) [PC — definição].
- **Implicação:** fonte pesada em corpo grande pode ser mais "legível" em laboratório e pior para ler um parágrafo. Avalie **títulos/sinalização pela legibilidade** e **texto corrido pela leiturabilidade** (Farias, 2013, cap. 3.3) [PC].
- **O termo é ambíguo e a medição frequentemente não tem validade ecológica.** Testes de Tinker (distância, piscada, tempo de reconhecimento) medem coisas diferentes e nem sempre valem para a leitura real (Martins, 2008, p. 57–60) [M].
- **A leitura depende de vários fatores interdependentes:** interesse, conhecimento prévio, forma e tamanho da letra, medida, espaços entre letras, palavras e linhas, layout, contraste e qualidade de impressão (Wrolstad, via Martins, 2008, p. 60) [M]. **Nunca otimize uma variável isolada.**
- **Familiaridade conta:** fontes muito usadas parecem mais legíveis em parte por serem familiares (Gill, Frutiger e Richardson, via Farias, 2013, cap. 3.3) [O]. Para público leigo ou idoso, prefira formas convencionais.

## 16. Idosos e baixa visão

- **Fique bem acima do tamanho crítico.** Com baixa visão, a diferença entre acuidade e tamanho crítico é muito maior que o dobro observado em leitores com visão normal (Legge & Bigelow, 2011, p. 7) [F]. Para material de terceira idade, use o corpo "recomendado" do §12 como **piso**.
- **Controle luz e contraste.** Pessoas acima dos 70 anos sem doença ocular perdem pouca acuidade em teste clínico, mas perdem muito com pouca luz, ofuscamento e impressão de baixo contraste (Haegerstrom-Portnoy et al., 1999, via Legge & Bigelow, 2011, p. 14) [F]. Logo: texto escuro sobre fundo claro e liso, **papel fosco** (sem brilho), nada de cinza-claro sobre branco nem texto sobre foto sem chapado/véu [F/PC].
- **Escolha traço homogêneo e formas diferenciadas** (Farias & Landim, 2020, n = 88, 7 cidades, incl. São Luís; p. 99, 102, 111–112) [M]:
  - prefira humanistas de traço uniforme, aberturas generosas e altura-x alta (o estudo aponta Trebuchet e Gill Sans como mais inclusivas que Times e Bodoni);
  - evite modulação forte, serifas finas e hastes curtas (didonas, Times em corpo pequeno);
  - garanta diferenciação nos pares de mesmo arquétipo, sobretudo **c/e** (e também o/a, I/l/1, rn/m);
  - catarata e glaucoma foram as condições com maior impacto negativo na percepção.
- **Escolaridade importa tanto quanto visão.** Leitores de escolaridade básica erraram mais e preferiram corpos maiores; quem tem baixa escolaridade ou problema visual severo preferiu, em média, ~12 pt (Farias & Landim, 2020, p. 109–111) [M]. A literatura citada pelos autores fixa **12 pt como mínimo** para leitores com problema de visão (p. 101). **Cuidado:** os próprios autores alertam que "10 pt" de uma fonte homogênea é maior que "10 pt" de uma modulada (p. 109). Use a altura-x (§12).
- **Pesos:** use regular a semibold no texto; nada de light/thin. Seminegrito é preferido e essencial para leitores com problema visual (Spencer, via Farias, 2013, cap. 3.3) [M].
- **Evite caixa-alta em blocos e itálico em texto** (Spencer, via Farias, 2013) [M]. Use frases curtas, alinhamento à esquerda e entrelinha ≥ 140% [PC].

## 17. Defeitos frequentes → correção

| Defeito | Por que é problema | Correção |
|---|---|---|
| Texto de apoio em 24–30 px num post | fica no limite crítico ou abaixo dele no celular (§13) | ≥ 40 px; corte texto em vez de reduzir corpo |
| Título em caixa-alta com tracking 0 | versais sem respiro ficam irregulares (Bringhurst, 2005, §2.1.6) | +5–10% e kerning óptico |
| Parágrafo inteiro em caixa-alta | caixa-alta em bloco é bem menos legível (Spencer, via Farias, 2013) | caixa-alta e baixa; versais só em rótulos curtos |
| Tracking negativo para caber | sufoca letras e aumenta o *crowding* (Lupton, 2006, p. 82; Arditi & Cho, 2005) | editar texto ou mudar layout |
| Fonte "light" em texto sobre foto | perde contraste e forma em baixa luz/tela pequena | regular/semibold sobre chapado ou véu |
| Texto cinza-claro em fundo branco | baixo contraste estreita a faixa fluente (Legge & Bigelow, 2011, p. 7) | escurecer o texto; contraste de valor alto |
| Três fontes "parecidas" | quase-semelhança parece erro | uma superfamília ou duas famílias claramente distintas |
| Justificado em coluna estreita | rios e espaços irregulares (Lupton, 2006, p. 84) | alinhar à esquerda |
| Palavra solitária na última linha do título | desequilibra a forma e a leitura | reescrever ou requebrar pelo sentido |
| Aspas retas, "--", x em "1080x1350" | marca de composição amadora (Bringhurst, 2005, §5.2) | “ ”, —/–, × |
| Versalete falso (maiúscula reduzida) | traço fino e fraco (Lupton, 2006, p. 44) | versalete genuíno ou versal espacejada |
| Fonte esticada horizontalmente | deforma contraste e proporção (Bringhurst, 2005, §2.1.9) | variante estreita/larga desenhada |
| Corpo definido "em pt" sem olhar a altura-x | fontes diferentes no mesmo pt têm tamanhos reais diferentes (Lupton, 2006, p. 37) | dimensionar pela altura-x (§12) |
| Texto gerado por IA de imagem com acentos | geradores de imagem erram letras e diacríticos com frequência | compor todo texto em camada tipográfica real, nunca na imagem gerada [PC] |

## 18. Checklist tipográfico final

**Tamanho e leitura**
- [ ] Defini distância de leitura e meio (celular/impresso/parede) antes de escolher tamanhos.
- [ ] Toda informação crítica tem altura-x ≥ 0,0035 × distância (de preferência ×2); corrigi pela fração de altura-x da fonte.
- [ ] Post: texto de apoio ≥ 40 px, nada importante < 36 px; título legível na miniatura da grade.
- [ ] Texto corrido não passa de ~2° de altura-x; impacto vem de peso/contraste/cor.

**Família e estilo**
- [ ] Máximo de 2 famílias; pareamento por parentesco estrutural ou contraste claro de função; alturas-x igualadas na mesma linha.
- [ ] Glifos PT-BR testados (Ã Õ Ç É Ê À, aspas curvas, meia-risca, travessão); acentos de maiúscula não colidem.
- [ ] Licença confirmada para o uso (impressão, web, logo, embutir em PDF).
- [ ] Nenhum falso itálico, falso bold, falso versalete, nem letra esticada ou comprimida.
- [ ] Sem light/thin em texto; sem modulação forte em corpo pequeno ou para público idoso.

**Hierarquia e espaço**
- [ ] ≤ 3 níveis visíveis; saltos de 1,5–2× entre níveis em peça rápida; ≤ 3 sinais por nível.
- [ ] Entrelinha: texto 120–145% (sem serifa e colunas largas no alto da faixa); títulos 90–110%; espaços verticais em múltiplos do módulo.
- [ ] Medida: 45–75 caracteres em texto corrido; 20–40 em peças rápidas; justificado só com ≥ ~48 caracteres.
- [ ] Caixa-alta espacejada (+5–10%); minúsculas sem tracking; título grande com kerning manual; nada de tracking negativo para caber.

**Acabamento**
- [ ] Alinhado à esquerda por padrão; títulos quebrados pelo sentido; sem hifenização em títulos e CTA.
- [ ] Sem palavra sozinha em fim de parágrafo/título; sem linha isolada no topo de coluna; sem "de / São Luís" quebrado.
- [ ] Meia-risca em intervalos (3–6), × em dimensões, espaço inseparável em `R$ 47` e `10 mm`, um espaço entre frases, reticências (…).
- [ ] Algarismos titulares com versais e em tabelas (tabulares); números longos agrupados.

**Teste**
- [ ] Camada informativa (o quê/quando/onde/CTA) sobrevive à redução a 25%.
- [ ] Impressão 1:1 vista da distância real; post visto no celular, na mão, com brilho médio.
- [ ] Para idosos/baixa visão: contraste alto, fundo liso e fosco, traço homogêneo, c/e diferenciados, corpo "recomendado" como piso.
