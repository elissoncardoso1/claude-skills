# Example: 1080×1350 social post (MCP) — executed 2026-10-22, result verified

Request: "Post 4:5 with the photo on top, title 'Coleção Outono', editable."

```
doc_new        {width:1080, height:1350, background:"#101820", name:"social-post"}   → {document:1}
doc_place      {path:"_claude-photocraft-test/in/base.png", center:[540,520]}         → {layer:10, scale:67.5, smartObject:true}
command_run    {id:"type.fonts", params:{family:"Helvetica"}}                          → Bold face exists
command_batch  steps:
  layer.newAdjustmentLayer.hueSaturation {saturation:-30}        → {layer:11}
  layer.createClippingMask {}                                    → clips to the photo only
  type.create {x:540, y:1050, text:"Coleção Outono", font:"Helvetica", fontStyle:"Bold", size:88, color:"#ffffff", align:"center"}
  type.create {x:540, y:1130, text:"Novidades na loja", font:"Helvetica", size:40, color:"#f2c14e", align:"center"}
  shape.create {kind:"rect", rect:[440,1190,200,6], fill:"#f2c14e"}
                                                                  → completed:5 failed:0
render_preview {max_side:600}     → checked: text centred, accents OK, desaturation only on the photo
doc_save       {path:"_claude-photocraft-test/out/social-post.pcraft"}
doc_export     {path:"_claude-photocraft-test/out/social-post.png"}   → warning: layers flattened (expected)
```
Visual note (judgement): large empty band above the photo; a next iteration would move the photo up or scale it to fill.
