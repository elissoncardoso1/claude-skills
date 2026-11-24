# LVGL 8 e 9: port mínimo, memória e diferenças de API

## Escopo e versões de referência

**Receitas documentais; não compiladas nem executadas.** Não são um sketch completo:
as inicializações TFT/GT911 e a orientação física devem vir da configuração local.
O [`README.md`](relatorio-unidade.md), §§3 e 7–8, prevalece: ESP32 clássico, PSRAM ausente
**por inferência**, ST7789 **240×320/retrato**, GT911 I2C 0x5D em SDA33/SCL32.
Para os exemplos **320×240/paisagem**, primeiro configurar e validar a rotação do
painel e transformar o touch para o mesmo espaço; não mudar a identificação física.

Bases: **v8.4.0** [8], **v9.6.0** [9]. O clone LVGL [HEAD] já é **10.0.0-dev**,
embora `library.json` ainda diga 9.6.0. Não usar seu template como se fosse release v9.
O HEAD smartdisplay [S] pede `^9.3.0`; sua integração não foi testada com 9.6.0.
Ver a matriz e os snapshots de releases em [versoes.md](versoes.md).

## `lv_conf.h`: sempre o template da versão efetivamente usada

Copiar **o template correspondente**, renomear para `lv_conf.h`, trocar seu `#if 0`
inicial por `#if 1` e fornecer o diretório ao compilador. Com inclusão simples,
definir `LV_CONF_INCLUDE_SIMPLE` no build da biblioteca, não só no sketch.
Não basta incluir o arquivo na aplicação se o LVGL foi compilado com outra configuração.
Fontes: [8] `lv_conf_template.h`, cabeçalho; [9] template e “Configuration”.

| Assunto | v8.4.0 [8] | v9.6.0 [9] |
|---|---|---|
| RGB565 | `LV_COLOR_DEPTH 16` | `LV_COLOR_FORMAT_DEFAULT LV_COLOR_FORMAT_RGB565` |
| Swap de 16 bits | `LV_COLOR_16_SWAP 0` para os exemplos abaixo | Formato normal RGB565; se escolher `RGB565_SWAPPED`, não trocar novamente no driver |
| Tick Arduino | `LV_TICK_CUSTOM 1`, incluir `Arduino.h`, expressão `millis()` | `lv_tick_set_cb()` no código; não copiar macros `LV_TICK_CUSTOM` do v8 |
| Heap interno LVGL | `LV_MEM_CUSTOM 0`, `LV_MEM_SIZE` (template: 48 KiB) | `LV_USE_STDLIB_MALLOC LV_STDLIB_BUILTIN`, `LV_MEM_SIZE` (template: 65536 bytes) |
| Resolução | `disp_drv.hor_res/ver_res` | `lv_display_create(hor_res, ver_res)` |
| Refresh parcial | `full_refresh = 0`, `direct_mode = 0` | `LV_DISPLAY_RENDER_MODE_PARTIAL` |

**Não generalizar o template 9.6 a todo 9.x.** O README smartdisplay [S], “Step 5”,
para sua integração orientada a 9.3.0 manda `LV_COLOR_DEPTH 16`; já o template 9.6
usa `LV_COLOR_FORMAT_DEFAULT` e sua documentação trata `LV_COLOR_DEPTH` como derivado.
Não adicionar `LV_COLOR_16_SWAP` a uma configuração v9 esperando o comportamento v8.

## Orçamento RGB565 sem depender de PSRAM

Proposta inicial, **não medição de RAM livre**: um buffer estático de **24 linhas**
(1/10 de 240). A recomendação de buffers em torno de 1/10 está nos ports oficiais [8,9].

| Área | Pixels | Bytes RGB565 |
|---|---:|---:|
| 320 × 24, um buffer | 7680 | **15360** |
| Dois buffers de 24 linhas | 15360 | **30720** |
| 320 × 240, quadro inteiro | 76800 | **153600** |
| Dois quadros inteiros | 153600 | **307200** |

