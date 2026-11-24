# Versões, dependências e limites de compatibilidade

## Escopo e autoridade

Consulta preservada em **24/11/2026 UTC** (23/11 no horário local da coleta).
**Não houve instalação, compilação, upload nem teste de execução nesta fase.**
“Declarado” abaixo significa evidência na fonte, não uma combinação validada nesta placa.

O [`README.md`](relatorio-unidade.md), §§3, 6–8, é a autoridade local: ESP32-D0WD-V3,
flash de 4 MB, ausência de PSRAM **inferida**, ST7789 240×320 em retrato e GT911.
O firmware analisado usa Arduino **3.3.12 / IDF 5.5.5 / TFT_eSPI**, sem LVGL ou
LovyanGFX. Isso documenta o binário existente, não comprova novo build nem touch funcional.
320×240 nas receitas LVGL significa **paisagem a configurar**, não a orientação já constatada.

## Releases observadas versus código coletado

As versões da coluna release vêm de `fontes/repositorios/releases/<nome>.latest.json`,
campos `tag_name`, `published_at`, `prerelease`, `name` e `body` [R].
`target_commitish: master` não é um SHA da release; não o usar como pin imutável.

| Projeto / nome do JSON | Última release estável retornada | Publicação UTC | O que existe nas fontes |
|---|---|---|---|
| Arduino-ESP32 / `espressif__arduino-esp32` | **4.0.0**, baseada em IDF **6.1.1** | 2026-11-19 | HEAD [A] declara 4.0.0; isso não prova identidade com a tag |
| ESP-IDF / `espressif__esp-idf` | **v6.1.1** | 2026-11-16 | Sem clone integral; release JSON, README versionado e snapshot `stable` [I] |
| LVGL / `lvgl__lvgl` | **v9.6.0** | 2026-09-16 | HEAD [L] já declara **10.0.0-dev**; suplementos separam 8.4.0 e 9.6.0 |
| TFT_eSPI / `Bodmer__TFT_eSPI` | **V2.5.43** | 2024-03-06 | HEAD [T]: `library.properties` = **2.5.44**, mas `library.json` = **2.5.43** |
| LovyanGFX / `lovyan03__LovyanGFX` | **1.3.0** | 2026-11-06 | Sem clone integral; arquivos da tag resolvida por commit [G] |
| esp32-smartdisplay / `rzeldent__esp32-smartdisplay` | **2.1.0** | 2024-11-16 | HEAD [S]: `library.json` = **2.1.2**, dependência `lvgl/lvgl: ^9.3.0` |
| CYD / `witnessmenow__ESP32-Cheap-Yellow-Display` | API `releases/latest`: **404** | — | Clone documental [C]; 404 não significa ausência de tags |
| Sunton / `MatthiasNeuhaus__platformio-espressif32-sunton` | API `releases/latest`: **404** | — | Clone de definições [B]; não é a mesma origem do submódulo rzeldent |

**Não chamar Arduino 3.x de “última versão” nem LVGL HEAD de “LVGL 9”.**
A documentação `stable` do IDF e GitHub `releases/latest` concordaram em **v6.1.1**:
HTML preservado [I], `<title>` e `DOCUMENTATION_OPTIONS.RELEASE`. `stable` é alias móvel;
IDF 5.5.5 do binário local é outra linha, não o significado atual desse alias.

### Conferência das notas de mudança

- **Arduino:** [A], `docs/en/migration_guides/2.x_to_3.0.rst`, “Introduction”,
  “LEDC” e “Timer”: 2.x parte de IDF 4.4; **3.0** parte de IDF **5.1**.
  Remove `ledcSetup`/`ledcAttachPin`, introduz `ledcAttach`; APIs de timers mudam.
  Não extrapolar “3.0 = IDF 5.1” a todo 3.x: a release **3.3.12** usa **5.5.5** [H].
  A release **2.0.17** usa **4.4.7** [H]. São pontos históricos identificados,
  não uma afirmação sobre qual é o último patch mantido de cada linha.
- **LVGL:** [L], `docs/src/changelog/CHANGELOG.mdx`, “v9.6.0 (16 September 2026)”,
  chama 9.6.0 de última release v9 e registra depreciações para v10.
  O cabeçalho `include/lvgl/lv_version.h` em HEAD já é 10.0.0-dev;
  `library.json` ainda diz 9.6.0. Os exemplos desta referência usam os suplementos
  versionados, não inferem API pela versão do manifesto desatualizado [V8, V9].
