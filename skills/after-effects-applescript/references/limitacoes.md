# O que não dá para fazer com ae_*

| Pedido | Situação | Alternativa |
|---|---|---|
| "Renderize agora" | o servidor só enfileira; render bloqueia o AE | o usuário clica em Render no AE ou usa `aerender` |
| "Me mostre como ficou" (imagem) | sem preview ou screenshot | descreva o estado lido por `ae_inspect_comp` |
| Importar footage, áudio ou imagem | não há ferramenta | `ae_run_extendscript`, se o usuário habilitar; senão, o usuário importa |
| Curvas de easing personalizadas, easing espacial | só `linear`, `ease` ou `hold` por trilha | aproxime com mais keyframes |
| Remover item da fila de render | não há ferramenta | o usuário remove no painel Render Queue |
| Câmeras, luzes, 3D, máscaras, expressões | não há ferramenta | `ae_run_extendscript` (habilitado pelo usuário) |
| Mais de 50 itens / 100 camadas / 20 keyframes por leitura | a resposta é truncada (`truncated:true`) | filtre por `comp_name` |
| AE fechado, ou um diálogo aberto no AE | o servidor não abre o app nem clica em diálogos | o usuário abre o app ou fecha o diálogo |
| Nomes de efeito em português | o nome exibido depende do idioma do AE | use o matchName (`ADBE Gaussian Blur 2`, `ADBE Fill`, `ADBE Glo2`) |
| Windows | só macOS | — |

Detalhes técnicos: `docs/LIMITACOES.md` do repositório.
