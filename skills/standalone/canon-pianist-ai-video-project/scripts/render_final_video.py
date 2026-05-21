#!/usr/bin/env python3
"""Render a final vertical MP4 from generated keyframes and Canon in D audio."""

from __future__ import annotations

import json
import math
import struct
import subprocess
import wave
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FFMPEG = Path(r"C:\Program Files\EVCapture\ffmpeg.exe")
OUTPUT = ROOT / "output"
KEYFRAMES = ROOT / "assets" / "keyframes"
SHOTS = ROOT / "shots.json"
FPS = 24
WIDTH = 1080
HEIGHT = 1920
SAMPLE_RATE = 44100
BPM = 80

NOTE_INDEX = {
    "C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
    "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
    "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11,
}


def run(cmd: list[str]) -> None:
    print(" ".join(str(part) for part in cmd))
    subprocess.run(cmd, check=True)


def note_frequency(note: str) -> float:
    name = note[:-1]
    octave = int(note[-1])
    midi = (octave + 1) * 12 + NOTE_INDEX[name]
    return 440.0 * (2 ** ((midi - 69) / 12))


def add_note(samples: list[float], start: float, duration: float, note: str, velocity: float, pan: float) -> None:
    freq = note_frequency(note)
    start_i = int(start * SAMPLE_RATE)
    end_i = min(len(samples) // 2, int((start + duration) * SAMPLE_RATE))
    left_gain = math.cos(pan * math.pi / 2)
    right_gain = math.sin(pan * math.pi / 2)
    attack = int(0.012 * SAMPLE_RATE)
    release = max(1, int(0.35 * SAMPLE_RATE))
    for i in range(start_i, end_i):
        t = (i - start_i) / SAMPLE_RATE
        remaining = (end_i - i) / SAMPLE_RATE
        env = min(1.0, (i - start_i) / max(1, attack))
        env *= 0.66 * math.exp(-t / (duration * 0.78)) + 0.18 * math.exp(-t / 2.9)
        if remaining < release / SAMPLE_RATE:
            env *= remaining / (release / SAMPLE_RATE)
        tone = (
            math.sin(2 * math.pi * freq * t)
            + 0.32 * math.sin(2 * math.pi * freq * 2.01 * t)
            + 0.15 * math.sin(2 * math.pi * freq * 3.002 * t)
            + 0.06 * math.sin(2 * math.pi * freq * 4.01 * t)
        )
        hammer = 0.05 * math.sin(2 * math.pi * freq * 7.7 * t) * math.exp(-t * 72.0)
        value = (tone + hammer) * env * velocity * 0.19
        samples[2 * i] += value * left_gain
        samples[2 * i + 1] += value * right_gain


def add_reverb(samples: list[float], delay_seconds: float, gain: float) -> None:
    delay = int(delay_seconds * SAMPLE_RATE) * 2
    for i in range(delay, len(samples)):
        samples[i] += samples[i - delay] * gain


def write_audio(path: Path, duration: float) -> None:
    total = int(duration * SAMPLE_RATE)
    samples = [0.0] * (total * 2)
    beat = 60.0 / BPM
    bar = beat * 4
    progression = [
        ("D3", ["D4", "F#4", "A4"]),
        ("A2", ["A3", "C#4", "E4"]),
        ("B2", ["B3", "D4", "F#4"]),
        ("F#2", ["F#3", "A3", "C#4"]),
        ("G2", ["G3", "B3", "D4"]),
        ("D3", ["D4", "F#4", "A4"]),
        ("G2", ["G3", "B3", "D4"]),
        ("A2", ["A3", "C#4", "E4"]),
    ]
    melodies = [
        ["F#5", "E5", "D5", "C#5", "B4", "A4", "B4", "C#5"],
        ["D5", "C#5", "B4", "A4", "G4", "F#4", "G4", "E4"],
        ["A4", "B4", "C#5", "D5", "E5", "F#5", "G5", "A5"],
        ["F#5", "D5", "E5", "C#5", "D5", "A4", "B4", "C#5"],
    ]
    current = 0.0
    bar_index = 0
    while current < duration - bar:
        bass, chord = progression[bar_index % len(progression)]
        intensity = min(1.0, 0.52 + bar_index * 0.025)
        add_note(samples, current, bar * 0.98, bass, 0.92 * intensity, 0.28)
        for j in range(4):
            for k, chord_note in enumerate(chord):
                add_note(samples, current + j * beat + k * 0.022, beat * 0.82, chord_note, 0.33 * intensity, 0.46 + k * 0.07)
        pattern = melodies[(bar_index // 2) % len(melodies)]
        step = beat / 2
        for n, note in enumerate(pattern):
            add_note(samples, current + n * step, step * 1.16, note, 0.45 * intensity, 0.66)
            if bar_index > 5 and n % 2 == 0:
                add_note(samples, current + n * step + step * 0.5, step * 0.86, pattern[(n + 2) % len(pattern)], 0.20, 0.74)
        current += bar
        bar_index += 1
    final_start = max(0, duration - 3.0)
    for note in ["D3", "A3", "D4", "F#4", "A4", "D5"]:
        add_note(samples, final_start, 2.8, note, 0.55, 0.55)
    add_reverb(samples, 0.092, 0.17)
    add_reverb(samples, 0.181, 0.11)
    add_reverb(samples, 0.337, 0.075)
    peak = max(abs(v) for v in samples) or 1
    norm = 0.91 / peak
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "wb") as wav:
        wav.setnchannels(2)
        wav.setsampwidth(2)
        wav.setframerate(SAMPLE_RATE)
        frames = bytearray()
        for value in samples:
            frames.extend(struct.pack("<h", int(max(-1, min(1, value * norm)) * 32767)))
        wav.writeframes(frames)


def main() -> None:
    if not FFMPEG.exists():
        raise SystemExit(f"ffmpeg not found: {FFMPEG}")
    data = json.loads(SHOTS.read_text(encoding="utf-8"))
    shots = data["shots"]
    OUTPUT.mkdir(parents=True, exist_ok=True)
    source = KEYFRAMES / "shot_01.png"
    if not source.exists():
        raise SystemExit(f"missing keyframe: {source}")
    duration = sum(float(shot["duration_seconds"]) for shot in shots)
    audio = OUTPUT / "canon_in_d_piano.wav"
    write_audio(audio, duration)

    segments: list[Path] = []
    crops = [
        ("0.50", "0.48", 1.00),
        ("0.42", "0.55", 1.18),
        ("0.48", "0.62", 1.35),
        ("0.58", "0.52", 1.14),
        ("0.46", "0.64", 1.30),
        ("0.42", "0.38", 1.28),
        ("0.60", "0.52", 1.16),
        ("0.50", "0.50", 1.04),
    ]
    for index, shot in enumerate(shots, start=1):
        dur = float(shot["duration_seconds"])
        cx, cy, base_zoom = crops[index - 1]
        out = OUTPUT / f"segment_{index:02d}.mp4"
        frames = int(dur * FPS)
        zoom = f"{base_zoom}+0.035*on/{frames}"
        vf = (
            f"scale={WIDTH*2}:{HEIGHT*2}:force_original_aspect_ratio=increase,"
            f"zoompan=z='{zoom}':x='iw*{cx}-(iw/zoom/2)+12*sin(on/50)':"
            f"y='ih*{cy}-(ih/zoom/2)+8*cos(on/60)':d={frames}:s={WIDTH}x{HEIGHT}:fps={FPS},"
            f"fade=t=in:st=0:d=0.35,fade=t=out:st={max(0, dur - 0.45):.2f}:d=0.45,"
            "format=yuv420p"
        )
        run([
            str(FFMPEG), "-y", "-loop", "1", "-i", str(source), "-t", f"{dur:.3f}",
            "-vf", vf, "-c:v", "libx264", "-preset", "medium", "-crf", "18", out.as_posix()
        ])
        segments.append(out)

    concat = OUTPUT / "segments.txt"
    concat.write_text("".join(f"file '{p.as_posix()}'\n" for p in segments), encoding="utf-8")
    silent = OUTPUT / "canon_pianist_silent.mp4"
    run([str(FFMPEG), "-y", "-f", "concat", "-safe", "0", "-i", str(concat), "-c", "copy", str(silent)])
    final = OUTPUT / "canon_pianist_final.mp4"
    run([
        str(FFMPEG), "-y", "-i", str(silent), "-i", str(audio),
        "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy",
        "-c:a", "aac", "-b:a", "192k", "-shortest", str(final)
    ])
    print(final)


if __name__ == "__main__":
    main()
