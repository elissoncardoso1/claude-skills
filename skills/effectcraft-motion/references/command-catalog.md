# Command catalog: EffectCraft 0.17.0 (generated)

Generated from `effectcraft-cli exec command.list --params '{"schemas":true}' --json` (734 commands). Do not edit by hand.

- `params` is the engine's own parameter doc (`?` = optional). Unknown keys are rejected with the accepted list.
- Full JSON Schema of any command: `effectcraft-cli exec command.describe '{"command":"ID"}' --empty --json` or MCP `describe_command {command}`.
- *Disabled on an empty project* means the command needs context (a selection, a saved file…); the `why` column explains.
- Search: `grep -n '^| \`keys\.' command-catalog.md`

## comp (31)

| id | label | params | why disabled (empty project) |
|---|---|---|---|
| `comp.activateRecent` | Activate Most Recent Composition in Hierarchy | {comp?} |  |
| `comp.addMarker` | Add Marker | {time?, comment?} |  |
| `comp.close` | Close Composition | {comp?} |  |
| `comp.copyFrame` | Copy Frame to Clipboard | {comp?, time?, scale?} |  |
| `comp.cropToLayerBounds` | Crop Comp to Selected Layer(s) Bounds | {layers?} | select a layer first |
| `comp.cropToRegionOfInterest` | Crop Comp to Region of Interest | {comp?} | draw a region of interest in the viewer first |
| `comp.deletePreset` | Delete Composition Preset | {name} |  |
| `comp.flowchart` | Composition Flowchart | {} |  |
| `comp.info` | Composition Info | {comp?} |  |
| `comp.miniFlowchart` | Composition Mini-Flowchart | {} |  |
| `comp.new` | New Composition... | {name?, width?, height?, frameRate?, duration? (s), startTime? (s) \| startTimecode?, background? [r,g,b]\|#hex, pixelAspect?, shutterAngle?, shutterPhase?, motionBlurSamples?, adaptiveSampleLimit? (16–256), preserveFrameRate?: bool, preserveResolution?: bool, renderer?: classic3D\|advanced3D, anchor?, open?} |  |
| `comp.open` | Open Composition | {comp: id\|name} |  |
| `comp.openInEssentialGraphics` | Open in Essential Graphics | {comp?} → makes it the Essential Graphics panel's Primary composition and shows the panel |  |
| `comp.presets` | Composition Presets | {} |  |
| `comp.renderer` | Renderer | {renderer?: advanced3d\|classic3d (omit to read), value?} |  |
| `comp.responsiveTime` | Responsive Design — Time | {op: intro\|outro\|workArea} |  |
| `comp.revealInProject` | Reveal Composition in Project | {comp?} |  |
| `comp.saveFrameAs` | File... | {path (.png; with queue: an output path or template), time?, scale?, queue?: bool (add a Render Queue item from the Frame Default templates instead of writing now)} |  |
| `comp.saveFrameAsExr` | ProEXR... | {path (.exr), comp?, time?, scale?} → a multi-layer OpenEXR: composite R,G,B,A + `<layer>.R/G/B/A` per layer (linear, premultiplied) |  |
| `comp.saveFrameAsPsd` | Photoshop Layers... | {path (.psd), comp?, time?, scale?} → a layered PSD: one layer per visible comp layer (blend mode, opacity) + the merged frame |  |
| `comp.savePreset` | Save Composition Preset | {name, width, height, pixelAspect, frameRate} (replaces a saved preset with the same name) |  |
| `comp.setPosterTime` | Set Poster Time | {} |  |
| `comp.setSwitch` | Composition Switch | {switch: hideShy\|motionBlur\|frameBlending\|draft3d, value?} |  |
| `comp.settings` | Composition Settings... | {comp?, name?, width?, height?, anchor? 0-8 (resize anchor, 4 = center), frameRate?, duration?, startTime? (s) \| startTimecode?, background?, shutterAngle?, shutterPhase?, motionBlurSamples?, adaptiveSampleLimit? (16–256), preserveFrameRate?: bool (nested or in the render queue it shows only its own frames), preserveResolution?: bool (nested, it renders at full size), pixelAspect?, renderer?: classic3D\|advanced3D} |  |
| `comp.trimToWorkArea` | Trim Comp to Work Area | {comp?} |  |
| `comp.vr.createEnvironment` | Create VR Environment... | {comp?, size?: face pixels (1024), position?: [x,y,z]} |  |
| `comp.vr.environments` | VR Environments | {} → [{output, name, cubeMap, faces: [{face, comp, camera}], view: [x, y, z]}] |  |
| `comp.vr.extractCubemap` | Extract Cubemap... | {comp?, faceSize?} |  |
| `comp.vr.setView` | VR View Orientation | {comp? (an environment's output / cube map / face comp), orientation?: [x, y, z] degrees, pan?, tilt?, roll?} → turns the six face cameras together |  |
| `comp.workArea` | Set Work Area | {start?, end?, set?: begin\|end (at CTI)} |  |
| `comp.workAreaToSelection` | Set Work Area to Selected Layers | {comp?, layers? (default the selected layers; the whole composition with none)} |  |

## layer (122)

| id | label | params | why disabled (empty project) |
|---|---|---|---|
| `layer.addItem` | Add Footage to Comp | {item: id\|name, time? (s, the In point), index? (1-based stack position; default above the selected layer), position? ([x, y] comp px; default the centre), duration? (s, for a still)} |  |
| `layer.addMarker` | Add Marker | {layers?, time?, comment?} |  |
| `layer.addMask` | New Mask | {layer?, shape?: rect\|ellipse\|rounded\|polygon\|star, rect? [x,y,w,h] (layer space; a polygon or star fits its width), mode?} | select a layer first |
| `layer.addShapeItem` | Add (Shape) | {layer?, kind: group\|rect\|ellipse\|star\|polygon\|path\|fill\|stroke\|gfill\|gstroke\|trim\|repeater\|round\|offset\|pucker\|twist\|zigzag\|wiggle\|merge\|frontColor\|bevelColor\|sideColor\|backColor, group?: uid\|path} → {uid, path} (frontColor…backColor: the group's Front / Bevel / Side / Back item, which colours that surface of every extruded paint in the group in Advanced 3D) | select a layer first |
| `layer.addTextAnimator` | Animate Text | {layer?, properties: [anchor\|position\|scale\|skew\|rotation\|opacity\|transformAll\|lineAnchor\|lineSpacing\|characterOffset\|characterValue\|blur\|fillColor\|fillHue\|fillSaturation\|fillBrightness\|fillOpacity\|strokeColor\|strokeHue\|strokeSaturation\|strokeBrightness\|strokeOpacity\|strokeWidth\|tracking\|frontColor\|bevelColor\|sideColor\|backColor\|perChar3d], name?} | select a text layer first |
| `layer.addTextAnimatorProperty` | Add Property | {layer?, animator?: uid\|index, property: (see layer.addTextAnimator)} | select a text layer first |
| `layer.addTextSelector` | Add Text Selector | {layer?, animator?: uid\|index, kind: range\|wiggly\|expression} | select a text layer first |
| `layer.align` | Align Layers | {edge: left\|hcenter\|right\|top\|vcenter\|bottom, to?: composition\|selection (default composition), layers?} | select a layer first |
| `layer.alignVideoToData` | Align Video to Data | {layer?, data?: data footage id\|name, key?: time field, videoStart?: ISO date-time \| hh:mm:ss \| timecode \| seconds (default: file creation time), dataStart? (comp s of the first sample, 0)} | select a layer first |
| `layer.applyTextPreset` | Apply Text Animation Preset | {layer?, preset: typewriter\|fadeUpCharacters\|bounceInWords\|trackingIn\|scramble\|blurIn\|jitter\|dropInLines} | select a text layer first |
| `layer.arrange` | Arrange | {layers?, to: front\|forward\|backward\|back, index?, above?: layer} | select a layer first |
| `layer.autoOrient` | Auto-Orient... | {mode: off\|alongPath\|towardsCamera\|towardsPointOfInterest, layers?} | select a layer first |
| `layer.autoTrace` | Auto-trace... | {layer?, timeSpan?: currentFrame\|workArea, channel?: alpha\|red\|green\|blue\|luminance, invert?, blur? (px, 1), tolerance? (px, 1), threshold? (%, 50), minimumArea? (px, 10), cornerRoundness? (%, 50), applyToNewLayer?} | select a layer first |
| `layer.cameraSettings` | Camera Settings... | {layer?, name?, type?, preset?, zoom?, focalLength?, angleOfView?, dof?, focusDistance?, aperture?, fStop?, blurLevel?, position?, poi?} |  |
| `layer.castsShadows` | Casts Shadows | {layers?, value?} | select a layer first |
| `layer.centerAnchor` | Center Anchor Point in Layer Content | {layers?} | select a layer first |
| `layer.channels` | Layer Channels | {layer?} → {channels: [name], layers: [{name, rgba: [r, g, b, a channel]}]} — a multi-layer OpenEXR layer's channels (EXtractoR's red / green / blue / alpha take these names) |  |
| `layer.create` | Create | {op: editableText\|shapesFromText\|masksFromText\|shapesFromVector, layers?} | select a layer first |
| `layer.deleteAllMarkers` | Delete All Markers | {layers?} | select a layer first |
| `layer.distribute` | Distribute Layers | {mode: left\|hcenter\|right\|top\|vcenter\|bottom (edges or centres), layers?} | select a layer first |
| `layer.enablePerChar3D` | Enable Per-character 3D | {layer?, enabled?: bool, toggle?: bool} | select a text layer first |
| `layer.enableTimeRemap` | Enable Time Remapping | {layers?, value?} | select a layer first |
| `layer.environment` | Environment Layer | {layers?, on?} | select a layer first |
| `layer.expressions` | Enable/Disable Expressions | {layers?, enabled: bool} | select a layer first |
| `layer.extendSelectionNext` | Extend Selection to Next Layer | {} |  |
| `layer.extendSelectionPrevious` | Extend Selection to Previous Layer | {} |  |
| `layer.frameBlending` | Frame Blending | {layers?, mode: off\|frameMix\|pixelMotion} | select a layer first |
| `layer.freezeFrame` | Freeze Frame | {layers?} | select a layer first |
| `layer.freezeOnLastFrame` | Freeze On Last Frame | {layers?} | select a layer first |
| `layer.hideOtherVideo` | Hide Other Video | {layers?} | select a layer first |
| `layer.lightSettings` | Light Settings... | {layer?, name?, kind?: Parallel\|Spot\|Point\|Ambient\|Environment, color?, intensity?, coneAngle?, coneFeather?, falloff?, radius?, falloffDistance?, castsShadows?, shadowDarkness?, shadowDiffusion?, position?, poi?} |  |
| `layer.markersLock` | Lock Markers | {layers?, value?} | select a layer first |
| `layer.mask.featherFalloff` | Feather Falloff | {layer?, mask?, mode: smooth\|linear} | select a layer first |
| `layer.mask.hideLocked` | Hide Locked Masks | {value?} |  |
| `layer.mask.invert` | Inverted | {layer?, mask?, value?} | select a layer first |
| `layer.mask.lock` | Locked | {layer?, mask?, value?} | select a layer first |
| `layer.mask.lockOthers` | Lock Other Masks | {layer?, mask?} | select a layer first |
| `layer.mask.mode` | Mask Mode | {layer?, mask?, mode: None\|Add\|Subtract\|Intersect\|Lighten\|Darken\|Difference} | select a layer first |
| `layer.mask.motionBlur` | Motion Blur | {layer?, mask?, mode: sameAsLayer\|on\|off} | select a layer first |
| `layer.mask.remove` | Remove Mask | {layer?, mask?} | select a layer first |
| `layer.mask.removeAll` | Remove All Masks | {layers?} | select a layer first |
| `layer.mask.reset` | Reset Mask | {layer?, mask?} | select a layer first |
| `layer.mask.selectNext` | Select Next Mask | {layer?} | select a layer first |
| `layer.mask.selectPrevious` | Select Previous Mask | {layer?} | select a layer first |
| `layer.mask.set` | Mask Settings | {layer?, mask?, field: feather\|opacity\|expansion, value} | select a layer first |
| `layer.mask.shape` | Mask Shape... | {layer?, mask?, rect: [x, y, w, h], shape?: rect\|ellipse} | select a layer first |
| `layer.mask.unlockAll` | Unlock All Masks | {layers?} | select a layer first |
| `layer.moveEarlier` | Move Layers 1 Frame Earlier | {layers?} | select a layer first |
| `layer.moveEarlier10` | Move Layers 10 Frames Earlier | {layers?} | select a layer first |
| `layer.moveInToStart` | Move Layer In Point to Beginning of Comp | {layers?} | select a layer first |
| `layer.moveLater` | Move Layers 1 Frame Later | {layers?} | select a layer first |
| `layer.moveLater10` | Move Layers 10 Frames Later | {layers?} | select a layer first |
| `layer.moveOutToEnd` | Move Layer Out Point to End of Comp | {layers?} | select a layer first |
| `layer.new3dPrimitive` | 3D Primitive | {kind: cube\|sphere\|plane\|torus\|cone\|cylinder, name?, width?, height?, depth?, radius?, tubeRadius?, segments?, rings?, position? [x,y,z], baseColor?, metallic?, roughness?, emissive?, castsShadows?, acceptsShadows?, acceptsLights?}; switches a Classic 3D comp to Advanced 3D |  |
| `layer.newAdjustment` | Adjustment Layer | {name?} |  |
| `layer.newCamera` | Camera... | {name?, type?: oneNode\|twoNode (default twoNode), preset?: 15mm\|20mm\|24mm\|28mm\|35mm\|50mm\|80mm\|135mm\|200mm, zoom?, focalLength? mm, angleOfView? deg, dof?, focusDistance?, aperture?, fStop?, blurLevel?, lockToZoom?, position? [x,y,z], poi? [x,y,z]} |  |
| `layer.newContentAwareFill` | Content-Aware Fill Layer... | {layer?, method?: object\|surface\|edgeBlend, range?: workArea\|entire, alphaExpansion? (px), lightingCorrection?: none\|subtle\|moderate\|strong, referenceLayer?, referenceTime? (s), outputDir?, wait?: bool} |  |
| `layer.newLight` | Light... | {kind?: Parallel\|Spot\|Point\|Ambient\|Environment (default Spot; Environment lights and reflects from an equirectangular image layer: prop.set its lightOptions/source to that layer's id, or leave it empty for the comp's Environment Layer, see layer.environment), name?, color?, intensity?, coneAngle?, coneFeather?, falloff?: None\|Smooth\|Inverse Square Clamped, radius?, falloffDistance?, castsShadows?, shadowDarkness?, shadowDiffusion?, position? [x,y,z], poi? [x,y,z]} |  |
| `layer.newModel` | 3D Model Layer | {item?: id or name of a 3D model footage item, path?: a .gltf, .glb, .obj, .stl or .fbx file to import, name?, time? (s), index? (1-based stack position), position? ([x, y] comp px)}; switches a Classic 3D comp to Advanced 3D |  |
| `layer.newNull` | Null Object | {name?} |  |
| `layer.newPrimitive` | New 3D Primitive | {kind: cube\|sphere\|plane\|torus\|cone\|cylinder, name?, width?, height?, depth?, radius?, tubeRadius?, segments?, rings?, position? [x,y,z], baseColor?, metallic?, roughness?, emissive?, castsShadows?, acceptsShadows?, acceptsLights?}; switches a Classic 3D comp to Advanced 3D |  |
| `layer.newShape` | Shape Layer | {kind?: rect\|rounded\|ellipse\|star\|polygon\|none, name?, size?, fill?, fillType?, fillBlend?, fillOpacity?, stroke?, strokeType?, strokeBlend?, strokeOpacity?, strokeWidth?, position?} |  |
| `layer.newSolid` | Solid... | {name?, color? #hex\|[r,g,b], width?, height?, pixelAspect?} |  |
| `layer.newText` | Text | {text?, name? (layer name; default the text), position? [x,y], box? [x,y,w,h] (paragraph text, comp space), vertical?, edit? (start editing), font?, style?, size?, fill?, stroke?, applyFill?, applyStroke?, strokeWidth?, tracking?, leading?, baselineShift?, hScale?, vScale?, tsume?, fauxBold?, fauxItalic?, allCaps?, smallCaps?, baseline?, superscript?, subscript?, kerning?, ligatures?, justify?, indentLeft?, indentRight?, indentFirst?, spaceBefore?, spaceAfter?, direction?, composer?, hangingPunctuation?, strokeOverFill?} (attributes as layer.setText) |  |
| `layer.nudge` | Nudge Layers | {x?, y? (comp pixels), layers?, merge?} | select a layer first |
| `layer.openLayer` | Open Layer | {layer?} | select a layer first |
| `layer.openSource` | Open Layer Source | {layer?} | select a layer first |
| `layer.precompose` | Pre-compose... | {layers?, name?, mode?: move\|leave, adjustDuration?, open?} | select a layer first |
| `layer.quality` | Quality | {layers?, quality: best\|draft\|wireframe} | select a layer first |
| `layer.quickOffset` | Quick Offset | {delta (comp s: the last layer's move), layers? (in order; default the selection), merge?, fromStart?: bool (with merge: delta is the whole drag)} | select a layer first |
| `layer.rename` | Rename | {layer?, name} | select a layer first |
| `layer.replaceSource` | Replace Layer Source | {comp?, layers?, layer?, item?: id\|name (default the Project panel selection), fixExpressions?: bool (accepted for After Effects compatibility)} → {layers, item} | select a footage, composition or solid layer |
| `layer.revealExpressionErrors` | Reveal Expression Errors | {comp?} |  |
| `layer.revealInFinder` | Reveal in Finder | {layer?} | select a layer first |
| `layer.revealSource` | Reveal Layer Source in Project | {layers?} | select a layer first |
| `layer.sampling` | Sampling | {layers?, sampling: bilinear\|bicubic, toggle?} | select a layer first |
| `layer.sceneEditDetection` | Scene Edit Detection... | {layer?, mode?: markers\|split\|splitPrecompose, threshold? (0…1, 0.25), wait?: bool} | select a layer first |
| `layer.select` | Select Layers | {layers: [id\|name\|#n], add?, toggle?} |  |
| `layer.selectNext` | Select Next Layer | {add?} |  |
| `layer.selectPrevious` | Select Previous Layer | {add?} |  |
| `layer.sequence` | Sequence Layers... | {layers? (in order), overlap?: bool, duration? (s), transition?: off\|dissolveFront\|crossDissolve} | select two or more layers |
| `layer.setBlendMode` | Blending Mode | {layers?, mode?: Normal\|Multiply\|Screen\|…, step?: ±1} | select a layer first |
| `layer.setComment` | Layer Comment | {layers?, comment} | select a layer first |
| `layer.setMask` | Mask Mode | {layer?, mask: index\|uid\|name, mode?, inverted?} | select a layer first |
| `layer.setParent` | Parent | {layers?, parent: layer\|null, compensate?: bool} | select a layer first |
| `layer.setSwitch` | Layer Switch | {layers?, switch: video\|audio\|solo\|lock\|shy\|collapse\|quality\|fx\|frameBlend\|motionBlur\|adjustment\|threeD\|guide\|preserveTransparency, value?, merge?, others? (the named layers alone: the other layers get the opposite state, or come back)} | select a layer first |
| `layer.setText` | Edit Text | {layer?, range?: [start, end] (characters; default all), text?, font?, style?, size?, fill?, stroke?, applyFill?, applyStroke?, strokeWidth?, tracking?, leading?: px\|"auto", baselineShift? px, hScale? %, vScale? %, tsume? %, fauxBold?, fauxItalic?, allCaps?, smallCaps?, baseline?: normal\|superscript\|subscript, superscript?, subscript?, kerning?: metrics\|optical\|number, ligatures?, discretionaryLigatures? (OpenType), contextualAlternates?, stylisticAlternates?, stylisticSets?: [1–20], ss01?, ss02?, ss03?, ss04?, ss05?, ss06?, ss07?, ss08?, ss09?, ss10?, ss11?, ss12?, ss13?, ss14?, ss15?, ss16?, ss17?, ss18?, ss19?, ss20?, swash?, titling?, ordinals?, fractions?, allSmallCaps?, figureStyle?: default\|lining\|oldStyle, figureWidth?: default\|proportional\|tabular, figures?, variations?: {tag: value} (variable font axes; null resets), justify?: left\|center\|right\|justifyLeft\|justifyCenter\|justifyRight\|justifyAll, indentLeft?, indentRight?, indentFirst?, spaceBefore?, spaceAfter?, direction?: ltr\|rtl, composer?: everyLine\|singleLine, hangingPunctuation?, strokeOverFill?, box?: [x,y,w,h]\|null (layer space), vertical?} | select a layer first |
| `layer.setTrackMatte` | Track Matte | {layer?, matte: layer\|null, kind?: alpha\|alphaInverted\|luma\|lumaInverted} | select a layer first |
| `layer.setTransform` | Transform Value | {layers?, prop: anchor\|position\|scale\|orientation\|rotation\|opacity, value} | select a layer first |
| `layer.settings` | Layer Settings... | {layer?, name?, color?, width?, height?, pixelAspect?, affectAll?: bool (default true; false gives this layer its own copy of a solid other layers use)} → {layer, solid?} | select a layer first |
| `layer.showAllVideo` | Show All Video | {comp?} |  |
| `layer.slip` | Slip Edit | {layers?, delta? (seconds) \| frames?, merge?} | select a layer first |
| `layer.slipBack` | Slip Edit 1 Frame Earlier | {layers?} | select a layer first |
| `layer.slipForward` | Slip Edit 1 Frame Later | {layers?} | select a layer first |
| `layer.stretchInToTime` | Stretch Layer In Point to Current Time | {layers?} | select a layer first |
| `layer.stretchOutToTime` | Stretch Layer Out Point to Current Time | {layers?} | select a layer first |
| `layer.style.add` | Add Layer Style | {style: dropShadow\|innerShadow\|outerGlow\|innerGlow\|bevelEmboss\|satin\|colorOverlay\|gradientOverlay\|stroke (or display name), layers?} | select a layer first |
| `layer.style.bevelEmboss` | Bevel and Emboss | {layers?} | select a layer first |
| `layer.style.colorOverlay` | Color Overlay | {layers?} | select a layer first |
| `layer.style.convertToEditable` | Convert to Editable Styles | {layers?} | select a layer first |
| `layer.style.dropShadow` | Drop Shadow | {layers?} | select a layer first |
| `layer.style.globalLight` | Global Light | {comp?, angle? (deg), altitude? (deg, 0..90), time? (s)} — no values returns the current setting |  |
| `layer.style.gradientOverlay` | Gradient Overlay | {layers?} | select a layer first |
| `layer.style.innerGlow` | Inner Glow | {layers?} | select a layer first |
| `layer.style.innerShadow` | Inner Shadow | {layers?} | select a layer first |
| `layer.style.list` | List Layer Styles | {layer?} |  |
| `layer.style.options` | Layer Style Options... | {layer?, style?: blendingOptions\|dropShadow\|…} | select a layer first |
| `layer.style.outerGlow` | Outer Glow | {layers?} | select a layer first |
| `layer.style.remove` | Remove Layer Style | {layer?, style: id\|name\|uid\|layerStyles} | select a layer first |
| `layer.style.removeAll` | Remove All | {layers?} | select a layer first |
| `layer.style.satin` | Satin | {layers?} | select a layer first |
| `layer.style.showAll` | Show All | {layers?} | select a layer first |
| `layer.style.stroke` | Stroke | {layers?} | select a layer first |
| `layer.style.toggle` | Toggle Layer Style | {layer?, style: id\|name\|uid\|layerStyles, value?} | select a layer first |
| `layer.timeReverse` | Time-Reverse Layer | {layers?} | select a layer first |
| `layer.timeStretch` | Time Stretch... | {layers?, percent?\|duration? (s), hold?: in\|current\|out, op?: reverse} | select a layer first |
| `layer.timing` | Layer Timing | {layers?, op?: moveInToTime\|moveOutToTime\|moveInToStart\|moveOutToEnd\|trimInToTime\|trimOutToTime, delta?, start?, in?, out?, inDelta?, outDelta? (seconds, per layer), merge?} | select a layer first |
| `layer.trackMatte` | Track Matte | {layers?, op: none\|alpha\|alphaInverted\|luma\|lumaInverted\|above\|below} | select a layer first |
| `layer.transform` | Transform | {layers?, op: reset\|center\|fit\|fitWidth\|fitHeight\|flipH\|flipV} | select a layer first |
| `layer.tree` | Layer Property Tree | {layer?, comp?, depth?, time? (comp s)} → nodes with `path` |  |
| `layer.unlockAll` | Unlock All Layers | {comp?} |  |
| `layer.updateMarkersFromSource` | Update Markers From Source | {layers?} | select a layer first |

## prop (18)

| id | label | params | why disabled (empty project) |
|---|---|---|---|
| `prop.addKey` | Add Keyframe | {layer?, path\|prop, time? (layer s by default), timeBase?: layer\|comp, value?} | select a layer first |
| `prop.convertExpressionToKeyframes` | Convert Expression to Keyframes | {layer?, path\|prop} | select a layer first |
| `prop.deselect` | Deselect Property | {layer?, path\|prop} | select a layer first |
| `prop.duplicateGroup` | Duplicate Property Group | {layer?, prop: uid} → {prop: new uid} | select a layer first |
| `prop.editGradient` | Edit Gradient... | {layer?, path\|prop, comp?} — a gradient property; opens the Gradient Editor at the current time | select a layer first |
| `prop.get` | Get Property | {layer?, path\|prop, time? (comp s)} |  |
| `prop.moveGroup` | Reorder Property Group | {layer?, prop: uid, index (1-based among its siblings)} | select a layer first |
| `prop.pickWhip` | Pick Whip (Link Property) | {layer?, path\|prop, target: {layer, path\|prop, dimension?}, expression?, range?: [start, end]} → sets an AE reference expression (`dimension`: one of the target's values, `position[0]`; with `expression`: inserts it there, replacing the characters in `range`, default the end) | select a layer first |
| `prop.removeGroup` | Delete Property Group | {layer?, prop: uid} | select a layer first |
| `prop.renameGroup` | Rename Property Group | {layer?, prop: uid, name} | select a layer first |
| `prop.reset` | Reset Property | {layer?, path\|prop, default?} → removes the expression; the value becomes `default`, else the property's own (an effect parameter's, a Transform property's), as a keyframe at the current time when the property is animated | select a layer first |
| `prop.select` | Select Property | {layer?, path\|prop, add?, selectKeys?} | select a layer first |
| `prop.separateDimensions` | Separate Dimensions | {layer?, value?} | select a layer first |
| `prop.set` | Set Property Value | {layer?, path\|prop, value, time? (layer s by default), timeBase?: layer\|comp, merge?, selected? (also the other selected layers), offset? (them by the same change), proportional? (with offset: Proportional Scrubbing, each layer by its share in selection order, the first none, the last all), dims? (with selected, a typed value: the components edited, e.g. [2] for Z; the other layers keep the rest of their own value)} | select a layer first |
| `prop.setExpression` | Add Expression | {layer?, path\|prop?, expression?, enabled?} (no path/prop: the selected properties) | select a layer first |
| `prop.setGroupEnabled` | Enable Property Group | {layer?, prop: uid, value?} | select a layer first |
| `prop.toggleAnimation` | Toggle Stopwatch | {layer?, path\|prop, value?, merge?, selected?} | select a layer first |
| `prop.toggleKey` | Add or Remove Keyframe at Current Time | {layer?, path\|prop, selected?} | select a layer first |

## keys (36)

| id | label | params | why disabled (empty project) |
|---|---|---|---|
| `keys.audioToKeyframes` | Convert Audio to Keyframes | {comp?} |  |
| `keys.copy` | Copy Keyframes | {} | select keyframes first |
| `keys.delete` | Delete Keyframes | {} | select keyframes first |
| `keys.deselectAll` | Deselect All Keyframes and Properties | {} |  |
| `keys.easyEase` | Easy Ease | {which?: both\|in\|out} | select keyframes first |
| `keys.easyEaseIn` | Easy Ease In | {} | select keyframes first |
| `keys.easyEaseOut` | Easy Ease Out | {} | select keyframes first |
| `keys.exponentialScale` | Exponential Scale | {} — two selected Scale keys | select keyframes first |
| `keys.info` | Keyframe Info | {keys?: [{layer, prop, time}]} |  |
| `keys.interpolation` | Keyframe Interpolation... | {interpolation?: linear\|bezier\|continuousBezier\|autoBezier\|hold, in?\|out?: linear\|bezier\|hold, autoBezier?, continuous?, spatial?: linear\|bezier\|continuousBezier\|autoBezier, roving?} | select keyframes first |
| `keys.move` | Move Keyframes | {delta (s), merge?} | select keyframes first |
| `keys.nudge` | Nudge Keyframes | {frames, merge?} | select keyframes first |
| `keys.nudgeBackward` | Move Keyframes 1 Frame Earlier | {} | select keyframes first |
| `keys.nudgeBackward10` | Move Keyframes 10 Frames Earlier | {} | select keyframes first |
| `keys.nudgeForward` | Move Keyframes 1 Frame Later | {} | select keyframes first |
| `keys.nudgeForward10` | Move Keyframes 10 Frames Later | {} | select keyframes first |
| `keys.paste` | Paste Keyframes | {layers?, prop?\|path?, time?} | no keyframes have been copied |
| `keys.quickOffset` | Quick Offset Keyframes | {delta (comp s: the last layer's keys' move), merge?, fromStart?: bool (with merge: delta is the whole drag)} | select keyframes first |
| `keys.rpfCameraImport` | RPF Camera Import | {path: .json\|.csv camera data, comp?} |  |
| `keys.select` | Select Keyframes | {keys: [{layer, prop: uid \| path (or `path`), time (layer s by default)}], timeBase?: layer\|comp, add?, toggle?: bool (Shift+click: in or out of the selection), selectProperties?: bool (their properties and layers too, as a Timeline click does)} |  |
| `keys.selectAll` | Select All Keyframes | {layers?, visible?: [{layer, prop}] (every key of these properties)} |  |
| `keys.selectEqual` | Select Equal Keyframes | {} | select keyframes first |
| `keys.selectFollowing` | Select Following Keyframes | {} | select keyframes first |
| `keys.selectLabelGroup` | Select Keyframe Label Group | {scope: selected\|all\|visibleSelected\|visibleAll, visible?: [prop uid]} |  |
| `keys.selectPrevious` | Select Previous Keyframes | {} | select keyframes first |
| `keys.set` | Edit Keyframe | {layer?, path\|prop, time (layer s by default), newTime? (same base), timeBase?: layer\|comp, value?, merge?} |  |
| `keys.setEase` | Set Keyframe Ease | {layer?, path\|prop, time (layer s), side: in\|out, dim?, speed?, influence? %, merge?} |  |
| `keys.setLabel` | Keyframe Label | {label: name\|none\|0–16} | select keyframes first |
| `keys.setSpatialTangents` | Edit Spatial Tangents | {layer?, path\|prop, time (layer s), in?: [dx,dy,dz?], out?, break?, merge?} |  |
| `keys.smooth` | Smoother | {tolerance? (property units, 1)} | select keyframes first |
| `keys.timeReverse` | Time-Reverse Keyframes | {} | select keyframes first |
| `keys.toggleHold` | Toggle Hold Keyframe | {} | select keyframes first |
| `keys.toggleTransform` | Add or Remove Transform Keyframe | {layers?, prop: anchor\|position\|scale\|rotation\|opacity} (Alt+Shift+A/P/S/R/T) | select a layer first |
| `keys.transform` | Transform Keyframes | {timeScale?, timeAnchor? (comp s), timeOffset? (s), valueScale?, valueAnchor?, valueOffset?, dim? \| dims?: [d…], merge?, fromStart?: bool (with merge: values are the whole transform since the drag started)} | select keyframes first |
| `keys.velocity` | Keyframe Velocity... | {inSpeed?, inInfluence? %, outSpeed?, outInfluence? % (numbers or per-dimension arrays), continuous?} | select keyframes first |
| `keys.wiggle` | Wiggler | {apply?: spatial\|temporal, noise?: smooth\|jagged, dimensions?: one\|same\|independent, dimension? (index for `one`), frequency? (keys/s, 5), magnitude?, seed?} | select keyframes first |

## text (13)

| id | label | params | why disabled (empty project) |
|---|---|---|---|
| `text.addSelector` | Add Text Selector | {layer?, animator?: uid\|index, kind: range\|wiggly\|expression} | select a layer first |
| `text.animatorFontAxes` | Variable Font Axes | {layer?, axis?: tag\|name (omit to list the font's axes), animator?: uid\|index} | select a text layer first |
| `text.animatorProperties` | Text Animator Properties | {} |  |
| `text.delete` | Delete Text | {layer?, direction?: backward\|forward, word?, range?: [start, end], merge?} | edit text or select a text layer |
| `text.edit` | Edit Text | {layer?, select?: [anchor, caret]\|"none", caret?, created?} → {layer, anchor, caret} | edit text or select a text layer |
| `text.endEdit` | Exit Text Editing | {} |  |
| `text.fontFeatures` | OpenType Features | {layer?, font?, style?} → {family, style, features: [tags], options: {smallCaps, superscript, stylisticSets: [n], fractions, …}} (what the font sets with its own glyphs) |  |
| `text.fonts` | List Fonts | {query?, variable?, rescan?} → {count, families: [{family, styles, origin: bundled\|system\|user, variable, nativeName?}], added} (variable: only variable fonts; rescan picks up fonts installed since launch) |  |
| `text.insert` | Type Text | {layer?, text, range?: [start, end], merge?} (replaces the selection) | edit text or select a text layer |
| `text.moveCaret` | Move Text Caret | {to: left\|right\|wordLeft\|wordRight\|lineStart\|lineEnd\|up\|down\|paraStart\|paraEnd\|start\|end, extend?} | not editing text |
| `text.presets` | Text Animation Presets | {} |  |
| `text.removeAllAnimators` | Remove All Text Animators | {layers?} | select a layer first |
| `text.setSelection` | Set Text Selection | {layer?, start, end?} \| {anchor, caret} \| {select: "all"} (character indices) | edit text or select a text layer |

## shape (8)

| id | label | params | why disabled (empty project) |
|---|---|---|---|
| `shape.dashes.add` | Add Dash or Gap | {layer?, prop?: stroke uid} | select a layer first |
| `shape.dashes.remove` | Remove Dash or Gap | {layer?, prop?: stroke uid} | select a layer first |
| `shape.fillStroke` | Fill and Stroke | {layers?, fillType?: none\|solid\|linear\|radial, strokeType?, fill?: color, stroke?: color, strokeWidth?, merge?} → {fill, stroke, strokeWidth, fillType, strokeType} (first layer) | select a layer first |
| `shape.newPath` | Pen Tool (Shape Path) | {layer?, vertices: [[x,y]…], inTangents?, outTangents?, closed?, space?: comp\|layer, fill?: [r,g,b]\|#hex\|false, fillType?, fillBlend?, fillOpacity?, stroke?, strokeType?, strokeBlend?, strokeOpacity?, strokeWidth? (default the Tools bar's, shape.toolOptions), name?} |  |
| `shape.newShape` | Shape Tool | {layer?, kind?: rect\|rounded\|ellipse\|polygon\|star, size? [w,h], position? [x,y] (the centre), space?: comp\|layer, name? (a new layer's), fill?, fillType?, fillBlend?, fillOpacity?, stroke?, strokeType?, strokeBlend?, strokeOpacity?, strokeWidth? (default the Tools bar's, shape.toolOptions)} → {layer, group} |  |
| `shape.stroke.taper` | Stroke Taper | {layer?, prop?: stroke uid, units?: pixels\|percent, startLength?, endLength?, startWidth? (%), endWidth? (%), startEase? (%), endEase? (%)} | select a layer first |
| `shape.stroke.wave` | Stroke Wave | {layer?, prop?: stroke uid, amount? (%), units?: pixels\|cycles, wavelength?, cycles?, phase? (°)} | select a layer first |
| `shape.toolOptions` | Shape Tool Options | {createsMask?: bool (Tool Creates Mask with a shape layer selected), fill?: [r,g,b]\|#hex\|false, fillType?: none\|solid\|linear\|radial, fillBlend?: blend mode, fillOpacity? %, stroke?, strokeType?, strokeBlend?, strokeOpacity?, strokeWidth? px, reset?} → the options |  |

## effect (21)

| id | label | params | why disabled (empty project) |
|---|---|---|---|
| `effect.apply` | Apply Effect | {effect: id\|name (e.g. Gaussian Blur), layers?} | select a layer first |
| `effect.applyLast` | Last Effect | {layers?} | select a layer first |
| `effect.copy` | Copy Effects | {layer?, effect? \| effects?: [uid\|name\|index]} (default: the selected effects) | select a layer first |
| `effect.cryptomatteAt` | Cryptomatte At | {layer?, effect?: index\|uid\|name, x, y (effect space), scale?, time?} → {name, hash, layer, selected} \| null — the Cryptomatte ID under the point |  |
| `effect.duplicate` | Duplicate Effect | {layer?, effect} | select a layer first |
| `effect.editDropdown` | Edit Dropdown Menu | {layer, path?\|prop?, items: [string]} |  |
| `effect.list` | List Effects | {filter?} → [{params: [{id, name, type, default, options?, min?, max?, sliderMin?, sliderMax?, decimals?}]}]; popup indices are zero-based (JSX uses one-based values) |  |
| `effect.manage` | Manage Effects... | {} |  |
| `effect.paste` | Paste Effects | {layers?} — adds the copied effects to the layers | select a layer first |
| `effect.pickColor` | Pick Effect Colour | {layer?, effect?: index\|uid\|name, param: id (e.g. screenColour) \| prop: uid, x, y (effect space), average?: bool (5×5), time?} — the colour of the effect's input there | select a layer first |
| `effect.pickCryptomatte` | Pick Cryptomatte | {layer?, effect?: index\|uid\|name, x, y (effect space), mode?: replace\|add\|remove (default replace), scale? (preview resolution, default 1), time?} → {name, hash, layer, selection, changed, selected} — edits the Cryptomatte effect's Selection with the ID under the point | select a layer first |
| `effect.plugins.list` | List Effect Plug-ins | {} → {api, wasm, plugins: [{id, name, category, version, author, source, params}]} |  |
| `effect.plugins.load` | Load Effect Plug-in... | {path (.wasm / .wat plug-in, API v1) \| folder (loads every .wasm in it)} |  |
| `effect.remove` | Remove Effect | {layer?, effect: index\|uid\|name} | select a layer first |
| `effect.removeAll` | Remove All | {layers?} | select a layer first |
| `effect.reorder` | Reorder Effect | {layer?, effect, index} | select a layer first |
| `effect.reset` | Reset Effect | {layer?, effect} | select a layer first |
| `effect.setLabel` | Effect Label | {layer?, effect, label: name\|index 0-16 (None clears)} | select a layer first |
| `effect.swapTintColors` | Swap Tint Colors | {comp?, layer?, effect?: index\|uid\|name} — swaps Tint's Map Black To and Map White To at the current layer time in one undo step | select a layer first |
| `effect.toggle` | Toggle Effect | {layer?, effect, value?} | select a layer first |
| `effect.warning` | Effect Warning | {layer?, effect?: index\|uid\|name (default: the selected effect), time?} → {effect, warning: string\|null} — what Effect Controls warns about (an OCIO config it can't read, transforms it passes through) |  |

## anim (9)

| id | label | params | why disabled (empty project) |
|---|---|---|---|
| `anim.addKeyframe` | Add Keyframe | {} — keys the selected properties at the CTI | select properties or effects first |
| `anim.applyBuiltinPreset` | Apply Built-in Animation Preset | {preset: id\|name (see anim.builtinPresets), layers?} | select a layer first |
| `anim.applyPreset` | Apply Animation Preset... | {path \| preset, layers?} | select a layer first |
| `anim.applyRecentPreset` | Recent Animation Presets | {index? \| path?, layers?} | select a layer first |
| `anim.browsePresets` | Browse Presets... | {} |  |
| `anim.builtinPresets` | Built-in Animation Presets | {category?} |  |
| `anim.clearRecentPresets` | Clear Recent Presets | {} | no recent animation presets |
| `anim.reveal` | Reveal Properties | {kind: keyframes\|animation\|modified} |  |
| `anim.savePreset` | Save Animation Preset... | {path (.ecpreset), name?} — saves the selected properties/effects | select properties or effects first |

## mask (17)

| id | label | params | why disabled (empty project) |
|---|---|---|---|
| `mask.addVertex` | Add Mask Vertex | {layer?, mask, point: [x,y], in?, out?, index?} | select a layer first |
| `mask.convertVertex` | Convert Vertex | {layer?, mask: uid (mask or shape Path item), index, smooth?} |  |
| `mask.deleteVertices` | Delete Mask Vertices | {vertices?} | select mask vertices first |
| `mask.featherPoint.add` | Add Mask Feather Point | {layer?, mask, segment?, t?: 0..1, point?: [x,y] (layer space), radius? (px, negative = inner), tension? (%)} → {index} |  |
| `mask.featherPoint.list` | Mask Feather Points | {layer?, mask} |  |
| `mask.featherPoint.remove` | Delete Mask Feather Point | {layer?, mask, index? \| all?} |  |
| `mask.featherPoint.set` | Move Mask Feather Point | {layer?, mask, index, segment?, t?, point? (slide along the path), radius?, toward?: [x,y] (radius from the drag point, layer space), tension? (%), merge?} |  |
| `mask.insertVertex` | Add Vertex | {layer?, mask: uid (mask or shape Path item), segment, t?: 0..1} |  |
| `mask.interpolate` | Apply Mask Interpolation | {layer?, mask?, times?: [from, to] (s; default the selected Mask Path keys), keyframeRate?: n\|auto, keyframeFields?, linearVertexPaths?, bendingResistance? (0-100), quality? (0-100), addVertices?: n\|false, addVerticesUnit?: pixels\|total\|percent, matchingMethod?: auto\|curve\|polyline, oneToOne?, firstVerticesMatch?} |  |
| `mask.interpolationOptions` | Mask Interpolation Options | {keyframeRate?: n\|auto, keyframeFields?, linearVertexPaths?, bendingResistance?, quality?, addVertices?: n\|false, addVerticesUnit?: pixels\|total\|percent, matchingMethod?: auto\|curve\|polyline, oneToOne?, firstVerticesMatch?} |  |
| `mask.moveVertices` | Move Mask Vertices | {vertices?: [{layer, mask, index}], delta: [dx,dy], merge?} | select mask vertices first |
| `mask.new` | New Mask from Points | {layer?, vertices: [[x,y]…], inTangents?, outTangents?, closed?, mode?} | select a layer first |
| `mask.remove` | Remove Mask | {layer?, mask} | select a layer first |
| `mask.removeAll` | Remove All Masks | {layer?} | select a layer first |
| `mask.selectVertices` | Select Mask Vertices | {vertices: [{layer, mask, index}], add?, toggle?} |  |
| `mask.setClosed` | Closed | {layer?, mask, closed?} | select a layer first |
| `mask.setVertex` | Set Mask Vertex | {layer?, mask, index, point?, in?, out?, merge?} | select a layer first |

## expr (2)

| id | label | params | why disabled (empty project) |
|---|---|---|---|
| `expr.errors` | Expression errors (the error bar) | {comp?, time? (s)} |  |
| `expr.languageMenu` | Expression Language menu | {} |  |

## file (61)

| id | label | params | why disabled (empty project) |
|---|---|---|---|
| `file.applyInterpretation` | Apply Interpretation | {items?} | select footage in the Project panel |
| `file.autoSave` | Auto-Save Now | {} |  |
| `file.clearRecent` | Clear Recent Projects | {} | no recent projects |
| `file.clearRecentFootage` | Clear Recent Footage | {} | no recent footage |
| `file.close` | Close | {comp?} |  |
| `file.closeProject` | Close Project | {} |  |
| `file.collectFiles` | Collect Files... | {folder} |  |
| `file.consolidateFootage` | Consolidate All Footage | {} |  |
| `file.createProxy` | Create Proxy | {kind: still\|movie, comp?\|item?, path?\|output? (template), resolution? (default 0.5)} |  |
| `file.cycleBitDepth` | Cycle Project Bit Depth | {} |  |
| `file.executeFile` | Execute File | {path, confirmed?} |  |
| `file.exportLottie` | Lottie JSON... | {comp?, path (.json or .lottie), includeExpressions?: bool, textAsShapes?: bool} |  |
| `file.exportTimeline` | Adobe Premiere Pro Project... | {comp?, path (Final Cut Pro XML .xml for Premiere Pro or .fcpxml .otio .edl .aaf .omf), format?: xml\|fcpxml\|otio\|edl\|aaf\|omf, prerender?: none\|unsupported\|all, precomps?: nest\|prerender} |  |
| `file.findMissing` | Find Missing | {what: footage\|effects\|fonts} |  |
| `file.import` | File... | {paths: [string] (files or folders), sequence?: bool (the Sequence checkbox: true imports numbered stills of one run as one image sequence, one picked file bringing its whole run and several picked files that range; default: a numbered still brings its run, except dropped files (drag), which import as stills as in After Effects; folders' runs import as sequences; false imports stills and a folder's files individually), alphabetical?: bool (Force Alphabetical Order: every image of that type in the folder, by name), frameRate?: fps (image sequences; default Settings ▸ Import ▸ Sequence Footage), importAs?: footage\|composition\|compositionLayerSizes (Photoshop, PDF, Illustrator and EPS files), layer?: name\|index (footage of one Photoshop layer), page?: number from 1 (PDF / Illustrator page), drag?: bool (dropped files: Settings ▸ Import ▸ Default Drag Import As; files import as stills unless sequence), addToComp?: bool (also add them to the active comp, at time?, index?, position? as in layer.addItem), background?: bool (probe the files in a background job, jobs.list / jobs.wait; returns {job})} |  |
| `file.importLottie` | Lottie... | {path (.json or .lottie)} |  |
| `file.importMultiple` | Multiple Files... | {paths: [string]} |  |
| `file.importPlaceholder` | Placeholder... | {name?, width?, height?, frameRate?, duration? (s)} |  |
| `file.importProject` | EffectCraft Project... | {path (.ecproj or .ecprojx)} — merges the project into a folder named after the file; returns {folder, items, comps, rootComps, primaryComp (the only root comp, else null), missingMedia, warnings} |  |
| `file.importRecent` | Import Recent Footage | {index? \| path?} | no recent footage |
| `file.importSolid` | Solid... | {name?, color?, width?, height?} |  |
| `file.importTimeline` | Adobe Premiere Pro Project... | {path (.xml Final Cut Pro XML from Premiere Pro or .fcpxml .otio .edl .aaf .omf), format?: auto\|xml\|fcpxml\|otio\|edl\|aaf\|omf, edlFrameRate?: number} |  |
| `file.importVanishingPoint` | Vanishing Point (.vpe)... | {} (always disabled: undocumented format) | Vanishing Point Exchange (.vpe) files can't be imported: the format has no public specification, and EffectCraft only implements documented formats |
| `file.incrementAndSave` | Increment and Save | {} | the project has not been saved yet |
| `file.installScript` | Install Script File... | {path (.jsx / .js)} → copies it to the Scripts folder; it appears in File ▸ Scripts |  |
| `file.installScriptUIPanel` | Install ScriptUI Panel... | {path (.jsx / .js)} → copies it to the ScriptUI Panels folder; it appears in the Window menu |  |
| `file.interpretFootage` | Main... | {items?, frameRate?: fps\|"file", alpha?: straight\|premultiplied\|ignore\|guess, guessAlpha?, matteColor?, invertAlpha?, loop?, pixelAspect?, fields?: off\|upper\|lower, colorProfile?: srgb\|rec709\|rec2020\|p3\|auto, linearLight?, preserveRgb? (the file's values unconverted), overrideStart?: bool (false: Use Source File Timecode), startTimecode?: timecode\|frame (Override Start)} | select footage in the Project panel |
| `file.interpretProxy` | Proxy... | {items?\|item?, alpha?, matteColor?, invertAlpha?, frameRate?, loop?, pixelAspect?, fields?, colorProfile?, linearLight?} | select an item in the Project panel first |
| `file.newCompFromSelection` | New Comp from Selection... | {duration? (s, for stills), single?: bool (one comp for all), dimensionsFrom?: index, sequence?: bool, overlap?: bool, overlapDuration? (s), transition?: off\|dissolveFront\|crossDissolve, addToRenderQueue?: bool} → {comps} | select an item in the Project panel first |
| `file.newFromTemplate` | New Project from Template... | {} → the Home screen's Templates tab |  |
| `file.newProject` | New Project | {} |  |
| `file.open` | Open Project... | {path} |  |
| `file.openDemoProject` | Open Demo Project | {} |  |
| `file.openRecent` | Open Recent | {index? \| path?} | no recent projects |
| `file.projectSettings` | Project Settings... | {bitDepth?: 8\|16\|32, colorEngine?: adobe\|ocio, workingSpace?: none\|srgb\|rec709\|rec2020\|p3\|acescg\|aces2065, workingGamma?: 2.2\|2.4 (with no working space), linearize?, blendLinear?, hdr?: clip\|compand\|toneMap, outputSpace?: srgb\|rec709\|rec2020\|p3\|rec2100pq\|rec2100hlg, renderer?: gpu\|software, timeDisplay?: timecode\|frames\|feet35\|feet16, frameStart?: 0\|1 (Frame Count: Start at 0 / Start at 1)} |  |
| `file.recoveryInfo` | Auto-Save Status | {} |  |
| `file.reduceProject` | Reduce Project | {} (keeps the selected comps and what they use) | select compositions in the Project panel |
| `file.relinkFootage` | Relink Missing Footage... | {folder: string (recursive desktop search, no symlinks; max 100000 entries), dryRun?: bool (report only), wait?: bool (return results inline; otherwise jobs.list/jobs.wait)} — relinks only unique exact filenames with compatible metadata; preserves interpretation and sequence ranges. Reports high/low confidence and ambiguous, incompatible, unsupported or notFound items. |  |
| `file.reloadFootage` | Reload Footage | {items?} | select footage in the Project panel |
| `file.rememberInterpretation` | Remember Interpretation | {item?} | select footage in the Project panel |
| `file.removeUnusedFootage` | Remove Unused Footage | {} |  |
| `file.replaceFootage` | File... | {path, item?, sequence?: bool (default true: a numbered still brings its image sequence), alphabetical?: bool} | select footage in the Project panel |
| `file.replaceWithLayeredComp` | With Layered Comp | {item?} | select an item in the Project panel first |
| `file.replaceWithPlaceholder` | Placeholder... | {item?, width?, height?, frameRate?, duration?} | select footage in the Project panel |
| `file.replaceWithPrecomp` | Replace with Precomposition | {item?} | select an item in the Project panel first |
| `file.replaceWithSolid` | Solid... | {item?, color?, width?, height?} | select footage in the Project panel |
| `file.revealInFinder` | Reveal in Finder | {item?} | select footage in the Project panel |
| `file.revert` | Revert | {} | the project has not been saved yet |
| `file.runScript` | Run Script File... | {path (.jsx/.js JavaScript, or a .jsonl/.json command script) \| name (an installed or sample script, see file.scripts.list) \| steps: [{command, params}]} |  |
| `file.save` | Save | {path?} |  |
| `file.saveAs` | Save As... | {path} |  |
| `file.saveCopy` | Save a Copy... | {path} |  |
| `file.saveCopyAsXml` | Save a Copy As XML... | {path: .ecprojx} |  |
| `file.scripts.list` | List Scripts | {} → [{name, panel, source: installed\|sample\|extension}] |  |
| `file.setProxy` | File... | {path, items?\|item?} | select an item in the Project panel first |
| `file.setProxyNone` | None | {items?\|item?} | select an item in the Project panel first |
| `file.timelineFormats` | Timeline Interchange Formats | {} |  |
| `file.uninstallScript` | Uninstall Script | {name} |  |
| `file.useProxy` | Use Proxy | {items?\|item?, on?} | select an item in the Project panel first |
| `file.watchFolder` | Watch Folder... | {folder, stop?: bool} → watches the folder for .ecproj files with queued renders, renders them and writes `<project>.status.json` |  |
| `file.watchFolder.poll` | Poll Watch Folder | {folder? (default: the watched one)} → renders new projects now: {watching, rendered: [{project, state: done\|failed, items: [{comp, status, output}]}]} | no folder is being watched |

## renderQueue (20)

| id | label | params | why disabled (empty project) |
|---|---|---|---|
| `renderQueue.add` | Add to Render Queue | {comp?: id\|name, template?: Render Settings template, format?: h264\|hevc\|av1\|prores\|uncompressed\|webm\|png\|jpeg\|tiff\|exr\|gif\|wav\|aiff, output?: path\|template, log?: errorsOnly\|plusSettings\|plusPerFrameInfo, quality?: best\|draft\|1-100 (jpeg, webm), resolution?: full\|half\|third\|quarter\|scale, proxyUse?, effects?, solo?, guideLayers?, colorDepth?, frameBlending?, fieldRender?, pulldown?, motionBlur?, timeSpan?: workArea\|comp\|custom, start?: s, end?: s, duration?: s, frameRate?: fps\|null, skipExisting?: bool, storageOverflow?: bool, channels?: rgb\|rgba\|alpha, color?, bitrate?: kbps, webmBitrate?, keyframeInterval?, proresProfile?, profile?, level?, rateControl?, webmCodec?, audioBitrate?, opusApplication?, crop?, resize?, includeProjectLink?, audio?: auto\|on\|off, sampleRate?, audioChannels?, audioFormat?, loop?: bool (values as in setRenderSettings / setOutputModule)} |  |
| `renderQueue.applyTemplate` | Apply Template | {item?\|index?, renderSettings?: template name, outputModule?: template name, module?: n} | the render queue is empty |
| `renderQueue.deleteTemplate` | Delete Template | {kind: renderSettings\|outputModule, name} |  |
| `renderQueue.duplicate` | Duplicate Render Item | {item?\|index?} | the render queue is empty |
| `renderQueue.formats` | Output Formats | {} |  |
| `renderQueue.list` | Render Queue Items | {} |  |
| `renderQueue.move` | Move in Render Queue | {item?\|index?, to: n (1-based)} | the render queue is empty |
| `renderQueue.remove` | Remove from Render Queue | {item?: id, index?: n} | the render queue is empty |
| `renderQueue.render` | Render | {wait?: bool (default true; the UI renders in the background)} | nothing is queued |
| `renderQueue.saveTemplate` | Save Template... | {kind: renderSettings\|outputModule, name, item?\|index? (save from this item), from?: template to copy, module?, params?: {setRenderSettings / setOutputModule keys}} |  |
| `renderQueue.setLog` | Render Queue: Log | {item?\|index?, log: errorsOnly\|plusSettings\|plusPerFrameInfo} | the render queue is empty |
| `renderQueue.setNotify` | Notify When Done | {notify?: bool (toggles)} |  |
| `renderQueue.setOutput` | Output To... | {item?\|index?, module?: n, path: file path or template like [compName].[fileExtension]} | the render queue is empty |
| `renderQueue.setOutputModule` | Output Module Settings... | {item?\|index?, module?: n (1 = first), template?: name, format?: h264\|hevc\|av1\|prores\|uncompressed\|webm\|png\|jpeg\|tiff\|exr\|gif\|wav\|aiff, channels?: rgb\|rgba\|alpha, color?: straight\|premultiplied, quality?: 1-100, bitrate?: kbps, webmBitrate?: bool, keyframeInterval?: frames (0 = auto), proresProfile?: proxy\|lt\|standard\|hq\|4444\|4444xq, profile?: main\|main10 (HEVC/AV1), level?: auto\|4.1, rateControl?: bitrate\|quality, webmCodec?: vp9\|av1, audioBitrate?: Opus kbps, opusApplication?: audio\|voice, crop?: bool\|{useRoi?, roi?, top?, left?, bottom?, right?}, cropTop?, cropLeft?, cropBottom?, cropRight?, resize?: bool\|{preset?, width?, height?, lockAspect?, quality?: low\|high}, resizeWidth?, resizeHeight?, postRenderAction?: none\|import\|importAndReplace\|setProxy, includeProjectLink?: bool, audio?: auto\|on\|off, sampleRate?, audioChannels?: mono\|stereo, audioFormat?: 16\|24\|32, loop?: bool, output?} | the render queue is empty |
| `renderQueue.setOverflowFolders` | Storage Overflow Folders | {folders: [path, …] (used in order when the output volume is full)} |  |
| `renderQueue.setRender` | Render Queue: Render Checkbox | {item?\|index?, render?: bool (toggles)} | the render queue is empty |
| `renderQueue.setRenderSettings` | Render Settings... | {item?\|index?, template?: name, quality?: best\|draft, resolution?: full\|half\|third\|quarter\|scale, proxyUse?: current\|all\|comp\|none, effects?: current\|allOn\|allOff, solo?: current\|allOff, guideLayers?: current\|allOff, colorDepth?: current\|8\|16\|32, frameBlending?: current\|onForChecked\|offForAll, fieldRender?: off\|upper\|lower, pulldown?: off\|WSSWW\|SSWWW\|SWWWS\|WWWSS\|WWSSW, motionBlur?: bool\|current\|onForChecked\|offForAll, timeSpan?: workArea\|comp\|custom, start?: s, end?: s, duration?: s, frameRate?: fps\|null, skipExisting?: bool, storageOverflow?: bool} | the render queue is empty |
| `renderQueue.setTemplateDefault` | Set Template Default | {kind: renderSettings\|outputModule, slot: movie\|still\|preRender\|movieProxy\|stillProxy, name} |  |
| `renderQueue.stop` | Stop Rendering | {} | not rendering |
| `renderQueue.templates` | Render Templates | {} |  |

## render (4)

| id | label | params | why disabled (empty project) |
|---|---|---|---|
| `render.addOutputModule` | Add Output Module | {item?\|index? (default: the last item), format?, output?, channels?, quality?, bitrate?, proresProfile?, audio?} | the render queue is empty |
| `render.backend` | Video Rendering and Effects | {backend?: gpu\|cpu} |  |
| `render.preRender` | Pre-render... | {comp?, output?: path\|template, format?} |  |
| `render.saveCurrentPreview` | Save Current Preview... | {comp?, path} |  |

## time (17)

| id | label | params | why disabled (empty project) |
|---|---|---|---|
| `time.back10` | Back 10 Frames | {} |  |
| `time.end` | Go to End | {} |  |
| `time.forward10` | Forward 10 Frames | {} |  |
| `time.go` | Go To | {to: start\|end\|workStart\|workEnd\|layerIn\|layerOut\|nextInOut\|prevInOut\|nextKey\|prevKey, prop?: uid, visible?: [{layer, prop}]} |  |
| `time.layerIn` | Go to Layer In Point | {} |  |
| `time.layerOut` | Go to Layer Out Point | {} |  |
| `time.nextFrame` | Next Frame | {} |  |
| `time.nextInOut` | Go to Next In or Out Point | {} |  |
| `time.nextKey` | Go to Next Keyframe or Marker | {visible?: [{layer, prop}] (only these properties' keys, as the Timeline shows them)} |  |
| `time.previousFrame` | Previous Frame | {} |  |
| `time.previousInOut` | Go to Previous In or Out Point | {} |  |
| `time.previousKey` | Go to Previous Keyframe or Marker | {visible?: [{layer, prop}]} |  |
| `time.set` | Go to Time... | {time? (s) \| frame? \| timecode?} |  |
| `time.start` | Go to Start | {} |  |
| `time.step` | Step Frames | {frames} |  |
| `time.workAreaEnd` | Go to Work Area End | {} |  |
| `time.workAreaStart` | Go to Work Area Start | {} |  |

## edit (27)

| id | label | params | why disabled (empty project) |
|---|---|---|---|
| `edit.clear` | Clear | {layers?} | select a layer first |
| `edit.copy` | Copy | {layers?} (keyframes, effects or shape items when they are selected) | select a layer first |
| `edit.copyExpressionOnly` | Copy Expression Only | {} | select layers or properties first |
| `edit.copyWithPropertyLinks` | Copy with Property Links | {layers?} (selected properties, or layers, as expressions linking to the originals) | select layers or properties first |
| `edit.copyWithRelativePropertyLinks` | Copy with Relative Property Links | {layers?} (like Copy with Property Links, using thisComp) | select layers or properties first |
| `edit.cut` | Cut | {layers?} (keyframes, effects or shape items when they are selected) | select a layer first |
| `edit.deselectAll` | Deselect All | {} |  |
| `edit.duplicate` | Duplicate | {layers?} (effects or shape items when they are selected) | select a layer first |
| `edit.editOriginal` | Edit Original... | {} | select a footage item or layer |
| `edit.extractWorkArea` | Extract Work Area | {layers?} |  |
| `edit.history` | History | {steps?: n (undo n steps), redo?: n} | nothing to undo |
| `edit.history.goto` | Go to History State | {index? (from edit.history.list) \| id? \| steps? (negative = back along the line)} |  |
| `edit.history.list` | History | {} → {states: [{index, id, label, parent, depth, current, line, future}], current, branches} |  |
| `edit.label` | Label | {label: Red\|Yellow\|Aqua\|…, layers?, keys?, target?: layers} |  |
| `edit.liftWorkArea` | Lift Work Area | {layers?} |  |
| `edit.paste` | Paste | {} (layers, keyframes at the CTI, effects, shape items into the selected shape layers, or property links / expressions) | the clipboard is empty |
| `edit.pasteReversedKeyframes` | Paste Reversed Keyframes | {layers?, prop?\|path?, time?} | select a layer first |
| `edit.pasteSvg` | Paste SVG as Shapes | {svg: SVG markup, name?, comp?} → {layer, skipped} (Edit ▸ Paste runs it for SVG on the system clipboard) |  |
| `edit.pasteTextFormattingOnly` | Paste Text Formatting Only | {layer?} (the copied text's formatting on the selected text or text layers) | edit text or select a text layer |
| `edit.pasteTextMatchFormatting` | Paste Text and Match Formatting | {text?} (the clipboard's text in the style at the caret) | edit text or select a text layer |
| `edit.purge` | Purge | {what?: all\|memoryAndDisk\|memory\|disk\|3d\|image\|snapshot} |  |
| `edit.purgeUndo` | Undo | {} |  |
| `edit.redo` | Redo | {} | nothing to redo |
| `edit.selectAll` | Select All | {} |  |
| `edit.selectLabelGroup` | Select Label Group | {} | select layers or project items first |
| `edit.splitLayer` | Split Layer | {layers?} | select a layer first |
| `edit.undo` | Undo | {} | nothing to undo |

## essential (22)

| id | label | params | why disabled (empty project) |
|---|---|---|---|
| `essential.addComment` | Add Comment | {comp?, text?, group?} |  |
| `essential.addGroup` | Add Group | {comp?, name?, index?} |  |
| `essential.addMedia` | Add Media Replacement | {layer, name?, group?} |  |
| `essential.addMirror` | Add Mirror | {comp?, control, name?, group?, index?} | add properties to Essential Graphics first |
| `essential.addProperty` | Add Property to Essential Graphics | {comp?, layer?, path?\|prop?: uid (default: the selected properties), name?, group?: control id, index?, as?: font (Source Text font family/style/size) \| scale (uniform Scale), mirror?: bool (a property already present is added as a mirror; default true)} | select a property in the timeline |
| `essential.canAdd` | Can Add Property to Essential Graphics | {layer, path\|prop, as?} → {ok, type?, reason?} |  |
| `essential.exportTemplate` | Essential Graphics Template... | {comp?, path (.ectemplate), name?} | add properties to Essential Graphics first |
| `essential.importTemplate` | Essential Graphics Template... | {path (.ectemplate), comp?, addToComp?: bool} |  |
| `essential.instance` | Essential Properties of a precomp layer | {layer} |  |
| `essential.linkProperty` | Link Property to Control | {comp?, control, layer?, path?\|prop? (default: the selected property)} | add properties to Essential Graphics first |
| `essential.list` | Essential Graphics controls | {comp?, supported?: bool} |  |
| `essential.move` | Move Control | {comp?, control, group?: id (null = top level), index?} |  |
| `essential.pushToComp` | Push Override Values to Source | {layer, control? (default: all overridden)} | select a precomp layer with Essential Properties |
| `essential.remove` | Remove Control | {comp?, control} |  |
| `essential.rename` | Rename Control | {comp?, control, name} |  |
| `essential.revert` | Revert | {layer, control? (default: all overridden)} | select a precomp layer with Essential Properties |
| `essential.set` | Set Essential Property | {layer, control: id\|name, value \| item (media)} | select a precomp layer with Essential Properties |
| `essential.setName` | Essential Graphics Name | {comp?, name} |  |
| `essential.setPrimary` | Primary Composition | {comp} |  |
| `essential.soloSupported` | Solo Supported Properties | {on?} |  |
| `essential.templateInfo` | Read a template's manifest | {path} |  |
| `essential.unlinkProperty` | Unlink Property | {comp?, control, layer?, path?\|prop? (default: the selected property)} | add properties to Essential Graphics first |

## project (13)

| id | label | params | why disabled (empty project) |
|---|---|---|---|
| `project.delete` | Delete Project Items | {items?: [id\|name] (default: selected)} (folders with their contents; layers using the items go too) |  |
| `project.deleteWithoutConfirmation` | Delete Project Items Without Confirmation | {} — the Project panel's selection, with the layers that use it; one undo step |  |
| `project.duplicate` | Duplicate Project Items | {items?: [id\|name] (default: selected)} → {items} |  |
| `project.move` | Move to Folder | {items?: [id\|name] (default: selected), folder: id\|name\|null (root)} |  |
| `project.newFolder` | New Folder | {name?, parent?} |  |
| `project.rename` | Rename Item | {item?: id\|name (default: selected), name} |  |
| `project.select` | Select Project Items | {items: [id\|name], add?} |  |
| `project.setComment` | Item Comment | {items?, comment} |  |
| `project.setLabel` | Item Label | {items?, label: name\|index} |  |
| `project.setProjectComment` | Project Comment | {comment} |  |
| `project.summary` | Project Summary | {} |  |
| `project.usage` | Project Item Usage | {items?: [id\|name] (default: selected)} → {items, layers, comps} that deleting them removes |  |
| `project.usedIn` | Project Item Used In | {item?: id\|name (default: selected)} → {item, count, comps: [{id, name, layers}]} |  |

## command (2)

| id | label | params | why disabled (empty project) |
|---|---|---|---|
| `command.describe` | Describe Command | {command} → id, label, menu, shortcut, params doc, JSON `schema`, enabled |  |
| `command.list` | List Commands | {filter?, enabledOnly?, schemas? (add each command's params JSON Schema)} |  |

## app (12)

| id | label | params | why disabled (empty project) |
|---|---|---|---|
| `app.about` | About EffectCraft... | {} |  |
| `app.capabilities` | App Capabilities | {} → version, command/effect counts, export formats, parity summary |  |
| `app.commandPalette` | Quick Apply... | {query?} |  |
| `app.find` | Find | {query?} |  |
| `app.gpuInfo` | GPU Information... | {} |  |
| `app.hide` | Hide EffectCraft | {} |  |
| `app.hideOthers` | Hide Others | {} |  |
| `app.keyboardShortcuts` | Keyboard Shortcuts | {} |  |
| `app.quit` | Quit EffectCraft | {} |  |
| `app.settings` | Settings... | {page?: general\|startup\|project\|composition\|previews\|appearance\|grids\|labels\|type\|import\|export\|audio\|disk\|memory\|video\|3d\|scripting} |  |
| `app.showAll` | Show All | {} |  |
| `app.templates` | Templates | {kind: renderSettings\|outputModule} |  |

## cache (1)

| id | label | params | why disabled (empty project) |
|---|---|---|---|
| `cache.diskStats` | Disk Cache Statistics | {} |  |

## camera (19)

| id | label | params | why disabled (empty project) |
|---|---|---|---|
| `camera.analyze` | Analyze | {layer?, effect?: uid\|name\|index, wait?: block until done} |  |
| `camera.cancel` | Cancel | {} | no 3D Camera Tracker analysis is running |
| `camera.create` | Create Camera | {layer?, effect?} |  |
| `camera.createFromSolve` | Create from Camera Solve | {kind: text\|solid\|null\|shadowCatcher\|camera, points?: [id] (default: selected), target?: {center, normal, size?} (comp world), multiple?, layer?, effect?} |  |
| `camera.deletePoints` | Delete Selected Points | {points?: [id] (default: selected), layer?, effect?, wait?} |  |
| `camera.dolly` | Dolly Camera | {amount (px, + = forward), layer?, merge?} |  |
| `camera.fromModel` | Create Cameras from 3D Model | {comp?, layers?: 3D model layers (default selected)} |  |
| `camera.fromView` | Create Camera from 3D View | {comp?} |  |
| `camera.linkFocusToLayer` | Link Focus Distance to Layer | {comp?, camera?, layer?} | select a camera layer |
| `camera.linkFocusToPoi` | Link Focus Distance to Point of Interest | {comp?, camera?} | select a camera layer |
| `camera.orbit` | Orbit Camera | {yaw\|dx deg, pitch\|dy deg, layer?, merge?} — current 3D view (camera layer in Active Camera) |  |
| `camera.orbitNull` | Create Orbit Null | {comp?, layer?: camera (default selected/active)} |  |
| `camera.pan` | Pan Camera | {dx, dy (comp px), layer?, merge?} |  |
| `camera.points` | 3D Camera Tracker Points | {layer?, effect?, time?: comp seconds} → visible solved points |  |
| `camera.selectPoints` | Select Track Points | {points: [id], add?, toggle?} |  |
| `camera.setFocusToLayer` | Set Focus Distance to Layer | {comp?, camera?, layer?} | select a camera layer |
| `camera.setGroundPlane` | Set Ground Plane and Origin | {points?: [id] (default: selected), layer?, effect?} |  |
| `camera.solveStatus` | 3D Camera Tracker Status | {layer?, effect?} |  |
| `camera.stereoRig` | Create Stereo 3D Rig | {comp?, configuration?: stereoPair\|centerRight\|centerLeft, sceneDepth? (% of comp width, default 3), convergence?: bool, convergenceOf?: poi\|zoom, zOffset?, view3d?: 3D Glasses view index (default 5 Balanced Colored Red Blue)} |  |

## contentFill (2)

| id | label | params | why disabled (empty project) |
|---|---|---|---|
| `contentFill.generate` | Generate Fill Layer | {layer?, method?: object\|surface\|edgeBlend, range?: workArea\|entire, alphaExpansion? (px), lightingCorrection?: none\|subtle\|moderate\|strong, referenceLayer?, referenceTime? (s), outputDir?, wait?: bool} | select a layer first |
| `contentFill.set` | Content-Aware Fill Settings | {method?: object\|surface\|edgeBlend, range?: workArea\|entire, alphaExpansion? (px), lightingCorrection?: none\|subtle\|moderate\|strong, referenceLayer?: layer\|null, referenceTime? (s)} |  |

## editor (1)

| id | label | params | why disabled (empty project) |
|---|---|---|---|
| `editor.state` | Editor State | {} |  |

## effects (1)

| id | label | params | why disabled (empty project) |
|---|---|---|---|
| `effects.copyPresetsFolderPath` | Copy Presets Folder Path | {} |  |

## engine (1)

| id | label | params | why disabled (empty project) |
|---|---|---|---|
| `engine.batch` | Run Commands (Batch) | {steps: [{command, params?}], label? (undo step name, default Batch), atomic?: bool (default true: a failing step rolls the whole batch back)} → {steps, results: [each step's result]}; a string param "$N" or "$N.key.0" is step N's result (1-based), e.g. {"layer": "$1.layer"} |  |

## face (5)

| id | label | params | why disabled (empty project) |
|---|---|---|---|
| `face.model.download` | Download Face Tracking Model | {id, wait?} — the official model, verified (desktop; uses the system curl) |  |
| `face.model.install` | Install Face Tracking Model | {path: model file, id?, wait?} — verified against the registry's SHA-256 |  |
| `face.model.remove` | Remove Face Tracking Model | {id} |  |
| `face.model.select` | Use Face Tracking Model | {id: classical\|mediapipe-face, wait?} (face tracking uses it; wait: loaded before returning) |  |
| `face.models` | Face Tracking Models | {} |  |

## footage (12)

| id | label | params | why disabled (empty project) |
|---|---|---|---|
| `footage.check` | Check Footage | {items?: [id], wait?} — look for every footage file (in the background unless `wait`) and flag missing items |  |
| `footage.clearInOut` | Clear In and Out | {} | open footage in the Footage panel first |
| `footage.info` | Footage Panel State | {} |  |
| `footage.missing` | Missing Footage | {} → {missing: [{item, name, path}]} |  |
| `footage.open` | Open in Footage Panel | {item: id\|name} |  |
| `footage.overlayEdit` | Overlay Edit | {item?, comp?, in? (s), out? (s), at? (comp s; default the current time)} | open footage in the Footage panel first |
| `footage.relink` | Relink Footage | {item, path} — point a footage item at its file's new location (keeps the interpretation) and relink the other missing files found in the same place | the project has no footage |
| `footage.reloadChanged` | Reload Changed Footage | {} — reload the footage whose file changed on disk since it was last seen (size or modification time; Settings ▸ Import ▸ Automatically Reload Footage runs this in the background; image sequences only with All Footage); files seen for the first time are only remembered. Returns {files, reloaded} |  |
| `footage.rippleInsertEdit` | Ripple Insert Edit | {item?, comp?, in? (s), out? (s), at? (comp s; default the current time)} | open footage in the Footage panel first |
| `footage.setIn` | Set In Point | {time? \| frame? (default: the panel's time)} | open footage in the Footage panel first |
| `footage.setOut` | Set Out Point | {time? \| frame? (default: the panel's time)} | open footage in the Footage panel first |
| `footage.setTime` | Footage Panel Time | {time? (s, source) \| frame?} | open footage in the Footage panel first |

## help (13)

| id | label | params | why disabled (empty project) |
|---|---|---|---|
| `help.appPage` | EffectCraft Home Page | {} |  |
| `help.discord` | Join the ArtCraft Discord... | {} |  |
| `help.docs` | EffectCraft Help... | {page?: help\|scripting\|expressions\|effects\|agents} |  |
| `help.enableLogging` | Enable Logging | {on?} |  |
| `help.github` | EffectCraft on GitHub | {} |  |
| `help.inAppTutorials` | In-App Tutorials... | {} → the Home screen's Learn tab |  |
| `help.onlineTutorials` | Online Tutorials... | {} |  |
| `help.reportIssue` | Provide Feedback... | {} |  |
| `help.revealLogFile` | Reveal Logging File | {} |  |
| `help.sibling` | Other ArtCraft Apps | {app: photocraft\|vectorcraft\|filmcraft\|lightcraft\|pdfcraft\|designcraft, kind?: page\|github} |  |
| `help.systemInfo` | System Information | {} |  |
| `help.systemReport` | System Compatibility Report... | {quiet?} |  |
| `help.website` | ArtCraft Website | {} |  |

## item (1)

| id | label | params | why disabled (empty project) |
|---|---|---|---|
| `item.metadata` | Metadata | {item?: id\|name} |  |

## jobs (3)

| id | label | params | why disabled (empty project) |
|---|---|---|---|
| `jobs.cancel` | Cancel Job | {job?: render\|track\|maskTrack\|warp\|camera\|roto\|task:<n>\|all} |  |
| `jobs.list` | Background Jobs | {} |  |
| `jobs.wait` | Wait for Background Jobs | {} |  |

## learn (5)

| id | label | params | why disabled (empty project) |
|---|---|---|---|
| `learn.list` | Learn Tutorials | {} → [{id, title, summary, minutes, steps}] |  |
| `learn.start` | Start Tutorial | {id} |  |
| `learn.state` | Tutorial State | {} → {tutorial, step, steps, done, current: {title, text, target, accepts}} \| null |  |
| `learn.step` | Tutorial Step | {action?: next\|back\|showMe\|goto, index?} |  |
| `learn.stop` | Close Tutorial | {} |  |

## light (3)

| id | label | params | why disabled (empty project) |
|---|---|---|---|
| `light.controlWithCamera` | Control Light with Camera | {comp?, layers?: lights (default selected), camera? (default active), on?: bool (default toggle)} |  |
| `light.environmentBackground` | Create Environment Light Background Layer | {comp?, layer?: environment light (default selected / first)} |  |
| `light.fromModel` | Create Lights from 3D Model | {comp?, layers?: 3D model layers (default selected)} |  |

## liquify (2)

| id | label | params | why disabled (empty project) |
|---|---|---|---|
| `liquify.clear` | Clear Liquify Mesh | {layer?, effect?: uid} |  |
| `liquify.stroke` | Liquify Stroke | {layer?, effect?: uid, tool?: warp\|turbulence\|twirlClockwise\|twirlCounterclockwise\|pucker\|bloat\|shiftPixels\|reflection\|clone\|reconstruction\|freeze\|thaw, points: [[x,y],…] (effect space), size?, pressure? (1-100), jitter? (1-100), cloneOffset?: [dx,dy], time? (s) \| frame?} |  |

## markers (5)

| id | label | params | why disabled (empty project) |
|---|---|---|---|
| `markers.convert` | Convert Marker | {layer? (layer marker → comp marker), index? \| at?, toLayer? (comp marker → layer marker)} |  |
| `markers.delete` | Delete Marker | {layer?, index? \| at? (comp s)} |  |
| `markers.list` | List Markers | {layer? (omit for composition markers)} |  |
| `markers.nested` | Nested Comp Markers | {layer: a precomp layer, comp?} — its comp's markers at their times in this comp (as on the layer bar) |  |
| `markers.set` | Marker Settings | {layer? (omit: comp marker), index? (0-based) \| at? (comp s) \| new?: true, time? (comp s), duration? (s), comment?, chapter?, url?, frameTarget?, cuePoint?: {name, navigation?, params?: [[name, value]…]} \| null, protected?, label?} |  |

## material (4)

| id | label | params | why disabled (empty project) |
|---|---|---|---|
| `material.duplicateAssign` | Duplicate and Assign Material | {layers? (first = source)} | select a layer first |
| `material.reset` | Reset Material | {layers?} | select a layer first |
| `material.revealSource` | Reveal Material Source in Project | {layer?} | select a layer first |
| `material.set` | Material Options | {layers?, castsShadows?: off\|on\|only, acceptsShadows?: off\|on\|only, acceptsLights?, appearsInReflections?, lightTransmission?, ambient?, diffuse?, specularIntensity?, specularShininess?, metal?, baseColor?, metallic?, roughness?, emissive?, time?} | select a layer first |

## mediaBrowser (7)

| id | label | params | why disabled (empty project) |
|---|---|---|---|
| `mediaBrowser.action` | Media Browser Action | {action}: an action from mediaBrowser.list's `actions` (web: openFolder, addFiles, uploadFolder) |  |
| `mediaBrowser.addFavorite` | Add to Favorites | {path?} |  |
| `mediaBrowser.fileInfo` | File Info | {path} |  |
| `mediaBrowser.go` | Go to Folder | {path?: folder \| "..", importableOnly?} |  |
| `mediaBrowser.import` | Import | {paths, sequence? (default true: a numbered still brings its image sequence), addToComp?, time?, index?, position? (where the layers go, as in layer.addItem)} |  |
| `mediaBrowser.list` | List Folder | {path?, importableOnly?} |  |
| `mediaBrowser.removeFavorite` | Remove from Favorites | {path?} |  |

## motion (1)

| id | label | params | why disabled (empty project) |
|---|---|---|---|
| `motion.sketch` | Motion Sketch | {layer?, points: [[t, x, y]…] (t = capture seconds) \| [[x, y]…] (one per frame), start? (s, default current time), captureSpeed? (%, 100), smoothing? (px, 1)} |  |

## objectMatte (5)

| id | label | params | why disabled (empty project) |
|---|---|---|---|
| `objectMatte.apply` | Object Matte | {layer?, effect? (uid: re-prompt this Object Matte instead of adding one), point: [x, y] (layer pixels: the object), box?: [x0, y0, x1, y1] (layer pixels, around the object), frame? (reference layer frame; default current), track?: follow the object from that frame (default true), before?, after? (frames to follow it; default 30, up to 600)} |  |
| `objectMatte.freeze` | Freeze Object Matte | {layer?, effect?, wait?} |  |
| `objectMatte.propagate` | Track Object Matte | {layer?, effect?, direction?: forward\|backward\|both, wait?: block until done} (a background job like Roto Brush propagation; roto.cancel stops it) |  |
| `objectMatte.status` | Object Matte Status | {layer?, effect?}: the job's progress, whether the instance is frozen, its frames and which are computed |  |
| `objectMatte.unfreeze` | Unfreeze Object Matte | {layer?, effect?} |  |

## paint (6)

| id | label | params | why disabled (empty project) |
|---|---|---|---|
| `paint.brushPreset` | Brush Preset | {preset?: index \| name} |  |
| `paint.options` | Paint Options | {color?, background?, opacity?, flow?, mode?, channels?, durationMode?, customFrames?, eraseMode?, diameter?, angle?, roundness?, hardness?, spacing?, preset?, sizePressure?, minSize?, opacityPressure?, flowPressure?, clonePreset?, cloneSource?, clonePoint?, cloneOffset?, aligned?, lockSourceTime?, cloneTimeShift?, cloneTime?, showOverlay?, overlayOpacity?, overlayDifference?, reset?} |  |
| `paint.presets` | Brush Presets | {} |  |
| `paint.removeStroke` | Delete Paint Stroke | {layer?, stroke: uid \| name} |  |
| `paint.setCloneSource` | Set Clone Source | {layer?, point: [x,y]} |  |
| `paint.stroke` | Paint Stroke | {layer?, kind?: brush\|clone\|eraser, points: [[x,y,pressure?],…] (effect space), time? (s) \| frame?, duration? (s, drawing time for Write On), color?: [r,g,b,a], diameter?, angle?, hardness?, roundness?, spacing?, opacity?, flow?, mode?, channels?: RGBA\|RGB\|Alpha, durationMode?: constant\|writeOn\|singleFrame\|custom, customFrames?, eraseMode?: layerSourceAndPaint\|paintOnly\|lastStrokeOnly, cloneSource?: layer id, clonePosition?: [x,y], cloneTimeShift? (s), lockSourceTime?, cloneTime? (s), sizePressure?, minSize?, opacityPressure?, flowPressure?} |  |

## path (6)

| id | label | params | why disabled (empty project) |
|---|---|---|---|
| `path.convertToBezier` | Convert To Bezier Path | {layer?, mask?} | select a layer first |
| `path.freeTransform` | Free Transform Points | {layer?, mask?, scale?: % \| [x%, y%], rotation?: deg, offset?: [dx, dy], anchor?: [x, y]} | select a layer first |
| `path.groupShapes` | Group Shapes | {layer?, items?: [uid]} | select a layer first |
| `path.rotoBezier` | RotoBezier | {layer?, mask?, value?} | select a layer first |
| `path.setFirstVertex` | Set First Vertex | {layer?, mask?: uid, index?} | select one mask vertex |
| `path.ungroupShapes` | Ungroup Shapes | {layer?, items?: [group uid]} | select a layer first |

## paths (3)

| id | label | params | why disabled (empty project) |
|---|---|---|---|
| `paths.nullsFollowPoints` | Nulls Follow Points | {layer?, path?\|prop?, pins?: [uid \| name…]} → a null per vertex (or puppet pin) following it (Position expressions) | select a layer first |
| `paths.pointsFollowNulls` | Points Follow Nulls | {layer?, path?\|prop?, pins?: [uid \| name…]} → a null per vertex (or Position / Advanced puppet pin); the path (pins) follow them (expressions) | select a layer first |
| `paths.tracePath` | Trace Path | {layer?, path?\|prop?, loop?: bool} → a null moving along the path (Progress slider) | select a layer first |

## playback (6)

| id | label | params | why disabled (empty project) |
|---|---|---|---|
| `playback.audio` | Audio | {value?: include audio in previews} |  |
| `playback.cacheWhenIdle` | Cache Frames When Idle | {value?} |  |
| `playback.scrubAudio` | Scrub Audio | {time? (s, default the current time)} — plays one frame of the comp's audio there (Ctrl/Cmd-drag the current time) |  |
| `playback.settings.get` | Preview Settings | {shortcut?: spacebar\|shiftSpacebar\|numpad0\|shiftNumpad0\|altNumpad0 (default: the one shown in the Preview panel)} → options + plan {start, end, first, step, fps} |  |
| `playback.settings.set` | Change Preview Settings | {shortcut?, current?: shortcut shown in the panel, reset?: bool, values?: {…}, includeVideo?, includeAudio?, includeOverlays?, includeLayerControls?, loop?, cacheBeforePlayback?, range?: workArea\|workAreaExtended\|entireDuration\|aroundCurrentTime, preRoll?, postRoll?: seconds, playFrom?: rangeStart\|currentTime, frameRate?: fps\|"auto", skip?, resolution?: auto\|full\|half\|third\|quarter\|custom, customResolution?, fullScreen?, playCachedFrames?, moveTimeToPreviewTime?} |  |
| `playback.toggle` | Play Current Preview | {shortcut?: spacebar\|shiftSpacebar\|numpad0\|shiftNumpad0\|altNumpad0 (whose Preview panel options to use; default spacebar)} |  |

## prefs (5)

| id | label | params | why disabled (empty project) |
|---|---|---|---|
| `prefs.get` | Get Setting | {key?: e.g. general.undoLevels (omit for all settings)} |  |
| `prefs.open` | Open Settings | {page?: general\|startup\|project\|composition\|previews\|appearance\|grids\|labels\|type\|import\|export\|audio\|disk\|memory\|video\|3d\|scripting} |  |
| `prefs.pages` | Settings Pages | {} |  |
| `prefs.reset` | Reset Settings | {page?: general\|labels\|project\|…} |  |
| `prefs.set` | Change Setting | {key, value, values?: {key: value}} |  |

## puppet (10)

| id | label | params | why disabled (empty project) |
|---|---|---|---|
| `puppet.addPin` | Add Puppet Pin | {layer?, kind?: position\|advanced\|bend\|starch\|overlap, position: [x,y] (effect space), time? (s) \| frame?, mesh?: uid, newMesh?, density?, expansion?, triangles?} |  |
| `puppet.follow` | Follow-Through... | {layer?, leader?: uid \| name (default: the first selected pin), pins?: [uid \| name…] (default: the other selected pins), delay? (s, 0.1), amount? (%, 100), cascade? (true: the k-th nearest pin trails k × delay)} |  |
| `puppet.info` | Puppet Mesh Info | {layer?, time? \| frame?} |  |
| `puppet.mesh` | Puppet Mesh Options | {layer?, mesh?: uid, density?, expansion?, triangles?, showMesh?, time?, merge?} |  |
| `puppet.movePin` | Move Puppet Pin | {layer?, pin: uid \| name, position: [x,y], time? \| frame?, merge?} |  |
| `puppet.recordOptions` | Record Options... | {speed? (%, 100), smoothing? (0-100), useDraftDeformation?, showMesh?} |  |
| `puppet.recordPin` | Record Puppet Pin | {layer?, pin: uid \| name, samples: [[t, x, y]…] (t = seconds since the drag began, effect space), pins?: [uid \| name…] (more pins that move by the same displacement), start? (s, default current time), speed? (%, Record Options), smoothing? (Record Options)} |  |
| `puppet.removePin` | Delete Puppet Pin | {layer?, pin?: uid \| name, pins?: [uid \| name…]} (default: the selected pins) |  |
| `puppet.selectPins` | Select Puppet Pins | {layer?, pins: [uid \| name…] ([] deselects), add?, toggle?} |  |
| `puppet.setPin` | Edit Puppet Pin | {layer?, pin: uid \| name, position?, scale? (%), rotation? (°), amount? (%), extent? (px), inFront?, time? \| frame?, merge?} |  |

## roto (14)

| id | label | params | why disabled (empty project) |
|---|---|---|---|
| `roto.cancel` | Stop Roto Brush | {} | no Roto Brush job is running |
| `roto.clearStrokes` | Remove Roto Brush Strokes | {layer?, effect?, frame? (only this layer frame), kind?} |  |
| `roto.freeze` | Freeze | {layer?, effect?, wait?} |  |
| `roto.model.download` | Download Roto Brush Model | {id, wait?} — the official weights, verified (desktop; uses the system curl) |  |
| `roto.model.install` | Install Roto Brush Model | {path: weights file, id?, wait?} — verified against the registry's SHA-256 |  |
| `roto.model.remove` | Remove Roto Brush Model | {id} |  |
| `roto.model.select` | Use Roto Brush Model | {id: classical\|mobilesam, wait?} (Roto Brush 2.0 / 3.0 use it; wait: loaded before returning) |  |
| `roto.models` | Roto Brush Models | {} |  |
| `roto.options` | Roto Brush Options | {diameter?, refineDiameter?, view?: alphaBoundary\|alpha\|alphaOverlay\|none, overlayColor?: [r,g,b], overlayOpacity?, boundaryColor?: [r,g,b], autoPropagate?} |  |
| `roto.propagate` | Propagate Roto Brush | {layer?, effect?, direction?: forward\|backward\|both, to? (layer frame: extend the span), wait?: block until done} |  |
| `roto.span` | Set Segmentation Span | {layer?, effect?, start?, end? (layer frames)} |  |
| `roto.status` | Roto Brush Status | {layer?, effect?, frame? (layer frame: also report its matte), matte?: include the matte (RLE, base64), compute?: compute the frame if needed, compareTo?: RLE matte to report the IoU against} |  |
| `roto.stroke` | Roto Brush Stroke | {layer?, kind?: fg\|bg\|refine\|refineErase, points: [[x, y], …] (layer pixels), frame? (layer frame; default current), radius? (layer px; default the tool's diameter / 2), effect?} |  |
| `roto.unfreeze` | Unfreeze | {layer?, effect?} |  |

## scopes (1)

| id | label | params | why disabled (empty project) |
|---|---|---|---|
| `scopes.analyze` | Lumetri Scopes | {comp?, time?\|frame?, scope?: waveformRgb\|waveformLuma\|waveformYc\|vectorscopeYuv\|vectorscopeHls\|histogram\|paradeRgb\|paradeYuv, standard?: rec601\|rec709\|rec2020, float?, clamp?, size?} |  |

## script (4)

| id | label | params | why disabled (empty project) |
|---|---|---|---|
| `script.run` | Run Script | {code (JavaScript: app, app.project, CompItem, Layer, Property… like After Effects scripting), name?, console? (Script Console context)} → {ok, result, output, error: {message, line, column} \| null} |  |
| `script.runTasks` | Run Scheduled Script Tasks | {} → runs the app.scheduleTask tasks that are due (frontends do it every frame) → {ran, output, errors, next (ms until the next task, or null)} |  |
| `script.settings.get` | Get Script Setting | {section, key} → {have, value} (app.settings.haveSetting / getSetting) |  |
| `script.settings.save` | Save Script Setting | {section, key, value (text)} → kept in the settings store (app.settings.saveSetting) |  |

## scriptui (6)

| id | label | params | why disabled (empty project) |
|---|---|---|---|
| `scriptui.click` | Click Script Window Control | {window?: id \| title, widget: id \| "#id" \| properties.name \| text} (buttons, checkboxes, radio buttons, tabs) |  |
| `scriptui.close` | Close Script Window | {window?, result? (a dialog's show() returns it; default 2 = Cancel)} |  |
| `scriptui.get` | Script Window Controls | {window?: id \| title} → {id, title, kind, root: {id, type, name, text, value, checked, items, selection, bounds, enabled, draw (onDraw paint list), children…}} |  |
| `scriptui.list` | List Script Windows | {} → [{window, title, kind: dialog\|palette\|window\|panel, script, modal, size}] |  |
| `scriptui.mouse` | Mouse Event on Script Window Control | {window?, widget, type: mousedown \| mouseup \| mousemove \| mouseover \| mouseout \| click (default), x?, y? (relative to the control; default its centre), button? (0 left, 1 middle, 2 right), detail? (click count), screenX?, screenY?, altKey?, ctrlKey?, metaKey?, shiftKey?} → the script's addEventListener listeners on the control and its containers receive a MouseEvent |  |
| `scriptui.set` | Set Script Window Control | {window?, widget, value: text \| number \| bool \| item index \| item text, changing?: bool (a live update: each keystroke / slider step; fires onChanging only)} (edit text, sliders, checkboxes, lists) → fires onChanging / onChange |  |

## shortcuts (7)

| id | label | params | why disabled (empty project) |
|---|---|---|---|
| `shortcuts.conflicts` | Keyboard Shortcut Conflicts | {} |  |
| `shortcuts.export` | Export Keyboard Shortcuts | {preset?, path?} |  |
| `shortcuts.import` | Import Keyboard Shortcuts | {path? \| preset?: exported document, name?} |  |
| `shortcuts.list` | List Keyboard Shortcuts | {query?, keys?, assigned?: bool} |  |
| `shortcuts.preset` | Keyboard Shortcut Preset | {op: select\|new\|duplicate\|delete\|rename, name?, from?, newName?} |  |
| `shortcuts.reset` | Reset Keyboard Shortcuts | {command?, params?} |  |
| `shortcuts.set` | Set Keyboard Shortcut | {command, params?, keys: "Cmd+Shift+K" \| [keys] \| null} |  |

## storage (3)

| id | label | params | why disabled (empty project) |
|---|---|---|---|
| `storage.clear` | Clear Browser Storage | {what: diskCache\|media\|projects\|autoSaves\|all} → {cleared, entries, bytes} | browser storage is only managed in the web app |
| `storage.info` | Browser Storage | {} → {available, backend, usage, quota, persisted, files: {count, bytes, media, projects, autoSaves}, diskCache: {enabled, entries, bytes, maxBytes, hits, misses, writes, evictions}} |  |
| `storage.persist` | Request Persistent Storage | {} → {requested, persisted} | browser storage is only managed in the web app |

## templates (5)

| id | label | params | why disabled (empty project) |
|---|---|---|---|
| `templates.create` | New Project from Template | {id (templates.list) \| path (.ectemplate), projectPath? (save the new project there; embedded footage goes to `<stem> Footage/` next to it), footageDir?} → an untitled copy (embedded footage extracted: `footage` lists the files) |  |
| `templates.delete` | Delete Template | {id: user/<file>} |  |
| `templates.list` | Project Templates | {thumbnails?: bool} → [{id, name, description, category, builtin, width, height, frameRate, duration, controls, thumbnail? (hex RGB 256×144)}] |  |
| `templates.saveAs` | Save as Template... | {name, description?, category?, overwrite?: bool (default true), embedFootage?: bool (default true: the footage files go into the template), embedLimitMB? (default 256: footage beyond it stays linked, with a warning)} → {id, path, embedded, embeddedBytes, linked: [{item, name, reason}], warning?} |  |
| `templates.thumbnail` | Template Thumbnail | {id} → {id, width, height, rgb (hex)} |  |

## track (22)

| id | label | params | why disabled (empty project) |
|---|---|---|---|
| `track.analyze` | Analyze | {layer?, tracker?, direction?: forward\|backward\|frameForward\|frameBackward, start? (s), end? (s), wait?: block until done} | no current track: use Track Motion first |
| `track.apply` | Apply | {layer?, tracker?, dimensions?: xy\|x\|y} | no current track: use Track Motion first |
| `track.camera` | Track Camera | {layer?, shotType?: fixed\|variable\|specify, aov?: degrees, solveMethod?: auto\|typical\|flat\|tripod, detailed?, lensDistortion?: solve k1/k2, undistort?: render undistorted, wait?} | select a layer to track |
| `track.delete` | Delete Tracker | {layer?, tracker?} | no current track: use Track Motion first |
| `track.editTargetDialog` | Edit Target... | {} | no current track: use Track Motion first |
| `track.extractFaceMeasurements` | Extract & Copy Face Measurements | {layer?} → keys a Face Measurements effect from the layer's Face Track Points (one key per tracked frame) and copies those keys | no Face Track Points: track a mask with Face Tracking (Detailed Features) first |
| `track.mask` | Track Mask | {layer?, mask?: uid\|index\|name, method?: position\|positionScale\|positionScaleRotation\|positionScaleRotationSkew\|perspective\|faceOutline\|faceDetailed, direction?: forward\|backward\|frameForward\|frameBackward, start? (s), end? (s), wait?: block until done} | select a mask to track |
| `track.maskMethod` | Mask Tracking Method | {method: position\|positionScale\|positionScaleRotation\|positionScaleRotationSkew\|perspective\|faceOutline\|faceDetailed} |  |
| `track.motion` | Track Motion | {layer?} | select a layer to track |
| `track.new` | New Tracker | {layer?, kind?: transform\|stabilize\|affine\|perspective\|raw, position?, rotation?, scale?, target?: layer} | select a layer to track |
| `track.options` | Motion Tracker Options | {layer?, tracker?, name?, channel?: rgb\|luminance\|saturation, blur? (px, 0 = off), enhance?, subpixel?, adaptEveryFrame?, threshold? (%), action?: continue\|stop\|extrapolate\|adapt, trackShape?} | no current track: use Track Motion first |
| `track.optionsDialog` | Options... | {} | no current track: use Track Motion first |
| `track.property` | Track this Property | {layer?, source?: layer} | select a property to track |
| `track.reset` | Reset | {layer?, tracker?} | no current track: use Track Motion first |
| `track.select` | Current Track | {layer?, tracker?: uid\|name\|#n} |  |
| `track.setPoint` | Move Track Point | {layer?, tracker?, point: n (1-based), center?: [x,y], featureSize?: [w,h], searchOffset?: [x,y], searchSize?: [w,h], attachOffset?: [x,y], move?: [dx,dy], time? (s)} | no current track: use Track Motion first |
| `track.setTarget` | Edit Target | {layer?, tracker?, target: layer\|null} | no current track: use Track Motion first |
| `track.setType` | Track Type | {layer?, tracker?, kind?: transform\|stabilize\|affine\|perspective\|raw, position?, rotation?, scale?} | no current track: use Track Motion first |
| `track.stabilize` | Stabilize Motion | {layer?} | select a layer to track |
| `track.status` | Tracker Status | {layer?, tracker?} |  |
| `track.stop` | Stop Analysis | {} | no track analysis is running |
| `track.warpStabilizer` | Warp Stabilizer VFX | {layer?, wait?} | select a layer to stabilize |

## view (78)

| id | label | params | why disabled (empty project) |
|---|---|---|---|
| `view.3d.activeCamera` | Active Camera | {comp?} |  |
| `view.3d.back` | Back | {comp?} |  |
| `view.3d.bottom` | Bottom | {comp?} |  |
| `view.3d.custom1` | Custom View 1 | {comp?} |  |
| `view.3d.custom2` | Custom View 2 | {comp?} |  |
| `view.3d.custom3` | Custom View 3 | {comp?} |  |
| `view.3d.default` | Default | {comp?} |  |
| `view.3d.front` | Front | {comp?} |  |
| `view.3d.last` | Switch to Last 3D View | {comp?} |  |
| `view.3d.left` | Left | {comp?} |  |
| `view.3d.right` | Right | {comp?} |  |
| `view.3d.top` | Top | {comp?} |  |
| `view.addGuide` | Add Guide... | {orientation?: vertical\|horizontal, position? (comp px, or percent with percent: true), percent?: bool} |  |
| `view.addPercentGuide` | Add Percentage Guide... | {orientation?: vertical\|horizontal, position? (percent of the comp)} |  |
| `view.assign3dShortcut` | Assign Shortcut to 3D View | {slot: F10\|F11\|F12, comp?} |  |
| `view.channel` | Show Channel | {channel: rgb\|red\|green\|blue\|alpha\|rgbStraight, colorized?, toggle?} |  |
| `view.channel.alpha` | Show Channel: Alpha | {} |  |
| `view.channel.blue` | Show Channel: Blue | {} |  |
| `view.channel.blueColorized` | Show Channel: Blue, Colorized | {} |  |
| `view.channel.green` | Show Channel: Green | {} |  |
| `view.channel.greenColorized` | Show Channel: Green, Colorized | {} |  |
| `view.channel.red` | Show Channel: Red | {} |  |
| `view.channel.redColorized` | Show Channel: Red, Colorized | {} |  |
| `view.channel.rgbStraight` | Show Channel: RGB Straight | {} |  |
| `view.clearGuides` | Clear Guides | {comp?} | the composition has no guides |
| `view.closeLockedViewer` | Close Locked Viewer | {} | no locked viewer |
| `view.convertGuides` | Convert Guides to Percentage | {comp?, to?: percent\|pixels, index?} | the composition has no guides |
| `view.customRgb` | My Custom RGB... | {name?, red?/green?/blue?/white?: [x, y] (CIE xy), gamma?, srgbCurve?: bool, icc?: path (RGB ICC profile, matrix/TRC or LUT-based A2B0: read when it changes, "" clears; a LUT profile simulates through its tables, `lutProfile` in the reply; typed-in numbers replace it), reload?, from?: a Simulate Output profile to start from, reset?, preserveRgb?, apply?: bool (default true: simulate it)} → the definition (kept in Settings) |  |
| `view.displayColor` | Viewer Color State | {} → display colour management, output simulation, display profile, locked viewer |  |
| `view.displayColorManagement` | Use Display Color Management | {value?} |  |
| `view.exportGuides` | Export Guides... | {path} | the composition has no guides |
| `view.exposure` | Adjust Exposure | {stops? \| delta?} |  |
| `view.extendedViewer` | Extended Viewer | {value?} |  |
| `view.fastPreviewMode` | Fast Previews | {mode: off\|adaptive\|draft\|fastDraft\|wireframe} |  |
| `view.fastPreviews.adaptive` | Fast Previews: Adaptive Resolution | {} |  |
| `view.fastPreviews.draft` | Fast Previews: Draft | {} |  |
| `view.fastPreviews.fastDraft` | Fast Previews: Fast Draft | {} |  |
| `view.fastPreviews.off` | Fast Previews: Off (Final Quality) | {} |  |
| `view.fastPreviews.wireframe` | Fast Previews: Wireframe | {} |  |
| `view.fullScreen` | Enter Full Screen | {} |  |
| `view.get3D` | 3D View State | {comp?} → current 3D view, view camera, active camera layer, lights |  |
| `view.grid` | Show Grid | {value?} |  |
| `view.guides` | Show Guides | {value?} |  |
| `view.importGuides` | Import Guides... | {path} |  |
| `view.layerControls` | Show Layer Controls | {value?} |  |
| `view.layout` | Switch View Layout | {views: 1\|2\|4} |  |
| `view.lockGuides` | Lock Guides | {value?} |  |
| `view.lookAtAll` | Look at All Layers | {comp?} |  |
| `view.lookAtSelected` | Look at Selected Layers | {comp?, layers?} | select a layer first |
| `view.moveGuide` | Move Guide | {comp?, index, position (comp px), merge?} |  |
| `view.newViewer` | New Viewer | {} — another Composition viewer of the active comp; the one in use is locked |  |
| `view.options` | View Options... | {} |  |
| `view.panelBackground` | Panel Background Color | {color?: black\|darkGray\|mediumGray\|lightGray\|white\|custom\|#hex, pick?: true} |  |
| `view.removeGuide` | Remove Guide | {comp?, index} |  |
| `view.res.auto` | Resolution: Auto | {comp?} |  |
| `view.res.custom` | Custom... | {factor?: 1..40 (render every n-th pixel), comp?} |  |
| `view.res.full` | Full | {comp?} |  |
| `view.res.half` | Half | {comp?} |  |
| `view.res.quarter` | Quarter | {comp?} |  |
| `view.res.third` | Third | {comp?} |  |
| `view.reset3DView` | Reset 3D View | {comp?} |  |
| `view.resetExposure` | Reset Exposure | {} |  |
| `view.rulers` | Show Rulers | {value?} |  |
| `view.set3DView` | Switch 3D View | {view: activeCamera\|default\|front\|left\|top\|back\|right\|bottom\|custom1\|custom2\|custom3, comp?} |  |
| `view.set3DViewCamera` | Set 3D View Camera | {view, eye? [x,y,z], poi? [x,y,z], zoom?} |  |
| `view.setPaneView` | Set View of Pane | {pane: 0 (main) \| 1 \| 2 \| 3, view: activeCamera\|default\|front\|left\|top\|back\|right\|bottom\|custom1\|custom2\|custom3, comp?} |  |
| `view.setRegionOfInterest` | Region of Interest | {rect?: [x, y, w, h] \| null} |  |
| `view.shareViewOptions` | Share View Options | {value?} |  |
| `view.showSnapshot` | Show Snapshot | {value?} | take a snapshot first (Shift+F5) |
| `view.simulateOutput` | Simulate Output | {profile: none\|rec709\|ntsc\|pal\|mac18\|srgb\|rec2020\|p3\|linear\|myCustom\|custom, preserveRgb?, space? (custom)} |  |
| `view.snapToGrid` | Snap to Grid | {value?} |  |
| `view.snapToGuides` | Snap to Guides | {value?} |  |
| `view.snapping` | Snapping | {value?} |  |
| `view.snappingOptions` | Snapping Options | {edgesExtended? (Snap Edges Extended), collapsedFeatures? (Snap to Features in Collapsed Compositions and Text Layers): bool, toggle?: one of those keys} → the options |  |
| `view.splitLockedViewer` | Split with New Locked Viewer | {comp?, view?: 3D view id} |  |
| `view.takeSnapshot` | Take Snapshot | {comp?, scale?: 0.05..1} |  |
| `view.zoomIn` | Zoom In | {} |  |
| `view.zoomOut` | Zoom Out | {} |  |

## warp (3)

| id | label | params | why disabled (empty project) |
|---|---|---|---|
| `warp.analyze` | Analyze | {layer?, effect?: uid\|name\|index, wait?: block until done} |  |
| `warp.cancel` | Cancel | {} | no Warp Stabilizer analysis is running |
| `warp.status` | Warp Stabilizer Status | {layer?, effect?} |  |

## window (9)

| id | label | params | why disabled (empty project) |
|---|---|---|---|
| `window.assignWorkspaceShortcut` | Assign Shortcut to Workspace | {slot: Shift+F10\|Shift+F11\|Shift+F12, workspace?} |  |
| `window.editWorkspaces` | Edit Workspaces... | {name, rename?: new name, delete?: bool} |  |
| `window.panel` | Show Panel | {panel: project\|effectControls\|composition\|layer\|timeline\|info\|audio\|preview\|effectsPresets\|properties\|character\|paragraph\|align\|tracker\|wiggler\|smoother\|motionSketch\|paint\|brushes\|renderQueue\|flowchart\|history\|markers\|tools\|lumetriScopes\|footage\|mediaBrowser\|metadata\|progress\|contentAwareFill\|createNullsFromPaths\|vrCompEditor} |  |
| `window.resetWorkspace` | Reset to Saved Layout | {} |  |
| `window.restoreScriptPanels` | Restore ScriptUI Panels | {} → reopens the ScriptUI panels open when EffectCraft last quit (frontends call it at launch) → {opened: [name], failed: [{name, error}]} |  |
| `window.saveWorkspace` | Save Changes to this Workspace | {} |  |
| `window.saveWorkspaceAs` | Save as New Workspace... | {name} |  |
| `window.scriptPanel` | ScriptUI Panel | {name (a script in the ScriptUI Panels folder, e.g. `Layer Tools.jsx`)} → opens it as a dockable panel |  |
| `window.workspace` | Workspace | {name: Default\|Standard\|Small Screen\|Animation\|Effects\|Motion Tracking\|Paint\|Text\|Minimal\|All Panels} |  |
