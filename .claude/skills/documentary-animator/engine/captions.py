"""Small burned-in captions (owner: "add small captions") + an .srt file for YouTube closed captions.
Bottom centre, Barlow SemiBold, white with a dark outline, the word being spoken in gold, <= 7 words per chunk.
Lines shown as typed text cards are skipped (the words are already on screen). Word timing is spread over each
voice clip by character count (no extra model needed); good enough for small captions."""
import re
from engine.core import W, H, GOLD, WHITE, F_LABEL2
from engine.kit import ink, fp
import skia

MAXW, SIZE, Y = 7, 50, 1045

def chunks(tl):
    out = []                                                # [(t0, t1, [(word, w0, w1), ...])]
    for l in tl.lines:
        if l.get('card') or l['id'] not in tl.clips: continue
        t0, d = tl.cues[l['id']]; words = l['text'].split()
        if not words: continue
        weights = [len(w) + 1 for w in words]; tot = sum(weights); acc = 0.0; timed = []
        for w, wt in zip(words, weights):
            a = t0 + d * acc / tot; acc += wt; timed.append((w, a, t0 + d * acc / tot))
        cur = []
        for i, item in enumerate(timed):
            cur.append(item)
            brk = len(cur) >= MAXW or re.search(r'[.!?;:]$', item[0]) or (re.search(r',$', item[0]) and len(cur) >= 4)
            if brk or i == len(timed) - 1: out.append((cur[0][1], cur[-1][2] + .15, cur)); cur = []
    return out

class Captions:
    def __init__(self, tl): self.ch = chunks(tl); self.font = skia.Font(F_LABEL2, SIZE)
    def draw(self, c, t):
        for t0, t1, words in self.ch:
            if t0 <= t < t1: break
        else: return
        f = self.font; sp = f.measureText(' '); ws = [f.measureText(w) for w, _, _ in words]; total = sum(ws) + sp * (len(ws) - 1)
        x = W / 2 - total / 2
        for (w, a, b), wd in zip(words, ws):
            col = GOLD if a <= t < b else WHITE
            c.drawString(w, x, Y, f, ink(9, (10, 17, 36))); c.drawString(w, x, Y, f, fp(col)); x += wd + sp

def srt(tl, path):
    def ts(s): h, s = divmod(s, 3600); m, s = divmod(s, 60); return f'{int(h):02d}:{int(m):02d}:{int(s):02d},{int(round((s % 1) * 1000)) % 1000:03d}'
    lines = []
    for i, (t0, t1, words) in enumerate(chunks(tl), 1): lines += [str(i), f'{ts(t0)} --> {ts(t1)}', ' '.join(w for w, _, _ in words), '']
    open(path, 'w', encoding='utf-8').write('\n'.join(lines)); return path
