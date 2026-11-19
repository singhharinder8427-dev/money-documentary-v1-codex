"""Isolated furniture and dressing previews."""
from .furniture import bench,cabinet,chair,cubicle,desk,lamp,podium,queue_posts,rotary_phone,street_sign
from .prop_stage import render_props


def desk_preview(c):
    desk(c,-130,26,260,63)


def chair_preview(c):
    chair(c,0,25)


def cabinet_preview(c):
    cabinet(c,-57,-91)


def podium_preview(c):
    podium(c,-55,54)


def posts_preview(c):
    queue_posts(c,-81,34,162)


def sign_preview(c):
    street_sign(c,0,59)


def bench_preview(c):
    bench(c,-115,28,230)


def phone_preview(c):
    rotary_phone(c,0,28)


def lamp_preview(c):
    lamp(c,0,38)


def cubicle_preview(c):
    cubicle(c,-90,38)


def stage(draw,scale):
    def wrapped(canvas):
        canvas.save()
        canvas.translate(480,273)
        canvas.scale(scale,scale)
        draw(canvas)
        canvas.restore()
    return wrapped


def previews():
    items=[
        ('cubicle-walls','Cubicle walls',cubicle_preview,2.8),('desk','Desk',desk_preview,1.96),
        ('conference-chair','Conference chair',chair_preview,2.65),('filing-cabinet','Filing cabinet',cabinet_preview,1.94),
        ('podium','Podium',podium_preview,2.5),('queue-posts','Queue posts',posts_preview,2.55),
        ('street-sign','Street sign',sign_preview,2.75),('park-bench','Park bench',bench_preview,2.3),
        ('period-phone','Period phone',phone_preview,3.85),('period-lamp','Period lamp',lamp_preview,3.3),
    ]
    return [(slug, title, stage(draw, scale)) for slug, title, draw, scale in items]


def render(output):
    return render_props(output, previews())
