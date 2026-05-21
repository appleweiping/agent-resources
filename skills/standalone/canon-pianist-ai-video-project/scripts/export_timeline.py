#!/usr/bin/env python3
"""Export subtitles, edit timeline, and prompt JSONL from shots.json."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SHOTS_PATH = ROOT / "shots.json"
EXPORTS = ROOT / "exports"


def srt_time(seconds: float) -> str:
    millis = int(round(seconds * 1000))
    hours, millis = divmod(millis, 3600_000)
    minutes, millis = divmod(millis, 60_000)
    secs, millis = divmod(millis, 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def main() -> None:
    data = json.loads(SHOTS_PATH.read_text(encoding="utf-8"))
    shots = data["shots"]
    EXPORTS.mkdir(parents=True, exist_ok=True)

    srt_lines: list[str] = []
    for index, shot in enumerate(shots, start=1):
        srt_lines.extend(
            [
                str(index),
                f"{srt_time(shot['start_seconds'])} --> {srt_time(shot['end_seconds'])}",
                shot["subtitle"],
                "",
            ]
        )
    (EXPORTS / "canon_pianist_subtitles.srt").write_text("\n".join(srt_lines), encoding="utf-8")

    with (EXPORTS / "canon_pianist_timeline.csv").open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "id",
                "title",
                "start_seconds",
                "duration_seconds",
                "end_seconds",
                "shot_type",
                "camera_movement",
                "music_rhythm_point",
                "subtitle",
            ],
        )
        writer.writeheader()
        for shot in shots:
            writer.writerow({key: shot[key] for key in writer.fieldnames})

    with (EXPORTS / "canon_pianist_prompts.jsonl").open("w", encoding="utf-8") as handle:
        for shot in shots:
            handle.write(
                json.dumps(
                    {
                        "id": shot["id"],
                        "title": shot["title"],
                        "duration_seconds": shot["duration_seconds"],
                        "prompt": shot["prompt"],
                        "negative_prompt": shot["negative_prompt"],
                    },
                    ensure_ascii=False,
                )
                + "\n"
            )

    print("Exported:")
    print(f"- {EXPORTS / 'canon_pianist_subtitles.srt'}")
    print(f"- {EXPORTS / 'canon_pianist_timeline.csv'}")
    print(f"- {EXPORTS / 'canon_pianist_prompts.jsonl'}")


if __name__ == "__main__":
    main()
