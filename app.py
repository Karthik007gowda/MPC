from flask import Flask, render_template, request, send_file, jsonify
import os
from werkzeug.utils import secure_filename
from mpc_to_qg import MPCToQGTranscompiler

app = Flask(__name__)

# Folder Configurations
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
OUTPUT_FOLDER = os.path.join(os.path.dirname(__file__), 'outputs')
ALLOWED_EXTENSIONS = {'xlsm', 'xlsx'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50 MB Max upload

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert_ciq():
    if 'mpc_file' not in request.files:
        return jsonify({"error": "No file uploaded."}), 400

    file = request.files['mpc_file']
    if file.filename == '':
        return jsonify({"error": "No file selected."}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(input_path)

        output_filename = f"QG_CIQ_Transformed_{filename.rsplit('.', 1)[0]}.xlsx"
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)

        try:
            transcompiler = MPCToQGTranscompiler(input_path)
            result = transcompiler.convert(output_path)
            
            return jsonify({
                "status": "SUCCESS",
                "download_url": f"/download/{output_filename}",
                "converted_sheets": result["converted_sheets"],
                "issue_count": result["issue_count"]
            })
        except Exception as e:
            return jsonify({"error": f"Transcompilation Failed: {str(e)}"}), 500

    return jsonify({"error": "Invalid file extension. Please upload an .xlsm or .xlsx MPC CIQ file."}), 400

@app.route('/download/<filename>')
def download_file(filename):
    file_path = os.path.join(app.config['OUTPUT_FOLDER'], filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return jsonify({"error": "File not found."}), 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
