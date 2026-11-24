# macOS: conexão e gravação com esptool v5

**Todos os comandos deste documento são exemplos não executados nesta fase.** Nada foi instalado, nenhuma porta foi aberta e nenhuma operação foi enviada à placa. Mesmo consultas podem resetar o ESP32 e carregar um stub em RAM; “leitura” não significa ausência de efeito operacional. Fonte: [opções avançadas, “Reset Modes” e “Disabling the Stub Loader”](https://docs.espressif.com/projects/esptool/en/latest/esp32/esptool/advanced-options.html).

## Fontes e sintaxe

A cópia [esptool latest](https://docs.espressif.com/projects/esptool/en/latest/esp32/) declara **v5**, sem patch fixado; link de código registrado no manifesto: `42265b9e`. `latest` não identifica uma versão imutável. Usar hífens (`chip-id`, `write-flash`, `default-reset`), não os underscores de receitas antigas. Fonte: [guia de migração](https://docs.espressif.com/projects/esptool/en/latest/esp32/migration-guide.html), “Command and Option Renaming” e “Reset Mode Renaming”.

Abreviações das fontes usadas em cada seção:

- **B**: [Basic Commands](https://docs.espressif.com/projects/esptool/en/latest/esp32/esptool/basic-commands.html), seções com o nome de cada comando.
- **A**: [Advanced Commands](https://docs.espressif.com/projects/esptool/en/latest/esp32/esptool/advanced-commands.html), seções com o nome de cada comando.
- **O**: [Advanced Options](https://docs.espressif.com/projects/esptool/en/latest/esp32/esptool/advanced-options.html).
- **T**: [Troubleshooting](https://docs.espressif.com/projects/esptool/en/latest/esp32/troubleshooting.html).
- **BOOT**: [Boot Mode Selection](https://docs.espressif.com/projects/esptool/en/latest/esp32/advanced-topics/boot-mode-selection.html).
- **R**: [README desta placa](relatorio-unidade.md), observações anteriores §§1–5 e 11, não verificações novas.
- Links públicos, canais e proveniência: [links](links.md).

## USB e porta comprovados, não adivinhados

| Item | Evidência anterior / consequência | Fonte |
|---|---|---|
| Ligação | USB-C de dados + energia, ponte WCH CH340, VID/PID **1A86:7523**; variante C/G não confirmada | R §1, logs `01_ioreg_usb.txt` e `01_ioreg_ch340_detail.txt` |
| Driver | AppleUSBCHCOM/DriverKit já utilizado; nenhum driver extra necessário naquela máquina | R §1; não é afirmação sobre todo macOS/CH340 |
| Porta | **`/dev/cu.usbserial-11220`**, sufixo dependente de porta/hub | R §§1 e 11 |
| Falso candidato | `/dev/cu.usbmodemSN234567892` é BillBoard do hub, não esta placa | R §1 |
| USB nativo | Não existe nessa ligação; não ativar `ARDUINO_USB_CDC_ON_BOOT` | R §11 |
| Velocidade | **115200 comprovada em leitura de 4 MB**; 460800 deu “Corrupt data” pelo hub Anker | R §11 |
| Reset | DTR/RTS→GPIO0/EN automático funcionou; `hard-reset` via RTS não remove a porta da ponte | R §11 |

Descoberta no host (exemplos, também não executados):

```sh
ls /dev/cu.usbserial-*
ioreg -p IOUSB -l -w 0
lsof /dev/cu.usbserial-11220
esptool version
esptool --help
```

Comparar a enumeração com a placa desconectada/conectada e conferir VID/PID; não copiar o sufixo cegamente. Fechar monitor serial/IDE que detenha a porta antes do esptool. Fontes: R §§1/11; T “A serial exception error occurred”. `ls`, `ioreg` e `lsof` são diagnósticos do host, não comandos do ROM.

Não instalar driver ou pacote por reflexo. A versão de esptool efetivamente disponível deve ser confirmada antes de adaptar receitas; esta fase documenta v5, não certifica a instalação local.

## Consultas e backup antes de qualquer escrita

Exemplos com porta explícita, 115200 e alvo clássico; cada chamada pode reiniciar a aplicação:

```sh
esptool --chip esp32 --port /dev/cu.usbserial-11220 --baud 115200 chip-id
esptool --chip esp32 --port /dev/cu.usbserial-11220 --baud 115200 read-mac
esptool --chip esp32 --port /dev/cu.usbserial-11220 --baud 115200 flash-id
esptool --chip esp32 --port /dev/cu.usbserial-11220 --baud 115200 read-flash 0 ALL backup-novo.bin
shasum -a 256 backup-novo.bin
```

`ALL` autodetecta o tamanho; para esta unidade, o tamanho previamente medido foi 4 MB (`0x400000`). Usar nome novo para não substituir backup existente; guardar hash, identificação e layout juntos. Fontes: B “read-flash”, “read-mac”, “flash-id”; R §§2–5. `chip-id` também aparece na migração “Flash Operations from Non-flash Related Commands”; o hash é uma checagem do arquivo local, não prova de que o firmware seja original.

**Não existe backup do firmware de fábrica**: o dump descrito em R é do sketch “AI DOCK”. Preservar esse dump não recupera a imagem comercial original. Fonte: R abertura e §6.

### Segurança: limite do ESP32 clássico

O registro desta unidade mostra `get-security-info` rejeitado pelo ROM com **FF00**. Não apresentar esse comando como consulta universal do ESP32 clássico nem interpretar “unsupported” como Secure Boot/Encryption desligados. No levantamento anterior foi usado:

```sh
# Exemplo de consulta de eFuse; NÃO executado nesta fase.
espefuse --chip esp32 --port /dev/cu.usbserial-11220 summary
```

O resultado anterior foi ABS_DONE_0/1=False e FLASH_CRYPT_CNT=0; é evidência daquela leitura, não garantia do estado atual. Fontes: R §4; migração “espefuse v5 / --port Option is Required”. Nenhum `burn-*`, desbloqueio ou alteração de eFuse faz parte deste procedimento.

## Preparar imagens sem acessar a placa

```sh
esptool --chip esp32 image-info app.bin
esptool --chip esp32 elf2image app.elf
esptool --chip esp32 merge-bin -o merged-flash.bin 0x1000 bootloader.bin 0x8000 partition-table.bin 0x10000 app.bin
```

Esses exemplos operam sobre arquivos locais (ainda assim podem criar/substituir arquivos). `image-info` mostra segmentos/cabeçalhos; `elf2image` converte ELF; `merge-bin` RAW preenche lacunas. A imagem RAW resultante do exemplo começa em 0 e seria gravada em 0, **não** em 0x1000. Não extrair a tabela de partições com `image-info` como se fosse um aplicativo. Fontes: B “image-info”, “elf2image”, “merge-bin / RAW Output Format”.

Os offsets do exemplo coincidem com R §5, mas **o layout do build escolhido é a autoridade para uma gravação nova**. Não misturar bootloader de um build, tabela de outro e app de um terceiro. `@flash_args` é expandido como argumentos normais: inspecioná-lo antes; não executar arquivo de parâmetros desconhecido. Fonte: B “merge-bin”; O “Specifying Arguments via File”.

## Escrita: exemplos perigosos, NÃO executados

**Os blocos abaixo apagam/substituem conteúdo. Não são instruções para executar agora.** Antes de autorizar qualquer escrita, conferir backup/hash, alvo, offsets, tamanho, arquivos, alimentação e segurança; fechar monitores. A falta de confirmação desses itens é motivo para parar.

```sh
# PERIGOSO: escreve três regiões; exemplo NÃO executado.
esptool --chip esp32 --port /dev/cu.usbserial-11220 --baud 115200 --before default-reset --after hard-reset write-flash 0x1000 bootloader.bin 0x8000 partition-table.bin 0x10000 app.bin

# PERIGOSO: restauração integral de um dump conhecido, NÃO executada.
# Só se o arquivo for dump completo desde zero, tamanho e origem conferidos.
esptool --chip esp32 --port /dev/cu.usbserial-11220 --baud 115200 write-flash 0x0 backup-integral-conferido.bin
```

`write-flash` apaga os setores afetados antes de gravar e verifica MD5 dos dados escritos. O setor mínimo é **4096 bytes**: limites não alinhados podem apagar bytes além do intervalo útil. Apagar toda a flash antes de cada upload é desnecessário. Fontes: B “Erasing Flash Before Write”; A “verify-flash”.

DIO/80 MHz são valores observados nesta placa (R §3), não parâmetros a impor em todo binário. O padrão de `write-flash` preserva modo/tamanho do cabeçalho; sobrescrevê-los pode alterar bytes e digest da imagem. Fonte: B “Setting Flash Mode and Size” e “elf2image”. Não usar QIO por cópia de uma receita genérica.

```sh
# PERIGOSO: apaga TODA a flash, inclusive NVS e dados; NÃO executado.
esptool --chip esp32 --port /dev/cu.usbserial-11220 --baud 115200 erase-flash

# PERIGOSO: apaga uma região ilustrativa, NÃO executado.
# 0x9000/0x5000 correspondem à NVS no layout anterior: perde configurações.
esptool --chip esp32 --port /dev/cu.usbserial-11220 --baud 115200 erase-region 0x9000 0x5000
```

Endereço/tamanho de `erase-region` precisam ser múltiplos de 0x1000. `--force` contorna proteções e pode inutilizar boot seguro/flash cifrada; **não é tratamento de erro** e foi deliberadamente excluído dos exemplos. Fontes: B “erase-flash & erase-region”, “Bootloader Protection”, “Encrypted Flash Protection”; layout: R §5.

## Comandos e opções avançados

Exemplos de leitura/verificação, não executados; mesmo assim podem resetar a placa:

```sh
esptool --chip esp32 --port /dev/cu.usbserial-11220 --baud 115200 verify-flash --diff 0x10000 app.bin
esptool --chip esp32 --port /dev/cu.usbserial-11220 --baud 115200 read-flash-status --bytes 1
esptool --chip esp32 --port /dev/cu.usbserial-11220 --baud 115200 read-flash-sfdp 16 4
esptool --chip esp32 --port /dev/cu.usbserial-11220 --baud 115200 --no-stub flash-id
```

- `verify-flash --diff`: comparação detalhada; repetir overrides de cabeçalho usados em `write-flash`, se houver, para não gerar divergência aparente. Fonte: A “Verify Flash Data”.
- `read-flash-status`: número de bytes/comandos suportados depende do datasheet da flash; `read-flash-sfdp` consulta parâmetros de descoberta se o chip os suportar. Não identificar modelo exato só pelo fabricante JEDEC. Fonte: A seções correspondentes; R §3 distingue identificação e inferência.
- `--no-stub`: usa apenas ROM, desabilitando recursos não implementados nele; em `read-flash` pode requerer `--flash-size`. Não é “modo sem efeitos”: ainda há conexão/reset. Fontes: O “Disabling the Stub Loader”; B “read-flash”.
- `--before no-reset`: serve quando download foi colocado manualmente; `--after no-reset` deixa no bootloader, `--after no-reset-stub` mantém o stub. São opções globais, antes do comando. Fonte: O “Reset Modes”.
- `dump-mem` e `read-mem` acessam ROM/RAM/registradores mapeados, não substituem `read-flash`; leitura de registradores também exige conhecimento de seus efeitos. Fonte: A “dump-mem” e “read-mem & write-mem”.
- **Perigosos, sem receita executável aqui:** `write-mem` muda memória/registradores; `load-ram` carrega **e executa imediatamente**; `write-flash-status` pode alterar proteção permanentemente. Fontes: A seções desses comandos.
- `--skip-flashed` compara MD5 e pula conteúdo igual; `--diff-with` grava setores diferentes e verifica depois. `--trust-flash-content` pode pular verificação de arquivos inalterados e foi omitido das receitas seguras. Recursos de `latest` podem não existir em todo patch v5; conferir ajuda da versão instalada. Fonte: B “Skipping Unchanged Content” e “Fast Reflashing”.
- Não usar `--spi-connection HSPI` para “selecionar o SPI da tela”: essa opção remapeia **a flash** e pode disputar os pinos TFT desta placa. Fontes: O “Overriding SPI Flash Connections”; R §9.

## Troubleshooting por sintoma

| Sintoma | Verificação / correção proposta, não executada | Fonte |
|---|---|---|
| Porta inexistente/ocupada | Confirmar cabo de dados, enumeração e sufixo atual; fechar IDE/monitor; conferir `lsof`; não escolher BillBoard do hub | T “A serial exception error occurred”; R §1 |
| “Failed to connect” / sem resposta | Conferir alimentação, cabo, porta e modo download; desconectar cargas externas dos straps | T “No serial data received”; BOOT “Boot Mode” |
| “Wrong boot mode” | GPIO0 deve estar baixo no reset para download e GPIO2 baixo/flutuante; não alterar eFuses | BOOT “GPIO0”, “GPIO2”; DS cap.3 |
| Reset automático falha | Se BOOT/EN estiverem acessíveis: manter BOOT, pulsar EN, iniciar sincronização e liberar BOOT; não presumir botões/conectores não identificados | BOOT “Manual Bootloader”; R §9 |
| “Invalid head of packet” / “Corrupt data” | Voltar a 115200; cabo curto e bom, ligação direta e energia estável; monitor fechado; taxa alta não comprovada nesta rota | T “Invalid head of packet”; R §11 |
| Grava mas não inicia | Checar offsets, imagem/partições, modo da flash, alimentação e straps; GPIO12 alto pode selecionar 1,8 V e impedir acesso à flash 3,3 V | T “Writing to flash succeeds but program doesn’t run”; BOOT “Other Pins”; R §3 |
| Monitor causa reset/download | Evitar DTR/RTS ativos; no PlatformIO, `monitor_rts = 0` e `monitor_dtr = 0` se ocorrer | R §11; BOOT “Automatic Bootloader” |
| Sem mensagens na serial | ROM a 115200; GPIO15 baixo pode silenciar boot; sketch anterior não escrevia no boot. Ausência de log não prova falta de energia | BOOT “Other Pins”; R §§6/11 |
| FF00 em `get-security-info` | Não suportado no ROM observado; usar leitura documentada das eFuses para avaliar segurança, sem `burn-*` | R §4 |

460800/921600 só devem ser ensaiados em uma tarefa futura autorizada, preferencialmente direto no Mac; **a única taxa comprovada no README é 115200**. Nenhum sucesso de gravação, restauração, verificação ou monitoramento é reivindicado por este documento.