Conta: `largura × linhas × 2`. Não usar um framebuffer completo por hábito:
além desses bytes existem heap LVGL, pilhas, Wi-Fi, fontes, imagens e buffers do driver.
Manter um buffer para começar; dois só se houver memória e transferência realmente
assíncrona para sobrepor desenho e envio [8,9], “One buffer” / “Two buffers”.
Buffers estáticos sobrevivem ao retorno da função; não colocar o draw buffer na pilha.
Para DMA, o driver precisa garantir alinhamento e memória apta ao periférico;
não supor que qualquer `malloc` ou PSRAM serve. Os exemplos abaixo são **bloqueantes**.
Se alterar stride/alinhamento em v9, recalcular pelo stride real; a conta acima usa
linhas RGB565 contíguas e `LV_DRAW_BUF_STRIDE_ALIGN 1` do template 9.6 [9].

## Display v8: capacidade em pixels

Fragmentos alternativos: escolher **v8 ou v9**, não compilar ambos.
Supõe `tft` TFT_eSPI já inicializado para 320×240 e `lv_init()` chamado antes do port.
Fonte da API: [8], “Draw buffer”, “Display driver” e `lv_hal_disp.h`.
A função `enviar565` está na seção “Transporte e byte order”.

```cpp
static lv_disp_draw_buf_t draw8;
static lv_disp_drv_t drv8;
static lv_color_t buf8[320 * 24];
static_assert(sizeof(lv_color_t) == 2, "Requer LV_COLOR_DEPTH 16");

static void flush8(lv_disp_drv_t *d, const lv_area_t *a, lv_color_t *p) {
    enviar565(a, reinterpret_cast<uint16_t *>(p));
    lv_disp_flush_ready(d); // envio bloqueante terminou
}

void registrar_display8() {
    lv_disp_draw_buf_init(&draw8, buf8, nullptr, 320 * 24); // PIXELS
    lv_disp_drv_init(&drv8);
    drv8.hor_res = 320;
    drv8.ver_res = 240;
    drv8.draw_buf = &draw8;
    drv8.flush_cb = flush8;
    drv8.full_refresh = 0;
    drv8.direct_mode = 0;
    lv_disp_drv_register(&drv8);
}
```

## Display v9.6: capacidade em bytes

Usar buffer de bytes/words RGB565, **não assumir que `sizeof(lv_color_t) == 2` no v9**.
O formato pertence ao display; `lv_display_set_color_format` não realoca buffers
se depois for trocado por um formato maior [9], “Color Format”.

```cpp
alignas(4) static uint8_t buf9[320 * 24 * 2];

static void flush9(lv_display_t *d, const lv_area_t *a, uint8_t *p) {
    enviar565(a, reinterpret_cast<uint16_t *>(p));
    lv_display_flush_ready(d); // envio bloqueante terminou
}

lv_display_t *registrar_display9() {
    lv_display_t *d = lv_display_create(320, 240);
    if (!d) return nullptr; // aplicação deve interromper a criação da UI
    lv_display_set_color_format(d, LV_COLOR_FORMAT_RGB565);
    lv_display_set_buffers(d, buf9, nullptr, sizeof(buf9),
                           LV_DISPLAY_RENDER_MODE_PARTIAL); // BYTES
    lv_display_set_flush_cb(d, flush9);
    return d;
}
```

Fontes: [9], “Creating a Display”, “Draw Buffer(s)”, “Flush Callback” e
`include/lvgl/display/lv_display.h`, `lv_display_create` / `lv_display_set_buffers`.
Não passar **7680** ao registro v9 como se fossem pixels, nem **15360** ao v8
como se fossem bytes: o primeiro subdimensiona, o segundo anuncia memória inexistente.

## Transporte e byte order

Adaptador **TFT_eSPI bloqueante** comum aos dois fragmentos, com RGB565 **normal**
na memória. Fonte: [T], `TFT_eSPI.cpp`, `pushColors(uint16_t*, uint32_t, bool)`.
A área LVGL tem extremos **inclusivos**, por isso `+1` na largura e altura [8,9].

```cpp
static void enviar565(const lv_area_t *a, uint16_t *pixels) {
    const uint32_t w = a->x2 - a->x1 + 1;
    const uint32_t h = a->y2 - a->y1 + 1;
    tft.startWrite();
    tft.setAddrWindow(a->x1, a->y1, w, h);
    tft.pushColors(pixels, w * h, true); // esta sobrecarga conta PIXELS
    tft.endWrite();
}
```

- Para este caminho, v8 `LV_COLOR_16_SWAP=0`, v9 formato `RGB565`, e **uma** troca
  na transmissão (`pushColors(..., true)`). Não pré-trocar o buffer também.
