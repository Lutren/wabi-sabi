from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter


ROOT = Path(__file__).resolve().parent
PNG_PATH = ROOT / "argus-icon.png"
ICO_PATH = ROOT / "argus-icon.ico"
SIZE = 512


def hex_points(center_x: int, center_y: int, radius: int) -> list[tuple[int, int]]:
    return [
        (center_x, center_y - radius),
        (center_x + int(radius * 0.86), center_y - radius // 2),
        (center_x + int(radius * 0.86), center_y + radius // 2),
        (center_x, center_y + radius),
        (center_x - int(radius * 0.86), center_y + radius // 2),
        (center_x - int(radius * 0.86), center_y - radius // 2),
    ]


def main() -> None:
    image = Image.new("RGBA", (SIZE, SIZE), "#07090f")
    draw = ImageDraw.Draw(image)

    for index in range(SIZE):
        glow = int(12 + (index / SIZE) * 36)
        draw.line((0, index, SIZE, index), fill=(7 + glow // 5, 10 + glow // 7, 18 + glow // 6, 255))

    cyan = (0, 229, 255, 255)
    cyan_soft = (142, 245, 255, 255)
    amber = (255, 179, 0, 255)
    amber_soft = (255, 211, 104, 255)

    center = SIZE // 2
    outer = hex_points(center, center, 170)
    inner = hex_points(center, center, 128)
    core = hex_points(center, center, 86)

    draw.rounded_rectangle((74, 74, SIZE - 74, SIZE - 74), radius=96, outline=(255, 255, 255, 18), width=2)
    draw.polygon(outer, outline=(0, 229, 255, 150), width=10)
    draw.polygon(inner, outline=(255, 179, 0, 170), width=7)
    draw.polygon(core, outline=cyan_soft, width=6)

    draw.ellipse((146, 186, 366, 326), outline=cyan_soft, width=12)
    draw.ellipse((216, 212, 296, 300), fill=amber)
    draw.ellipse((236, 230, 276, 272), fill=(7, 9, 15, 255))
    draw.arc((150, 170, 362, 342), start=25, end=155, fill=(255, 179, 0, 150), width=7)
    draw.arc((150, 170, 362, 342), start=205, end=335, fill=(0, 229, 255, 120), width=7)

    draw.line((194, 368, 318, 368), fill=amber_soft, width=10)
    draw.line((216, 398, 298, 398), fill=cyan_soft, width=8)
    draw.line((240, 430, 280, 430), fill=amber_soft, width=7)

    glow_layer = image.filter(ImageFilter.GaussianBlur(radius=10))
    image = Image.blend(glow_layer, image, 0.78)

    image.save(PNG_PATH, format="PNG")
    image.save(ICO_PATH, format="ICO", sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)])


if __name__ == "__main__":
    main()
