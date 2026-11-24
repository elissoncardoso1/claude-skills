# Cor — referência operacional para peças estáticas

> Escopo: cartaz, post, carrossel, capa, flyer, anúncio. Este arquivo trata de **decisão cromática**; conversão CMYK, perfis ICC e TAC ficam no arquivo de produção gráfica.
> Fontes primárias: Albers (2013, ed. 50 anos, *Interaction of Color*, Yale); Pedrosa (*Da cor à cor inexistente*, 10ª ed., Senac — paginação desta edição); Jonauskaite et al. (2020, *Psychological Science* 31(10)); Guimarães (*A cor como informação*) **apenas via mapa comentado** (o PDF disponível é escaneado, sem texto verificável).
> Níveis de evidência: **forte** (fenômeno/achado empírico robusto) · **moderada** (empírico com limites relevantes) · **prática consagrada** (consenso profissional, pouca medição) · **opinião** (posição de autor).

## Índice
1. Princípio-mestre: cor é relativa
2. Fenômenos de interação — como explorar, como evitar acidentes
3. Valor antes de matiz (teste em escala de cinza)
4. Construção de paleta para uma peça
5. Semântica cor–emoção: o que Jonauskaite et al. (2020) realmente mostram
6. Cor como código em séries e campanhas
7. Contraste de leitura (metas transferíveis do WCAG)
7b. Acidentes frequentes e correção rápida
8. Checklist de cor
9. Notas de verificação

---

## 1. Princípio-mestre: cor é relativa

- **Nunca aprove uma cor isolada (amostra, swatch, código HEX).** Aprove-a dentro do layout, ao lado das vizinhas reais e na área real. Albers abre o método afirmando que a cor é "o meio mais relativo da arte" (Albers, 2013, p. 8) — a mesma tinta lida de forma diferente conforme o entorno. **Forte** (fenômeno perceptivo replicável).
- **Distinga cor influenciadora de cor influenciada.** Fundos grandes e saturados empurram; manchas pequenas são empurradas. A mudança acontece em duas direções simultâneas — claridade e matiz — em intensidades variáveis (Albers, 2013, p. 9). Consequência prática: o fundo de um post decide como o logo e o CTA vão parecer; escolha o fundo **depois** de fixar as cores que não podem mudar (marca, alerta), e teste-as sobre ele.
- **Nenhum olho treinado é imune.** Albers trata o contraste simultâneo como fenômeno psicofisiológico do qual nem o especialista escapa (Albers, 2013, p. 23). Não confie em "eu sei que é o mesmo azul"; meça. **Forte.**
- **Harmonias de manual não garantem nada.** Círculos de complementares, tríades e tétrades parecem bons em diagrama porque lá todas as cores têm a mesma área, forma e frequência; na peça real, quantidade, forma, repetição, luz ambiente e material alteram o resultado (Albers, 2013, pp. 41–42). Use esquemas de roda só para gerar candidatos; decida no contexto. **Opinião** de autor com forte respaldo pedagógico.
- Pedrosa sintetiza a mesma ideia: a beleza ou agressividade de uma combinação nasce da **indução** mútua entre cores, e um matiz rende mais quando modificado pela indução justa das vizinhas (Pedrosa, p. 210). **Opinião.**

## 2. Fenômenos de interação — como explorar, como evitar acidentes

