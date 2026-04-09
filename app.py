from flask import Flask, request, send_file, render_template
from agent import generate_slide_content
from ppt_builder import build_ppt
import os

app = Flask(__name__)

# Home page (UI)
@app.route("/")
def home():
    return render_template("index.html")


# Generate PPT route
@app.route("/generate")
def generate():
    topic = request.args.get("topic")

    # Safety check
    if not topic:
        return "❌ Please enter a topic!"

    print(f"Generating PPT for: {topic}")

    # Generate content using AI
    data = generate_slide_content(topic)

    if not data:
        return "❌ Error generating content. Try again."

    # Create filename
    filename = topic.replace(" ", "_") + ".pptx"

    # Build PPT
    build_ppt(data, filename)

    # Send file to user
    return send_file(filename, as_attachment=True)


# Run app (for local testing)
if __name__ == "__main__":
    app.run(debug=True)
