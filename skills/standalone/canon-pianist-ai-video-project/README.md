# Canon in D - AI Video Generation Project

This project contains a production-ready prompt package for creating a 30-60 second AI video:

> A professional concert pianist performing Canon in D on a grand piano inside an elegant concert hall.

The old failed local-render project was removed. This new project is designed for Runway, Pika, Kling, Sora, or similar video generation tools.

## Project Files

- `shots.json` - machine-readable shot list, prompts, negative prompts, timing, subtitles, and export settings.
- `prompts.md` - copy-ready prompts for video generation tools.
- `scripts/export_timeline.py` - exports subtitles and a simple edit timeline.
- `exports/` - generated SRT and CSV files.
- `references/frames/` - extracted frames from the user-provided reference videos.

## Creative Direction

The reference videos suggest a vertical short-video portrait style: intimate framing, soft beauty lighting, gentle motion, and a young East Asian female subject with delicate natural features. This project upgrades that feel into a luxury classical concert setting:

- vertical 9:16 short video
- young adult East Asian female pianist
- elegant black concert dress
- glossy black grand piano
- warm golden stage lighting
- deep red curtain and polished wooden floor
- close-up hands, side profile, and refined portrait shots
- emotional, graceful, refined atmosphere

## Recommended Workflow

1. Open `prompts.md`.
2. Generate each shot separately in Runway, Pika, Kling, Sora, or another video model.
3. Use 5-8 seconds per clip, matching the durations in `shots.json`.
4. Use the same reference image or seed for every shot if your tool supports it.
5. Add a piano recording of Canon in D during editing.
6. Place each generated clip on the timeline using the timing in `shots.json`.
7. Use the generated subtitles only if you want text overlays; otherwise keep the video clean.

## Important Prompt Rules

Keep these exact ideas in every prompt:

- professional concert pianist
- grand piano
- performing Canon in D
- elegant concert hall
- cinematic lighting
- realistic hands playing piano keys
- emotional, graceful, refined atmosphere
- 4K, shallow depth of field, smooth camera movement

Avoid hand and keyboard problems with:

- two realistic hands
- five fingers on each hand
- natural pianist hand posture
- accurate black and white piano key layout
- slow graceful controlled movement

Do not ask the model for rapid virtuoso fingering or exact note-perfect Canon in D performance. Add the real music in post.

## Suggested Platform Settings

Runway:
- Generate each shot separately.
- Use image-to-video or character reference when available.
- Motion: slow to medium-low.

Pika:
- Keep hand close-up shots short.
- Use the negative prompt aggressively.
- Prefer image-to-video for shots S03 and S05.

Kling:
- Use high-quality mode.
- Fix seed where available.
- Use the same character reference for all shots.

Sora:
- Use each shot prompt as a standalone clip prompt.
- If reference chaining is available, feed the previous accepted clip or still into the next shot.

## Export Timeline

Run:

```powershell
python .\scripts\export_timeline.py
```

This creates:

- `exports/canon_pianist_subtitles.srt`
- `exports/canon_pianist_timeline.csv`
- `exports/canon_pianist_prompts.jsonl`

## Final Edit

Recommended order:

1. S01 Golden Hall Opening
2. S02 First Phrase Side Profile
3. S03 Hands on Canon Pattern
4. S04 Over the Shoulder Reflection
5. S05 Three-Quarter Keyboard View
6. S06 Portrait of Concentration
7. S07 Low Dolly Along the Piano
8. S08 Final Cadence and Soft Fade

Total duration: 48 seconds.
