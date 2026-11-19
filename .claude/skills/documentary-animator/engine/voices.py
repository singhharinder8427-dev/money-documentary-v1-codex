"""Voices (LOCKED): narrator = the owner's ElevenLabs recording; characters = Kokoro (free, local), one fixed voice
per character. Speech-to-text (Parakeet) cuts the narration into one clip per script line and checks the final mix.
Setup once per machine (GitHub release URLs; Hugging Face is often blocked):
  pip install sherpa-onnx soundfile scipy numpy skia-python
  R=https://github.com/k2-fsa/sherpa-onnx/releases/download
  curl -L -O $R/tts-models/kokoro-multi-lang-v1_0.tar.bz2 && tar xjf kokoro-multi-lang-v1_0.tar.bz2
  curl -L -O $R/asr-models/sherpa-onnx-nemo-parakeet-tdt-0.6b-v2-int8.tar.bz2 && tar xjf sherpa-onnx-nemo-parakeet-tdt-0.6b-v2-int8.tar.bz2
Models folder: $DOCANIM_MODELS (default ~/models)."""
import os, re, difflib, numpy as np, soundfile as sf
MODELS = os.path.expanduser(os.environ.get('DOCANIM_MODELS', '~/models'))
KOKORO = os.path.join(MODELS, 'kokoro-multi-lang-v1_0')
PARAKEET = os.path.join(MODELS, 'sherpa-onnx-nemo-parakeet-tdt-0.6b-v2-int8')

# Kokoro v1.0 speaker ids (American voices first - US audience). The final pick per character is made in the first
# short test render, then written here and never changed, so each character sounds the same in every video.
KOKORO_IDS = {'af_heart': 3, 'af_bella': 2, 'af_nicole': 6, 'af_sarah': 9, 'af_sky': 10, 'am_adam': 11, 'am_echo': 12, 'am_eric': 13,
              'am_fenrir': 14, 'am_liam': 15, 'am_michael': 16, 'am_onyx': 17, 'am_puck': 18, 'bm_george': 26, 'bm_lewis': 27}
CHARACTER_VOICES = {   # candidates until the test render; then locked
    'ceo': ('am_onyx', 0.95), 'analyst': ('am_eric', 1.0), 'worker': ('am_adam', 1.0), 'banker': ('am_fenrir', 0.97),
    'investor': ('af_bella', 1.0), 'saver': ('af_sarah', 1.0), 'grad': ('am_liam', 1.05), 'scammer': ('am_puck', 1.0),
    'agent': ('am_echo', 0.97), 'reporter': ('af_nicole', 1.0), 'retiree': ('am_michael', 0.92)}
