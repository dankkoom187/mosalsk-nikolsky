"""Сборка изображений для прототипа сайта Свято-Никольского собора.

Источники — в ../_materials/mosalsk-nikolsky. Результат — assets/img.
Запуск: python tools/images.py
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT.parent / "_materials" / "mosalsk-nikolsky"
OUT = ROOT / "assets" / "img"
OUT.mkdir(parents=True, exist_ok=True)

QUALITY = {"jpg": 84, "webp": 80, "avif": 55}


def open_image(path: Path) -> Image.Image:
    im = Image.open(path)
    im = ImageOps.exif_transpose(im)
    return im.convert("RGB")


def save_variants(im: Image.Image, name: str, widths: list[int], ratio: float | None = None) -> None:
    for width in widths:
        if ratio:
            height = round(width / ratio)
            variant = ImageOps.fit(im, (width, height), method=Image.Resampling.LANCZOS)
        else:
            height = round(im.height * width / im.width)
            variant = im.resize((width, height), Image.Resampling.LANCZOS)
        base = OUT / f"{name}-{width}"
        variant.save(base.with_suffix(".jpg"), "JPEG", quality=QUALITY["jpg"], optimize=True, progressive=True)
        variant.save(base.with_suffix(".webp"), "WEBP", quality=QUALITY["webp"], method=6)
        variant.save(base.with_suffix(".avif"), "AVIF", quality=QUALITY["avif"], speed=5)


def main() -> None:
    hero = open_image(SRC / "photos-commons" / "commons-original.jpg")
    save_variants(hero, "hero", [800, 1200, 1600, 1920], ratio=3 / 2)

    og = ImageOps.fit(hero, (1200, 630), method=Image.Resampling.LANCZOS)
    og.save(OUT / "og.jpg", "JPEG", quality=86, optimize=True, progressive=True)

    about = ImageOps.fit(hero, (720, 900), method=Image.Resampling.LANCZOS)
    save_variants(about, "about", [400, 720], ratio=4 / 5)

    history_specs = [
        ("history-1878", "sobory-1878-postcard.jpg", 4 / 3, [400, 800]),
        ("history-1900", "sobory-1900-view.jpg", 4 / 3, [400, 800]),
        ("history-1942", "sobory-1942.jpg", 4 / 3, [400, 800]),
        ("history-1990", "sobory-1990-belltower.jpg", 3 / 4, [400, 600]),
    ]
    for name, filename, ratio, widths in history_specs:
        im = open_image(SRC / "photos-gazeta" / filename)
        save_variants(im, name, widths, ratio=ratio)

    vk_specs = [
        ("shrine-analoy", "vk-4195-pokrov-2.jpg"),
        ("shrine-reliquary", "vk-4198-moleben-2.jpg"),
        ("community-social", "vk-4193-social-1.jpg"),
        ("community-liturgy", "vk-4203-liturgy-3.jpg"),
        ("interior", "vk-4208-akathist-2.jpg"),
    ]
    for name, filename in vk_specs:
        im = open_image(SRC / "photos-vk" / filename)
        if name in {"shrine-analoy", "interior"}:
            im = im.crop((0, 0, im.width, round(im.height * 0.92)))
        save_variants(im, name, [400, 800], ratio=4 / 5)

    print("Готово:", OUT)


if __name__ == "__main__":
    main()
