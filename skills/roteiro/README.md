# Skill: Roteiro — criação e revisão

Skill para escrever, estruturar, diagnosticar e revisar roteiros audiovisuais em português, cobrindo **longa, curta, série/piloto, episódio, documentário, institucional e YouTube**.

Construída a partir de 16 livros de roteiro e dramaturgia (Field, Snyder, McKee, Truby, Vogler, Campbell, Seger, Comparato, Campos, Saraiva & Cannito, Douglas, Bernard, Rabiger, Lucena, Friedmann e Eves).

## Estrutura

```
SKILL.md                      # entrada: princípios, triagem, modos criação/revisão
references/
  estrutura.md                # Field, Snyder, McKee, Truby, Vogler; atos e modelos
  personagens.md              # Seger, Truby, Vogler; ficha, arco, elenco
  cena-dialogo-formato.md     # teste de cena, diálogo, escrita visual, formato BR/EUA/Fountain
  serie-tv.md                 # grade de atos, A/B/C, piloto, bíblia, novela
  documentario.md             # história, ponto de ataque, proposta, tratamento, ética
  institucional.md            # método de 7 passos, duas colunas, duração, cliente
  youtube.md                  # empacotamento, gancho, retenção, shorts
  processo-e-reescrita.md     # documentos, passes de reescrita, feedback
  revisao.md                  # protocolo, rubrica, parecer, falácias
  glossario.md                # PT-BR ↔ inglês
  fontes.md                   # o que veio de onde, limites
assets/
  beat-sheet.md               # planilha de 15 batidas
  escaleta.md                 # tabela de cenas
  duas-colunas.md             # roteiro imagem/som (e versão YouTube)
  ficha-personagem.md
  biblia-serie.md
  proposta-documentario.md
  relatorio-revisao.md
scripts/
  diagnostico.py              # métricas heurísticas de um roteiro em texto/Fountain
dist/                         # pacote pronto (gerado)
  roteiro/                    # cópia limpa, sem PDFs
  roteiro.skill               # zip no formato Agent Skills
  roteiro.zip                 # mesmo conteúdo, extensão .zip
```

## Como instalar

A skill segue o padrão aberto **Agent Skills** (`SKILL.md` + `references/` + `assets/` + `scripts/`). Funciona em OpenCode, Claude Code e Claude.ai.

### OpenCode

```bash
ln -s "$PWD/skills/roteiro" ~/.config/opencode/skills/roteiro
```

### Claude Code

A pasta pessoal de skills é `~/.claude/skills/`. Duas opções:

**Symlink (uma fonte de verdade):**

```bash
ln -s "$PWD/skills/roteiro" ~/.claude/skills/roteiro
```

**Cópia do pacote limpo (funciona sem o SSD externo):**

```bash
rm -rf ~/.claude/skills/roteiro
cp -R skills/roteiro ~/.claude/skills/roteiro
```

Depois, no Claude Code:

- invoque direto: `/roteiro`
- ou peça em linguagem natural; a `description` dispara a skill.

O corpo da skill só carrega quando ela é usada; as referências são lidas sob demanda.

### Claude.ai / API

Compacte a pasta `skills/roteiro` em zip e envie em **Customize → Skills**, ou use o arquivo no fluxo da Skills API. O frontmatter usa apenas os campos do padrão (`name`, `description`), compatível com upload.

## Como usar

Peça em linguagem natural. Exemplos:

- "Quero escrever um longa sobre uma família que descobre um segredo do pai. Me ajuda a estruturar."
- "Meu roteiro tem 110 páginas e o Ato II não funciona. Diagnostica."
- "Transforma esta ideia em escaleta de série."
- "Revisa este episódio e me dá um parecer com prioridades."
- "Tenho uma entrevista de 40 minutos; como viro isso em documentário?"
- "Preciso de um roteiro de vídeo institucional de 90 segundos para uma cooperativa."
- "Meu vídeo do YouTube perde audiência no primeiro minuto. O que está errado?"

## Diagnóstico automático

```bash
python3 scripts/diagnostico.py meu_roteiro.fountain --formato longa
python3 scripts/diagnostico.py episodio.txt --formato serie -o relatorio.md
```

No Claude Code, use `${CLAUDE_SKILL_DIR}/scripts/diagnostico.py` para apontar para o script dentro da skill.

O script conta cenas, páginas estimadas, diálogo, personagens, distribuição por ato e sinaliza padrões suspeitos. **Não substitui leitura humana** — é um ponto de partida.

## Pacote

`dist/roteiro.skill` é um zip com `roteiro/SKILL.md` na raiz, no formato do `package_skill.py` oficial (anthropics/skills). Também é gerado `dist/roteiro.zip`, com o mesmo conteúdo.

O pacote **não inclui os PDFs** nem o texto extraído (`_extratos/`): esses ficam apenas neste diretório de trabalho, como fontes. No pacote instalado, `dist/` não existe — `SKILL.md`, `references/`, `assets/` e `scripts/` estão na raiz da skill.

Para regerar o pacote após editar a skill:

```bash
python3 scripts/empacotar.py
```

O script valida o frontmatter e as referências, cria a cópia limpa e os dois zips. Também pode ser validado pelo padrão:

```bash
npx -y skills-ref validate dist/roteiro
```

## Fontes

Os PDFs originais não são distribuídos (direitos autorais). A síntese está em `references/`; os limites de cada obra estão em `references/fontes.md`. Nenhum trecho protegido é reproduzido em extensão.

## Licença e uso

As referências bibliográficas são citadas para estudo. A skill é um material de trabalho; ajuste-a ao seu contexto de produção.
