# Links, revisões e proveniência

Índice das origens coletadas na fase 1 e das revisões inspecionadas na fase 2. Não confundir canal móvel, versão documental, release de software e revisão do silício. Os JSONs locais registram URL solicitada/final, horário, falhas e hashes; o índice não afirma uma nova consulta remota.

## Canais oficiais

- ESP-IDF: [stable](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/) · [latest](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/). A cópia stable declara v6.1.1; não é a v5.5.5 do firmware analisado (README §6).
- esptool: [latest / v5](https://docs.espressif.com/projects/esptool/en/latest/esp32/). A cópia não fixa patch; link de fonte registrado: `42265b9e`. Não se pressupõe um canal `stable` equivalente nem compatibilidade de todo recurso latest com todo v5.
- Hardware: [latest](https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32/index.html); erratas: [latest](https://docs.espressif.com/projects/esp-chip-errata/en/latest/esp32/index.html).
- Arduino-ESP32: [documentação stable](https://docs.espressif.com/projects/arduino-esp32/en/stable/) · [latest](https://docs.espressif.com/projects/arduino-esp32/en/latest/). Links de navegação; conteúdo desses dois canais não foi coletado nesta fase.

`stable` pode avançar e `latest/master` não é release congelado. Para reprodução, conservar PDFs/HTML locais e os commits dos repositórios, não apenas esses aliases.

## Revisões verificadas no conteúdo dos PDFs

Páginas físicas, contando a capa; não são datas HTTP nem versão do formato PDF.

| Documento local | Revisão / evidência |
|---|---|
| `espressif/esp32_datasheet_en.pdf` | v5.3, capa p.1; histórico p.70: 2026.07 |
| `espressif/esp32_technical_reference_manual_en.pdf` | v5.9, capa p.1 |
| `espressif/esp-chip-errata-en-master-esp32.pdf` | v3.1, capa p.1; não confundir com chip v3.1 |
| `espressif/esp-hardware-design-guidelines-en-master-esp32.pdf` | capa Release master, Nov 12 2026; histórico p.37 v1.9, 2025-09-17 |
| `espressif/esp32-wroom-32_datasheet_en.pdf` | v3.8, capa p.1, NRND; não identifica o módulo desta placa |
| `componentes/ST7789V.pdf` | v1.3, 2014/03, capa p.1 e histórico §11 p.316; variante V não comprova sufixo do chip instalado |
| `componentes/GT911_Datasheet.pdf` | Rev.09, March 11 2015, p.2 física/p.1 impressa; histórico §12 p.23 física/p.22 impressa |
| `componentes/IP5306.pdf` | V1.10 no rodapé p.1; conteúdo diz 2.1A charger/discharger, divergindo do título nos metadados PDF. Não converter metadado em especificação elétrica |
| `componentes/XPT2046-XPTEK.pdf` | modelo na p.1; revisão explícita não identificada na busca textual por marcadores de revisão; datas PDF/XMP não a substituem |

As três cópias de componentes ST7789V/GT911/IP5306 vieram de terceiros, não dos fabricantes do silício. XPT2046 pertence a variantes resistivas; o firmware desta placa identifica GT911 (README §8). A inclusão de IP5306 na coleção não prova que ele esteja nesta placa. Para os PDFs Mischianti, a revisão continua não estabelecida aqui; ano/mês da URL não a determina.

## ESP-IDF, chip e ferramentas: URLs originais e destinos

Fonte dos itens: registros Espressif (base local `esp32-docs/fontes/espressif/registros.json`, não publicada) e registros esptool (base local `esp32-docs/fontes/esptool/registros.json`, não publicada). Arquivos ficam sob `fontes/<grupo>/`; redirecionamentos são preservados, inclusive as URLs que falharam.

- `espressif/inicio.html` — original: <https://docs.espressif.com/projects/esp-idf/en/stable/esp32/>
- `espressif/hardware-reference.html` — original: <https://docs.espressif.com/projects/esp-idf/en/stable/esp32/hw-reference/index.html>
- `espressif/esp32_technical_reference_manual_en.pdf` — original: <https://www.espressif.com/sites/default/files/documentation/esp32_technical_reference_manual_en.pdf>; destino: <https://documentation.espressif.com/esp32_technical_reference_manual_en.pdf>
- `espressif/esp32_datasheet_en.pdf` — original: <https://espressif.com/sites/default/files/documentation/esp32_datasheet_en.pdf>; destino: <https://documentation.espressif.com/esp32_datasheet_en.pdf>
- `espressif/hardware-design-guidelines.html` — original: <https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32/index.html>
- `espressif/silicon-errata.html` — original: <https://docs.espressif.com/projects/esp-chip-errata/en/latest/esp32/index.html>
- `espressif/modules.html` — original: <https://espressif.com/en/products/modules?id=ESP32>; sem destino confirmado (consultar falha no registro)
- `espressif/esp-hardware-design-guidelines-en-master-esp32.pdf` — original: <https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32/esp-hardware-design-guidelines-en-master-esp32.pdf>
- `espressif/esp-chip-errata-en-master-esp32.pdf` — original: <https://docs.espressif.com/projects/esp-chip-errata/en/latest/esp32/esp-chip-errata-en-master-esp32.pdf>
- `espressif/related-documentation-and-resources.html` — original: <https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32/related-documentation-and-resources.html>
- `espressif/product-overview.html` — original: <https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32/product-overview.html>
- `espressif/revision-history.html` — original: <https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32/revision-history.html>
- `espressif/devkitc-discovery.html` — original: <https://documentation.espressif.com/esp-dev-kits/en/latest/esp32/esp32-devkitc/user_guide.html>
- `espressif/wroom32-search.html` — original: <https://www.espressif.com/en/search/node/esp32-wroom-32>; sem destino confirmado (consultar falha no registro)
- `espressif/esp32-wroom-32_datasheet_en.pdf` — original: <https://documentation.espressif.com/esp32-wroom-32_datasheet_en.pdf>
- `esptool/inicio.html` — original: <https://docs.espressif.com/projects/esptool/en/latest/esp32/>
- `esptool/advanced-topics.html` — original: <https://docs.espressif.com/projects/esptool/en/latest/esp32/advanced-topics/index.html>
- `esptool/troubleshooting.html` — original: <https://docs.espressif.com/projects/esptool/en/latest/esp32/troubleshooting.html>
- `esptool/migration-guide.html` — original: <https://docs.espressif.com/projects/esptool/en/latest/esp32/migration-guide.html>
- `esptool/esptool-index.html` — original: <https://docs.espressif.com/projects/esptool/en/latest/esp32/esptool/index.html>
- `esptool/boot-mode-selection.html` — original: <https://docs.espressif.com/projects/esptool/en/latest/esp32/advanced-topics/boot-mode-selection.html>
- `esptool/basic-commands.html` — original: <https://docs.espressif.com/projects/esptool/en/latest/esp32/esptool/basic-commands.html>
- `esptool/advanced-commands.html` — original: <https://docs.espressif.com/projects/esptool/en/latest/esp32/esptool/advanced-commands.html>
- `esptool/advanced-options.html` — original: <https://docs.espressif.com/projects/esptool/en/latest/esp32/esptool/advanced-options.html>

## Componentes: fabricante, cópia e descoberta

Fonte: registros componentes (base local `esp32-docs/fontes/componentes/registros.json`, não publicada). A cópia pública não implica autorização de redistribuição irrestrita; consultar os avisos de cada documento.

### ST7789

- Fabricante: Sitronix; origem efetiva: Newhaven Display (`fabricante_de_displays_copia_de_datasheet_de_terceiro`).
- PDF original solicitado: <https://newhavendisplay.com/content/datasheets/ST7789V.pdf>; [cópia local](https://newhavendisplay.com/content/datasheets/ST7789V.pdf).
- Descoberta/catálogo: <https://www.sitronix.com.tw/en/products/aiot-device-ddi/>.
- Limite registrado: Documento da variante ST7789V, não confirmação de equivalência ao ST7789 sem sufixo nem identificação do silício da placa. Datasheet público não localizado no fabricante Sitronix.

### XPT2046

- Fabricante: XPTEK; origem efetiva: XPTEK (`fabricante`).
- PDF original solicitado: <http://www.xptek.com.cn/uploadfile/download/201707171401161883.pdf>; [cópia local](http://www.xptek.com.cn/uploadfile/download/201707171401161883.pdf).
- Descoberta/catálogo: <http://www.xptek.com.cn/>.
- Descoberta/catálogo: <http://www.xptek.com.cn/cn/productview.asp?id=326>.
- Limite registrado: Link de manual/datasheet indicado pela página oficial XPT2046; HTTP sem TLS no endereço publicado. Divergência preservada: ModDate PDF=2017-07-17T12:18:06Z, ModifyDate XMP=2011-12-06T09:46:28+08:00; nenhuma convertida em revisão.

### GT911

- Fabricante: Goodix; origem efetiva: FORTEC Integrated (`distribuidor_integrador_de_displays_copia_de_terceiro`).
- PDF original solicitado: <https://www.fortec-integrated.de/fileadmin/pdf/produkte/Touchcontroller/DDGroup/GT911_Datasheet.pdf>; [cópia local](https://www.fortec-integrated.de/fileadmin/pdf/produkte/Touchcontroller/DDGroup/GT911_Datasheet.pdf).
- Descoberta/catálogo: <https://www.goodix.com/en/product/touch/touch_screen_controller>.
- Descoberta/catálogo: <https://www.crystalfontz.com/controllers/GOODIX/GT911>.
- Limite registrado: Catálogo oficial Goodix localizado; PDF público do fabricante não localizado. Crystalfontz recusou HTTP 403; usada cópia do integrador/distribuidor FORTEC.

### IP5306

- Fabricante: Injoinic; origem efetiva: Electrokit (`distribuidor_de_eletronica_copia_de_terceiro`).
- PDF original solicitado: <https://www.electrokit.com/upload/quick/12/91/662c_IP5306.pdf>; [cópia local](https://www.electrokit.com/upload/quick/12/91/662c_IP5306.pdf).
- Descoberta/catálogo: <https://www.injoinic.com/>.
- Descoberta/catálogo: <https://www.injoinic.com/product>.
- Limite registrado: PDF público do fabricante não localizado na busca e catálogo consultados. Não substituído por IP5356H/IP5506/IP5566 retornados na busca. Variante/revisão exata pendente da fase 2. Alerta de metadados: título PDF menciona 1.2A/1A, diferente do título comercial/indexado 2.1A/2.1A; conteúdo/modelo/revisão não validados nesta fase. Não usar parâmetros elétricos sem conferência na fase 2.

## Mischianti: originais da placa

Fonte: registros Mischianti (base local `esp32-docs/fontes/mischianti/registros.json`, não publicada). Material de terceiro sobre a família; não substitui a identificação da unidade nem resolve automaticamente variantes C/R/N.

- [ESP32-2432S032_Schematics.pdf](https://mischianti.org/wp-content/uploads/2025/05/ESP32-2432S032_Schematics.pdf) — <https://mischianti.org/wp-content/uploads/2025/05/ESP32-2432S032_Schematics.pdf>.
- [ESP32-2432S032.Specifications-EN.pdf](https://mischianti.org/wp-content/uploads/2025/05/ESP32-2432S032.Specifications-EN.pdf) — <https://mischianti.org/wp-content/uploads/2025/05/ESP32-2432S032.Specifications-EN.pdf>.
- [ESP32-2432S032-ST7789-touch-Cheap-Yellow-Display-pinout-high.png](https://mischianti.org/wp-content/uploads/2025/05/ESP32-2432S032-ST7789-touch-Cheap-Yellow-Display-pinout-high.png) — <https://mischianti.org/wp-content/uploads/2025/05/ESP32-2432S032-ST7789-touch-Cheap-Yellow-Display-pinout-high.png>.

## Repositórios e releases

Fonte: registros Git/release (base local `esp32-docs/fontes/repositorios/registros.json`, não publicada) e manifesto parcial (base local `esp32-docs/fontes/repositorios/MANIFESTO-parte.md`, não publicada). Commits abaixo identificam o checkout local; não são tags de release. Clone raso, sem submódulos inicializados e sem download LFS: os inventários explicitam esses limites.

- **witnessmenow/ESP32-Cheap-Yellow-Display** — original clone: <https://github.com/witnessmenow/ESP32-Cheap-Yellow-Display.git>; [snapshot](https://github.com/witnessmenow/ESP32-Cheap-Yellow-Display/tree/0564a140c76de76ef34a8b7115044e7c6c852695); local `fontes/repositorios/witnessmenow__ESP32-Cheap-Yellow-Display/`; commit `0564a140c76de76ef34a8b7115044e7c6c852695`.
- **rzeldent/esp32-smartdisplay** — original clone: <https://github.com/rzeldent/esp32-smartdisplay.git>; [snapshot](https://github.com/rzeldent/esp32-smartdisplay/tree/38e9ebabe3e4044159c4e95192d432607ed70588); local `fontes/repositorios/rzeldent__esp32-smartdisplay/`; commit `38e9ebabe3e4044159c4e95192d432607ed70588`.
- **MatthiasNeuhaus/platformio-espressif32-sunton** — original clone: <https://github.com/MatthiasNeuhaus/platformio-espressif32-sunton.git>; [snapshot](https://github.com/MatthiasNeuhaus/platformio-espressif32-sunton/tree/216215c270c09900b14eb0f9e140d98c40717a00); local `fontes/repositorios/MatthiasNeuhaus__platformio-espressif32-sunton/`; commit `216215c270c09900b14eb0f9e140d98c40717a00`.
- **Bodmer/TFT_eSPI** — original clone: <https://github.com/Bodmer/TFT_eSPI.git>; [snapshot](https://github.com/Bodmer/TFT_eSPI/tree/16e37595040eac69cd628e4bffb56fc30cad6299); local `fontes/repositorios/Bodmer__TFT_eSPI/`; commit `16e37595040eac69cd628e4bffb56fc30cad6299`.
- **espressif/arduino-esp32** — original clone: <https://github.com/espressif/arduino-esp32.git>; [snapshot](https://github.com/espressif/arduino-esp32/tree/58531a10123010af0b60921e7b537f77bfe032a0); local `fontes/repositorios/espressif__arduino-esp32/`; commit `58531a10123010af0b60921e7b537f77bfe032a0`.
- **lvgl/lvgl** — original clone: <https://github.com/lvgl/lvgl.git>; [snapshot](https://github.com/lvgl/lvgl/tree/ab2a8b4ba503917ede0769ce9d5b254ca0b8f37d); local `fontes/repositorios/lvgl__lvgl/`; commit `ab2a8b4ba503917ede0769ce9d5b254ca0b8f37d`.

Consultas de releases/latest da fase 1 (não atualizadas aqui; latest do GitHub não é HEAD nem pré-release):

- `witnessmenow/ESP32-Cheap-Yellow-Display` — API original: <https://api.github.com/repos/witnessmenow/ESP32-Cheap-Yellow-Display/releases/latest>; HTTP 404: nenhuma release retornada nessa consulta; isso não significa repositório inexistente.
- `rzeldent/esp32-smartdisplay` — API original: <https://api.github.com/repos/rzeldent/esp32-smartdisplay/releases/latest>; release [2.1.0](https://github.com/rzeldent/esp32-smartdisplay/releases/tag/2.1.0).
- `MatthiasNeuhaus/platformio-espressif32-sunton` — API original: <https://api.github.com/repos/MatthiasNeuhaus/platformio-espressif32-sunton/releases/latest>; HTTP 404: nenhuma release retornada nessa consulta; isso não significa repositório inexistente.
- `Bodmer/TFT_eSPI` — API original: <https://api.github.com/repos/Bodmer/TFT_eSPI/releases/latest>; release [V2.5.43](https://github.com/Bodmer/TFT_eSPI/releases/tag/V2.5.43).
- `espressif/arduino-esp32` — API original: <https://api.github.com/repos/espressif/arduino-esp32/releases/latest>; release [4.0.0](https://github.com/espressif/arduino-esp32/releases/tag/4.0.0).
- `lvgl/lvgl` — API original: <https://api.github.com/repos/lvgl/lvgl/releases/latest>; release [v9.6.0](https://github.com/lvgl/lvgl/releases/tag/v9.6.0).
- `espressif/esp-idf` — API original: <https://api.github.com/repos/espressif/esp-idf/releases/latest>; release [v6.1.1](https://github.com/espressif/esp-idf/releases/tag/v6.1.1).
- `lovyan03/LovyanGFX` — API original: <https://api.github.com/repos/lovyan03/LovyanGFX/releases/latest>; release [1.3.0](https://github.com/lovyan03/LovyanGFX/releases/tag/1.3.0).

A fonte de pinagem citada no README é outra origem e deve permanecer identificada: <https://github.com/rzeldent/platformio-espressif32-sunton/blob/main/esp32-2432S032C.json>. Não substituir silenciosamente por MatthiasNeuhaus nem apresentar uma como checkout da outra.

## Leituras locais recomendadas

- [Identificação e evidência da unidade](relatorio-unidade.md): §§1–4 USB/chip/memória/segurança, §§7–9 tela/touch/pinos, §11 conexão medida.
- [Chip ESP32](chip-esp32.md): fontes por página/seção e limites de aplicação à placa.
- [Gravação no macOS](gravacao-macos.md): exemplos v5 não executados e operações perigosas separadas.
- Manifesto agregado (base local `esp32-docs/fontes/MANIFESTO.md`, não publicada): coleta/integridade; versões inicialmente nulas não foram retroativamente alteradas nesta fase.

Não confundir atualização de biblioteca com compatibilidade do projeto: LVGL, Arduino core, TFT_eSPI e smartdisplay têm interfaces/versionamentos independentes. Os links de releases são inventário, não recomendação de upgrade ou instalação.