- **TFT_eSPI:** [T], `README.md`, “News”, item 1: o autor relata DMA do **ESP32-S3**
  testado com pacote Arduino **3.3.6**. A frase anterior mistura “ESP-IDF” com
  “2.0.14”; não tratá-la como mapeamento de versões IDF. Também não é um teste do
  ESP32 clássico desta placa nem garantia para release V2.5.43.
- **smartdisplay:** [S], `README.md`, “Version history”: novembro/2024 indica
  **2.1.0 / LVGL 9.2.2**; setembro/2025 indica **2.1.2 / LVGL 9.3.0**, com nota
  de remoção de DMA por problemas em algumas placas. O JSON da release 2.1.0 diz
  apenas “Upgrade to LVGL 9.2.”. “Dependencies” ainda cita 9.1.0; para o HEAD,
  usar `library.json` e ler o código, não essa frase antiga.
- **LovyanGFX:** [R], JSON próprio, “Breaking changes”, “SPI / DMA” e “Fixes”:
  1.3.0 altera vida útil de buffers assíncronos e layouts de objetos e contém
  ajustes para IDF 6.1. Não transportar otimizações de PSRAM de S3/C5/P4 para D0WD.
- **IDF:** [R], JSON próprio, “Major changes” / “Breaking changes”: 6.1.1 é
  correção da linha 6.1, mas há alterações de API; “patch” não dispensa leitura.

## Matriz de integração — não é certificado de compatibilidade

Legenda: **adaptador** = é preciso ligar display/touch/tick à API LVGL escolhida;
**declarado** = upstream cita o ambiente; **NV** = combinação exata não verificada.
LVGL é a UI; TFT_eSPI/LovyanGFX são alternativas de driver. smartdisplay já fornece
outra integração por `esp_lcd`; não empilhar os três inicializadores no mesmo painel [S].

| Ambiente | LVGL 8 | LVGL 9 | TFT_eSPI | LovyanGFX | esp32-smartdisplay |
|---|---|---|---|---|---|
| Arduino 2.x / IDF 4.4; ponto 2.0.17/4.4.7 [A,H] | API v8 + adaptador [V8] | API v9 + adaptador [V9]; build NV | Manifesto declara Arduino [T]; pin exato e build NV | Declara Arduino [G]; versão/core exatos NV | HEAD não promete esta combinação; usa APIs `esp_lcd`, LVGL ^9.3.0 [S]; NV |
| Arduino 3.0 / IDF 5.1 [A] | API v8 + adaptador, revisar timer/LEDC [A,V8] | API v9 + adaptador [V9] | Migração do core precisa revisão; não aplicar garantia do S3/3.3.6 [T] | Declara Arduino, sem certificar todos 3.x [G] | Arduino declarado; core não fixado em `library.json` [S]; NV |
| Arduino 3.3.12 / IDF 5.5.5 [H] | Não presente no firmware local; novo build NV | Não presente no firmware local; novo build NV | Presente no binário local [README §6]; versão da biblioteca não identificada | Ausente no binário local; candidato, não teste [G] | Ausente no binário local; combinação NV [S] |
| ESP-IDF nativo (sem Arduino) | Portar display, touch e tempo [V8] | Portar display, touch e tempo [V9] | Manifesto só declara Arduino; não é receita de IDF nativo [T] | Declara `espidf`, README aborda integração [G]; build exato NV | `frameworks: arduino`; não equivale a componente IDF nativo [S] |
| Arduino 4.0.0 / IDF 6.1.1 [R] | Dependências e port precisam build novo | Dependências e port precisam build novo | NV nesta coleta | Release contém ajustes IDF 6.1 [R], mas placa/core juntos NV | `^9.3.0` não resolve mudanças do core; NV |

**Separação v8/v9:** v8 usa `lv_disp_drv_t`/`lv_indev_drv_t` e tamanho do draw buffer
em **pixels**; v9 usa `lv_display_t`/`lv_indev_t` e `lv_display_set_buffers` em
**bytes**. Trocar só o número no gerenciador não migra o código [V8,V9].
Nem todo 9.x tem configuração idêntica: o template **9.6.0** usa
`LV_COLOR_FORMAT_DEFAULT`; o README smartdisplay orientado a 9.3.0 ainda ensina
`LV_COLOR_DEPTH 16`. Ver [lvgl.md](lvgl.md), sem copiar o template de HEAD v10.

### Decisão prática e limites

1. Para preservar o caminho do binário existente, partir da configuração local
   TFT_eSPI e Arduino 3.3.12, mas só declarar reproduzido depois de compilar/testar.
