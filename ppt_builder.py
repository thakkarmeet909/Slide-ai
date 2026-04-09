from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

# Themes
THEMES = {
    'navy':   (RGBColor(0x1A,0x1A,0x2E), RGBColor(0x16,0x21,0x3E), RGBColor(0x0F,0x3A,0x60)),
    'dark':   (RGBColor(0x1C,0x1C,0x1C), RGBColor(0x2C,0x2C,0x2C), RGBColor(0x44,0x44,0x44)),
    'green':  (RGBColor(0x1A,0x2E,0x1A), RGBColor(0x16,0x3E,0x21), RGBColor(0x0F,0x60,0x3A)),
    'purple': (RGBColor(0x1A,0x0A,0x2E), RGBColor(0x2A,0x10,0x4E), RGBColor(0x3A,0x15,0x6E)),
}

WHITE = RGBColor(255,255,255)

def build_ppt(data, filename="output.pptx", theme="navy"):
    DARK_BG, BLUE_BG, ACCENT = THEMES.get(theme, THEMES['navy'])

    prs = Presentation()
    prs.slide_width = Inches(13.33)
    prs.slide_height = Inches(7.5)

    # Title Slide
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = DARK_BG

    title_box = slide.shapes.add_textbox(Inches(1), Inches(2), Inches(10), Inches(2))
    title_box.text_frame.text = data["title"]

    # Slides
    for s in data["slides"]:
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        slide.background.fill.solid()
        slide.background.fill.fore_color.rgb = BLUE_BG

        heading = slide.shapes.add_textbox(Inches(1), Inches(1), Inches(10), Inches(1))
        heading.text_frame.text = s["heading"]

        content = slide.shapes.add_textbox(Inches(1), Inches(2), Inches(10), Inches(4))
        tf = content.text_frame

        for b in s["bullets"]:
            p = tf.add_paragraph()
            p.text = b
            p.level = 0

    prs.save(filename)
