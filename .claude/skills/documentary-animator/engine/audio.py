"""All music and sound effects are generated in code (LOCKED option D), placed from the script's beat marks.
Mood map: suspense (night story parts) | twist (silence + low boom) | lesson (warm, day lesson part) |
ending (theme returns softer, ends on silence). Sound logo on the title card. Fixed SFX set.
Mix: music ducks under speech, soft limiter, then ffmpeg loudnorm to -14 LUFS.
Music is chosen by mood tag, so licensed / ElevenLabs tracks can replace it later: pass a wav per mood to music()."""
import subprocess, numpy as np, soundfile as sf
from scipy.signal import butter, lfilter, fftconvolve, resample_poly

SR = 48000
rng = np.random.default_rng(11)
def secs(n): return np.arange(int(n * SR)) / SR
def lp(x, fc, o=2): b, a = butter(o, min(fc, SR / 2 - 100) / (SR / 2), 'low'); return lfilter(b, a, x)
def hp(x, fc, o=2): b, a = butter(o, fc / (SR / 2), 'high'); return lfilter(b, a, x)
def bp(x, f1, f2, o=2): b, a = butter(o, [f1 / (SR / 2), min(f2, SR / 2 - 100) / (SR / 2)], 'band'); return lfilter(b, a, x)
def env(n, att=0.005, dec=0.3):
    t = np.arange(n) / SR; return np.minimum(t / max(att, 1e-4), 1) * np.exp(-t / max(dec, 1e-4))
def note_hz(n): return 440.0 * 2 ** ((n - 69) / 12)   # MIDI note -> Hz
def noise(n): return rng.standard_normal(n)
def add(buf, clip, t, gain=1.0):
    i = int(t * SR)
    if i >= len(buf) or i + len(clip) <= 0: return
    j0 = max(0, -i); i = max(i, 0); k = min(len(clip) - j0, len(buf) - i); buf[i:i + k] += clip[j0:j0 + k] * gain

# ======================= instruments
def pluck(f, dur=0.6, bright=1.0):
    t = secs(dur); y = sum((1 / k) * np.sin(2 * np.pi * f * k * t) * np.exp(-t * (4 + k * 3 / bright)) for k in range(1, 7)); return y * env(len(t), .002, dur)
def piano(f, dur=1.6):
    t = secs(dur); y = sum((0.6 ** (k - 1)) * np.sin(2 * np.pi * f * k * t * (1 + 0.0004 * k * k)) * np.exp(-t * (1.6 + k * .9)) for k in range(1, 6)); return y * env(len(t), .004, dur)
def marimba(f, dur=0.5):
    t = secs(dur); return (np.sin(2 * np.pi * f * t) + .25 * np.sin(2 * np.pi * f * 4 * t) * np.exp(-t * 30)) * env(len(t), .001, .22)
def synth_pulse(f, dur=0.3, cutoff=900):
    t = secs(dur); saw = 2 * ((f * t) % 1) - 1; sq = np.sign(np.sin(2 * np.pi * f * 0.5 * t)) * .3; return lp(saw + sq, cutoff) * env(len(t), .004, dur * .5)
def drone(f, dur):
    t = secs(dur); y = np.sin(2 * np.pi * f * t) + .5 * np.sin(2 * np.pi * f * 1.003 * t) + .3 * lp(2 * ((f * 2 * t) % 1) - 1, 300)
    sw = np.minimum(t / 2.0, 1) * np.minimum((dur - t) / 1.5, 1); return y * np.clip(sw, 0, 1)
def kick(dur=0.35):
    t = secs(dur); f = 45 + 90 * np.exp(-t * 28); return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(len(t), .001, .18)
def hat(dur=0.04, level=1.0): return hp(noise(int(dur * SR)), 7000) * env(int(dur * SR), .0005, .012) * level
def shaker(dur=0.09): return bp(noise(int(dur * SR)), 4000, 11000) * env(int(dur * SR), .02, .03)