### 2.1 Contraste simultâneo (uma cor parecendo duas)
- **O que é:** a mesma cor parece diferente sobre fundos diferentes; o fundo "puxa" a figura para o oposto de si em claridade e em matiz (Albers, 2013, pp. 18–19, 22). Pedrosa, seguindo Chevreul, separa contraste **simultâneo** (vizinhança), **sucessivo** (pós-imagem após fixar o olhar) e **misto** (a pós-imagem soma-se à cor vista em seguida) (Pedrosa, pp. 180–181). **Forte.**
- **Explorar:** para que *uma* cor de marca pareça duas (ex.: série de cartazes com fundos alternados), coloque-a sobre dois fundos opostos; o efeito máximo exige que ela fique topologicamente "no meio" dos dois fundos (Albers, 2013, pp. 18–19). Ajuste os fundos, não só a figura.
- **Evitar:** em carrosséis e séries com fundos variados, a cor do logo/CTA vai **parecer** mudar de cartão para cartão. Se a consistência percebida importa, use fundo neutro ou placa (selo) de cor fixa atrás do elemento-chave. **Prática consagrada.**
- **Cinzas são os mais vulneráveis.** Um cinza neutro ao lado de um matiz puro tende a se tingir do complementar desse matiz; um cinza levemente azulado ao lado de laranja saturado pode parecer bem azul (Pedrosa, p. 161). Texto cinza sobre fundo colorido muda de "temperatura": confira no layout. **Forte.**

### 2.2 Subtração (duas cores parecendo uma)
- **O que é:** o fundo subtrai da figura o próprio matiz e a própria claridade. Três vermelhos diferentes sobre um fundo igual a um deles: esse um "desaparece" (Albers, 2013, pp. 20–21). **Forte.**
- **Explorar:** para unificar fotos de origens diferentes, ponha-as sobre um fundo que contenha a dominante que as diferencia — as diferenças encolhem.
- **Evitar:** elementos que precisam ser distinguidos (botão ativo × inativo, categoria A × B, legenda de gráfico) **não** devem ficar sobre fundo próximo a um deles. O fundo vai apagar exatamente a diferença que codifica a informação.

### 2.3 Transparência ilusória e mistura imaginada
- **O que é:** três chapas opacas sobrepostas parecem transparentes quando a cor da interseção é uma mistura plausível das duas "cores-mãe" (Albers, 2013, pp. 24–26). A interseção mais próxima de uma das mães faz aquela forma parecer **na frente**; a mistura equidistante (média) parece plana, frontal (Albers, 2013, pp. 29–32). **Forte** (como efeito perceptivo); a leitura espacial é **prática consagrada**.
- **Explorar:** sobreposições de formas chapadas (estética de serigrafia, Bauhaus, risografia) criam profundidade sem sombra nem gradiente; use para dar camadas a título + forma.
- **Regras de execução:** (a) a interseção precisa ser **mais clara que a mãe mais escura e mais escura que a mais clara** — senão a ilusão quebra (Albers, 2013, p. 29); (b) bordas suaves (cores próximas) leem como conexão, bordas duras (cores distantes) como separação/distância (Albers, 2013, p. 31). Use isso para agrupar ou separar planos.
- **Evitar:** em modos de mesclagem digitais (multiply/screen), confira se o resultado continua plausível; misturas "impossíveis" leem como terceira forma opaca, não como transparência.

### 2.4 Mistura óptica e efeito Bezold
- **O que é:** pontos, linhas ou padrões finos de duas cores, vistos de longe, fundem-se numa terceira; o efeito depende de **tamanho do elemento e distância** (Albers, 2013, p. 33). Bezold notou que trocar **uma única cor** num padrão fino muda a aparência de todo o conjunto (Albers, 2013, p. 33). **Forte.**
- **Explorar:** tramas, hachuras e padrões de pequena escala produzem cores "que não estão lá" e texturas vibrantes, úteis em fundos de cartaz.
- **Evitar (crítico em post/miniatura):** a peça de feed é vista em miniatura. Padrões, texto fino colorido e contornos finos podem se misturar opticamente com o fundo e virar uma mancha de cor intermediária. Teste a peça reduzida a ~20–25% da largura (tamanho de feed/miniatura). Contornos coloridos finos em volta de letras mudam a cor percebida da letra inteira (efeito tipo Bezold). **Prática consagrada** apoiada em fenômeno forte.

