"""Rendering: one MP4 per shot (frames drawn in skia, piped into ffmpeg), joined without re-encoding, then the
audio mix is muxed on. LOCKED output: 1920x1080, 30 fps, H.264 at 24 Mbps.
Before ANY render of a new video, ask the owner: render on their Windows PC or in the cloud? Never assume.
On the PC with an NVIDIA card, set DOCANIM_ENCODER=h264_nvenc for faster encoding (same 24 Mbps)."""
import os, subprocess, math, shutil, pathlib
import skia
from engine.core import W, H, FPS, VIDEO_BITRATE
from engine.kit import ease, lerp, C, vignette as _vignette

def _enc_args():
    enc = os.environ.get('DOCANIM_ENCODER', 'libx264')
    rate = ['-b:v', VIDEO_BITRATE, '-maxrate', VIDEO_BITRATE, '-bufsize', '48M']
    if enc == 'libx264': return ['-c:v', 'libx264', '-preset', 'medium', *rate, '-pix_fmt', 'yuv420p']
    return ['-c:v', enc, *rate, '-pix_fmt', 'yuv420p']

def _focus(focus, e):
    """focus = (x, y) or a pan ((x0, y0), (x1, y1)) eased over the shot."""
    if isinstance(focus[0], (tuple, list)): (a, b), (c_, d) = focus; return (lerp(a, c_, e), lerp(b, d, e))
    return focus

def _clamp(focus, z):
    """Keep the camera inside the 1920x1080 world so no black edges show."""
    hx, hy = W / (2 * z), H / (2 * z)
    return (min(max(focus[0], hx), W - hx), min(max(focus[1], hy), H - hy))

def render_shot(out, dur, draw, zoom=(1.0, 1.07), focus=(960, 540), rot=(0.0, 0.0), whip_in=False, whip_out=False, shake=None, hud=None):
    """Render one shot to `out` (mp4).
    draw(c, t): draws the frame at local time t (seconds) in 1920x1080 world space.
    zoom: camera push-in from zoom[0] to zoom[1] with ease-in-out (every shot moves 5-10%). focus: world point kept centred.
    rot: small camera rotation in degrees (top-down desk shots). whip_in/out: horizontal whip-blur transition.
    shake(t) -> (dx, dy) optional camera shake (e.g. from widgets.stamp).
    hud(c, t): drawn on top in SCREEN space (name tags, place tags, labels) so the camera never crops them."""
    n = max(1, round(dur * FPS)); surf = skia.Surface(W, H); c = surf.getCanvas(); tmp = out + '.tmp.mp4'
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgra', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          *_enc_args(), '-r', str(FPS), tmp], stdin=subprocess.PIPE)
    for f in range(n):
        t = f / FPS; e = ease(f / max(n - 1, 1)); wx = sig = 0
        if whip_out and n - f <= 5: wx = -((6 - (n - f)) ** 2) * 34; sig = (6 - (n - f)) * 16
        if whip_in and f < 4: wx = (4 - f) ** 2 * 52; sig = (4 - f) * 18
        dx, dy = shake(t) if shake else (0, 0)
        c.clear(C((0, 0, 0))); c.save(); c.translate(W / 2 + wx + dx, H / 2 + dy); z = lerp(zoom[0], zoom[1], e); c.scale(z, z)
        fx, fy = _clamp(_focus(focus, e), z); c.rotate(lerp(rot[0], rot[1], e)); c.translate(-fx, -fy); draw(c, t); c.restore()
        if getattr(draw, 'vignette', 0):
            _vignette(c, draw.vignette, getattr(draw, 'vignette_inner', .42))
        if hud: hud(c, t)
        if sig:
            img = surf.makeImageSnapshot(); c.clear(C((0, 0, 0))); bp = skia.Paint(); bp.setImageFilter(skia.ImageFilters.Blur(sig, 0.01, skia.TileMode.kClamp))
            c.drawImage(img, 0, 0, skia.SamplingOptions(), bp)
        p.stdin.write(surf.makeImageSnapshot().toarray(colorType=skia.kBGRA_8888_ColorType).tobytes())
    p.stdin.close()
    if p.wait() != 0: raise RuntimeError(f'ffmpeg failed for {out}')
    os.replace(tmp, out); return out

def still(draw, t, path, zoom=1.0, focus=(960, 540), hud=None):
    """One test frame (for contact sheets before the long render)."""
    surf = skia.Surface(W, H); c = surf.getCanvas(); c.clear(C((0, 0, 0))); c.save(); c.translate(W / 2, H / 2); c.scale(zoom, zoom); fx, fy = _clamp(_focus(focus, .6), zoom); c.translate(-fx, -fy)
    draw(c, t); c.restore()
    if getattr(draw, 'vignette', 0):
        _vignette(c, draw.vignette, getattr(draw, 'vignette_inner', .42))
    if hud: hud(c, t)
    surf.makeImageSnapshot().save(path, skia.kPNG); return path

def contact_sheet(paths, out, cols=3):
    from PIL import Image
    ims = [Image.open(p).convert('RGB').resize((640, 360)) for p in paths]; rows = math.ceil(len(ims) / cols)
    S = Image.new('RGB', (640 * cols, 360 * rows), (20, 33, 61))
    for i, im in enumerate(ims): S.paste(im, ((i % cols) * 640, (i // cols) * 360))
    S.save(out, quality=88); return out

def join(shot_files, out):
    """Concatenate shot MP4s without re-encoding (all shots share size, fps, encoder)."""
    lst = pathlib.Path(out).with_suffix('.txt'); lst.write_text(''.join(f"file '{pathlib.Path(s).resolve()}'\n" for s in shot_files))
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', str(lst), '-c', 'copy', out], check=True); return out

def mux(video, wav, out):
    """Put the final audio mix on the video (video stream copied, AAC 256 kbps)."""
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', video, '-i', wav, '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '256k',
                    '-shortest', '-movflags', '+faststart', out], check=True); return out

def frame_sheet(video, out, every=7):
    """One frame every N seconds tiled into a sheet (check for cut-off labels, overlaps, framing)."""
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', video, '-vf', f'fps=1/{every},scale=384:216,tile=5x4', '-frames:v', '1', out], check=True); return out

def render_parallel(jobs, workers=None):
    """jobs: list of (fn, args) - each fn renders one shot. Runs in separate processes (default: CPU count - 1)."""
    from concurrent.futures import ProcessPoolExecutor
    workers = workers or max(1, (os.cpu_count() or 2) - 1)
    with ProcessPoolExecutor(workers) as ex: return list(ex.map(_call, jobs))
def _call(job): fn, args = job; return fn(*args)
