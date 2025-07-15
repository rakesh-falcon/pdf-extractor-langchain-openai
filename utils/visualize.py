from PIL import Image, ImageDraw
import uuid
import os

def draw_low_conf_boxes(image, boxes, output_dir="static/annotated"):
    os.makedirs(output_dir, exist_ok=True)

    # Work on a copy of the original image
    draw = ImageDraw.Draw(image)

    for box in boxes:
        x, y, w, h = box["bbox"]
        draw.rectangle([x, y, x + w, y + h], outline="red", width=3)

    file_name = f"{uuid.uuid4().hex}.png"
    save_path = os.path.join(output_dir, file_name)
    image.save(save_path)

    return f"/{save_path}"  # Relative URL to static folder
