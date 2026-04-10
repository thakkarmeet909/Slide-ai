from flask import Flask, request, jsonify, send_file, render_template
from flask_cors import CORS
import tempfile, os

from agent import generate_slide_content
from ppt_builder import build_ppt

app = Flask(__name__)
CORS(app)

last_preview = {}

# 🌐 HOME PAGE (UI)
@app.route("/")
def home():
    return render_template("index.html")


# 🚀 MAIN GENERATE (WORKS FOR BOTH API + UI)
@app.route("/generate", methods=["GET", "POST"])
def generate():
    global last_preview

    # 🔄 HANDLE BOTH JSON (POST) AND URL PARAMS (GET)
    if request.method == "POST":
        data = request.json or {}
        topic = data.get("topic", "")
        extra = data.get("extra", "")
        num_slides = data.get("num_slides", 6)
        theme = data.get("theme", "elegant")
    else:
        topic = request.args.get("topic", "")
        extra = request.args.get("extra", "")
        theme = request.args.get("theme", "elegant")

        try:
            num_slides = int(request.args.get("slides", 6))
        except:
            num_slides = 6

    if not topic:
        return jsonify({'error': 'No topic provided'}) if request.method == "POST" else "❌ Please enter a topic!"

    try:
        print(f"🔥 Topic: {topic} | Slides: {num_slides} | Theme: {theme}")

        # 🧠 GENERATE AI CONTENT
        slide_data = generate_slide_content(topic, extra, num_slides)

        if not slide_data:
            raise Exception("Slide generation failed")

        # 🖼️ IMAGE PREVIEW (FOR FRONTEND)
        image_prompt = slide_data.get("image_prompt", topic).replace(" ", "%20")
        slide_data["image_url"] = f"https://image.pollinations.ai/prompt/{image_prompt}?width=800&height=450&nologo=true"

        last_preview = slide_data

        # 📁 TEMP FILE FOR DOWNLOAD
        tmp = tempfile.NamedTemporaryFile(suffix=".pptx", delete=False)
        tmp.close()

        build_ppt(slide_data, tmp.name, theme=theme)

        return send_file(
            tmp.name,
            as_attachment=True,
            download_name=topic[:30].replace(" ", "_") + ".pptx",
            mimetype="application/vnd.openxmlformats-officedocument.presentationml.presentation"
        )

    except Exception as e:
        print("❌ ERROR:", e)
        return jsonify({'error': str(e)}), 500 if request.method == "POST" else f"❌ Error: {str(e)}"


# 👀 PREVIEW DATA (FOR FRONTEND UI)
@app.route("/last_preview")
def preview():
    return jsonify(last_preview)


# ▶️ RUN SERVER
if __name__ == "__main__":
    app.run(debug=True, port=5000)
