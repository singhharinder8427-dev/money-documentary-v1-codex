"""Runner for one video. Usage (from the video's folder, e.g. videos/<slug>/):
   python <skill>/make_video.py voices   # Kokoro character lines + cut the ElevenLabs narration into line clips
   python <skill>/make_video.py stills   # contact sheet of the busiest frames -> check before the long render
   python <skill>/make_video.py render   # ASK THE OWNER FIRST: PC or cloud? Renders every shot (parallel)
   python <skill>/make_video.py audio    # voices + code music by mood + SFX, ducked, -14 LUFS
   python <skill>/make_video.py final    # join shots + mux audio -> out/final.mp4, frame sheet
   python <skill>/make_video.py check    # speech-to-text of the final mix vs the script
The video folder holds: script.json (documentary-script skill), narration.wav/mp3 (owner's ElevenLabs file, narrator
lines only, in script order), shots.py (written per video from template/shots.py: def build(tl) -> list of shots)."""
import os, sys, json, glob, pathlib, importlib.util
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import numpy as np, soundfile as sf
from engine import render, audio as A, timeline as T

V = pathlib.Path.cwd(); OUT = V / 'out'; VO = V / 'voices'; OUT.mkdir(exist_ok=True); VO.mkdir(exist_ok=True)
def script(): return json.load(open(V / 'script.json'))
def clips():
    c = json.load(open(VO / 'clips.json')) if (VO / 'clips.json').exists() else {}
    return {k: tuple(v) for k, v in c.items()}
def shots_mod():
    spec = importlib.util.spec_from_file_location('shots_video', V / 'shots.py'); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
def timeline():
    s = script(); m = shots_mod(); return T.build(s['lines'], clips(), shot_breaks=getattr(m, 'SHOT_BREAKS', ()), title_after=s.get('title_after'))
def shot_list():
    tl = timeline(); sh = shots_mod().build(tl); t = 0.0
    for i, x in enumerate(sh): x.setdefault('name', f'{i:03d}'); x['t0'] = t; t += x['dur']
    return tl, sh

def cmd_voices():
    from engine import voices as Vc
    s = script(); res = clips(); narr = [(l['id'], l['text']) for l in s['lines'] if l.get('speaker', 'NARRATOR') == 'NARRATOR' and not l.get('silent')]
    nf = next(iter(glob.glob(str(V / 'narration.*'))), None)
    if nf: res.update(Vc.split_narration(nf, narr, str(VO)))
    else: print('No narration.* yet - narrator lines use Kokoro placeholders (am_michael) until the ElevenLabs file arrives.')
    for l in s['lines']:
        sp = l.get('speaker', 'NARRATOR').lower()
        if l.get('silent') or l['id'] in res: continue
        who = l.get('voice') or (sp if sp in Vc.CHARACTER_VOICES else 'retiree' if sp == 'narrator' else None)   # 'voice' = which cast voice a real person uses
        if who is None: print('unknown speaker', sp, '-> add it to CHARACTER_VOICES'); continue
        res[l['id']] = Vc.character_line(l['text'], who, str(VO / f"{l['id']}.wav"))
    json.dump(res, open(VO / 'clips.json', 'w'), indent=1); print(len(res), 'voice clips ready')

