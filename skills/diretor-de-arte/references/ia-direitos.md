# IA generativa e direitos autorais no fluxo de design — referência operacional

Fonte principal: U.S. Copyright Office (USCO, 2025), *Copyright and Artificial Intelligence, Part 2: Copyrightability* (jan. 2025; páginas = numeração impressa do relatório). Complementares (só via mapa, não lidos aqui): USCO Parte 3 (treinamento, pré-publicação, 9 maio 2025); *Thaler v. Perlmutter*, D.C. Cir., 18 mar. 2025.
Níveis: **[N]** posição normativa oficial dos EUA (órgão de registro, não lei nem tribunal); **[J]** decisão judicial citada; **[C]** caso de registro concreto; **[I]** inferência operacional deste arquivo para o fluxo de design (não está na fonte).
**Isto não é parecer jurídico. Vale para registro nos EUA. Não afirme nada sobre o Brasil com base neste arquivo (ver §6).**

## 1. Princípio de base

- **Exija autoria humana.** Nos EUA a proteção requer que um humano tenha determinado elementos expressivos suficientes; nenhum tribunal reconheceu direito sobre material criado por não humano (USCO, 2025, p. 7–8) [N/J].
- **Esforço não é autoria.** Tempo, custo e número de tentativas são irrelevantes; protege-se originalidade, não "suor" (USCO, 2025, p. 8–9, 20, citando *Feist*) [N/J].
- **O critério é controle, não previsibilidade.** Aleatoriedade não elimina autoria se o humano canaliza a execução (ex.: Pollock controlava cor, camadas, gesto; fotógrafo de natureza escolhe ângulo, local, exposição) (USCO, 2025, p. 20–21) [N].
- **Máquina como ferramenta não impede proteção** — desde a fotografia (*Burrow-Giles*, 1884), desde que haja escolhas expressivas humanas (USCO, 2025, p. 9) [J].
- **IA não é coautora.** Não forma intenção, não assina contrato: não há "obra conjunta" humano+IA nem obra sob encomenda feita por IA (USCO, 2025, p. 10, 19 nota) [N].

## 2. O que É e o que NÃO É protegível (EUA)

| Contribuição humana | Status | Fonte |
|---|---|---|
| **Uso assistivo** (remover objetos/multidões, correção de cor, nitidez, rotoscopia, revisão de texto) | Não limita a proteção da obra humana | p. 11–12 [N] |
| **IA como brainstorming** (gerar, consultar, mas não incorporar o output) | Não afeta a obra humana resultante | p. 12 [N] |
| **Prompt sozinho**, simples ou detalhado | Insuficiente para tornar o usuário autor do output, com a tecnologia atual | p. 18–19, 41 [N] |
| **Texto do prompt em si** | Pode ser protegido se for criativo — questão separada do output | p. 13 [N] |
| **Reprompting iterativo** (centenas de revisões) | Não muda a análise: equivale a "rolar o dado" de novo | p. 20 [N] |
| **"Autoria por adoção"** (escolher o melhor output) | Escolher entre opções não controladas não é ato criativo | p. 21 [N] |
| **Input expressivo próprio** (desenho, foto, layout do autor) perceptível no output | Protegido na parte humana perceptível, escopo análogo a obra derivada | p. 22–24 [N/C] |
| **Seleção, coordenação e arranjo** criativos de material gerado + humano | Protege a composição como um todo, não o material gerado isolado | p. 24–25 [N/C] |
| **Modificação humana** do output (edição que acrescenta autoria) | Protege a contribuição acrescentada; caso a caso | p. 25–27 [N] |
| **Edição regional** (selecionar área e regerar com novo prompt) | Pode dar controle sobre seleção e posição de elementos; caso a caso | p. 26–27 [N] |
| **Elemento gerado dentro de obra humana maior** | Não afeta a proteção da obra maior | p. 27 [N] |
| **Arranjo de só 2–3 elementos** | Em geral insuficiente (*de minimis*) | p. 27, nota 138 [N] |

