# Fontes (base de evidência)

Use para citar evidência com o ID. Achados de papers valem para os modelos e datas testados; docs de provedor refletem a versão coletada em out/2026.

## Papers

| ID | Referência | Achado-chave | Ressalva |
|---|---|---|---|
| F01 | Brown et al. 2020 — *Language Models are Few-Shot Learners* (GPT-3) | Aprendizado em contexto com zero/one/few-shot; few-shot escala melhor com tamanho | Falha em tarefas de comparar textos (WiC, ANLI) |
| F02 | Wei et al. 2022 — *Chain-of-Thought Prompting* | Raciocínio antes da resposta: GSM8K ~18→~57% (PaLM 540B) | Emergente (~100B+); sem ganho em tarefas de 1 passo |
| F03 | Kojima et al. 2022 — *Zero-Shot Reasoners* | "Let's think step by step": MultiArith 17,7→78,7% | Sem ganho em senso comum; wording importa |
| F04 | Wang et al. 2023 — *Self-Consistency* | Voto de maioria em várias cadeias: GSM8K +17,9; 5–10 amostras bastam | Custo; requer respostas discretas |
| F05 | Zhou et al. 2023 — *Least-to-Most* | Decompor → resolver em sequência; SCAN 99,7% vs 16,2% CoT | Prompts de decomposição não generalizam entre domínios |
| F06 | Yao et al. 2023 — *ReAct* | Pensamento↔ação↔observação reduz alucinação; combinar com CoT-SC é melhor | Loops; buscas ruins descarrilam |
| F07 | Yao et al. 2023 — *Tree of Thoughts* | Game of 24: 4%→74% | ~100× custo; desnecessário em muitas tarefas |
| F08 | Schick et al. 2023 — *Toolformer* | Delegar cálculo/busca a ferramentas; decisão de chamar é sensível ao wording | Sem encadeamento de ferramentas |
| F09 | Lewis et al. 2020 — *RAG* | Recuperação reduz alucinação e permite atualizar conhecimento trocando o índice | BM25 vence em consultas centradas em entidades |
| F10 | Liu et al. (TACL) — *Lost in the Middle* | Curva em U; queda >20% no meio; mais documentos saturam | — |
| F11 | Zhao et al. 2021 — *Calibrate Before Use* | Vieses de maioria/recência/token comum; ordem 54→93%; calibração com "N/A" +30% | Requer logprobs; classificação |
| F12 | Lu et al. 2022 (ACL) — *Fantastically Ordered Prompts* | Ordem de exemplos vai de ~SOTA a aleatório; não transfere entre modelos | Classificação |
| F13 | Sclar et al. 2024 (ICLR) — *FormatSpread* | Formatação neutra muda até 76 pontos; rankings invertem | Entradas curtas |
| F14 | Schulhoff et al. 2024 — *The Prompt Report* | Taxonomia de 58 técnicas; Zero-shot-CoT piorou no MMLU (gpt-3.5); DSPy > humano no estudo de caso | Observacional |
| F15 | Mei et al. 2025 — *Survey of Context Engineering* | Contexto como montagem dinâmica de instruções, conhecimento, ferramentas, memória, estado | Números citados de terceiros |
| F16 | Geng et al. 2025 — *JSONSchemaBench* | Decodificação restrita: mais conformidade, ~50% mais rápida, até ~4% mais acurada | Cobertura de features varia |
| F17 | Zheng et al. 2023 — *LLM-as-a-Judge / MT-Bench* | Juiz forte ~85% de concordância; vieses de posição, verbosidade, autopreferência | Foco em utilidade, não segurança |
| F18 | Greshake et al. 2023 — *Indirect Prompt Injection* | Conteúdo recuperado controla apps com LLM; defesas por filtro são "whack-a-mole" | Sem taxa quantificada |
| F19 | Yi et al. 2025 (KDD) — *BIPIA* | Todos vulneráveis; modelos mais capazes, maior ASR; delimitação + multi-turn + lembrete reduzem | Defesas caixa-preta não tornam robusto |
| F20 | Zhou et al. 2023 — *APE* | LLM gera e seleciona instruções ≥ humanas em 24/24 tarefas | Ganhos modestos, específicos do modelo |
| F21 | Yang et al. — *OPRO* | Otimização iterativa via meta-prompt; até +50% no BBH | Prompts específicos do avaliador; sobreajuste |
| F22 | Khattab et al. — *DSPy* | Assinaturas + módulos + compilação: GSM8K 25→82% (GPT-3.5) | Preprint |
| F23 | Yuksekgonul et al. 2024 — *TextGrad* | Feedback textual como gradiente; system prompt de modelo barato 77,8→91,9 | Estabilidade |
| S5a | Xiao et al. 2026 — *When Does Persona Prompting Actually Help?* | Persona ≈ sem efeito no agregado; ↑profundidade, ↓clareza | Um modelo; juiz LLM |
| S5b | Li et al. 2023 — *EmotionPrompt* | Ganhos com estímulos emocionais em modelos antigos | Métricas relativas infladas |
| S5c | Zhao et al. 2026 — *Do Emotions in Prompts Matter?* | Prefixos emocionais estáticos ≈ ruído em modelos atuais | Prefixos curtos, só acurácia |
| S5d | Zhang et al. 2024 — *Revisiting OPRO* | Modelos pequenos são maus otimizadores; few-shot CoT é baseline melhor | Compute limitado |

## Documentação oficial (coletada out/2026)

| ID | Fonte | Conteúdo usado |
|---|---|---|
| F24 | OpenAI — Prompt Engineering Guide | Roles, estrutura do developer prompt, few-shot com XML, prompts agênticos e de código, versionamento |
| F25 | OpenAI — Model Spec | Cadeia de comando, dados não confiáveis, escopo de autonomia, informação privilegiada |
| F26 | OpenAI — Reasoning models | `reasoning.effort`, custos, preservação de raciocínio, `phase`, conselhos de prompt |
| F27 | OpenAI — Structured Outputs | Schema strict, subconjunto suportado, casos de borda |
| F28 | OpenAI — Evaluation / Datasets | Datasets, anotação, graders |
| F29 | Anthropic — Building Effective Agents (2024) | Workflows vs agentes, padrões, ACI |
| F30 | Anthropic — Effective Context Engineering (2025) | Context rot, altitude certa, just-in-time, compactação, notas, subagentes |
| F31 | Anthropic — Writing Effective Tools for Agents (2025) | Design, namespacing, respostas, erros, avaliação de ferramentas |
| F32 | Anthropic — Agent Skills (2025) | Divulgação progressiva, autoria e segurança de skills |
| F33 | Agent Skills — Open Specification | Formato SKILL.md, limites, estrutura |
| F34 | Anthropic — Prompting best practices (Claude) | Clareza, XML, exemplos, contexto longo, formato, ferramentas, thinking, agentes |
| F35 | Google — Gemini Prompt Design Strategies | Few-shot, parâmetros, iteração, Gemini 3, template agêntico |
| F36 | Google — Gemini Structured Outputs | Subconjunto JSON Schema, limitações |
| F37 | OpenAI — Safety in Building Agents | Injeção, vazamento, mitigações |

Fontes complementares apenas localizadas (não lidas na íntegra): docs de parâmetros OpenAI/Gemini, adaptive thinking (Anthropic), structured outputs de Cohere/Mistral/DeepSeek, chat templates Llama/Qwen/Hugging Face, Bedrock Guardrails.
