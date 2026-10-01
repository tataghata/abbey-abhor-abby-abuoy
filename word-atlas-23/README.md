# The difficult word atlas

23 original illustrated studies, each saved directly in the current working directory as an **8000 × 10000, 80-megapixel lossless PNG**. Together the images contain 1.84 billion pixels. Each uses an sRGB color profile and 400 dpi metadata, corresponding to a 20 × 25 inch print.

- [Browse the searchable gallery](../word-atlas-23.html).
- [Open the 23-page print edition](../word-atlas-23-print.pdf), with vector text and per-word bookmarks.
- [See the contact sheet](contact-sheet.png).
- [Read all 23 companion essays in one document](essays.md).

Each image contains a definition, pronunciation approximation, etymology, four explanatory sections, a concept-specific illustration, and an original literary sentence. The companion essays go further into distinctions, examples, limits, and suggested reading. Joyce supplies the playful ambition of the commission; none of the sentences is presented as his work.

The images were rendered locally using procedural graphics and native macOS typography. The artwork is a visual interpretation, and each entry identifies relevant limits of its metaphor. Philosophical frameworks, rhetorical usages, and scientific mechanisms are distinguished where needed.

| No. | Full-resolution image | Companion | Inquiry |
| --- | --- | --- | --- |
| 01 | [aporia](../atlas-01-aporia-8000x10000.png) | [Essay](notes/01-aporia.md) | The passage that thinking cannot find |
| 02 | [apophasis](../atlas-02-apophasis-8000x10000.png) | [Essay](notes/02-apophasis.md) | Saying through the shape of refusal |
| 03 | [anagnorisis](../atlas-03-anagnorisis-8000x10000.png) | [Essay](notes/03-anagnorisis.md) | Recognition rewrites what came before |
| 04 | [anacoluthon](../atlas-04-anacoluthon-8000x10000.png) | [Essay](notes/04-anacoluthon.md) | The sentence changes its mind midway |
| 05 | [anastomosis](../atlas-05-anastomosis-8000x10000.png) | [Essay](notes/05-anastomosis.md) | Separate routes discover a shared passage |
| 06 | [apophenia](../atlas-06-apophenia-8000x10000.png) | [Essay](notes/06-apophenia.md) | A pattern can outrun its evidence |
| 07 | [autopoiesis](../atlas-07-autopoiesis-8000x10000.png) | [Essay](notes/07-autopoiesis.md) | A living network remakes its conditions |
| 08 | [chiasmus](../atlas-08-chiasmus-8000x10000.png) | [Essay](notes/08-chiasmus.md) | The second crossing changes the first |
| 09 | [clinamen](../atlas-09-clinamen-8000x10000.png) | [Essay](notes/09-clinamen.md) | The smallest swerve changes the possible |
| 10 | [consilience](../atlas-10-consilience-8000x10000.png) | [Essay](notes/10-consilience.md) | Independent evidence meets in one explanation |
| 11 | [deixis](../atlas-11-deixis-8000x10000.png) | [Essay](notes/11-deixis.md) | Meaning points from a situated speaker |
| 12 | [epoché](../atlas-12-epoche-8000x10000.png) | [Essay](notes/12-epoche.md) | Suspend assent; inspect how things appear |
| 13 | [heteroglossia](../atlas-13-heteroglossia-8000x10000.png) | [Essay](notes/13-heteroglossia.md) | Many social languages inhabit one language |
| 14 | [hysteresis](../atlas-14-hysteresis-8000x10000.png) | [Essay](notes/14-hysteresis.md) | The present retains a path-dependent past |
| 15 | [hypallage](../atlas-15-hypallage-8000x10000.png) | [Essay](notes/15-hypallage.md) | Grammar lends an attribute next door |
| 16 | [liminality](../atlas-16-liminality-8000x10000.png) | [Essay](notes/16-liminality.md) | Between an old status and a new |
| 17 | [metalepsis](../atlas-17-metalepsis-8000x10000.png) | [Essay](notes/17-metalepsis.md) | When the teller enters the told |
| 18 | [palimpsest](../atlas-18-palimpsest-8000x10000.png) | [Essay](notes/18-palimpsest.md) | What is overwritten may still speak |
| 19 | [parataxis](../atlas-19-parataxis-8000x10000.png) | [Essay](notes/19-parataxis.md) | Beside, without being placed beneath |
| 20 | [quiddity](../atlas-20-quiddity-8000x10000.png) | [Essay](notes/20-quiddity.md) | The whatness a definition pursues |
| 21 | [semiosis](../atlas-21-semiosis-8000x10000.png) | [Essay](notes/21-semiosis.md) | How something comes to signify |
| 22 | [synecdoche](../atlas-22-synecdoche-8000x10000.png) | [Essay](notes/22-synecdoche.md) | A part speaks for its whole |
| 23 | [tmesis](../atlas-23-tmesis-8000x10000.png) | [Essay](notes/23-tmesis.md) | A word makes room inside itself |

## Source and reproduction

`catalog.json` contains the complete poster text. `source/art/` contains all 23 native-resolution transparent artwork layers. The renderer in `source/render-atlas.swift` composes the print typography, images, previews, PDF, and contact sheet. The group source scripts record the procedural constructions.

On macOS with Swift and AppKit, compile the renderer from the parent CWD:

```sh
swiftc -O word-atlas-23/source/render-atlas.swift -o /tmp/render-word-atlas
/tmp/render-word-atlas --preview-only
/tmp/render-word-atlas --pdf
/tmp/render-word-atlas --contact-sheet
```

Running the renderer without flags creates any missing full-resolution PNGs and preserves existing final PNGs. Previews, the PDF, and the contact sheet are generated artifacts. `--ids=1,2,3` selects individual entries. The full art inputs are retained locally, so rendering the finished collection does not require a network service.
