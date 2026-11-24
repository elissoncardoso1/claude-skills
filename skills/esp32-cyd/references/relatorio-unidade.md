# Ficha técnica: ESP32-2432S032C ("Cheap Yellow Display" 3,2", touch capacitivo)

Levantamento feito em 2026-11-23 só com leitura (esptool/espefuse em modo leitura, dump da flash e análise estática). Nada foi gravado na placa.

**Níveis:** **[C]** CONFIRMADO (medido, string ou disassembly inequívoco, ou informado pelo dono) · **[I]** INFERIDO (evidência indireta ou documentação pública, com a fonte citada) · **[NV]** NÃO VERIFICADO.

> ⚠️ **A flash não tem mais o firmware de fábrica.** O app gravado é um sketch Arduino chamado **"AI DOCK"**, compilado em
> 16/set/2026 a partir de `~/Arduino/...` (core 3.3.12 + TFT_eSPI). NVS, app1 e SPIFFS estão 100% em 0xFF, então a flash
> foi apagada antes da gravação. Não existe cópia do firmware original. Esse sketch foi a fonte das respostas abaixo: ele mostra a configuração
> de tela e touch que alguém usou com esta placa. Se você tiver o código-fonte dele em outra máquina, ele confirma tudo o que está aqui.

## 1. USB

| Item | Valor | Nível | Evidência |
|---|---|---|---|
| Cabo | USB-C é a única ligação (energia + dados) | [C] | dono da placa |
| Tipo de ligação | **Ponte USB-serial**, não é USB nativo | [C] | ioreg: `USB Serial`, idVendor 6790 = **0x1A86** (WCH) |
| Chip da ponte | WCH CH340 (PID **0x7523**, bcdDevice 0x0264) | [C] / variante exata (CH340C/G…) [NV] | `logs/01_ioreg_usb.txt`, `01_ioreg_ch340_detail.txt` |
| Porta | `/dev/cu.usbserial-11220` | [C] | IOCalloutDevice. O sufixo vem do locationID (hub Anker); muda se trocar de porta/hub |
| Driver macOS | Nativo da Apple (DriverKit `com.apple.DriverKit-AppleUSBCHCOM`); **nenhum driver extra** | [C] | IOMatchedPersonality |
| Comportamento no reset | Porta **não some** no reset (a ponte fica sempre enumerada) | [C] | vários resets via RTS sem a porta mudar |
| `/dev/cu.usbmodemSN234567892` | **Não** é a placa (é o "BillBoard" do hub) | [C] | ioreg |

## 2. Chip

| Item | Valor | Nível | Evidência |
|---|---|---|---|
| SoC | **ESP32-D0WD-V3, revisão v3.1** | [C] | `02_chip-id.txt` |
| Núcleos / frequência | Dual core, 240 MHz (CHIP_CPU_FREQ_RATED=1, FREQ_LOW=0) | [C] | chip-id + espefuse |
| Cristal | 40 MHz | [C] | chip-id |
| MAC (Wi-Fi STA) | xx:xx:xx:xx:xx:xx (ocultado) (CRC OK) | [C] | read-mac / espefuse |
| Wi-Fi / BT | Presentes, não desabilitados por eFuse | [C] | espefuse DISABLE_BT=False |
| Pacote | CHIP_PACKAGE=1 (D0WD) | [C] | espefuse |
| ADC Vref | 1142 mV em eFuse | [C] | espefuse |

## 3. Memória

| Item | Valor | Nível | Evidência |
|---|---|---|---|
| Flash | **4 MB**, fabricante JEDEC **0x5E**, device 0x4016 | [C] | `02_flash-id.txt` |
| Fabricante da flash | 0x5E = Zbit Semiconductor (ex.: ZB25VQ32) | [I] | tabela JEDEC; não há marcação lida no chip |
| Modo / freq. da flash | **DIO, 80 MHz** | [C] | cabeçalhos do bootloader/app + boot log `mode:DIO, clock div:1` |
| Tensão da flash | 3,3 V (GPIO12 no strap, sem eFuse XPD_SDIO_FORCE) | [C] | flash-id/espefuse |
| PSRAM | **Ausente** | [I] | o D0WD-V3 não tem PSRAM interna; GPIO16/17 (que uma PSRAM externa usaria) vão para o LED RGB [I-fonte pública]. O boot log do app não sai na serial, então não deu para medir. |