### 2.5 Bordas vibrantes e bordas que somem
- **Bordas vibrantes:** matizes contrastantes com **claridade quase igual** (ex.: vermelho puro × verde médio, azul × laranja de mesmo valor) produzem bordas que tremem, duplicam ou "fazem sombra"; Albers registra que o efeito incomoda e só aparece em publicidade "gritante" (Albers, 2013, p. 61). **Nunca** use esse par para texto sobre fundo. Para impacto, use-o em formas grandes e **sem** leitura. **Forte** (efeito); a avaliação estética é **opinião**.
- **Bordas que somem:** cores vizinhas de matiz próximo e **claridade realmente igual** fazem o limite desaparecer (Albers, 2013, p. 62). Útil em fusões visuais (ver retórica visual, arquivo de conceito); desastroso para separar figura e fundo.

### 2.6 Distribuição de área controla a força do efeito
- Efeitos de interação ficam fortes quando a cor influenciada é pequena e o fundo é grande e homogêneo; padrões em mosaico, com influência vinda de vários lados, **anulam** os efeitos (Albers, 2013, pp. 10–11). Em layouts muito fragmentados (grade de muitas fotos, mosaico de cards), não conte com efeitos de contraste — eles se cancelam. **Prática consagrada** (demonstração didática).

## 3. Valor antes de matiz (teste em escala de cinza)

- **Resolva hierarquia e legibilidade com valor (claro–escuro); use matiz para expressão e código.** Matiz sem diferença de valor não separa figura de fundo de forma confiável (ver §2.5). **Forte** (convergência Albers + literatura de legibilidade do mapa, princípio 19).
- **Desconfie do seu julgamento de claridade entre matizes diferentes.** Nos testes de Albers com estudantes de arte, cerca de 60% das escolhas sobre "qual cor do par é mais escura" estavam erradas (Albers, 2013, p. 13). Dado didático, não experimento controlado: **moderada**. Implicação: use instrumento (luminância calculada ou conversão para cinza), não o olho.
- **Procedimento obrigatório — teste de cinza:**
  1. Converta a peça para escala de cinza **por luminância** (não pela média RGB; prefira dessaturação perceptual — L* do Lab ou luminância relativa).
  2. A hierarquia deve sobreviver: o elemento dominante continua dominante? O título se separa do fundo? O CTA aparece?
  3. Se dois elementos que devem se distinguir viram o mesmo cinza, mude **o valor** de um deles antes de mexer no matiz.
  4. Repita em miniatura (≈ 20–25%).
- **Reprodução altera valores.** Albers observa que fotografia e reprodução tendem a escurecer escuros, clarear claros e achatar os cinzas médios (Albers, 2013, pp. 13–14). Na prática: diferenças sutis de meio-tom podem sumir na impressão, na tela do celular com brilho baixo ou na compressão do Instagram. Deixe margem de valor entre elementos críticos. **Prática consagrada.**
- **Escala de valores de Pedrosa:** organize a peça a partir de três referências — máxima luz, máxima sombra e um cinza médio, que atua como mediador das induções cromáticas (Pedrosa, p. 159). **Opinião** útil como ponto de partida de composição tonal.
- **Clarear vs. escurecer matizes (Pedrosa, p. 159, opinião):** amarelos e cores de alto valor ficam mais bonitos degradados com branco (tints) do que escurecidos com preto (amarelo + preto tende a "sujar", esverdeando); vermelhos e azuis aceitam bem o escurecimento. Use ao gerar variações claras/escuras de cores de marca.

## 4. Construção de paleta para uma peça

