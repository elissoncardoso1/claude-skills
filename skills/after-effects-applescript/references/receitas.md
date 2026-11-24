# Receitas (sequências de ferramentas)

Todas usam `comp_name`. Valores entre `<>` são do pedido.

## Lower third (barra + nome entrando da esquerda)
1. `ae_add_layer {layer_type:"shape_rectangle", width:800, height:120, color:"<cor>", position:[560,900], name:"Barra"}`
2. `ae_add_layer {layer_type:"text", text:"<nome>", name:"Nome", position:[200,915]}`: agora Nome=1 e Barra=2
3. `ae_set_keyframes {tracks:[`
   `{layer_index:2, property:"position", easing:"ease", keyframes:[{time:0,value:[-400,900]},{time:0.5,value:[560,900]}]},`
   `{layer_index:1, property:"position", easing:"ease", keyframes:[{time:0,value:[-760,915]},{time:0.5,value:[200,915]}]}]}`

## Pulso (logo ou elipse)
`ae_add_layer {layer_type:"shape_ellipse", width:300, height:300, color:"<cor>"}` e depois
`ae_set_keyframes {tracks:[{layer_index:1, property:"scale", keyframes:[{time:0,value:[100,100]},{time:0.5,value:[120,120]},{time:1,value:[100,100]}]}]}`

## Fundo desfocado com cor sobreposta
1. `ae_add_layer {layer_type:"solid", color:"<cor>"}`
2. `ae_apply_effect {layer_index:1, effect:"Gaussian Blur", params:{Blurriness:25}}`
3. `ae_apply_effect {layer_index:1, effect:"ADBE Fill", params:{Color:"#F05378", Opacity:0.4}}`
   O Fill com `Opacity` 1 (o padrão) **substitui** toda a cor da camada. Para "sobreposição" ou "tingir", use 0.3–0.6. Para "trocar a cor", use 1.

## Sequência de palavras (uma após a outra, centralizadas)
Adicione as camadas em ordem inversa (a última palavra primeiro, sempre com `color`). Assim a primeira palavra fica no índice 1.
Tempos e centralização vão no mesmo lote (comp 1920x1080):
`ae_set_layer_properties {changes:[{layer_index:1,in_point:0,out_point:2,justification:"center",center_anchor:true,position:[960,540]}, {layer_index:2,in_point:2,out_point:4, …mesmo}, {layer_index:3,in_point:4,out_point:6, …mesmo}]}`

## Contagem regressiva 3-2-1
`ae_add_layer {layer_type:"text", text:"3"}` e depois
`ae_set_keyframes {tracks:[{layer_index:1, property:"Text/Source Text", easing:"hold", keyframes:[{time:0,value:"3"},{time:1,value:"2"},{time:2,value:"1"}]}]}`

## Rotação orbital
Crie os textos "A" e "B", depois `ae_add_layer {layer_type:"null_object", name:"Controle", position:[540,540]}` (índice 1).
Em seguida: `ae_set_layer_properties {changes:[{layer_index:2,parent_index:1},{layer_index:3,parent_index:1}]}`
e `ae_set_keyframes {tracks:[{layer_index:1, property:"rotation", keyframes:[{time:0,value:0},{time:4,value:360}]}]}`

## Efeito só num trecho
`ae_add_layer {layer_type:"adjustment"}`, depois `ae_apply_effect {layer_index:1, effect:"Glow"}`, depois
`ae_set_layer_properties {changes:[{layer_index:1, in_point:2, out_point:4}]}`

## Salvar e entregar
1. Pergunte ao usuário onde salvar.
2. `ae_save_project_as {path:"/abs/projeto.aep"}`
3. `ae_queue_render {output_path:"/abs/video.mp4"}`
4. Diga ao usuário: "Está na fila de render; clique em Render no After Effects."

## Animar parâmetro de efeito
Use o caminho que `ae_apply_effect` devolve:
`ae_set_keyframes {tracks:[{layer_index:1, property:"Effects/Gaussian Blur/Blurriness", keyframes:[{time:0,value:40},{time:1,value:0}]}]}`