## 4. Segurança

| Item | Valor | Nível |
|---|---|---|
| Secure Boot v1/v2 | Desativado (ABS_DONE_0/1 = False, BLOCK2 zerado) | [C] |
| Flash Encryption | Desativado (FLASH_CRYPT_CNT = 0, BLOCK1 zerado), então o dump está em texto claro | [C] |
| JTAG | Habilitado (JTAG_DISABLE = False) | [C] |
| Download UART | Habilitado | [C] |
| eFuses gravados além de fábrica | Nenhum (WR_DIS=0, RD_DIS=0, BLOCK3 zerado) | [C] |
| `get-security-info` | Não suportado no ROM do ESP32 clássico (erro FF00); por isso usei `espefuse summary` | [C] |

## 5. Partições (`logs/04_partition_table.txt`)

| Nome | Tipo | Offset | Tamanho | Conteúdo no dump |
|---|---|---|---|---|
| nvs | data/nvs | 0x9000 | 20 KB | vazio (0xFF) |
| otadata | data/ota | 0xE000 | 8 KB | seq=1, então **app0** está ativa |
| app0 | app/ota_0 | 0x10000 | 1280 KB | sketch "AI DOCK" (≈353 KB) |
| app1 | app/ota_1 | 0x150000 | 1280 KB | vazio |
| spiffs | data/spiffs | 0x290000 | 1408 KB | vazio |
| coredump | data/coredump | 0x3F0000 | 64 KB | — |

Layout idêntico ao `default.csv` do core Arduino-ESP32 [C]. Bootloader em 0x1000: ESP-IDF v5.5.5, compilado em 16/set/2026 21:39:25 [C].

## 6. Firmware gravado (`logs/04_image-info.txt`, `04_strings_app0.txt`)

| Item | Valor | Nível |
|---|---|---|
| Projeto (cabeçalho) | `arduino-lib-builder`, versão `6671d0b` (padrão de todo sketch Arduino-ESP32 3.x) | [C] |
| Nome do sketch | "* A I   D O C K *" (título na tela), strings `claude`, `BTN:`, `DBG touch %u %u`, `TOUCH FAIL` | [C] |
| Core | Arduino-ESP32 **3.3.12**, ESP-IDF **v5.5.5**, FQBN `esp32:esp32:esp32` | [C] |
| Compilação | 16/set/2026 21:15:45, em `/home/<usuário>/...` (Linux) | [C] |
| Bibliotecas | **TFT_eSPI** (`TFT_eSPI_ESP32.c`), **Wire** (I2C master). **Não há** LVGL, LovyanGFX, Arduino_GFX, XPT2046 nem SD | [C] presença / [C] ausência por busca de strings |
| Saída serial do app | Nenhuma no boot (só o ROM/bootloader escrevem); `DBG touch` só aparece ao tocar | [C] |
| Firmware de fábrica | Não está presente | [C] |

## 7. Tela: respostas a), b), d)

