"""Run and validate this episode using the shared Dirty Dollar animation engine."""
import argparse
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

PROJECT = Path(__file__).resolve().parent
ASSET_ROOT = PROJECT.parents[1] / 'work'
CLOUD_SKILL = ASSET_ROOT / 'dirty-dollar-sales-floor-integration' / '.claude' / 'skills' / 'documentary-animator'
WORD = re.compile(r"[\w]+(?:[-’'][\w]+)*")
SCRIPT = PROJECT / 'script.json'
FONTS = 'AlfaSlabOne-Regular.ttf BarlowCondensed-Bold.ttf BarlowCondensed-SemiBold.ttf DSEG7Classic-Bold.ttf SpecialElite-Regular.ttf'.split()


def boot():
    configured = os.environ.get('DOCANIM_SKILL')
    candidates = ([Path(configured).expanduser()] if configured else
                  [p / '.claude' / 'skills' / 'documentary-animator' for p in PROJECT.parents] + [CLOUD_SKILL])
    skill = next((p.resolve() for p in candidates if (p / 'make_video.py').is_file()), None)
    if skill is None:
        raise SystemExit('Set DOCANIM_SKILL to the documentary-animator directory in your Dirty Dollar Codex checkout.')
    if skill == CLOUD_SKILL:
        for path in ('animation-deps', 'animation-audio-deps', 'kokoro-deps'):
            sys.path.insert(0, str(ASSET_ROOT / path))
        os.environ.setdefault('DOCANIM_FONTS', '/tmp/dd-lesson-fonts')
        os.environ.setdefault('DOCANIM_MODELS', str(ASSET_ROOT / 'kokoro-models'))
        espeak = ASSET_ROOT / 'kokoro-espeak' / 'bin'
        os.environ['PATH'] = os.pathsep.join((str(espeak), os.environ.get('PATH', '')))
    os.environ.setdefault('DOCANIM_CACHE', str(PROJECT / 'out' / 'sets'))
    os.chdir(PROJECT)
    sys.path.insert(0, str(skill))
    return skill


def load_script():
    import shots
    data = json.loads(SCRIPT.read_text(encoding='utf-8'))
    lines = data['lines']
    sources = (PROJECT / 'sources.md').read_text(encoding='utf-8')
    known_sources = set(re.findall(r'^\| (S\d+) \|', sources, re.M))
    ids = [line['id'] for line in lines]
    expected = ['HOOK', 'CH1', 'CH2', 'CH3', 'TWIST', 'CH4', 'CH5', 'END']
    if list(dict.fromkeys(line['beat'] for line in lines)) != expected:
        raise ValueError('The script beats are out of order.')
    if len(ids) != len(set(ids)) or not all(line['text'].strip() and line['sources'] for line in lines):
        raise ValueError('Script cue IDs, text, or sources are incomplete.')
    if set().union(*(set(line['sources']) for line in lines)) - known_sources:
        raise ValueError('The script references a source missing from sources.md.')
    if {line['visual'] for line in lines} != shots.VISUALS:
        raise ValueError('The script and picture coverage disagree.')
    if any(place not in shots.SETS for place in shots.SETS_BY_SCENE.values()):
        raise ValueError('The picture plan references a location missing from the engine.')
    if data['title_after'] != next(line['id'] for line in reversed(lines) if line['beat'] == 'HOOK'):
        raise ValueError('The title must follow the last hook cue.')
    return data


def validated_plan(runner, data, *, measured):
    from engine import audio, timeline, voices
    from engine.core import FPS
    import shots

    if measured:
        clips = runner.clips()
        ids = {line['id'] for line in data['lines'] if not line.get('silent')}
        if set(clips) != ids or any(not Path(wav).is_file() or seconds <= 0 for wav, seconds in clips.values()):
            raise ValueError('Every spoken cue needs a measured voice clip. Run the voices stage first.')
    else:
        clips = {line['id']: ('', max(.65, len(WORD.findall(voices.speakable(line['text']))) * 60 / 155))
                 for line in data['lines'] if not line.get('silent')}

    tl = timeline.build(data['lines'], clips, shot_breaks=shots.SHOT_BREAKS, title_after=data['title_after'])
    picture = shots.build(tl)
    cursor = 0
    for shot in picture:
        frames = round(shot['dur'] * FPS)
        if round(shot['t0'] * FPS) != cursor or frames < 1:
            raise ValueError(f"{shot['name']} leaves a gap or has no frames.")
        if any(not 0 <= time < shot['dur'] or effect not in audio.SFX for time, effect in shot.get('sfx', ())):
            raise ValueError(f"{shot['name']} has an invalid sound cue.")
        cursor += frames
    if cursor != round(tl.total * FPS) or picture[-1]['name'] != 'endscreen':
        raise ValueError('Picture coverage misses part of the timeline.')
    print(f'{len(data["lines"])} voice cues, {len(picture)} picture shots, {cursor:,} frames '
          f'at {FPS} fps, {cursor / FPS:.2f}s ({"measured" if measured else "estimated"}).')
    return tl, picture