### 4.1 Papéis: dominante, subordinada, acento
- **Dominante** (fundo ou maior massa): define clima e temperatura; ocupa a maior área.
- **Subordinada(s)**: estrutura, blocos de texto, segunda massa; apoia sem competir.
- **Acento**: a cor que o olho deve achar primeiro (CTA, dado-chave, palavra do título); área pequena, máximo contraste de valor **e** de matiz com a vizinhança.
- Fundamento: Albers trata quantidade (extensão em área e recorrência em número) como o principal instrumento de equilíbrio, ênfase e dominância; o mesmo conjunto de 4 cores pode parecer 4 paletas diferentes só mudando proporções e posições (Albers, 2013, pp. 43–44). **Prática consagrada / opinião de autor.**
- **Qualquer cor "combina" com qualquer outra se a quantidade estiver certa** (Albers, 2013, p. 44). Antes de trocar uma cor que "não funciona", teste mudar a área dela. **Opinião** (amplamente adotada no ensino).

### 4.2 Proporções de área (pontos de partida, não regras)
- Comece com algo como **60–75% dominante / 20–30% subordinada / 3–10% acento** e ajuste olhando. Não há base empírica para números exatos; é **prática consagrada**.
- Referência histórica de compensação por luminosidade (Schopenhauer, relatado por Albers, 2013, p. 43): cores claras pedem área menor que suas opostas escuras — amarelo:violeta ≈ 3:9, laranja:azul ≈ 4:8, vermelho:verde ≈ 6:6. Use como heurística: **quanto mais clara/saturada a cor, menos área ela precisa para pesar**. **Opinião** histórica.
- Aumentar a quantidade de uma cor tende a aproximá-la visualmente do observador (Albers, 2013, p. 44) — cores em grande área "avançam". **Opinião.**
- **Recorrência também é quantidade:** repetir o acento em 2–3 pontos pequenos cria percurso de leitura; repeti-lo em 8 pontos o transforma em textura e mata a hierarquia. **Prática consagrada.**

### 4.3 Economia de 2–3 cores
- Para cartaz, post e capa, **parta de 2–3 cores + preto/branco/neutro**. Menos cores = mais controle de interação, código mais claro, melhor leitura em miniatura, impressão mais barata (spot colors, risografia, serigrafia). O mapa associa essa economia ao design brasileiro dos anos 60, onde cor chapada funciona como imagem (Mapa, Área 4.3). **Prática consagrada.**
- Fotografia colorida conta como "cor": se a peça tem foto rica em cor, reduza a paleta gráfica (1 cor + neutros) ou trate a foto (duotone, monocromia) para não brigar.
- **Cinza-colorido / tons rompidos (Pedrosa, pp. 159–162):** misturar um par complementar em partes iguais gera um cinza que pode servir de cor de passagem entre os dois; cinzas levemente coloridos dão unidade ao conjunto. Use para fundos e áreas de apoio que precisam "costurar" cores fortes. **Opinião** de colorista.

### 4.4 Procedimento de paleta para uma peça
1. Fixe as cores **não negociáveis** (marca, código de série, alertas).
2. Defina o **valor** de cada papel (fundo claro × escuro) antes do matiz.
3. Escolha a dominante pelo clima pretendido (ver §5, com cautela).
4. Escolha o acento pelo contraste máximo com a dominante **no ponto onde será usado**.
5. Monte em layout real; ajuste **áreas** antes de trocar cores.
6. Rode o teste de cinza (§3) e de miniatura (§2.4).
7. Verifique contraste de texto (§7).

## 5. Semântica cor–emoção: o que Jonauskaite et al. (2020) realmente mostram

### 5.1 O estudo
- 4.598 participantes, 30 nações, 22 línguas; associavam 20 conceitos de emoção (Roda de Emoções de Genebra) a **12 termos de cor** — palavras, **não amostras de cor** (Jonauskaite et al., 2020, pp. 2–5). Coleta online, majoritariamente pessoas alfabetizadas digitalmente (p. 14).
- **O Brasil não está entre as 30 nações.** As latino-americanas são Colômbia e México. Generalizar para público brasileiro é inferência.