- Atenção à sobrecarga TFT: `pushColors(uint8_t*, len)` recebe **bytes**;
  `pushColors(uint16_t*, len, swap)` recebe **pixels** [T], implementação e comentários.
  `setSwapBytes` também existe para `pushImage`; não misturar contratos de APIs.
- **v9.6** oferece `LV_COLOR_FORMAT_RGB565_SWAPPED` nativamente [9], “Swapping
  Endian-ness”. Se optar por ele, usar transporte que preserve a ordem já produzida;
  o adaptador acima foi escrito para o formato normal, não para esse formato.
- A ordem dos **bytes** de RGB565 não é a ordem **RGB/BGR** do controlador.
  Corrigir vermelho/azul trocados via configuração RGB/BGR não equivale a corrigir
  os dois bytes de cada pixel. Validar vermelho, verde, azul, preto e branco;
  inversão ST7789 é ainda outro ajuste (README local §7).
- Com LovyanGFX, adaptar o flush a `pushImage`/`pushPixels` e ao contrato de swap
  escolhido [G]; não copiar parâmetros do TFT cegamente. Se usar DMA/assíncrono,
  só sinalizar `*_flush_ready` quando o consumidor terminar de ler o buffer.
  LovyanGFX 1.3.0 documenta espera no **destino** com `waitDMA()` para fontes ainda
  em uso, inclusive sprites; `endWrite()` e modo da transação fazem diferença [R,G].
- Em `esp_lcd_panel_draw_bitmap`, o fim da região é **exclusivo**: usar `x2+1,y2+1`.
  O port smartdisplay [S], `lv_flush_hardware`, faz isso e troca RGB565 para um
  staging buffer, concluindo pelo callback de transferência. Não copiá-lo como
  prova de RAM suficiente: há uma alocação extra e fallback a PSRAM inexistente
  segundo a hipótese local; revisar também falhas de alocação antes de adotá-lo.

## Tempo: tick não substitui o handler

v8.4 Arduino, editar estas opções **no template v8** [8], “HAL SETTINGS”:

```c
#define LV_TICK_CUSTOM 1
#define LV_TICK_CUSTOM_INCLUDE "Arduino.h"
#define LV_TICK_CUSTOM_SYS_TIME_EXPR (millis())
```

v9.6 Arduino, depois de `lv_init()` [9], “Tick Interface” / `lv_tick.h`:

```cpp
static uint32_t tick_ms() { return millis(); }
// Em setup(), após lv_init():
// lv_tick_set_cb(tick_ms);
```

Em IDF nativo, a expressão equivalente é
`(uint32_t)(esp_timer_get_time() / 1000LL)` com `esp_timer.h`: converter
**microssegundos para milissegundos** [8] template; [9] “Tick Interface”.
Alternativa: `lv_tick_inc(periodo_ms)` em fonte periódica confiável.
Escolher **uma fonte**, não incrementar também quando o tempo já vem de callback.
Não assumir que um tick FreeRTOS equivale a 1 ms: converter a unidade se usar o RTOS.

Ambas as majors precisam de `lv_timer_handler()` regularmente [8,9].
Ponto inicial simples Arduino, **não promessa de FPS ou periodicidade exata**:

```cpp
void loop() {
    lv_timer_handler();
    delay(5);
}
```

Evitar I/O demorado nesse loop. `delay(5)` não mede o tempo gasto renderizando;
`lv_tick_inc(5)` por iteração acumularia erro quando o loop atrasar.
No RTOS, concentrar LVGL numa task ou proteger acessos com o mesmo mutex;
LVGL não é thread-safe [9], “Operating Systems and Threads”. Não desenhar widgets
na ISR; limitar o caminho periódico ao mecanismo de tempo permitido.

## Touch: callback mudou, o protocolo GT911 não vem do LVGL

Registrar após criar o display [8], “Input device interface”. O código de leitura
GT911 precisa fornecer **estado atual** e coordenadas já transformadas para paisagem.
Sem toque: `LV_INDEV_STATE_RELEASED`; com toque válido: `LV_INDEV_STATE_PRESSED`,
`data->point.x` em 0..319 e `data->point.y` em 0..239.
Não converter falha I2C em toque em (0,0); liberar o estado e registrar o erro.
Validar os quatro cantos antes de assumir troca/inversão de eixos (README local §13).

