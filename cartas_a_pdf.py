from PIL import Image
import os
import math

# Configuración de la impresora
dpi = 300

# Tamaño de papel a imprimir: A3
a3_width_in, a3_height_in = 11.69,16.54
a3_width_px = int(a3_width_in * dpi)
a3_height_px = int(a3_height_in * dpi)

# Tamaño de las cartas
card_width_in, card_height_in = 2.75, 3.75
card_width_px = int(card_width_in * dpi)
card_height_px = int(card_height_in * dpi)

# Tamaño de cartas con margen
margin_px = 20
effective_card_width = card_width_px + margin_px
effective_card_height = card_height_px + margin_px

# Carpetas de input/output
front_folder = "./cards_front"
back_folder = "./cards_back"
output_folder = "./output_pages"
os.makedirs(output_folder, exist_ok=True)

# Cargar cartas con nombre "dq"
front_files = sorted(
    f for f in os.listdir(front_folder) if f.lower().startswith("dq") and f.lower().endswith(".png")
)
total_cards = len(front_files)
print(f"Se han encontrado {total_cards} cartas.")

# Calcular cantidad de cartas por papel
cols = a3_width_px // effective_card_width
rows = a3_height_px // effective_card_height
cards_per_page = cols * rows
print(f"{cols} columnas × {rows} filas -> {cards_per_page} cartas/página.")

# Crear paginas
def make_page(image_paths, reverse_order=False):
    sheet = Image.new("RGB", (a3_width_px, a3_height_px), "white")
    for i, img_path in enumerate(image_paths):
        card_img = Image.open(img_path).convert("RGB")
        card_img.thumbnail((card_width_px, card_height_px), Image.LANCZOS)
        card_canvas = Image.new("RGB", (card_width_px, card_height_px), "white")
        paste_x = (card_width_px - card_img.width) // 2
        paste_y = (card_height_px - card_img.height) // 2
        card_canvas.paste(card_img, (paste_x, paste_y))

        # Determinar filas/columnas
        row = i // cols
        col = i % cols
        if reverse_order:
            # Invertir orden de cartas (para cartas del reverso)
            col = cols - 1 - col

        x = col * effective_card_width + (a3_width_px - cols * effective_card_width) // 2
        y = row * effective_card_height + (a3_height_px - rows * effective_card_height) // 2
        sheet.paste(card_canvas, (x, y))
    return sheet

# Generar cartas frontales (izquierda -> derecha)
front_pages = []
for page_num in range(math.ceil(total_cards / cards_per_page)):
    start_idx = page_num * cards_per_page
    end_idx = min(start_idx + cards_per_page, total_cards)
    front_paths = [os.path.join(front_folder, f) for f in front_files[start_idx:end_idx]]
    front_pages.append(make_page(front_paths))

# generar cartas del reverso (derecha -> izquierda)
back_pages = []
for page_num in range(math.ceil(total_cards / cards_per_page)):
    start_idx = page_num * cards_per_page
    end_idx = min(start_idx + cards_per_page, total_cards)
    back_paths = []
    for f in front_files[start_idx:end_idx]:
        type_part = f.split("_")[1]
        back_name = f"dq_{type_part}_back.png"
        back_path = os.path.join(back_folder, back_name)
        if not os.path.exists(back_path):
            raise FileNotFoundError(f"Back card not found: {back_path}")
        back_paths.append(back_path)
    back_pages.append(make_page(back_paths, reverse_order=True))

# Guardar como PNG y PDF
all_pages = []
for idx, (front, back) in enumerate(zip(front_pages, back_pages), start=1):
    front_png = os.path.join(output_folder, f"page_{idx:02d}_front.png")
    back_png = os.path.join(output_folder, f"page_{idx:02d}_back.png")
    front.save(front_png, dpi=(dpi, dpi))
    back.save(back_png, dpi=(dpi, dpi))
    all_pages.extend([front, back])
    print(f"Página guardada en formato PNG: Página {idx}")

pdf_path = os.path.join(output_folder, "cartas.pdf")
all_pages[0].save(pdf_path, save_all=True, append_images=all_pages[1:], dpi=(dpi, dpi))
print(f"PDF guardado: {pdf_path}")
