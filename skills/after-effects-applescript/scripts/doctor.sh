#!/usr/bin/env bash
# Diagnóstico do ambiente do servidor ae-applescript-mcp. Somente leitura.
# Uso: bash scripts/doctor.sh   (respeita AE_APP_PATH)
APP="${AE_APP_PATH:-/Applications/Adobe After Effects 2027/Adobe After Effects 2027.app}"
ok()   { printf 'OK    %s\n' "$1"; }
fail() { printf 'FALHA %s\n      → %s\n' "$1" "$2"; FAILED=1; }

[ "$(uname)" = Darwin ] && ok "macOS $(sw_vers -productVersion)" || fail "não é macOS" "o servidor só funciona no macOS"
command -v uv >/dev/null && ok "uv $(uv --version | cut -d' ' -f2)" || fail "uv ausente" "instale: brew install uv"

if [ -d "$APP" ]; then
  ok "app: $(defaults read "$APP/Contents/Info" CFBundleShortVersionString 2>/dev/null) em $APP"
else
  fail "After Effects não encontrado em $APP" "ajuste AE_APP_PATH; instalados: $(ls -d /Applications/Adobe\ After\ Effects*/*.app 2>/dev/null | tr '\n' ' ')"
  exit 1
fi

if [ "$(osascript -e "application \"$APP\" is running" 2>/dev/null)" != true ]; then
  fail "After Effects fechado" "peça ao usuário para abrir o After Effects e esperar a tela inicial; o servidor não abre o app"
  exit 1
fi
ok "After Effects aberto"

OUT=$(mktemp "${TMPDIR:-/tmp}/ae-doctor.XXXXXX")
RES=$(osascript - "var f=new File('$OUT'); f.open('w'); f.write(app.version + '|' + app.project.numItems + '|' + app.project.dirty); f.close();" <<OSA 2>&1
on run argv
  with timeout of 20 seconds
    tell application "$APP" to return DoScript (item 1 of argv) override true
  end timeout
end run
OSA
)
case "$RES" in
  *-1743*) fail "Automação negada" "Ajustes do Sistema › Privacidade e Segurança › Automação: permita que este app controle o 'Adobe After Effects'";;
  *-1712*) fail "AE não respondeu em 20 s" "o AE está ocupado (render, diálogo aberto?); peça ao usuário para verificar a janela do AE";;
  0) if [ -s "$OUT" ]; then IFS='|' read -r V N D < "$OUT"; ok "DoScript funcionando (AE $V, $N itens no projeto, alterações não salvas: $D)";
     else fail "DoScript não gravou resultado" "há um diálogo aberto no AE? peça ao usuário para fechá-lo"; fi;;
  *) fail "DoScript devolveu '$RES'" "provável diálogo/alerta aberto no AE; peça ao usuário para fechá-lo";;
esac
rm -f "$OUT"
[ -z "$FAILED" ] && echo "Tudo certo." || exit 1
