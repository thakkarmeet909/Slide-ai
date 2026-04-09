from agent import generate_slide_content
from ppt_builder import build_ppt

topic = input("Enter presentation topic: ")

# Step 1: AI generates slide content
data = generate_slide_content(topic)

# Step 2: Build the .pptx
filename = topic.replace(" ", "_")[:30] + ".pptx"
build_ppt(data, filename)

print(f"\nDone! Open the file: {filename}")