// TFT_eSPI — User_Setup.h para ESP32-2432S032C (CYD 3,2" ST7789 + touch GT911)
// Gerado a partir do dump da placa (ver ../references/placa-2432S032.md). Cada linha traz seu nível de evidência.
// [C] = CONFIRMADO no firmware gravado (disassembly do TFT_eSPI::init / setup), [I] = INFERIDO,
// [V1] = VALIDAR NO PRIMEIRO TESTE.
//
// Uso no PlatformIO: ver platformio.ini (USER_SETUP_LOADED + -include).
// Uso no Arduino IDE: copiar sobre libraries/TFT_eSPI/User_Setup.h.

#define USER_SETUP_ID 2432032

// ---- Controlador ----------------------------------------------------------
#define ST7789_DRIVER            // [C] sequência de init = ST7789_Init.h (0xB2,0xB7,0xBB,0xC0..0xC6,0xD0,E0/E1)
#define TFT_WIDTH  240           // [C] construtor TFT_eSPI(240,320) e CASET 0..0xEF
#define TFT_HEIGHT 320           // [C] RASET 0..0x13F
#define TFT_RGB_ORDER TFT_BGR    // [I] MADCTL=0x08 (bit BGR) na init. [V1] se vermelho/azul trocados, use TFT_RGB
// Inversão: a init observada envia INVON (0x21). Não defina TFT_INVERSION_ON/OFF de início.
// [V1] se as cores saírem invertidas (fundo branco quando pedir preto), defina TFT_INVERSION_OFF.

// ---- Barramento SPI da tela ------------------------------------------------
#define TFT_MISO 12              // [C] SPIClass::begin(14, 12, 13, -1)
#define TFT_MOSI 13              // [C]
#define TFT_SCLK 14              // [C]
#define TFT_CS   15              // [C] pinMode(15,OUTPUT)+digitalWrite(15,HIGH) no init
#define TFT_DC    2              // [C] pinMode(2,OUTPUT)+digitalWrite(2,HIGH) no init
#define TFT_RST  -1              // [C] nenhum pino de reset acionado no init (reset por software 0x01)

// ---- Backlight -------------------------------------------------------------
#define TFT_BL   27              // [C] pinMode(27,OUTPUT)+digitalWrite(27,HIGH) no setup e no init
#define TFT_BACKLIGHT_ON HIGH    // [C] backlight ligado com nível alto

// ---- Porta SPI -------------------------------------------------------------
// [I] O cartão SD usa outros pinos (18/19/23, CS 5). Para usar SD e tela juntos, a tela
// deve ficar no HSPI. O firmware analisado não permite afirmar qual porta usava. [V1] ao usar SD.
#define USE_HSPI_PORT

// ---- Velocidades -----------------------------------------------------------
#define SPI_FREQUENCY       40000000  // [C] literal 40000000 passado ao beginTransaction
#define SPI_READ_FREQUENCY  20000000  // [NÃO VERIFICADO] valor padrão do TFT_eSPI
// Touch NÃO é do TFT_eSPI: GT911 é I2C (SDA 33, SCL 32, addr 0x5D). Não defina TOUCH_CS.

// ---- Fontes (escolha de projeto, não é dado da placa) -----------------------
#define LOAD_GLCD
#define LOAD_FONT2
#define LOAD_FONT4
#define LOAD_FONT6
#define LOAD_FONT7
#define LOAD_FONT8
#define LOAD_GFXFF
#define SMOOTH_FONT
