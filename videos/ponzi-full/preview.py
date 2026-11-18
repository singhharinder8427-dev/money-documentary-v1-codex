"""Render and label every shot's review stills on the production machine."""
import csv
import math
import os
from pathlib import Path
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFont
import skia
import soundfile

VIDEO = Path(__file__).resolve().parent
REPO = VIDEO.parents[1]
SKILL = REPO / ".claude" / "skills" / "documentary-animator"
PREVIEW = VIDEO / "out" / "review"
MAX_SECONDS = 300.0
SAMPLE_POINTS = (("first", 0.0), ("middle", .52), ("last", 1.0))


def make_voices():
    subprocess.run([sys.executable, str(SKILL / "make_video.py"), "voices"],
                   cwd=VIDEO, check=True)


def load_cut():
    # The house runner resolves video paths against its current directory.
    sys.path.insert(0, str(SKILL))
    import make_video as runner

    script = runner.script()
    clips = runner.clips()
    for line in script["lines"]:
        if line.get("silent"):
            continue
        identifier = line["id"]
        clip = clips.get(identifier)
        if not clip or not Path(clip[0]).is_file():
            raise ValueError(f"Voice clip missing for {identifier}.")
        actual = soundfile.info(clip[0]).duration
        if actual <= 0 or abs(clip[1] - actual) > .04:
            raise ValueError(f"Voice timing differs from the WAV for {identifier}: {actual:.3f}s.")

    timeline = runner.timeline()
    if timeline.total >= MAX_SECONDS:
        raise ValueError(f"The timeline is {timeline.total:.2f}s including the end screen. "
                         "Shorten the narration before rendering.")
    timeline, shot_list = runner.shot_list()
    if not math.isclose(sum(s["dur"] for s in shot_list), timeline.total, abs_tol=1e-6):
        raise ValueError("The shots do not span the complete voice timeline.")
    from engine.core import FPS

    video_frames = sum(max(1, round(s["dur"] * FPS)) for s in shot_list)
    if video_frames / FPS >= MAX_SECONDS:
        raise ValueError(f"The video would encode to {video_frames / FPS:.2f}s. Shorten the cut.")
    print(f"{len(shot_list)} shots. Voice timeline {timeline.total:.2f}s. "
          f"Picture {video_frames / FPS:.2f}s including end screen.")
    return timeline, shot_list


def sample_frame(shot, frame, target):
    from engine.core import FPS, H, W
    from engine.kit import ease, lerp
    from engine.render import _clamp

    frame_count = max(1, round(shot["dur"] * FPS))
    t = frame / FPS
    progress = ease(frame / max(frame_count - 1, 1))
    z = lerp(*shot.get("zoom", (1.0, 1.07)), progress)
    angle = lerp(*shot.get("rot", (0, 0)), progress)
    fx, fy = _clamp(shot.get("focus", (W / 2, H / 2)), z)
    shake = shot.get("shake")
    dx, dy = shake(t) if shake else (0, 0)
    whip, blur = 0, 0
    if shot.get("whip_out") and frame_count - frame <= 5:
        q = 6 - (frame_count - frame)
        whip, blur = -(q ** 2) * 34, q * 16
    if shot.get("whip_in") and frame < 4:
        q = 4 - frame
        whip, blur = q ** 2 * 52, q * 18

    surface = skia.Surface(W, H)
    canvas = surface.getCanvas()
    canvas.clear(skia.ColorBLACK)
    canvas.save()
    canvas.translate(W / 2 + dx + whip, H / 2 + dy)
    canvas.scale(z, z)
    canvas.rotate(angle)
    canvas.translate(-fx, -fy)
    shot["draw"](canvas, t)
    canvas.restore()
    if blur:
        image = surface.makeImageSnapshot()
        canvas.clear(skia.ColorBLACK)
        paint = skia.Paint()
        paint.setImageFilter(skia.ImageFilters.Blur(blur, .01, skia.TileMode.kClamp))
        canvas.drawImage(image, 0, 0, skia.SamplingOptions(), paint)
    surface.makeImageSnapshot().save(str(target), skia.kPNG)


def sheets(rows):
    cols = len(SAMPLE_POINTS)
    per_sheet = 6
    cell_w, image_h, caption_h = 480, 270, 30
    font = ImageFont.load_default()
    for offset in range(0, len(rows), per_sheet):
        batch = rows[offset:offset + per_sheet]
        sheet = Image.new("RGB", (cols * cell_w, len(batch) * (image_h + caption_h)),
                          "#14213D")
        draw = ImageDraw.Draw(sheet)
        for row, samples in enumerate(batch):
            for col, path in enumerate(samples):
                x = col * cell_w
                y = row * (image_h + caption_h)
                with Image.open(path) as im:
                    sheet.paste(im.convert("RGB").resize((cell_w, image_h),
                                                         Image.Resampling.LANCZOS), (x, y))
                draw.text((x + 9, y + image_h + 5), path.stem.replace("_", " "),
                          fill="white", font=font)
        number = offset // per_sheet + 1
        sheet.save(PREVIEW / f"contact_sheet_{number:02d}.jpg", quality=93)


def create_previews():
    timeline, shot_list = load_cut()
    from engine.core import FPS, H, W
    PREVIEW.mkdir(parents=True, exist_ok=True)
    rows = []
    failures = []
    with (PREVIEW / "shots.csv").open("w", newline="", encoding="utf-8") as report:
        writer = csv.writer(report)
        writer.writerow(("shot", "time_seconds", "opening_cue", "frames", "image_check", "visual_review"))
        boundaries = sorted((timeline.at(line["id"]), line["id"]) for line in timeline.lines)
        boundaries.extend((event["t0"], event["kind"]) for event in timeline.events)
        boundaries.sort()

        for index, shot in enumerate(shot_list):
            frame_count = max(1, round(shot["dur"] * FPS))
            opening = min(boundaries, key=lambda item: abs(item[0] - shot["t0"]))[1]
            row = []
            blank = []
            for label, fraction in SAMPLE_POINTS:
                frame = round((frame_count - 1) * fraction)
                path = PREVIEW / f"{index:03d}_{opening.replace(':', '-')}_{label}.png"
                sample_frame(shot, frame, path)
                with Image.open(path) as im:
                    extrema = im.convert("L").getextrema()
                    if im.size != (W, H) or extrema[1] - extrema[0] < 12:
                        blank.append(label)
                row.append(path)
            status = "FAIL " + ", ".join(blank) if blank else "PASS"
            if blank:
                failures.append(index)
            print(f"{index:03d} {opening:>9}  image {status}  visual UNVERIFIED")
            writer.writerow((index, f'{shot["t0"]:.3f}', opening, frame_count, status, "UNVERIFIED"))
            rows.append(row)

    sheets(rows)
    print(PREVIEW)
    if failures:
        raise ValueError(f"Blank or mis-sized previews for shots {failures}.")
    print("Image checks passed. Visually inspect the sheets before approving the render.")


if __name__ == "__main__":
    os.chdir(VIDEO)
    commands = sys.argv[1:]
    if commands not in ([], ["--voices"]):
        raise SystemExit("Usage: python preview.py [--voices]")
    if commands:
        make_voices()
    create_previews()