### 5.2 Achados principais
- **Padrão compartilhado alto:** similaridade média nação–padrão global r = 0,88 (de 0,68 no Egito a 0,94 na Espanha) (p. 9). **Forte** (como associação conceitual).
- **Associações proeminentes globais (probabilidade ≥ 0,4)** (p. 8):
  - preto → tristeza, medo, ódio
  - vermelho → amor, raiva
  - rosa → amor, alegria, prazer
  - cinza → tristeza, decepção
  - amarelo → alegria
  - laranja → alegria, diversão
  - branco → alívio
- **Carga emocional:** em todas as nações, vermelho e preto foram os termos mais associados a alguma emoção; marrom, o menos (p. 9). Implicação: vermelho e preto "falam alto", mas falam **coisas ambivalentes** (amor *e* raiva; tristeza *e* medo) — o contexto (imagem, título) decide qual leitura vence.
- **Mais e menos estáveis entre culturas:** rosa, verde, turquesa e preto variam pouco; **roxo e amarelo variam mais** (p. 9). Roxo teve a menor concordância (r ≈ 0,66).
- **Exemplos de variação local** (p. 9; p. 11): na Nigéria, vermelho também evocou medo; na China, branco também evocou tristeza (luto); no Egito, amarelo não foi associado a alegria; na Grécia, roxo evocou tristeza (luto).
- **Proximidade linguística e geográfica** prediz maior semelhança entre nações (p. 9); um classificador acertou a nação do participante acima do acaso (34% vs. 9,7%) (p. 9). Há, portanto, especificidade cultural real, mas menor que o núcleo comum.
- Sexo quase não muda o padrão (r = 0,987); idade muda pouco o padrão, mas pessoas de 50–60 anos associam menos cores a emoções (p. 11).

### 5.3 O que **não** se pode concluir
- **Não é causalidade.** O estudo mede associação entre *conceitos* (palavra "vermelho" ↔ palavra "raiva"); os próprios autores dizem que não se sabe se as pessoas *sentem* raiva ao *ver* vermelho (Jonauskaite et al., 2020, p. 13). Não prometa ao cliente que "azul gera confiança" ou "vermelho aumenta conversão" — o mapa já classifica isso como mito (Mapa, §5).
- **Não é sobre tons específicos.** "Vermelho" como palavra cobre de carmim a coral. A leitura de um tom concreto depende de saturação, valor, vizinhança (§1–2) e imagem.
- **Não substitui conhecimento local.** Guimarães (via mapa) insiste que a simbologia é construída também linguística e culturalmente, com exemplos da mídia brasileira (Mapa, Área 3.4). Verifique conotações locais: partidos, times, datas religiosas, campanhas de saúde já estabelecidas (ex.: "Outubro Rosa", "Setembro Amarelo" no Brasil — códigos que o público já reconhece e que podem colidir com sua peça). **Prática consagrada.**

### 5.4 Como usar na peça
- Use as associações como **apoio semântico redundante**: a cor reforça o que título e imagem já dizem; nunca carrega sozinha a mensagem. **Moderada.**
- Prefira cores de associação mais estável (rosa, verde, preto) quando a mensagem emocional for crítica; trate roxo e amarelo como mais ambíguos. **Moderada.**
- Para vermelho e preto, **ancore** a emoção pretendida com imagem e texto, pois as duas leituras opostas são prováveis. **Moderada.**
- Público internacional ou de outra cultura: cheque luto (branco, roxo), sorte/celebração (vermelho) e conotações políticas antes de fechar a paleta.

## 6. Cor como código em séries e campanhas

