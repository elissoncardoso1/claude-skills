// Esqueleto testado para ESP32-2432S032C: tela ST7789 (TFT_eSPI) + touch GT911 (I2C, sem biblioteca).
// Paisagem 320x240 (setRotation(1)). O GT911 reporta em retrato 240x320; getTouch converte.
#include <Arduino.h>
#include <TFT_eSPI.h>
#include <Wire.h>

constexpr uint8_t GT_SDA = 33, GT_SCL = 32, GT_ADDR = 0x5D;
// Calibração: se o toque cair no lugar errado, olhe "DBG touch" na serial e ajuste.
#define TOUCH_SWAP_XY 0
#define TOUCH_INV_X   0
#define TOUCH_INV_Y   0

TFT_eSPI tft;
uint16_t gtMaxX = 240, gtMaxY = 320;
bool touchOk = false;

bool gtRead(uint16_t reg, uint8_t *buf, uint8_t n) {
  Wire.beginTransmission(GT_ADDR);
  Wire.write(reg >> 8); Wire.write(reg & 0xFF);      // registrador de 16 bits, MSB primeiro
  if (Wire.endTransmission() != 0) return false;
  if (Wire.requestFrom(GT_ADDR, n) != n) return false;
  for (uint8_t i = 0; i < n; i++) buf[i] = Wire.read();
  return true;
}

void gtWrite(uint16_t reg, uint8_t v) {
  Wire.beginTransmission(GT_ADDR);
  Wire.write(reg >> 8); Wire.write(reg & 0xFF); Wire.write(v);
  Wire.endTransmission();
}

// true se há dedo; x/y em coordenadas da tela em paisagem.
bool getTouch(int &x, int &y) {
  uint8_t st;
  if (!gtRead(0x814E, &st, 1) || !(st & 0x80)) return false;   // bit7 = buffer pronto
  uint8_t p[4];
  bool ok = (st & 0x0F) && gtRead(0x8150, p, 4);                // 1º ponto: X lo/hi, Y lo/hi
  gtWrite(0x814E, 0);                                           // sempre zerar, senão trava
  if (!ok) return false;
  long rx = p[0] | (p[1] << 8), ry = p[2] | (p[3] << 8);
  if (TOUCH_SWAP_XY) std::swap(rx, ry);
  int px = rx * 240 / gtMaxX, py = ry * 320 / gtMaxY;           // retrato
  if (TOUCH_INV_X) px = 239 - px;
  if (TOUCH_INV_Y) py = 319 - py;
  x = py; y = 239 - px;                                         // retrato -> rotação 1
  Serial.printf("DBG touch raw=%ld,%ld tela=%d,%d\n", rx, ry, x, y);
  return true;
}

void setup() {
  Serial.begin(115200);
  pinMode(TFT_BL, OUTPUT);
  digitalWrite(TFT_BL, TFT_BACKLIGHT_ON);
  tft.init();
  tft.setRotation(1);
  tft.fillScreen(TFT_BLACK);

  Wire.begin(GT_SDA, GT_SCL);
  uint8_t id[4] = {0}, mx[4];
  touchOk = gtRead(0x8140, id, 4) && id[0] == '9';              // Product ID "911"
  if (touchOk && gtRead(0x8048, mx, 4)) {                       // resolução configurada no GT911
    uint16_t ax = mx[0] | (mx[1] << 8), ay = mx[2] | (mx[3] << 8);
    if (ax && ay) { gtMaxX = ax; gtMaxY = ay; }
  }
  Serial.printf("GT911 id=%.4s max=%ux%u\n", (char *)id, gtMaxX, gtMaxY);
  tft.drawCentreString(touchOk ? "TOQUE NA TELA" : "TOUCH FAIL", 160, 112, 4);
}

void loop() {
  static uint32_t last = 0;
  int x, y;
  if (millis() - last > 20 && getTouch(x, y)) {                 // ~50 Hz basta; poll mais rápido não ajuda
    last = millis();
    tft.fillCircle(x, y, 4, TFT_YELLOW);
  }
}