| Etapa | v8.4 [8], “Touchpad, mouse or any pointer” | v9.6 [9], “Touchpad and Mouse / Example” |
|---|---|---|
| Assinatura de leitura | `void read8(lv_indev_drv_t *drv, lv_indev_data_t *data)` | `void read9(lv_indev_t *indev, lv_indev_data_t *data)` |
| Criar | `static lv_indev_drv_t in; lv_indev_drv_init(&in);` | `lv_indev_t *in = lv_indev_create();` |
| Tipo | `in.type = LV_INDEV_TYPE_POINTER;` | `lv_indev_set_type(in, LV_INDEV_TYPE_POINTER);` |
| Callback | `in.read_cb = read8;` | `lv_indev_set_read_cb(in, read9);` |
| Registrar/associar | `lv_indev_drv_register(&in);` | `lv_indev_set_display(in, display);` |

O corpo das duas callbacks preenche os mesmos campos `point` e `state`; muda o tipo
do primeiro argumento. Isso não implementa I2C, reset/INT, rotação ou polling GT911.
Não usar exemplo de touch resistivo XPT2046 como se fosse o GT911 desta placa.
Com smartdisplay, `smartdisplay_init()` já cria os dispositivos [S], README “Step 7”;
não registrar outro port TFT/GT911 por cima nem duplicar a fonte de tick.

## Fontes e commits

Base dos caminhos: `fontes/repositorios/`. URLs imutáveis por commit, horários e
SHA-256 dos suplementos: `suplementos/MANIFESTO-parte.md` (base local `esp32-docs/fontes/repositorios/suplementos/MANIFESTO-parte.md`, não publicada).
As abreviações abaixo representam **prefixos de nomes de arquivo**, não novos diretórios.

- **[8]** v8.4.0 @ `4495f428630cc1741bd8bfd977f080e8460e8e8d`, em `suplementos/`:
  `lvgl__lvgl__lv_conf_template.h`; `lvgl__lvgl__src__hal__lv_hal_disp.h`;
  prefixo `lvgl__lvgl__docs__porting__` + `display.md`, `indev.md`, `tick.md`,
  `timer-handler.md`; `lvgl__lvgl__docs__get-started__quick-overview.md`.
- **[9]** v9.6.0 @ `80ca777e37a2b176770726a02e07a6fb79ef0b39`, em `suplementos/`:
  `lvgl__v9.6.0__lv_conf_template.h`; prefixo `lvgl__v9.6.0__docs__src__` +
  `main-modules__display__setup.mdx`, `main-modules__display__color_format.mdx`,
  `main-modules__indev__pointer.mdx`, `integration__overview.mdx`,
  `integration__configuration.mdx`, `main-modules__timer.mdx`;
  prefixo `lvgl__v9.6.0__include__lvgl__` + `display__lv_display.h`, `tick__lv_tick.h`,
  `indev__lv_indev.h` (inclui `lv_indev_set_display`).
- **[HEAD]** clone `lvgl__lvgl/` @ `ab2a8b4ba503917ede0769ce9d5b254ca0b8f37d`:
  `include/lvgl/lv_version.h`, `library.json` (divergência de versão).
- **[T]** `Bodmer__TFT_eSPI/` @ `16e37595040eac69cd628e4bffb56fc30cad6299`:
  `TFT_eSPI.cpp`, `pushColors`, `setSwapBytes`, `pushImage`.
- **[G]** LovyanGFX 1.3.0 @ `dd228d15a03900ce658fd62e120dc7cc489915dd`:
  `suplementos/lovyan03__LovyanGFX__src__lgfx__v1__LGFXBase.hpp`,
  `pushImage`, `pushPixels`, `setSwapBytes`, `waitDMA`.
- **[R]** `releases/lovyan03__LovyanGFX.latest.json`, `body`, “Breaking changes”:
  snapshot da release 1.3.0, sem commit próprio do JSON; commit da tag em [G].
- **[S]** `rzeldent__esp32-smartdisplay/` @ `38e9ebabe3e4044159c4e95192d432607ed70588`:
  `library.json`, `README.md` (“Step 5”, “Step 7”, “Ticker”),
  `include/lvgl_panel_common.h`, funções `lvgl_create_display`, `lv_flush_hardware`,
  `lvgl_panel_color_trans_done`; `src/lvgl_touch_gt911_i2c.c` (port GT911).