- **Uma cor = um significado, fixo em toda a série.** Se o laranja marca "evento" no cartão 1, não pode marcar "promoção" no cartão 4. Guimarães trata a cor como informação e recomenda codificação consistente em série (Mapa, Área 3.4 — conteúdo não verificado no original). **Prática consagrada.**
- **Limite o número de códigos:** 3–5 categorias diferenciadas por cor é um teto prático para leitura rápida; acima disso, combine cor com forma, ícone, posição ou rótulo. **Prática consagrada.**
- **Código precisa sobreviver ao contraste simultâneo (§2.1) e à subtração (§2.2):** se os fundos variam entre peças da série, a cor-código vai parecer variar. Coloque o código sobre base neutra constante (faixa, selo, borda) ou fixe também o fundo. **Forte** (fenômeno) / **prática** (solução).
- **Código não pode depender só de matiz.** Diferencie categorias também por valor (claro × escuro) para que sobrevivam ao teste de cinza, impressão P&B e daltonismo. Daltonismo vermelho–verde é a forma mais comum; evite par vermelho/verde de mesmo valor como único diferenciador. (Fora das fontes deste arquivo; **prática consagrada** em acessibilidade.)
- **Variação planejada:** uma série pode alternar paletas por peça (ex.: cada palestrante, uma cor) desde que um elemento fixo (tipografia, grid, cor de marca em selo) garanta a unidade. Albers mostra que as mesmas cores podem parecer "elencos" distintos só com redistribuição de quantidades (Albers, 2013, p. 44) — útil para variar sem trocar a paleta. **Opinião.**

## 7. Contraste de leitura (metas transferíveis do WCAG)

> **Aviso:** a WCAG 2.x é norma de acessibilidade **para conteúdo web**. Não é norma de impresso nem de imagem estática em rede social. Use as razões abaixo como **meta mínima transferível** — são o melhor critério quantitativo disponível e são calculáveis. **Prática consagrada** (fora das fontes deste arquivo; ver Área 9 do mapa).

- **Texto corrido, legenda, informação de rodapé, datas, preço:** razão de contraste ≥ **4,5:1** entre texto e fundo imediato.
- **Texto grande** (no WCAG: ≥ 18 pt regular ou ≥ 14 pt bold; em peça social, títulos grandes e grossos lidos em miniatura): ≥ **3:1**. Na dúvida sobre "grande" em miniatura de feed, trate como texto normal (4,5:1).
- **Elementos gráficos que carregam informação** (ícones, setas, bordas de botão, cores-código de gráfico): ≥ **3:1** contra a vizinhança.
- **Logotipos e texto puramente decorativo** são isentos no WCAG — mas, se o logo precisa ser reconhecido em miniatura, persiga 3:1 mesmo assim.
- **Texto sobre foto:** meça no **pior trecho** do fundo atrás das letras, não na média. Se não atinge a meta, use: placa/tarja sólida ou semitransparente, escurecimento/clareamento local da foto, sombra difusa ampla, ou mova o texto para área calma.
- **Por que valor, não matiz:** a fórmula do WCAG usa luminância relativa; pares de matiz forte e mesma luminância (§2.5) falham e ainda vibram.
- **Impresso:** papel não emite luz, tintas reduzem gama e ganho de ponto escurece meios-tons (Albers, 2013, pp. 13–14, sobre perda de meio-tom na reprodução). Para impresso, mire **acima** das metas (≥ 7:1 para texto pequeno é uma folga prudente) e teste prova física. **Opinião** prudente.
- **Público idoso/baixa visão:** contraste alto + peso não fino + nada de texto sobre imagem (Mapa, princípio 38, Legge & Bigelow 2011; Farias & Landim 2020).

## 7b. Acidentes frequentes e correção rápida