# ======================= music by mood
AM_PROG = [(57, [57, 60, 64]), (53, [53, 57, 60]), (50, [50, 53, 57]), (52, [52, 56, 59])]   # Am F Dm E (tension)
C_PROG = [(48, [60, 64, 67]), (45, [57, 60, 64]), (41, [53, 57, 60]), (43, [55, 59, 62])]    # C Am F G (warm)
def music_suspense(dur, bpm=92, soft=False):
    out = np.zeros(int(dur * SR) + SR); beat = 60 / bpm; bar = beat * 4; nb = int(dur / bar) + 1
    out[:int(dur * SR)] += lp(drone(note_hz(33), dur), 400) * .35
    for b in range(nb):
        root, ch = AM_PROG[(b // 2) % 4]; t0 = b * bar
        for i in range(8):                                                       # 8th-note low pulse
            if not soft: add(out, synth_pulse(note_hz(root - 12), beat * .45, 700 + 500 * (i % 4 == 0)), t0 + i * beat / 2, .22 if i % 4 == 0 else .14)
        pat = [0, 2, 1, 2, 0, 2, 1, 2] if b % 2 == 0 else [0, 1, 2, 1, 0, 2, 1, 0]   # plucked strings ostinato
        for i, k in enumerate(pat): add(out, pluck(note_hz(ch[k] + 12), .5, .8), t0 + i * beat / 2, .12 if soft else .1)
        for i in range(4): add(out, hat(.03), t0 + i * beat, .05 if soft else .08)  # ticking clock
        if b % 4 == 0 and not soft: add(out, kick(.6), t0, .35)
    return out[:int(dur * SR)]
def music_lesson(dur, bpm=100):
    out = np.zeros(int(dur * SR) + 2 * SR); beat = 60 / bpm; bar = beat * 4; nb = int(dur / bar) + 1
    mel = [76, 79, 81, 79, 76, 74, 72, 74]
    for b in range(nb):
        bass, ch = C_PROG[b % 4]; t0 = b * bar
        add(out, piano(note_hz(bass), bar * 1.1), t0, .22)
        for i, n in enumerate(ch + ch[1:2]): add(out, piano(note_hz(n), 1.4), t0 + i * beat, .13)
        for i in range(4):
            if (b + i) % 2 == 0: add(out, marimba(note_hz(mel[(b * 2 + i) % 8])), t0 + i * beat + beat / 2, .1)
        for i in range(8): add(out, shaker(), t0 + i * beat / 2, .035)
        add(out, kick(.3), t0, .18); add(out, kick(.3), t0 + 2 * beat, .14)
    return out[:int(dur * SR)]
def music_twist(dur):
    out = np.zeros(int(dur * SR)); add(out, boom(), 0.0, 1.0); add(out, lp(drone(note_hz(33), max(dur - 1, .5)), 250) * .2, 1.0); return out
def music_ending(dur):
    """Theme returns softer, then RESOLVES on a clear final chord that rings out (owner: the end must feel like an end)."""
    y = music_suspense(dur, soft=True); t = secs(dur)[:len(y)]; y = y * np.clip((dur - 2.6 - t) / 1.0, 0, 1)
    out = np.zeros(len(y) + 4 * SR); out[:len(y)] = y; t0 = max(dur - 2.6, 0)
    for n_, g in ((45, .5), (57, .35), (60, .3), (64, .3), (69, .25)):        # A minor, low A to high A
        add(out, piano(note_hz(n_), 4.0), t0, g)
    add(out, kick(.8) * .5, t0); add(out, lp(drone(note_hz(33), 3.5), 200) * .25, t0)
    return out[:int((dur + 2.0) * SR)]
def music_endscreen(dur):
    """Soft, warm bed under the outro + end screen."""
    out = np.zeros(int(dur * SR) + 2 * SR); bar = 60 / 84 * 4
    for b in range(int(dur / bar) + 1):
        bass, ch = C_PROG[b % 4]; t0 = b * bar
        add(out, piano(note_hz(bass), bar * 1.2), t0, .16)
        for i, n_ in enumerate(ch): add(out, piano(note_hz(n_ + 12), 1.6), t0 + i * bar / 3, .07)
    y = out[:int(dur * SR)]; t = secs(dur)[:len(y)]; return y * np.clip(t / 1.0, 0, 1) * np.clip((dur - t) / 2.5, 0, 1)
MOODS = {'suspense': music_suspense, 'lesson': music_lesson, 'twist': music_twist, 'ending': music_ending, 'endscreen': music_endscreen, 'silence': lambda d: np.zeros(int(d * SR))}

def music(segments, total, xfade=1.0, files=None):
    """segments: [(t0, t1, mood), ...] covering the video. files: optional {mood: 'track.wav'} to use real tracks instead."""
    out = np.zeros(int(total * SR) + SR)
    for t0, t1, mood in segments:
        d = t1 - t0 + (xfade if mood not in ('twist', 'silence', 'ending') else 0)
        if files and mood in files:
            y, sr = sf.read(files[mood]); y = y.mean(1) if y.ndim > 1 else y
            if sr != SR: y = resample_poly(y, SR, sr)
            y = np.tile(y, int(np.ceil(d * SR / len(y))))[:int(d * SR)]
        else: y = MOODS[mood](d)
        n = len(y); fi = np.minimum(np.arange(n) / (xfade * SR), 1) if mood not in ('twist', 'silence') else np.ones(n)
        fo = np.minimum((n - np.arange(n)) / (xfade * SR), 1) if mood != 'ending' else np.ones(n); add(out, y * fi * fo, t0)
    return out[:int(total * SR)]

# ======================= sound effects (fixed set)
def type_key(strength=1.0):
    """One typewriter keystroke: sharp key strike + metallic typebar clack + small platen thump (varied every key)."""
    n = int(.09 * SR); t = np.arange(n) / SR; v = rng.uniform(.85, 1.15)
    strike = bp(noise(n), 2500, 9000) * np.exp(-t / .0025) * .9
    clack = sum(a * np.sin(2 * np.pi * f * v * t + rng.uniform(0, 6)) * np.exp(-t / d) for f, a, d in ((1850, .5, .018), (3150, .35, .012), (4700, .2, .008)))
    thump = np.sin(2 * np.pi * rng.uniform(110, 150) * t) * np.exp(-t / .02) * .45
    y = (strike + clack + thump) * env(n, .0004, .05); return y * rng.uniform(.75, 1.0) * strength
def carriage_ding():
    """End of a typed line: small bell + carriage return ratchet."""
    out = np.zeros(int(.9 * SR)); t = secs(.9)
    bell = (np.sin(2 * np.pi * 2093 * t) + .4 * np.sin(2 * np.pi * 5230 * t)) * np.exp(-t / .35) * .25
    add(out, bell, 0)
    for k in range(7): add(out, type_key(.35), .12 + k * .028)
    return out
import os as _os, glob as _glob
TYPEWRITER_DIR = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', 'assets', 'typewriter')
_BANK = None
def _bank():
    """Real typewriter recording (CC0) cut into single key hits: assets/typewriter/keys_*.wav, space.wav, ding.wav.
    Falls back to the code-made keystroke if the folder is empty."""
    global _BANK
    if _BANK is None:
        _BANK = {'keys': [load(p) for p in sorted(_glob.glob(_os.path.join(TYPEWRITER_DIR, 'key_*.wav')))]}
        for n in ('space', 'ding', 'return'):
            p = _os.path.join(TYPEWRITER_DIR, n + '.wav'); _BANK[n] = load(p) if _os.path.exists(p) else None
    return _BANK
def typing(char_times, text=None):
    """Typewriter for a typed card: ONE key hit per character at the exact times the letters appear
    (widgets.type_times), a softer thunk for spaces, and a carriage ding + return at the end."""
    if not char_times: return np.zeros(1)
    b = _bank(); end = max(char_times) + 1.6; out = np.zeros(int(end * SR) + 1)
    for i, t in enumerate(char_times):
        ch = text[i] if text and i < len(text) else 'a'
        if ch == ' ':
            add(out, b['space'] if b['space'] is not None else type_key(.5), t, .6)
        elif b['keys']:
            add(out, b['keys'][int(rng.integers(len(b['keys'])))], t + rng.uniform(-.004, .004), rng.uniform(.8, 1.0))
        else:
            add(out, type_key(rng.uniform(.8, 1.0)), t + rng.uniform(-.004, .004))
    tail = max(char_times) + .3
    if b['ding'] is not None: add(out, b['ding'], tail, .7)
    else: add(out, carriage_ding(), tail)
    if b['return'] is not None: add(out, b['return'], tail + .25, .6)
    return out
def stamp_thud():
    n = int(.4 * SR); t = np.arange(n) / SR; f = 50 + 70 * np.exp(-t * 20)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, .001, .14) + bp(noise(n), 300, 3000) * env(n, .0005, .02) * .6
def tick(): n = int(.012 * SR); return hp(noise(n), 3500) * env(n, .0003, .003)
def counter_ticks(dur, n_ticks=None):
    """Ticks that speed up while a number climbs."""
    out = np.zeros(int(dur * SR) + SR); n_ticks = n_ticks or int(dur * 14)
    for i in range(n_ticks): add(out, tick(), dur * (1 - (1 - i / n_ticks) ** 0.6) * 0.98, .5)
    return out[:int(dur * SR)]
def ding():   # gold: money landed
    t = secs(1.0); return (np.sin(2 * np.pi * 1760 * t) + .5 * np.sin(2 * np.pi * 2637 * t) + .2 * np.sin(2 * np.pi * 3520 * t)) * env(len(t), .001, .35) * .5
def low_tone():   # orange: a loss landed
    t = secs(1.0); f = 110 - 25 * t; return lp(2 * ((np.cumsum(f) / SR) % 1) - 1, 500) * env(len(t), .01, .45) * .7
def falling_tone():
    t = secs(.7); f = 880 * (220 / 880) ** (t / .7); return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(len(t), .01, .35) * .4
def whoosh(dur=0.45):
    n = int(dur * SR); x = noise(n); y = np.zeros(n); seg = n // 6
    for k in range(6): f = 300 * 2 ** (k * .6); y[k * seg:(k + 1) * seg] = bp(x, f, f * 3)[k * seg:(k + 1) * seg]
    t = np.arange(n) / n; return y * np.sin(np.pi * t) ** 2 * .7
def paper_slide(dur=0.35):
    n = int(dur * SR); t = np.arange(n) / n; return bp(noise(n), 1200, 6000) * np.sin(np.pi * t) * (0.6 + 0.4 * np.abs(np.sin(t * 60))) * .35
def coin():
    t = secs(.9); parts = [(2093, 1), (3322, .6), (5120, .4), (6902, .25)]
    return sum(a * np.sin(2 * np.pi * f * t) * np.exp(-t * (5 + f / 1500)) for f, a in parts) * (1 + .3 * np.sin(2 * np.pi * 7 * t)) * env(len(t), .001, .9) * .35
def cash():
    out = np.zeros(int(1.2 * SR)); add(out, stamp_thud() * .3, 0); add(out, coin(), .05); add(out, coin(), .12, .7); add(out, ding() * .6, .1); return out
def pop():
    t = secs(.06); f = 900 * np.exp(-t * 40) + 250; return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(len(t), .001, .02) * .5
def shutter():
    out = np.zeros(int(.2 * SR)); add(out, tick() * 3, 0); add(out, tick() * 3, .09); return out
def boom():
    t = secs(2.2); f = 36 + 40 * np.exp(-t * 6); return (np.sin(2 * np.pi * np.cumsum(f) / SR) * env(len(t), .004, .9) + lp(noise(len(t)), 200) * env(len(t), .002, .12) * .5) * .9
def sound_logo():
    """2-second sound logo for every title card: typewriter clacks + coin ring."""
    out = np.zeros(int(2.0 * SR)); [add(out, type_key() * 1.3, .05 + i * .11) for i in range(3)]; add(out, stamp_thud() * .25, .38); add(out, coin() * 1.4, .42); add(out, ding() * .5, .45)
    return out
SFX = dict(type_key=type_key, ding_carriage=carriage_ding, stamp=stamp_thud, tick=tick, ding=ding, low_tone=low_tone, falling=falling_tone, whoosh=whoosh,
           paper=paper_slide, coin=coin, cash=cash, pop=pop, shutter=shutter, boom=boom, logo=sound_logo)

# ======================= voices
def load(path):
    y, sr = sf.read(path); y = y.mean(1) if y.ndim > 1 else y
    return resample_poly(y, SR, sr) if sr != SR else y
def compress(x, thr_db=-22, ratio=3.2, makeup_db=4, win=0.01):
    n = max(1, int(win * SR)); e = np.sqrt(np.convolve(x ** 2, np.ones(n) / n, mode='same') + 1e-12); db = 20 * np.log10(e)
    gr = np.where(db > thr_db, (db - thr_db) * (1 - 1 / ratio), 0.0); a = np.exp(-1 / (0.12 * SR))
    gr = lfilter([1 - a], [1, -a], gr); return x * 10 ** ((makeup_db - gr) / 20)
def room(x, wet=0.05):
    n = int(.35 * SR); ir = noise(n) * np.exp(-np.arange(n) / SR / .07); ir = lp(ir, 5000); ir /= np.abs(ir).sum() / 4
    return x * (1 - wet) + fftconvolve(x, ir)[:len(x)] * wet
def voice_chain(x, kind='narrator', ref_rms=None):
    """Clean-up: high-pass, presence, compression, light room. Characters get a touch more room and are level-matched
    to the narrator (ref_rms) so the switch between ElevenLabs and Kokoro sounds smooth."""
    y = hp(x, 72); y = y + .25 * bp(y, 2800, 4200); y = compress(y)
    if ref_rms:
        r = np.sqrt(np.mean(y[np.abs(y) > 1e-3] ** 2) + 1e-12); y = y * (ref_rms / r)
    return room(y, .05 if kind == 'narrator' else .12)
def rms(x): v = x[np.abs(x) > 1e-3]; return float(np.sqrt(np.mean(v ** 2))) if len(v) else 0.0

# ======================= final mix
def mix(voice, music_track, sfx, out_wav, music_gain=0.32, sfx_gain=0.30, duck=0.6, loudnorm=True):   # music level approved; SFX lowered (owner)
    """voice / music / sfx: mono float arrays at 48 kHz (same length or shorter). Music ducks under speech."""
    n = max(len(voice), len(music_track), len(sfx)); V, Mu, S = (np.pad(a, (0, n - len(a))) for a in (voice, music_track, sfx))
    w = int(.15 * SR); ve = np.sqrt(np.convolve(V ** 2, np.ones(w) / w, mode='same')); ve = ve / (ve.max() + 1e-9)
    g = 1 - duck * np.clip(ve / 0.08, 0, 1); a = np.exp(-1 / (0.25 * SR)); g = lfilter([1 - a], [1, -a], g)
    y = V + Mu * music_gain * g + S * sfx_gain; y = np.tanh(y * 0.9) / 0.9
    st = np.stack([y, y], 1).astype(np.float32); raw = out_wav.replace('.wav', '_raw.wav'); sf.write(raw, st, SR)
    if loudnorm:   # two-pass loudnorm to -14 LUFS (YouTube standard), true peak -1.5 dB
        import json
        r = subprocess.run(['ffmpeg', '-hide_banner', '-i', raw, '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json', '-f', 'null', '-'], capture_output=True, text=True)
        m = json.loads(r.stderr[r.stderr.rindex('{'):r.stderr.rindex('}') + 1])
        af = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}"
              f":measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', raw, '-af', af, '-ar', str(SR), out_wav], check=True)
    else: sf.write(out_wav, st, SR)
    return out_wav
