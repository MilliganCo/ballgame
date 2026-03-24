from PIL import Image, ImageDraw, ImageFont, ImageCms
import numpy as np
import os

# === ПАРАМЕТРЫ ИЗОБРАЖЕНИЯ ===
DPI = 300
WIDTH_CM, HEIGHT_CM = 56, 56  # Холст 56x56 см
WIDTH_PX, HEIGHT_PX = int(WIDTH_CM * DPI / 2.54), int(HEIGHT_CM * DPI / 2.54)

# === ПАРАМЕТРЫ КВАДРАТОВ ===
SQUARE_SIZE_CM = 2
SQUARE_SIZE_PX = int(SQUARE_SIZE_CM * DPI / 2.54)
GAP_SIZE_CM = 1
GAP_SIZE_PX = int(GAP_SIZE_CM * DPI / 2.54)
TEXT_HEIGHT_PX = int(0.25 * DPI / 2.54)

# === СОЗДАЁМ ИЗОБРАЖЕНИЕ В RGB === (конвертируем в CMYK потом!)
image = Image.new("RGB", (WIDTH_PX, HEIGHT_PX), (255, 255, 255))  # Белый фон
draw = ImageDraw.Draw(image)


# === СОЗДАЁМ ГРАДИЕНТ CMYK ===
def generate_gradient_cmyk(rows, cols):
    shades = np.zeros((rows, cols, 4), dtype=int)
    for row in range(rows):
        for col in range(cols):
            c = 0
            m = np.interp(col, [0, cols - 1], [5, 20])
            y = np.interp(row, [0, rows - 1], [100, 80])
            k = np.interp(row, [0, rows - 1], [0, 20])
            shades[row, col] = (int(c), int(m), int(y), int(k))
    return shades


# === ГЕНЕРАЦИЯ ГРАДИЕНТА ===
cols = (WIDTH_PX - GAP_SIZE_PX) // (SQUARE_SIZE_PX + GAP_SIZE_PX)
rows = (HEIGHT_PX - GAP_SIZE_PX) // (SQUARE_SIZE_PX + GAP_SIZE_PX)
gold_shades = generate_gradient_cmyk(rows, cols)

# === ЗАГРУЗКА ШРИФТА ===
try:
    font = ImageFont.truetype("D:/Рабочий стол [2]/DejaVu_Sans.ttf", TEXT_HEIGHT_PX)
except IOError:
    font = ImageFont.load_default()

# === РИСОВАНИЕ КВАДРАТОВ И ТЕКСТА ===
for row in range(rows):
    for col in range(cols):
        x0 = GAP_SIZE_PX + col * (SQUARE_SIZE_PX + GAP_SIZE_PX)
        y0 = GAP_SIZE_PX + row * (SQUARE_SIZE_PX + GAP_SIZE_PX)
        x1 = x0 + SQUARE_SIZE_PX
        y1 = y0 + SQUARE_SIZE_PX
        color = tuple(gold_shades[row, col])

        # Конвертация CMYK в RGB для рисования
        r = 255 * (1 - color[0] / 100) * (1 - color[3] / 100)
        g = 255 * (1 - color[1] / 100) * (1 - color[3] / 100)
        b = 255 * (1 - color[2] / 100) * (1 - color[3] / 100)
        rgb_color = (int(r), int(g), int(b))

        draw.rectangle([x0, y0, x1, y1], fill=rgb_color)

        # Подпись CMYK
        text_x = x0 + 2
        text_y = y1 + 1
        text = f"{color[0]},{color[1]},{color[2]},{color[3]}"
        draw.text((text_x, text_y), text, fill=(0, 0, 0), font=font)

# === КОНВЕРТАЦИЯ В CMYK С ICC-ПРОФИЛЕМ ===
icc_profile_path = "D:/BackUp_AcronisTI/1/SAi Production Suite Cloud/ICCProfile/CMYK/CoatedFOGRA39.icc"
if os.path.exists(icc_profile_path):
    cmyk_profile = ImageCms.getOpenProfile(icc_profile_path)
    srgb_profile = ImageCms.createProfile("sRGB")

    # Конвертация изображения в CMYK с ICC-профилем
    image = ImageCms.profileToProfile(image, srgb_profile, cmyk_profile, outputMode="CMYK")

# === СОХРАНЕНИЕ TIFF В CMYK С ICC ===
image_path = "D:/Рабочий стол [2]/gold_shades_cmyk_icc_fixed.tiff"
image.save(image_path, "TIFF", dpi=(DPI, DPI), icc_profile=cmyk_profile.tobytes() if icc_profile_path else None)

print(f"Файл сохранён: {image_path}")