def ready(skill):
    import skia
    import sherpa_onnx
    from engine import audio, core, voices

    for filename in FONTS:
        if not (Path(core.FONT_DIR) / filename).is_file():
            raise FileNotFoundError(Path(core.FONT_DIR) / filename)
    assets = {
        Path(voices.KOKORO): ('model.onnx', 'voices.bin', 'tokens.txt', 'lexicon-us-en.txt', 'espeak-ng-data'),
        Path(voices.PARAKEET): ('encoder.int8.onnx', 'decoder.int8.onnx', 'joiner.int8.onnx', 'tokens.txt'),
    }
    absent = [root / filename for root, names in assets.items() for filename in names if not (root / filename).exists()]
    if absent:
        raise FileNotFoundError(', '.join(str(p) for p in absent))
    for program in ('ffmpeg', 'ffprobe', 'espeak-ng'):
        if not shutil.which(program):
            raise FileNotFoundError(f'{program} is missing from PATH.')
    phonemes = subprocess.check_output(['espeak-ng', '-q', '--ipa=3', '-v', 'en-us', 'investigation'], text=True)
    if not phonemes.strip():
        raise ValueError('eSpeak NG returned an empty English pronunciation.')
    encoders = subprocess.check_output(['ffmpeg', '-hide_banner', '-encoders'], text=True)
    if 'libx264' not in encoders:
        raise ValueError('FFmpeg is missing the software H.264 encoder.')
    if not Path(audio.TYPEWRITER_DIR, 'ATTRIBUTION.md').is_file() or not list(Path(audio.TYPEWRITER_DIR).glob('key_*.wav')):
        raise FileNotFoundError('The engine’s recorded typewriter sound assets are missing.')
    print(f'{skill}\nSkia {skia.__version__}, Sherpa ONNX {sherpa_onnx.__version__}, '
          f'{core.W}×{core.H} at {core.FPS} fps.')
    print('Verified fonts, FFmpeg/FFprobe, eSpeak NG, voice and transcription model files, and sound assets.')
    print(f'Free space on the project volume: {shutil.disk_usage(PROJECT).free / (1024**3):.2f} GiB.')


def review(tl, picture, folder):
    import skia
    from PIL import Image, ImageDraw
    from engine import render
    from engine.core import FPS, H, W
    from make_video import _with_captions
    folder.mkdir(parents=True, exist_ok=True)
    for page, start in enumerate(range(0, len(picture), 9), 1):
        group = picture[start:start + 9]
        sheet = Image.new('RGB', (1152, len(group)*236), '#14213D')
        captions = ImageDraw.Draw(sheet)
        for row, shot in enumerate(group):
            frames = round(shot['dur'] * FPS)
            hud = _with_captions(tl, shot)
            for column, frame in enumerate((0, (frames - 1)//2, frames - 1)):
                t = frame / FPS
                progress = render.ease(frame / max(1, frames - 1))
                zoom = render.lerp(*shot['zoom'], progress)
                fx, fy = render._clamp(render._focus(shot.get('focus', (960, 540)), progress), zoom)
                surface = skia.Surface(W, H)
                canvas = surface.getCanvas()
                canvas.clear(skia.ColorBLACK)
                canvas.save()
                canvas.translate(W / 2, H / 2)
                canvas.scale(zoom, zoom)
                canvas.rotate(render.lerp(*shot.get('rot', (0, 0)), progress))
                canvas.translate(-fx, -fy)
                shot['draw'](canvas, t)
                canvas.restore()
                draw = shot['draw']
                if getattr(draw, 'vignette', 0):
                    render._vignette(canvas, draw.vignette, getattr(draw, 'vignette_inner', .42))
                if hud:
                    hud(canvas, t)
                pixels = surface.makeImageSnapshot().toarray(colorType=skia.kRGBA_8888_ColorType)
                still = Image.fromarray(pixels).convert('RGB')
                sheet.paste(still.resize((384, 216), Image.Resampling.LANCZOS), (column * 384, row * 236 + 20))
                captions.text((column * 384 + 5, row * 236 + 4), f"{shot['name']} {shot['setting']} · {t:.2f}s",
                              fill='white')
        sheet.save(folder / f'contact-{page:02d}.jpg', quality=88)
    print(folder)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('stage', choices=('ready', 'plan', 'voices', 'stills', 'render', 'audio', 'final', 'check'))
    stage = parser.parse_args().stage
    skill = boot()
    import make_video as runner

    data = load_script()
    if stage in ('ready', 'plan'):
        if stage == 'ready':
            ready(skill)
        validated_plan(runner, data, measured=bool(runner.clips()))
        return
    if stage == 'voices':
        runner.cmd_voices()
        validated_plan(runner, data, measured=True)
        return
    tl, picture = validated_plan(runner, data, measured=True)
    if stage == 'stills':
        review(tl, picture, PROJECT / 'out' / 'review')
    else:
        getattr(runner, f'cmd_{stage}')()


if __name__ == '__main__':
    main()