def cmd_stills():
    tl, sh = shot_list(); pick = [x for x in sh if x.get('check', True)]
    pick = pick[:: max(1, len(pick) // 9)][:9]
    paths = [render.still(x['draw'], x['dur'] * .6, str(OUT / f"still_{x['name']}.png"), x.get('zoom', (1, 1.07))[0], x.get('focus', (960, 540)), _with_captions(tl, x)) for x in pick]
    print(render.contact_sheet(paths, str(OUT / 'stills.jpg')))

def _with_captions(tl, x):
    """Shot HUD + small burned-in captions (absolute time = shot start + t). CAPTIONS=0 turns them off."""
    if os.environ.get('CAPTIONS', '1') == '0': return x.get('hud')
    from engine.captions import Captions
    cap = Captions(tl); hud = x.get('hud'); t0 = x['t0']
    def h(c, t):
        if hud: hud(c, t)
        cap.draw(c, t0 + t)
    return h
def _render_one(i):
    tl, sh = shot_list(); x = sh[i]; f = str(OUT / f"shot_{x['name']}.mp4")
    if os.path.exists(f) and not os.environ.get('FORCE'): return f
    return render.render_shot(f, x['dur'], x['draw'], x.get('zoom', (1.0, 1.07)), x.get('focus', (960, 540)), x.get('rot', (0, 0)),
                              x.get('whip_in', False), x.get('whip_out', False), x.get('shake'), _with_captions(tl, x))
def cmd_render():
    tl, sh = shot_list(); print(f'{len(sh)} shots, {sum(x["dur"] for x in sh):.1f} s')
    from concurrent.futures import ProcessPoolExecutor
    with ProcessPoolExecutor(max(1, (os.cpu_count() or 2) - 1)) as ex: list(ex.map(_render_one, range(len(sh))))
    print('shots rendered')

def cmd_audio():
    tl, sh = shot_list(); total = sum(x['dur'] for x in sh)
    narr = [k for k, v in tl.clips.items() if tl.by_id[k].get('speaker', 'NARRATOR') == 'NARRATOR']
    ref = np.mean([A.rms(A.voice_chain(A.load(tl.clips[k][0]), 'narrator')) for k in narr[:6]]) if narr else None
    voice = tl.voice_track(ref)
    files = {m: str(p) for m in A.MOODS for p in V.glob(f'music_{m}.wav')}          # optional real tracks per mood
    mus = A.music(tl.mood_segments(), total, files=files or None)
    sfx = np.zeros(int(total * A.SR) + A.SR)
    for x in sh:                                                                      # per-shot SFX events
        for tr, name in x.get('sfx', ()): A.add(sfx, A.SFX[name]() if callable(A.SFX[name]) else A.SFX[name], x['t0'] + tr)
        if x.get('whip_out'): A.add(sfx, A.whoosh(), x['t0'] + x['dur'] - .2, .8)
    for e in tl.events:                                                               # cards
        if e['kind'] == 'title': A.add(sfx, A.sound_logo(), e['t0'] + .05)
        if e['kind'] == 'chapter': A.add(sfx, A.boom() * .5, e['t0'])
        if e['kind'] == 'outro': A.add(sfx, A.sound_logo(), e['t0'] + .05)
    for l in tl.lines:                                                                # text cards type, counters tick
        t0, d = tl.cues[l['id']]
        if l.get('card'):
            from engine.widgets import type_times
            A.add(sfx, A.typing(type_times(l['text'], d), l['text']), t0, .55)   # one key per letter, synced to the card
        if l.get('counter'):
            A.add(sfx, A.counter_ticks(1.4), t0 + .2, .6); A.add(sfx, A.low_tone() if l['counter'].get('colour') == 'orange' else A.ding(), t0 + 1.6, .7)
    out = A.mix(voice[:int(total * A.SR)], mus, sfx[:int(total * A.SR)], str(OUT / 'mix.wav')); print(out)

def cmd_final():
    tl, sh = shot_list(); files = [str(OUT / f"shot_{x['name']}.mp4") for x in sh]
    v = render.join(files, str(OUT / 'video_noaudio.mp4')); f = render.mux(v, str(OUT / 'mix.wav'), str(OUT / 'final.mp4'))
    from engine.captions import srt
    print(f, render.frame_sheet(f, str(OUT / 'frames.jpg')), srt(tl, str(OUT / 'captions.srt')))

def cmd_check():
    from engine import voices as Vc
    s = script(); txt = ' '.join(l['text'] for l in s['lines'] if not l.get('silent'))
    print('transcript match:', round(Vc.transcript_check(str(OUT / 'mix.wav'), txt), 3), '(aim > 0.9; the owner still watches once for timing)')

if __name__ == '__main__':
    {'voices': cmd_voices, 'stills': cmd_stills, 'render': cmd_render, 'audio': cmd_audio, 'final': cmd_final, 'check': cmd_check}[sys.argv[1]]()
