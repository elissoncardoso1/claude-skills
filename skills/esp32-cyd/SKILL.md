---
name: esp32-cyd
description: Use quando o pedido envolver a placa ESP32-2432S032C ("Cheap Yellow Display", CYD 3,2", Sunton) ou qualquer ESP32 ligado ao Mac por /dev/cu.usbserial: criar, compilar, gravar ou depurar firmware com PlatformIO/Arduino, tela ST7789 com TFT_eSPI, touch capacitivo GT911, Wi-Fi/WiFiManager, backup ou restauração da flash com esptool, monitor serial, cores trocadas, touch no lugar errado, "TOUCH FAIL", "Corrupt data", Wi-Fi que não conecta (motivo 34, 15, 201).
---

# ESP32-2432S032C (CYD 3,2") no macOS

A ficha técnica completa, com o nível de evidência de cada item, está em `references/relatorio-unidade.md`. Esta skill resume o que já foi testado na placa. Os projetos de referência que funcionam são `ai-dock/` (touch + serial com o Mac) e `pixel-clima/` (Wi-Fi + API + sprites), na mesma pasta.

## Regras

1. **Faça backup antes da primeira gravação** em uma placa desconhecida (ver "Backup"). Gravar apaga o firmware anterior e não tem volta.
2. **Não use `ls /dev/tty.*`.** Use sempre `/dev/cu.usbserial-*`. O sufixo muda conforme a porta ou o hub, então confira antes de gravar e ajuste o `platformio.ini`.
3. **Comece pelos templates** em `templates/`. A pinagem e a configuração do TFT_eSPI já foram validadas, então não precisa redescobrir nada.
4. **Não adicione biblioteca de touch.** O GT911 é lido direto pelo Wire, com cerca de 30 linhas em `templates/main.cpp`.
5. **Ferramentas:** defina `ESP32_HOME` como a pasta dos seus projetos ESP32 (com um venv que tenha platformio, esptool e espefuse) e use `$ESP32_HOME/.venv/bin/{pio,esptool,espefuse}`. Não há `pio` nem `arduino-cli` no PATH.

## Referências: abra antes de decidir

A base documental fica em `$ESP32_HOME/esp32-docs/` (base local opcional, não publicada). Originais, textos de trabalho, clones e hashes ficam só nessa base, não nesta skill. Os links para relatório/fontes nas referências apontam para essa base local; os URLs públicos e commits permitem consultar as fontes sem ela. A coleta é de 23/nov/2026 (-03); canais stable/latest mudam.

- Antes de escolher pinos, alimentação, bateria ou touch, leia [references/placa-2432S032.md](references/placa-2432S032.md), especialmente “Divergências”.
- Antes de reutilizar GPIO, SPI, I2C, ADC ou PWM, leia [references/chip-esp32.md](references/chip-esp32.md).
- Antes de escolher bibliotecas/core ou atualizar dependências, leia [references/versoes.md](references/versoes.md). Diferencie release, HEAD e versão do firmware; a matriz documental não é teste de compatibilidade nesta placa.
- Antes de escrever `lv_conf.h`, registrar display/touch ou dimensionar buffers, leia [references/lvgl.md](references/lvgl.md). Escolha v8 ou v9 e o template da versão exata; v8 conta pixels, v9 conta bytes no registro do buffer.
- Antes de backup, upload, restauração ou diagnóstico USB, leia [references/gravacao-macos.md](references/gravacao-macos.md). Seus comandos são exemplos, não autorização de escrita.
- Para canais atualizados, revisões dos PDFs e proveniência, leia [references/links.md](references/links.md); o manifesto completo está em `esp32-docs/fontes/MANIFESTO.md`.

### Regras para outras placas e novas dependências

1. **Confirme a variante N/R/C e a revisão antes de aplicar templates:** N não tem touch, R usa XPT2046/SPI, C usa GT911/I2C. O nome incompleto “2432S032” ou “CYD v2” não identifica sozinho a unidade. A regra de não adicionar biblioteca de touch acima é para o caminho GT911 desta unidade, não para toda a família.
2. **A pinagem e os níveis de evidência do relatório prevalecem sobre fontes externas.** [C] inclui configuração recuperada do firmware, não necessariamente medição elétrica ou teste funcional. Nunca promover [I]/[NV] por concordância de duas fontes. Se o relatório faltar numa placa nova, marcar documentação externa como não verificada.
3. **Nesta unidade, mantenha flash DIO** (80 MHz observado); não trocar por QIO copiando exemplo genérico. Para uma gravação nova, conferir cabeçalhos e layout do build; não alterar parâmetros de um backup às cegas.
4. **RST exige identificar o sinal e a revisão:** LCD, touch e EN são diferentes. Aqui o LCD usa `TFT_RST=-1` no sketch e GPIO15 é CS; ligação física ao EN não foi medida. GPIO35 é somente entrada, não saída de reset. INT21/RST25 do GT911 são inferidos.
5. **Sem PSRAM é hipótese conservadora, não medição.** Dimensione buffers internos, mas não afirme detecção negativa. IPS/BGR também são inferidos no relatório; valide cores/orientação antes de fechar a configuração.
6. **Não prometer consumo de deep-sleep do chip para a placa inteira.** O modo existe no ESP32; LDOs, ponte, periféricos e possível desligamento do boost precisam de medição. Bateria/IP5306 e sua polaridade/variante exigem identificação física antes do uso.
7. **Use exatamente uma integração de display/touch.** TFT_eSPI/LovyanGFX com port LVGL e smartdisplay são caminhos alternativos. Não empilhar inicializadores nem misturar APIs LVGL 8/9; fixe dependências e registre um build real antes de declarar compatibilidade.

## Hardware (níveis do relatório)

| Item | Valor |
|---|---|
| SoC | [C] ESP32-D0WD-V3 rev 3.1, 240 MHz, cristal de 40 MHz; **PSRAM ausente [I], não medida** |
| Flash | 4 MB, DIO 80 MHz, partições `default.csv` (app0/app1 de 1280 KB cada) |
| USB | Ponte CH340 (1A86:7523) com driver nativo do macOS. **Não há USB CDC nativo**, então nunca use `ARDUINO_USB_CDC_ON_BOOT` |
| Tela | [C] ST7789 240×320, INVON, SPI a 40 MHz; IPS e ordem BGR [I], cores ainda exigem validação |
| Tela, pinos | SCLK 14, MOSI 13, MISO 12, CS 15, DC 2, RST -1, **BL 27 (HIGH)** |
| Touch | GT911 I2C **0x5D**, SDA 33, SCL 32 (INT 21 e RST 25 [I], não usados) |
| Extras [I] | SD: CS 5, SCK 18, MOSI 23, MISO 19 · LED RGB 4/16/17 (polaridade não verificada) · LDR 34 · alto-falante 26 |

[I] = vem de fonte pública (rzeldent/platformio-espressif32-sunton) e ainda não foi medido na placa.

## Novo projeto

```sh
P=${ESP32_HOME:-$HOME/esp32}
mkdir -p $P/meu-projeto/src
cp $P/esp32-cyd/templates/{platformio.ini,User_Setup.h} $P/meu-projeto/
cp $P/esp32-cyd/templates/main.cpp $P/meu-projeto/src/
ls /dev/cu.usbserial-*                       # confira a porta e ajuste upload_port/monitor_port
cd $P/meu-projeto
$P/.venv/bin/pio run                         # compilar
$P/.venv/bin/pio run -t upload               # gravar (entra em modo download sozinho, via DTR/RTS)
$P/.venv/bin/pio device monitor              # 115200; monitor_rts/dtr = 0 evita reset ao abrir
```

O `platformio.ini` usa `-D USER_SETUP_LOADED=1 -include $PROJECT_DIR/User_Setup.h`, então o `User_Setup.h` da biblioteca **não** é editado.

Para ler a serial a partir de um script (como o listener do Mac), abra com pyserial e defina `s.dtr = s.rts = False` logo depois de abrir, como em `ai-dock/mac/dock_listener.py`. Se não fizer isso, a placa reseta.

## Tela e touch

- `setRotation(1)` deixa a tela em paisagem, 320×240. O GT911 continua reportando em retrato, 240×320. A conversão `x = py; y = 239 - px` está em `getTouch()` no template.
- Se o toque cair no lugar errado, leia `DBG touch raw=… tela=…` na serial, toque nos 4 cantos e ajuste `TOUCH_SWAP_XY`, `TOUCH_INV_X` e `TOUCH_INV_Y`.
- Depois de ler o registrador `0x814E`, **sempre** escreva 0 nele. Se não zerar, o GT911 para de mandar pontos.
- A resolução real do GT911 fica no registrador `0x8048` (4 bytes LE). Use esse valor para escalar, não 240×320 fixo.
- Para animação sem flicker, desenhe em `TFT_eSprite` e depois faça `pushSprite`. Sem PSRAM, um sprite de 16 bits ocupa 2 bytes por pixel, e a tela inteira (150 KB) costuma não caber. Use faixas, como `dockSpr` 320×112 no ai-dock.
- Debounce do toque: só aceite um novo toque **depois** que a animação do anterior terminar. Se não, o mesmo toque abre a ação duas vezes.
- Imagens: converta para RGB565 em um array `const` (vai para a flash). O script de exemplo é `ai-dock/icons/make_icons.py`, que gera RGB565 + alfa 50×50. Para fonte bitmap, veja `pixel-clima/tools/make_font.py`.

## Wi-Fi

- Padrão usado: `WiFiManager` com `autoConnect(AP, senha)`, portal em 192.168.4.1, `setConfigPortalTimeout(180)` e **`setConnectTimeout(20)`**. Sem o connect timeout, cada tentativa trava por 60 s.
- Para ver por que a conexão cai, registre `ARDUINO_EVENT_WIFI_STA_DISCONNECTED` e imprima `info.wifi_sta_disconnected.reason`. Código em `pixel-clima/src/main.cpp`.

| Motivo | Significado | O que fazer |
|---|---|---|
| 15 / 204 | Senha errada (handshake) | Reconfigurar no portal |
| 201 | SSID não encontrado | O ESP32 só enxerga **2,4 GHz**. Confira o nome e a banda |
| 2 / 202 | Autenticação recusada | Modo WPA3-only ou filtro de MAC no roteador |
| 34 | MISSING_ACKS | Foi tentado `WiFi.setTxPower(WIFI_POWER_8_5dBm)` depois de `WiFi.mode(WIFI_STA)`. **Não verificado**: ainda havia falhas depois disso. Teste também alimentação e cabo USB direto (sem hub), aproximar do roteador e fixar o canal |

- Dados sem chave de API, como no pixel-clima: `ip-api.com` dá cidade/lat/lon pelo IP (aproximado), Open-Meteo com `timezone=auto` dá o clima e o offset do fuso, e `configTime(offset, 0, "pool.ntp.org")` acerta a hora.

## Problemas comuns

| Sintoma | Causa / correção |
|---|---|
| `Corrupt data` ao ler ou gravar | Velocidade alta passando pelo hub. Use `upload_speed = 115200`. Ligado direto no Mac, teste 460800 |
| Vermelho e azul trocados | No `User_Setup.h`, troque `TFT_BGR` por `TFT_RGB` |
| Cores em negativo | Defina `TFT_INVERSION_OFF` |
| Tela preta, mas o código roda | Backlight: `pinMode(27, OUTPUT); digitalWrite(27, HIGH)` antes de desenhar |
| `TOUCH FAIL` / id vazio | `Wire.begin(33, 32)` não foi chamado ou foi chamado com os pinos trocados. Se INT/RST forem mexidos no reset, o GT911 pode passar a responder em **0x14** |
| Placa reseta ao abrir o monitor | `monitor_rts = 0` e `monitor_dtr = 0` |
| Não entra em modo de gravação | Segure BOOT, toque em RST/EN e solte BOOT |
| Flash quase cheia (>90%) | Fontes do TFT_eSPI que não são usadas. Remova `LOAD_FONT6/7/8` e `SMOOTH_FONT` do User_Setup.h. Ou use `board_build.partitions = huge_app.csv` (perde o OTA) |
| GPIO12 travando o boot | Ele é o strap da tensão da flash. Não puxe para HIGH no boot |

## Backup e restauração

```sh
E=$ESP32_HOME/.venv/bin/esptool
PORT=/dev/cu.usbserial-11220  # exemplo: conferir a enumeração atual, não selecionar a primeira porta
$E -p $PORT -b 115200 read-flash 0 0x400000 backup.bin && shasum -a 256 backup.bin > backup.bin.sha256   # ~6 min
$E -p $PORT -b 115200 write-flash --flash-mode dio --flash-freq 80m --flash-size 4MB 0x0 backup.bin    # restaurar
```

Backup de um firmware compilado (sem ler a placa): copie `.pio/build/cyd32c/{bootloader,partitions,firmware}.bin`, ou junte tudo com `esptool merge-bin -o merged.bin 0x1000 bootloader.bin 0x8000 partitions.bin 0xe000 boot_app0.bin 0x10000 firmware.bin`.

Já existem: `backups/ai-dock-v2-macos-icons/` (merged 0x0) e o dump original (sketch "AI DOCK" antigo, **não** é o de fábrica) em `esp32-docs/backup/` e as instruções em `esp32-docs/backup/RESTAURAR.md`.

## Pendências da placa

Ainda não verificados: polaridade do LED RGB, cartão SD junto com a tela (o template usa `USE_HSPI_PORT` para isso), conectores extras e a correção do Wi-Fi motivo 34.