| Item | Valor | Nível | Evidência |
|---|---|---|---|
| a) Controlador | **ST7789** | [C] | `logs/04_tft_init_sequence.txt`: TFT_eSPI::init envia 01, 11, 13, 36=08, B6, 3A=55, **B2** 0C 0C 00 33 33, **B7**=35, **BB**=28, C0, C2, C3, C4, C6, **D0** A4 A1, E0/E1, 21, 2A, 2B, 29, que é a sequência do `ST7789_Init.h` do TFT_eSPI (o ILI9341 usa EF/CF/ED/E8/CB/F7) |
| b) Resolução | **240 × 320** | [C] | construtor `TFT_eSPI(240, 320)` @0x400d1afc; CASET 0..0x00EF, RASET 0..0x013F |
| Compatível com 3,2"? | Sim: 240×320 é o padrão em painéis de 2,8" a 3,2" | [I] |
| b) Orientação usada | `setRotation(0)`: **retrato**; texto centralizado em x=120 | [C] | @0x400d1cdd `setRotation(tft, 0)`; `drawCentreString("AI DOCK",120,30)`, `("TOUCH FAIL",120,310)` |
| Ordem de cor | BGR (MADCTL 0x08 na init) | [I] | só a constante foi observada; precisa ser validada com cor real |
| Inversão | INVON (0x21) enviado na init | [C] |
| Tipo de painel | IPS | [I] | `DISPLAY_IPS` em rzeldent/esp32-2432S032C.json |
| d) Bibliotecas | TFT_eSPI; sem LVGL | [C] | strings |

## 8. Touch: resposta c)

| Item | Valor | Nível | Evidência |
|---|---|---|---|
| Controlador | **GT911 (capacitivo)** | [C] | rotina @0x400d1b44: `beginTransmission(0x5D)`, endereço de registrador em 16 bits (MSB, LSB); leitura de **0x8140** (Product ID "911", 4 bytes) no setup; leitura e zeragem de **0x814E** (status de toque) no loop. Ver `logs/04_disasm_setup_touch.txt` |
| Barramento | **I2C** | [C] | `Wire.begin(sda=33, scl=32, freq=0)` @0x400d1cf3; driver `i2c.master` |
| Endereço I2C | **0x5D** | [C] | `movi.n a11, 0x5d` |
| SDA / SCL | **GPIO33 / GPIO32** | [C] | args do Wire.begin |
| INT / RST | GPIO21 / GPIO25 | [I] | rzeldent esp32-2432S032C.json; o sketch não usa esses pinos |
| Resistivo (XPT2046)? | Não | [C] | ausência de strings/código XPT2046, presença do GT911 |
| Funciona? | [NV] | — | o sketch tem um caminho `TOUCH FAIL` para quando o Product ID não bate; não sabemos qual caminho rodou |

## 9. Periféricos e pinagem: resposta e)

| Função | GPIO | Nível | Evidência |
|---|---|---|---|
| TFT SCLK | 14 | [C] | `SPIClass::begin(14, 12, 13, -1)` @0x400d42b5 |
| TFT MOSI | 13 | [C] | idem |
| TFT MISO | 12 | [C] | idem (atenção: GPIO12 é strap da tensão da flash; precisa estar baixo no boot) |
| TFT CS | 15 | [C] | `pinMode(15,OUTPUT)` @0x400d42c9 |
| TFT DC | 2 | [C] | `pinMode(2,OUTPUT)` @0x400d42d7 |
| TFT RST | nenhum (reset por SW) | [C] | sem pinMode de reset; `ST7789_DEV_CONFIG_RESET=NC` [I] |
| Backlight | 27, ativo em HIGH | [C] | `pinMode(27)`+`digitalWrite(27,1)` @0x400d1cc4 e @0x400d464a |
| SPI clock da tela | 40 MHz | [C] | literal 40000000 @0x400d3f92 |
| Touch SDA / SCL | 33 / 32 | [C] | §8 |
| Touch INT / RST | 21 / 25 | [I] | rzeldent JSON |
| Cartão SD (CS/SCK/MOSI/MISO) | 5 / 18 / 23 / 19 | [I] | rzeldent JSON (`TF_*`) |
| LED RGB (R/G/B) | 4 / 16 / 17 | [I] | rzeldent JSON (`RGB_LED_*`); polaridade [NV] (em CYDs costuma ser ativo em LOW, não confirmado) |
| LDR (CdS) | 34 (só entrada/ADC) | [I] | rzeldent JSON (`CDS`) |
| Áudio / alto-falante | 26 (DAC2) | [I] | rzeldent JSON (`SPEAK`) |
| Conectores extras (P3/CN1) | [NV] | — | não constam na fonte nem no firmware; exige foto da placa |

