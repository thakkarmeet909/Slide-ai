from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import tempfile, os
from agent import generate_slide_content
from ppt_builder import build_ppt

app = Flask(__name__)
CORS(app)  # allows your HTML page to talk to Flask

last_preview = {}  # stores slide data for preview

@app.route('/generate', methods=['POST'])
def generate():
    global last_preview
    data = request.json
    topic = data.get('topic', '')
    extra = data.get('extra', '')
    num_slides = data.get('num_slides', 6)
    theme = data.get('theme', 'navy')

    if not topic:
        return jsonify({'error': 'No topic provided'}), 400

    try:
        slide_data = generate_slide_content(topic, extra, num_slides)
        last_preview = slide_data

        tmp = tempfile.NamedTemporaryFile(suffix='.pptx', delete=False)
        tmp.close()
        build_ppt(slide_data, tmp.name, theme=theme)

        return send_file(
            tmp.name,
            as_attachment=True,
            download_name=topic[:30].replace(' ', '_') + '.pptx',
            mimetype='application/vnd.openxmlformats-officedocument.presentationml.presentation'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/last_preview')
def preview():
    return jsonify(last_preview)

if __name__ == '__main__':
    app.run(debug=True, port=5000)