2. Para UI nova, fixar uma major LVGL e o adaptador correspondente. Para reproduzir
   smartdisplay, registrar SHA + versão **resolvida** do LVGL: `^9.3.0` não fixa patch
   nem minor. Não presumir que 9.6.0 foi validado com esse HEAD [S].
3. Para IDF nativo, usar port LVGL próprio ou driver que declare IDF; não chamar a
   versão IDF embutida no Arduino de SDK livremente substituível [A,G].
4. Registrar core, IDF, biblioteca, template `lv_conf.h`, flags, definição de placa
   e SHA. O build/hardware continua **NV** até prova real; nenhum conjunto foi compilado aqui.

## Fontes locais e commits (identificadores usados acima)

Todos os caminhos de repositório abaixo partem de `fontes/repositorios/`.
As fontes extras e seus URLs exatos, tamanho, instante UTC e SHA-256 estão em
`suplementos/MANIFESTO-parte.md` (base local `esp32-docs/fontes/repositorios/suplementos/MANIFESTO-parte.md`, não publicada).
Os links versionados efetivamente usados nos downloads estão preservados ali.

- **[R]** `releases/*.latest.json` e `MANIFESTO-parte.md`, §§“GitHub API releases/latest”
  e “Método e limites”. São snapshots de API, **sem commit Git próprio**;
  `registros.json` / `metadados/*.release.json` guardam proveniência da fase 1.
- **[A]** `espressif__arduino-esp32/` @ `58531a10123010af0b60921e7b537f77bfe032a0`:
  `cores/esp32/esp_arduino_version.h`; `docs/en/migration_guides/2.x_to_3.0.rst`.
- **[L]** `lvgl__lvgl/` @ `ab2a8b4ba503917ede0769ce9d5b254ca0b8f37d`:
  `include/lvgl/lv_version.h`, `library.json`, `docs/src/changelog/CHANGELOG.mdx`.
- **[T]** `Bodmer__TFT_eSPI/` @ `16e37595040eac69cd628e4bffb56fc30cad6299`:
  `README.md` (“News”), `library.properties`, `library.json` (“version”, “frameworks”).
- **[S]** `rzeldent__esp32-smartdisplay/` @ `38e9ebabe3e4044159c4e95192d432607ed70588`:
  `README.md` (“Dependencies”, “Version history”), `library.json`,
  `src/lvgl_panel_st7789_spi.c` e `include/lvgl_panel_common.h` (integração `esp_lcd`).
- **[G]** LovyanGFX 1.3.0 @ `dd228d15a03900ce658fd62e120dc7cc489915dd`:
  `suplementos/lovyan03__LovyanGFX__library.json` e `...__README.md`,
  “Supported platforms” e seção sobre Arduino como componente ESP-IDF.
- **[I]** IDF v6.1.1 @ `051e4c4eb20346e043cdd47bc388fde75ff8af63`:
  `suplementos/espressif__esp-idf__README.md` (“ESP-IDF”),
  `suplementos/espressif__esp-idf__v6.1.1__commit.json`;
  `suplementos/esp-idf__stable__esp32.html` é snapshot HTTP **sem commit próprio**.
- **[H]** `suplementos/espressif__arduino-esp32__2.0.17__release.json` e
  `...__3.3.12__release.json`: `name`/`body`, snapshots de releases por tag,
  **sem SHA de checkout atribuído**; não houve clone dessas duas tags.
- **[V8]** LVGL v8.4.0 @ `4495f428630cc1741bd8bfd977f080e8460e8e8d`:
  `suplementos/lvgl__lvgl__docs__porting__display.md`, `...__indev.md`,
  `...__tick.md`, `...__timer-handler.md`, `lvgl__lvgl__lv_conf_template.h`.
- **[V9]** LVGL v9.6.0 @ `80ca777e37a2b176770726a02e07a6fb79ef0b39`:
  `suplementos/lvgl__v9.6.0__lv_conf_template.h`, `...__include__lvgl__lv_version.h`,
  `...__docs__src__main-modules__display__setup.mdx`,
  `...__docs__src__integration__overview.mdx`.
- **[C]** `witnessmenow__ESP32-Cheap-Yellow-Display/` @
  `0564a140c76de76ef34a8b7115044e7c6c852695` (documentação, não release de framework).
- **[B]** `MatthiasNeuhaus__platformio-espressif32-sunton/` @
  `216215c270c09900b14eb0f9e140d98c40717a00` (definições coletadas; não medir hardware por elas).
