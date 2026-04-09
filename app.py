from flask import Flask, request, send_file
from agent import generate_slide_content
from ppt_builder import build_ppt

app = Flask(__name__)

@app.route("/")
def home():
    return '''
    <h1>AI PPT Generator 🚀</h1>
    <p>Click below to generate:</p>
    <a href="/generate?topic=Artificial Intelligence">
        Generate AI PPT
    </a>
    '''

@app.route("/generate")
def generate():
    topic = request.args.get("topic")

    if not topic:
        return "Please provide a topic like /generate?topic=AI"

    data = generate_slide_content(topic)

    if not data:
        return "Error generating PPT"

    filename = topic.replace(" ", "_") + ".pptx"

    build_ppt(data, filename)

    return send_file(filename, as_attachment=True)

if __name__ == "__main__":
    app.run()