| Sintoma na peça | Causa provável | Correção |
|---|---|---|
| Logo/CTA "muda de cor" entre cartões do carrossel | Contraste simultâneo com fundos diferentes (Albers, 2013, pp. 8–9) | Selo/placa de fundo fixo atrás do elemento; ou fundo constante |
| Texto colorido "treme" ou cansa | Matizes opostos com valor igual (Albers, 2013, p. 61) | Separe por valor (clareie/escureça um dos dois) ou use texto neutro |
| Categoria A e B parecem iguais | Fundo subtrai a diferença (Albers, 2013, pp. 20–21) | Fundo neutro; diferencie também por valor e forma |
| Título some em miniatura | Diferença só de matiz; meio-tom perdido na redução | Teste de cinza; aumente diferença de valor; peso mais grosso |
| Textura fina vira mancha lamacenta | Mistura óptica dependente de escala (Albers, 2013, p. 33) | Aumente a escala do padrão ou simplifique para chapado |
| Sobreposição parece "colada", não transparente | Interseção fora do intervalo de valor das cores-mãe (Albers, 2013, p. 29) | Ajuste a interseção para valor intermediário |
| Paleta "não combina" | Áreas equivalentes, sem dominante (Albers, 2013, pp. 41–44) | Redistribua quantidades antes de trocar cores |
| Amarelo escurecido parece sujo/esverdeado | Tom de alto valor rebaixado com preto (Pedrosa, p. 159) | Gere variações de amarelo pelo matiz (para ocre/laranja), não com preto |
| Cinza de apoio parece azulado/rosado | Indução do matiz vizinho (Pedrosa, p. 161) | Cinza levemente aquecido/esfriado para compensar, conferido no layout |
| Foto colorida briga com a paleta gráfica | Cores demais em jogo | Reduza a paleta gráfica a 1 cor + neutros ou trate a foto (duotone) |

## 8. Checklist de cor

Antes de entregar, confirme:

- [ ] Cada cor foi aprovada **no layout**, ao lado das vizinhas reais, não como swatch isolado.
- [ ] Cores não negociáveis (marca, código) foram testadas sobre **todos** os fundos onde aparecem.
- [ ] Nenhum cinza ou cor neutra de texto mudou de temperatura por contraste simultâneo.
- [ ] Elementos que devem ser distinguidos **não** estão sobre fundo que subtrai a diferença.
- [ ] Nenhum texto está sobre par de matizes contrastantes com valor igual (bordas vibrantes).
- [ ] **Teste de cinza** por luminância: hierarquia, título e CTA sobrevivem.
- [ ] **Teste de miniatura** (≈ 20–25%): padrões finos, contornos coloridos e texto colorido não viraram mancha.
- [ ] Paleta de 2–3 cores + neutros (ou justificativa para mais).
- [ ] Papéis claros: uma dominante, subordinada(s), **um** acento; áreas ajustadas antes de trocar cores.
- [ ] Semântica de cor usada como reforço, ancorada por imagem/texto; nenhuma promessa causal ("cor X converte mais").
- [ ] Conotações locais/culturais verificadas (luto, política, times, campanhas temáticas do mês).
- [ ] Em série: uma cor = um significado; código também diferenciado por valor; base neutra constante sob o código.
- [ ] Contraste: texto normal ≥ 4,5:1; texto grande e gráficos informativos ≥ 3:1; medido no pior trecho; folga extra para impresso.
- [ ] Transparências simuladas são plausíveis (interseção entre os valores das mães).

## 9. Notas de verificação

- Albers: paginação da edição de 50 anos (Yale, 2013); números das páginas extraídos do texto. Pranchas não foram consultadas; os princípios foram descritos sem reproduzir exercícios.
- Pedrosa: OCR ruidoso; páginas 159, 161–162, 180–181 e 210 conferidas pela marcação de página do arquivo. A tese de Pedrosa de que a "cor inexistente" é registrável por câmera (p. 210) é posição do autor, não consenso.
- Jonauskaite et al. (2020): páginas do artigo (1–16). Tabela S6 e figuras suplementares não consultadas.
- Guimarães: **não verificado no original** (PDF sem camada de texto). Tudo que é atribuído a ele vem do mapa comentado (Área 3.4).
- Razões WCAG: citadas de conhecimento da norma (WCAG 2.1, critérios 1.4.3 e 1.4.11), não de fonte desta pasta.
