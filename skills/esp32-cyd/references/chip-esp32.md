# ESP32 clássico: chip, memória e periféricos

Escopo: ESP32-D0WD-V3; não transportar limites de S2/S3/C3 para este chip. Nesta placa, D0WD-V3 revisão **v3.1**, dois núcleos a 240 MHz e cristal de 40 MHz são observações anteriores, não medições desta fase. Fonte: [README, §2](relatorio-unidade.md#2-chip).

## Fontes e revisões inspecionadas

As páginas abaixo são **páginas físicas do PDF, contando a capa**; no datasheet e no TRM coincidem com a numeração impressa. Textos extraídos disponíveis em `fontes/espressif/texto/`.

- **DS**: [ESP32 Series Datasheet](https://documentation.espressif.com/esp32_datasheet_en.pdf), **v5.3**, capa p.1; histórico p.70, entrada 2026.07. Não confundir revisão documental com revisão v3.1 do silício.
- **TRM**: [Technical Reference Manual](https://documentation.espressif.com/esp32_technical_reference_manual_en.pdf), **v5.9**, capa p.1; capítulos enumerados em p.3.
- **ERR**: [Series SoC Errata](https://docs.espressif.com/projects/esp-chip-errata/en/latest/esp32/esp-chip-errata-en-master-esp32.pdf), **v3.1**, capa p.1; identificação do chip §1, pp.4–8; matriz de aplicabilidade §2. A coincidência “3.1” do documento com a revisão desta placa não significa que sejam a mesma versão.
- **HDG**: [Hardware Design Guidelines](https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32/esp-hardware-design-guidelines-en-master-esp32.pdf), capa “Release master”, 12/nov/2026; histórico **v1.9, 2025-09-17**, p.37. `master/latest` é canal, não revisão congelada.
- [ESP32-WROOM-32](https://documentation.espressif.com/esp32-wroom-32_datasheet_en.pdf): **v3.8**, capa p.1, marcado NRND. É documentação de um módulo específico, não prova de que esta placa o utilize.
- URLs oficiais, redirecionamentos e limites das cópias: [links](links.md); integridade e coleta: manifesto (base local `esp32-docs/fontes/MANIFESTO.md`, não publicada).

## CPU, rádio e memória

| Recurso | Limite do chip / distinção da placa | Fonte |
|---|---|---|
| CPU | Xtensa LX6 de 32 bits, até 240 MHz; D0WD-V3 dual-core | DS §1.2 p.11 e §4.1.1 p.26 |
| ROM | 448 KB para boot e funções básicas; não é espaço gravável de aplicativo | DS §4.1.2 p.26 |
| SRAM interna | 520 KB para instruções e dados; não equivale ao heap livre do firmware | DS §4.1.2 p.26 |
| RTC | 8 KB FAST + 8 KB SLOW; retenção depende dos domínios alimentados e configuração de sono | DS §4.1.2 p.26, §4.3 pp.30–31 |
| Flash/PSRAM do encapsulamento | D0WD-V3 não incorpora nenhuma; outros membros da família incorporam | DS tabela 1-1 p.11 |
| Flash desta placa | **4 MB externos**, JEDEC fabricante 0x5E/device 0x4016; cabeçalhos DIO/80 MHz | README §3; não extrapolar a outras CYDs |
| PSRAM desta placa | **Ausente [I]**, ainda não medida; sem PSRAM interna não exclui por si só uma externa | README §§3 e 13 |
| Wi-Fi | 802.11 b/g/n em **2,4 GHz**, não 5 GHz | DS “Wi-Fi” p.3, §4.6 pp.32–34 |
| Bluetooth | Bluetooth 4.2 BR/EDR + Bluetooth LE | DS “Bluetooth” p.3, §4.7 pp.34–35 |

Não calcular buffers pela SRAM nominal inteira: memória do programa, pilhas, RTOS, drivers e rádio competem por ela. Essa é uma consequência de projeto, não medição do heap desta placa (DS §4.1.2; TRM cap.3 “System and Memory”).

## GPIO, matriz e restrições

- São 34 GPIOs no SoC, mas funções multiplexadas, flash e ligações da placa reduzem os disponíveis. A matriz GPIO roteia sinais; não cria saída em um pino somente de entrada. Fontes: DS §§2.2–2.3 pp.14–17, §4.8.1 p.36; TRM cap.6 “IO MUX and GPIO Matrix”.
- **GPIO34–39 são somente entrada e não têm pull-up/pull-down internos**; não usar para PWM, SCL ou SDA bidirecional. GPIO37/38 podem não estar acessíveis em módulos/placas. Fontes: DS tabela 2-1 p.14, §2.3.1 p.17; acessibilidade desta placa permanece [NV], README §9.
- GPIO6–11 são sinais da flash na ligação SPI usual: não tratá-los como expansão livre. GPIO16/17 também podem participar de memória externa em outros projetos. Fontes: DS §2.6 pp.20–21, §4.8.2 p.36.
- UART0 e JTAG dividem pinos com GPIO; preservar o acesso de depuração e verificar os circuitos existentes antes de reutilizar. Fonte: DS §2.3.1 p.17, tabela 4-6 pp.46–50.

## SPI: memória não é barramento de tela

- Há quatro controladores: SPI0 participa do acesso à memória externa, SPI1 pode operar como mestre; SPI2/HSPI e SPI3/VSPI admitem mestre/escravo. “Quatro SPI” não significa quatro barramentos livres para periféricos. Fontes: DS §4.8.2 p.36; TRM cap.20 “SPI Controller”.
- Clock, CPOL/CPHA e comprimento são configuráveis. IO_MUX e matriz permitem roteamento sujeito a limites elétricos/temporização; não prometer a mesma frequência em qualquer pinagem. Fontes: DS §4.8.2 p.36; TRM cap.20.
- Nesta placa a tela usa SCLK14/MOSI13/MISO12/CS15/DC2, a **40 MHz no firmware analisado**; não é limite garantido de outro painel. SD em 18/23/19/CS5 é apenas inferido da definição pública. Fonte: README §9, itens [C]/[I].
- Compartilhar SPI exige CS independente e transações coerentes; antes de remapear, considerar GPIO12/15 e GPIO2 como straps. Fonte de hardware: DS cap.3 pp.22–25; uso da placa: README §9.

## I2C

- Dois controladores, mestre ou escravo; endereçamento de 7/10 bits. Standard 100 kbit/s e Fast 400 kbit/s; o datasheet menciona até 5 MHz condicionado à força dos pull-ups, **não uma recomendação para o GT911**. Fontes: DS §4.8.4 p.37; TRM cap.21 “I2C Controller”.
- SDA/SCL são roteáveis pela matriz em GPIOs compatíveis com entrada/saída, respeitando pull-ups e os dispositivos conectados. Fonte: DS §§2.3.1 e 4.8.4; TRM cap.21.
- Touch desta placa: SDA33/SCL32, endereço **0x5D**, por disassembly do sketch; não assumir os genéricos 21/22. INT21/RST25 são apenas [I]. Fonte: README §8.

## LEDC / PWM

- 16 canais: oito high-speed e oito low-speed, cada grupo com quatro timers. Canais ligados ao mesmo timer compartilham frequência/resolução, não necessariamente duty. Fontes: DS §4.8.8 p.39; TRM §§28.1–28.2.3 pp.629–632.
- Até 20 bits de resolução do contador, mas frequência e resolução competem; a tabela do TRM exemplifica 5 kHz/13 bits com APB 80 MHz. Não anunciar 20 bits em qualquer frequência. Fonte: TRM §28.2.2 pp.630–631.
- Fade automático existe; aguardar o fim antes de reconfigurar os registradores de fade. Há restrição em fade descendente com duty máximo e passo 1. Fontes: TRM §28.2.3 pp.632–633; ERR §3.33 “LEDC-3.12”.
- Backlight GPIO27 ativo HIGH foi confirmado; RGB 4/16/17 e sua polaridade não receberam o mesmo nível de confirmação. PWM para brilho é possibilidade de projeto, não teste feito aqui. Fonte: README §9.

## ADC1, ADC2 e Wi-Fi

- Dois SAR ADCs de até 12 bits, 18 canais no total. **ADC1**: CH0…CH7 em GPIO36,37,38,39,32,33,34,35; **ADC2**: CH0…CH9 em GPIO4,0,2,15,13,12,14,27,25,26. Fontes: DS tabela 2-1 pp.14–15, §4.9.1 pp.43–44.
- **ADC2 é compartilhado com o Wi-Fi**: quando o rádio usa SAR ADC2, a aplicação não mede seus pinos por esse ADC; após liberação, pode utilizá-lo. Não prometer operação simultânea contínua nem erro de API idêntico em todas as versões. Fonte: TRM §31.3, nota na p.748.
- Para sensores com Wi-Fi, preferir ADC1 **livre no circuito**. Aqui GPIO32/33 já estão no touch e GPIO34 é LDR [I]; ser ADC1 não torna o pino desocupado. Fonte: README §§8–9.
- Leitura bruta de 12 bits não é precisão de 12 bits em volts: considerar atenuação, não linearidade, filtragem e calibração. As faixas calibradas documentadas não equivalem automaticamente a 0–3,3 V com exatidão uniforme. Fonte: DS §4.9.1, tabelas 4-3/4-4 pp.43–44.
- Vref 1142 mV foi lida anteriormente nas eFuses desta unidade; não copiar esse valor para outra placa. Fonte: README §2.

## Straps e boot: cargas externas também contam

Os níveis são amostrados no reset e depois os pinos podem assumir funções normais. Pull-ups/pull-downs dos periféricos podem vencer os pulls fracos internos. Fonte: DS cap.3, pp.22–25.

| Pino | Estado padrão / papel no reset | Cuidados |
|---|---|---|
| GPIO0 | Pull-up; alto = boot SPI, baixo = download com GPIO2 baixo | BOOT costuma puxá-lo para GND |
| GPIO2 | Pull-down; deve estar baixo para download | Na placa também é DC da tela |
| GPIO12 / MTDI | Pull-down; baixo seleciona VDD_SDIO típico 3,3 V; alto seleciona LDO 1,8 V, salvo override eFuse | Nesta placa flash 3,3 V; não puxar alto no reset |
| GPIO15 / MTDO | Pull-up; alto habilita mensagens U0TXD; também timing SDIO | Baixo pode silenciar o ROM sem significar chip morto |
| GPIO5 | Pull-up; participa do timing SDIO slave | SD CS inferido nesta placa |

Fontes de cada linha: DS tabelas 3-1/3-3/3-4/3-5 e §3.2 pp.22–25; correspondência física: README §§3 e 9. VDD_SDIO pode ser imposto por eFuses: **não queimá-las para contornar uma ligação errada**; são irreversíveis (DS cap.3 p.22).

## Limite de confiança

A revisão v3.1 do chip não elimina todas as erratas: consultar a matriz ERR §2 para a revisão, periférico e condição de uso. Valores de chip/módulo não certificam pinagem, revisão de PCB, polaridade, presença de PSRAM nem estado atual do firmware. Para gravar, consultar [macOS/esptool v5](gravacao-macos.md); esta referência não executou comunicação com a placa.