### Exemplos do relatório (parafraseados)

- **Gato de óculos (p. 19–20) [C]:** o USCO gerou uma imagem com um prompt longo (sujeito, cenário, luz, lente, enquadramento). O resultado atendeu parte das instruções, ignorou outras (ambiente de madeira) e inventou o que não foi pedido (raça, pose, uma mão humana segurando o jornal). Rodado de novo, saiu outra imagem. Lição: o prompt descreve a ideia; o sistema decide a expressão.
- **"Rose Enigma" (p. 23–24) [C]:** a autora desenhou à mão e usou o desenho como input. Registro concedido só para a autoria pictórica humana perceptível e separável (contorno da máscara, posição de traços, arranjo de hastes e folhas); excluídos realismo 3D, luz, sombras gerados.
- **"Suryast" (p. 23, nota 124) [C]:** foto do requerente + instrução para aplicar o estilo de *A noite estrelada* de Van Gogh. Registro recusado: a obra humana de entrada não ficou claramente perceptível e o controle foi insuficiente.
- **"Zarya of the Dawn" (p. 24–25) [C]:** HQ com imagens geradas + texto humano. Protegidos o texto e a seleção/disposição de imagens e texto nas páginas; as imagens isoladas, não.
- **Edição por região (p. 26) [C]:** exemplo de gerar candidatas, escolher, selecionar uma área e regenerar com prompt alterado, repetidamente — pode configurar controle, mas o órgão não deu veredito geral.
- **Randy Travis (p. 38) [C]:** modelo vocal de IA usado como ferramenta para realizar escolhas da equipe humana; registrado. A distinção assistivo × gerador vale igualmente para criadores com deficiência.

## 3. Práticas para o fluxo de design com IA

1. **Documente a contribuição humana em cada peça** [I, ancorado em p. 3, 22–27]: guarde esboços, rascunho de layout, arquivos-fonte em camadas, versões intermediárias e um registro curto "o que a IA gerou / o que o humano decidiu". O USCO pede que, havendo mais que material gerado *de minimis*, o requerente declare o uso e descreva a contribuição humana (p. 3) [N].
2. **Construa camadas autorais** [I, ancorado em p. 24–27]: trate a imagem gerada como matéria-prima e faça a autoria nas camadas que o humano controla — grid, tipografia, hierarquia, texto, recorte e enquadramento, retoque, composição de múltiplos elementos, cor final. Mais de 2–3 elementos arranjados com critério.
3. **Comece por input próprio quando a exclusividade importa** [I, ancorado em p. 22–24]: esboço, foto ou ilustração do cliente/estúdio como base (img2img, controle estrutural), garantindo que traços dessa obra permaneçam perceptíveis no resultado.
4. **Prefira edição localizada a re-prompt global** [I, ancorado em p. 20, 26–27]: inpainting, edição por região e retoque manual aproximam-se mais de controle que regenerar a imagem inteira.
5. **Não prometa exclusividade nem titularidade** sobre imagem puramente gerada por prompt [I, ancorado em p. 18–21]. Em proposta/contrato, diga que a proteção recai sobre a peça final composta e a contribuição humana, não sobre o output bruto.
6. **Nunca credite a IA como autora** e não registre a IA como coautora (p. 10, 19 nota; *Thaler*, via mapa) [N/J].
7. **Não imite artistas vivos nem obras identificáveis.** Não use nomes de artistas, títulos de obras ou logos em prompts; não aplique "estilo de [obra X]" a material próprio. O caso *Suryast* mostra que transferir o estilo de uma obra famosa não gera autoria (p. 23, nota 124) [C]; a questão de infração/treinamento é da Parte 3 (via mapa, não lida aqui) [I].
8. **Descreva estilo por sistema, não por autor** [I]: em vez de "no estilo de [artista]", descreva regras formais (paleta, técnica, grid, textura, época) — coerente com `repertorio-historico.md`.
9. **Use IA assistiva sem receio** de perder proteção da obra humana: remoção de objetos, extensão de fundo, upscale, correção de cor (p. 11–12) [N].
10. **Brainstorming sem incorporação é livre** (p. 12) [N]: gerar *moodboards* e alternativas para referência e então desenhar/compor do zero mantém a obra integralmente humana.
11. **Prefira ferramentas com política clara de dados de treino e indenização** (USCO Parte 3, via mapa) [I — não verificado aqui].
12. **Registre a ferramenta, versão, data e seed** de cada geração [I]; seeds reduzem mas não eliminam variação (p. 7) [N].

