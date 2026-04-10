from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
import requests
import tempfile
import os

# 🎨 THEMES
THEMES = {
    "elegant": {
        "bg1": RGBColor(0x1A, 0x1A, 0x2E),
        "bg2": RGBColor(0x16, 0x21, 0x3E),
        "accent": RGBColor(0xE2, 0xC2, 0x7D),
        "text": RGBColor(0xFF, 0xFF, 0xFF),
        "sub": RGBColor(0xCC, 0xAA, 0x66),
        "bullet_bg": RGBColor(0x0D, 0x11, 0x22),
        "bullet_border": RGBColor(0x2A, 0x35, 0x5A),
        "arrow": RGBColor(0xE2, 0xC2, 0x7D),
    }
}

# 🖼️ FETCH IMAGE
def fetch_image(image_prompt):
    try:
        safe = image_prompt.replace(" ", "%20")
        url = f"https://image.pollinations.ai/prompt/{safe}?width=800&height=450"
        res = requests.get(url)

        if res.status_code == 200:
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
            tmp.write(res.content)
            tmp.close()
            return tmp.name
        return None
    except:
        return None

# ✏️ TEXTBOX
def add_textbox(slide, text, l, t, w, h, size=18, bold=False, color=None):
    box = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    tf = box.text_frame
    p = tf.paragraphs[0]
    run = p.add_run()
    run.text = text
    run.font.size = Pt(size)
    run.font.bold = bold
    if color:
        run.font.color.rgb = color

# 🎨 BACKGROUND
def set_bg(slide, color):
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = color

# 🏆 TITLE SLIDE (WITH IMAGE)
def make_title_slide(prs, title, subtitle, t, image_path=None):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(slide, t["bg1"])

    if image_path:
        slide.shapes.add_picture(image_path, Inches(7), Inches(0), Inches(6), Inches(7.5))

    add_textbox(slide, title, 0.5, 2, 6, 2, 40, True, t["text"])
    add_textbox(slide, subtitle, 0.5, 4.2, 6, 1, 18, False, t["sub"])

# 📄 CONTENT SLIDE
def make_content_slide(prs, heading, bullets, note, t):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(slide, t["bg2"])

    add_textbox(slide, heading, 0.5, 0.3, 12, 1, 28, True, t["accent"])

    for i, b in enumerate(bullets):
        add_textbox(slide, f"• {b}", 0.7, 1.5 + i, 10, 1, 18, False, t["text"])

    if note:
        slide.notes_slide.notes_text_frame.text = note

# 🚀 MAIN BUILDER
def build_ppt(data, filename="output.pptx", theme="elegant"):
    t = THEMES.get(theme, THEMES["elegant"])

    prs = Presentation()
    prs.slide_width = Inches(13.33)
    prs.slide_height = Inches(7.5)

    # 🎨 IMAGE PROMPT SUPPORT
    image_prompt = data.get("image_prompt", data["title"])
    img = fetch_image(image_prompt)

    make_title_slide(prs, data["title"], data["subtitle"], t, img)

    for s in data["slides"]:
        make_content_slide(
            prs,
            s["heading"],
            s["bullets"],
            s.get("speaker_note", ""),
            t
        )

    prs.save(filename)
    print("✅ PPT Created:", filename)