Fonte pública: <https://github.com/rzeldent/platformio-espressif32-sunton/blob/main/esp32-2432S032C.json>. Cópia dos valores em `logs/05_fonte_publica_pinagem.txt`.

## 10. Identificação comercial

**Modelo provável: Sunton ESP32-2432S032C** (CYD 3,2", touch capacitivo GT911). Confiança **alta**:
ST7789 240×320, GT911 em 0x5D com SDA33/SCL32, backlight 27, SPI 14/13/12, CS15 e DC2 **coincidem exatamente** com a definição pública
da 2432S032C (as variantes R/N usariam XPT2046 ou nenhum touch). Somam-se a tela de 3,2" informada pelo dono, ESP32-D0WD-V3, 4 MB e CH340.
O que não dá para separar sem olhar a placa: a revisão do PCB e a variante USB-C vs micro-USB do mesmo modelo. Se quiser fechar 100%, mande uma foto do verso.

## 11. Como conectar e gravar no macOS via USB-C

| Item | Valor |
|---|---|
| Porta | `/dev/cu.usbserial-11220` (use sempre `cu.`, não `tty.`). Para achar: `ls /dev/cu.usbserial-*` |
| Driver | nenhum: o macOS já traz o AppleUSBCHCOM |
| Velocidade | **115200** comprovada (4 MB lidos sem erro). A 460800 a leitura falhou com "Corrupt data" através do hub Anker; teste 460800/921600 ligando direto no Mac |
| Modo de gravação | **Automático** (DTR/RTS → GPIO0/EN). Todas as conexões do esptool entraram sem apertar BOOT |
| Reset | `--after hard-reset` via RTS funcionou; a porta continua presente durante e depois do reset (é ponte, não USB nativo) |
| Monitor serial | 115200 8N1. Ao abrir o monitor com DTR/RTS ativos, a placa pode resetar ou ficar em download; no PlatformIO use `monitor_rts = 0` e `monitor_dtr = 0` se isso acontecer |
| Boot log | Só o ROM e o bootloader escrevem (`ets Jul 29 2019`, `rst:0x1 POWERON_RESET`, `boot:0x13 SPI_FAST_FLASH_BOOT`, `mode:DIO`). Log completo em `logs/03_boot_log_115200.txt` |
| USB CDC | **Não se aplica** (sem USB nativo). Não defina `ARDUINO_USB_CDC_ON_BOOT` |

## 12. Arquivos

- `config/platformio.ini` e `config/User_Setup.h`: configuração do TFT_eSPI, com o nível de cada linha e marcas `[V1]` para validar no primeiro teste
- `backup/`: dump, SHA-256, `RESTAURAR.md` e recortes em `extracted/`
- `logs/`: saídas brutas, boot log, strings, `xt_calls.tsv` (todas as chamadas com argumentos imediatos), sequência de init da tela, disassembly do touch
- `tools/`: `capture_boot.py` (captura do boot log) e `xt_analyze.py` (análise Xtensa com Capstone 6)
- `COMANDOS.md`: todos os comandos, em ordem

## 13. Pendências e primeiro teste

- [NV] Se o touch respondeu de fato (o sketch tem o caminho `TOUCH FAIL`); polaridade do LED RGB; PSRAM medida; conectores extras; variante exata do CH340.
- [I] SD, LED RGB, LDR, áudio e INT/RST do touch vêm só da fonte pública.
- **Primeiro teste recomendado:** sketch TFT_eSPI com estes arquivos. Ele deve: (1) acender o backlight; (2) `fillScreen` em vermelho, verde, azul, preto e branco, para validar `TFT_RGB_ORDER` e a inversão; (3) ler o registrador 0x8140 do GT911 em 0x5D e imprimir "911" na serial; (4) imprimir as coordenadas tocadas nos quatro cantos, para fechar a orientação touch × tela em `setRotation(0)`.