### Checklist por peça com IA [I]
- [ ] Output bruto guardado + arquivo final em camadas + esboço/input humano, se houver.
- [ ] Nota de 3 linhas: ferramenta/versão/data; o que foi gerado; o que foi decidido/feito por humano.
- [ ] Elementos autorais humanos identificáveis: layout, tipografia, texto, edição, composição de vários elementos.
- [ ] Nenhum nome de artista, obra, marca ou personagem protegido no prompt.
- [ ] Nenhuma promessa de exclusividade sobre o elemento gerado; cliente informado do uso de IA.
- [ ] Nenhuma afirmação sobre a lei brasileira; dúvida jurídica → advogado.

## 4. Respostas-padrão para o cliente

- "Um prompt bem detalhado deixa a imagem protegida?" → Nos EUA, segundo o USCO (2025, p. 18–21), não; o que conta é a expressão determinada por humano.
- "A peça é nossa com exclusividade?" → A composição final com contribuição humana tende a ser protegível nos EUA; o elemento gerado isolado, não. Para o Brasil, **consulte advogado** (ver §6).
- "Posso usar no estilo de [artista/obra]?" → Não fazemos. Traduzimos a referência em regras formais próprias.

## 5. Estado e prazo de validade

- O USCO diz que a conclusão sobre prompts vale "na tecnologia atual" e pode mudar se as ferramentas derem mais controle — ou ficar ainda mais firme com otimização automática de prompts (p. 21–22) [N]. Reveja este arquivo a cada nova orientação do USCO.
- O USCO não recomenda mudança legislativa; espera que os tribunais detalhem caso a caso (p. 40–41) [N].
- *Thaler*: o relatório (jan. 2025) ainda o descreve como em recurso (p. 8). O mapa registra a decisão do D.C. Circuit (18 mar. 2025) mantendo a recusa e a negativa de certiorari pela Suprema Corte em 2 mar. 2026 — **esta última não verificada no registro da própria Corte** (fonte: análises de escritórios). Ao citar, diga "segundo análises jurídicas".

## 6. Lacuna explícita — Brasil e outras jurisdições

- **Brasil (Lei 9.610/1998), projetos de lei e jurisprudência brasileira: NÃO verificados.** O relatório do USCO não menciona o Brasil. **Não afirme posição jurídica brasileira**; não diga "no Brasil também é assim". Formule: "nos EUA, segundo o Copyright Office…; para o Brasil, é preciso consulta jurídica".
- **UE:** o USCO relata que a maioria dos Estados-membros, em questionário do Conselho da UE (2024), entende que as regras atuais bastam e que só há proteção com contribuição humana significativa (p. 29) [N, relato de segunda mão]. AI Act e direito de cada país **não verificados**.
- Outros relatos do USCO, também de segunda mão (p. 28–30): Coreia (só pessoa natural é autora; protege-se a parte modificada e a compilação), Japão (caso a caso: instruções, nº de tentativas, seleção, acréscimos humanos), China (tribunal de Pequim reconheceu autoria com 150+ prompts e ajustes, sem efeito de precedente), Reino Unido (lei de 1988 protege obra "gerada por computador" atribuindo autoria a quem fez os arranjos — aplicação à IA incerta). **Ou seja: jurisdições divergem; a regra dos EUA não é universal.**