LEXICON_EXTRA = 'lex_extra.txt'   # per-video extra pronunciations (written automatically by prepare_text)
# Hand-checked pronunciations (Kokoro symbols, space-separated). Add names here when they come up.
MANUAL_LEX = {"sec's": 'ˌ ɛ s ˌ i s ˈ i z', 'sec': 'ˌ ɛ s ˌ i s ˈ i', 'ponzi': 'p ˈ ɑ n z i', 'pulitzer': 'p ˈ ʊ l ɪ t s ə ɹ', 'gov': 'ɡ ˈ ʌ v', 'madoff': 'm ˈ A d ɔ f', 'nvidia': 'ɛ n v ˈ ɪ d i ə'}
_ONES = 'zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen'.split()
_TENS = 'zero ten twenty thirty forty fifty sixty seventy eighty ninety'.split()
def _words(n):
    if n < 20: return _ONES[n]
    if n < 100: return _TENS[n // 10] + ('' if n % 10 == 0 else '-' + _ONES[n % 10])
    if n < 1000: return _ONES[n // 100] + ' hundred' + ('' if n % 100 == 0 else ' ' + _words(n % 100))
    for v, name in ((10**12, 'trillion'), (10**9, 'billion'), (10**6, 'million'), (1000, 'thousand')):
        if n >= v: return _words(n // v) + ' ' + name + ('' if n % v == 0 else ' ' + _words(n % v))
def speakable(text):
    """Numbers spelled out for the voice (the script keeps digits): years 1100-1999 / 2010-2099 read as pairs,
    $ amounts, percents, commas."""
    def num(m):
        raw = m.group(0); dollar = raw.startswith('$'); r = raw.lstrip('$'); pct = r.endswith('%'); r = r.rstrip('%')
        if '.' in r:
            a, b = r.replace(',', '').split('.'); w = _words(int(a)) + ' point ' + ' '.join(_ONES[int(d)] for d in b)
        else:
            n = int(r.replace(',', ''))
            if not dollar and ',' not in r and (1100 <= n <= 1999 or 2010 <= n <= 2099) and len(r) == 4: w = _words(n // 100) + ' ' + (_words(n % 100) if n % 100 >= 10 else ('hundred' if n % 100 == 0 else 'oh ' + _words(n % 100)))
            else: w = _words(n)
        return w + (' percent' if pct else '') + (' dollars' if dollar else '')
    ORD = {1: 'first', 2: 'second', 3: 'third', 4: 'fourth', 5: 'fifth', 6: 'sixth', 7: 'seventh', 8: 'eighth', 9: 'ninth', 10: 'tenth', 11: 'eleventh',
           12: 'twelfth', 13: 'thirteenth', 20: 'twentieth', 30: 'thirtieth'}
    def ordinal(m):
        n = int(m.group(1))
        if n in ORD: return ORD[n]
        if n < 100 and n % 10 in ORD: return _TENS[n // 10] + '-' + ORD[n % 10]
        return _words(n) + 'th'
    text = re.sub(r'\b(\d+)(?:st|nd|rd|th)\b', ordinal, text)                      # 2nd -> second
    t = re.sub(r'\$?\d+(?:,\d{3})*(?:\.\d+)?%?', num, text)
    t = re.sub(r'(\w)\s*dollars\s+(million|billion|trillion|thousand)', r'\1 \2 dollars', t)
    return t
_LEXSET = None
def _known():
    global _LEXSET
    if _LEXSET is None:
        _LEXSET = set()
        for f in ('lexicon-us-en.txt',):
            for line in open(os.path.join(KOKORO, f), encoding='utf-8'): _LEXSET.add(line.split(' ', 1)[0].lower())
    return _LEXSET
def _espeak_ipa(word):
    import subprocess, shutil
    if not shutil.which('espeak-ng'): return None
    ipa = subprocess.run(['espeak-ng', '-q', '--ipa=3', '-v', 'en-us', word], capture_output=True, text=True).stdout.strip()
    ipa = ipa.replace('\u200d', '').replace('ː', '').replace('ɚ', 'əɹ').replace('ᵻ', 'ɪ').replace('tʃ', 'ʧ').replace('dʒ', 'ʤ').replace('_', '')
    toks = set(l.split(' ')[0] for l in open(os.path.join(KOKORO, 'tokens.txt'), encoding='utf-8') if l.strip())
    return ' '.join(ch for ch in ipa if ch in toks and not ch.isspace()) or None
def prepare_text(text):
    """Make a line safe for Kokoro: spell numbers out, and add every word missing from its dictionary to
    lex_extra.txt (hand-checked MANUAL_LEX first, then espeak-ng). Without this Kokoro silently SKIPS unknown words."""
    t = speakable(text); known = _known(); have = {}
    if os.path.exists(LEXICON_EXTRA): have = {l.split(' ', 1)[0]: 1 for l in open(LEXICON_EXTRA, encoding='utf-8') if l.strip()}
    new = []
    for w in re.findall(r"[A-Za-z][A-Za-z'’-]*", t):
        for part in w.replace('’', "'").split('-'):
            k = part.lower()
            if not k or k in known or k in have: continue
            p = MANUAL_LEX.get(k) or _espeak_ipa(part)
            if p: new.append(f'{k} {p}'); have[k] = 1
            else: print('NO PRONUNCIATION for', part, '- add it to MANUAL_LEX')
    if new:
        with open(LEXICON_EXTRA, 'a', encoding='utf-8') as f: f.write('\n'.join(new) + '\n')
        global _TTS; _TTS = None   # reload so Kokoro sees the new words
    return t

_TTS = None
def kokoro():
    global _TTS
    if _TTS is None:
        import sherpa_onnx
        if not os.path.exists(LEXICON_EXTRA): open(LEXICON_EXTRA, 'w').write('')
        # US dictionary only: the GB file overrides US words (non-rhotic 'part' -> 'pot')
        M = KOKORO; cfg = sherpa_onnx.OfflineTtsConfig(model=sherpa_onnx.OfflineTtsModelConfig(kokoro=sherpa_onnx.OfflineTtsKokoroModelConfig(
            model=f'{M}/model.onnx', voices=f'{M}/voices.bin', tokens=f'{M}/tokens.txt', data_dir=f'{M}/espeak-ng-data', dict_dir=f'{M}/dict',
            lexicon=f'{LEXICON_EXTRA},{M}/lexicon-us-en.txt', lang='en-us'), num_threads=max(1, (os.cpu_count() or 2) - 1)))
        _TTS = sherpa_onnx.OfflineTts(cfg)
    return _TTS

def character_line(text, who, out):
    """Synthesize one character line with that character's fixed Kokoro voice; trimmed; returns (path, seconds)."""
    name, speed = CHARACTER_VOICES[who]; t = prepare_text(text); a = kokoro().generate(t, sid=KOKORO_IDS[name], speed=speed)
    s = np.array(a.samples, dtype=np.float32); idx = np.where(np.abs(s) > 0.012 * np.abs(s).max())[0]
    s = s[max(idx[0] - 300, 0): idx[-1] + 1500]; sf.write(out, s, a.sample_rate); return out, len(s) / a.sample_rate

_ASR = None
def asr():
    global _ASR
    if _ASR is None:
        import sherpa_onnx; M = PARAKEET
        _ASR = sherpa_onnx.OfflineRecognizer.from_transducer(encoder=f'{M}/encoder.int8.onnx', decoder=f'{M}/decoder.int8.onnx', joiner=f'{M}/joiner.int8.onnx',
                                                             tokens=f'{M}/tokens.txt', num_threads=max(1, (os.cpu_count() or 2) - 1), model_type='nemo_transducer')
    return _ASR
def _mono16k(path):
    from scipy.signal import resample_poly
    y, sr = sf.read(path); y = y.mean(1) if y.ndim > 1 else y; return resample_poly(y, 16000, sr).astype(np.float32) if sr != 16000 else y.astype(np.float32)
def words_with_times(path, chunk=24.0):
    """Speech-to-text with word timings: [(word, start, end)]. Decodes in 24 s chunks with 1 s overlap."""
    y = _mono16k(path); out = []; step = int((chunk - 1) * 16000); L = int(chunk * 16000); i = 0
    while i < len(y):
        seg = y[i:i + L]; st = asr().create_stream(); st.accept_waveform(16000, seg); asr().decode_stream(st); r = st.result
        toks, ts = list(r.tokens), list(r.timestamps); cur = None
        for tk, t in zip(toks, ts):
            t = t + i / 16000
            if tk.startswith('▁') or tk.startswith(' ') or cur is None:
                if cur: out.append(cur)
                cur = [tk.strip('▁ '), t, t + .2]
            else: cur[0] += tk; cur[2] = t + .2
        if cur: out.append(cur)
        i += step
    out.sort(key=lambda w: w[1]); ded = []
    for w in out:
        if not ded or w[1] > ded[-1][1] + .05: ded.append(w)
    return [(w, a, b) for w, a, b in ded if w]
def norm(s): return re.sub(r"[^a-z0-9$%']+", ' ', s.lower()).split()

def split_narration(narration_wav, lines, outdir):
    """Cut the owner's ElevenLabs narration (one file, narrator lines in script order) into one clip per line.
    lines: [(id, text)] narrator lines only. Returns {id: (clip_path, seconds)}. Aligns speech-to-text words to the
    script with difflib; lines that can't be matched are reported so the owner can check them."""
    os.makedirs(outdir, exist_ok=True); W_ = words_with_times(narration_wav); hyp = [norm(w)[0] if norm(w) else '' for w, _, _ in W_]
    ref, owner = [], []
    for k, (lid, txt) in enumerate(lines):
        for w in norm(txt): ref.append(w); owner.append(k)
    sm = difflib.SequenceMatcher(None, ref, hyp, autojunk=False); hit = {}
    for a, b, n in sm.get_matching_blocks():
        for j in range(n): hit.setdefault(owner[a + j], []).append(b + j)
    y, sr = sf.read(narration_wav); y = y.mean(1) if y.ndim > 1 else y; res, missing = {}, []
    bounds = []
    for k in range(len(lines)):
        if k in hit: bounds.append((W_[min(hit[k])][1], W_[max(hit[k])][2]))
        else: bounds.append(None); missing.append(lines[k][0])
    for k, (lid, _) in enumerate(lines):
        if bounds[k] is None: continue
        a, b = bounds[k]; nxt = next((bb[0] for bb in bounds[k + 1:] if bb), len(y) / sr)
        a = max(0, a - .12); b = min(nxt - .02, b + .35)
        clip = y[int(a * sr):int(b * sr)]; p = os.path.join(outdir, f'{lid}.wav'); sf.write(p, clip, sr); res[lid] = (p, len(clip) / sr)
    if missing: print('NOT MATCHED (check these lines in the narration):', missing)
    return res

def transcript_check(mix_wav, script_text):
    """Transcribe the final mix and compare with the script. Returns similarity 0..1 (aim > 0.9)."""
    hyp = ' '.join(norm(' '.join(w for w, _, _ in words_with_times(mix_wav)))); ref = ' '.join(norm(script_text))
    return difflib.SequenceMatcher(None, ref.split(), hyp.split(), autojunk=False).ratio()
