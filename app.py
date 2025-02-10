from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from pdf2docx import Converter
from docx import Document
from reportlab.pdfgen import canvas
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route("/")
def home():
    return "PDF to DOCX and DOCX to PDF Converter API"

@app.route("/pdf-to-docx", methods=["POST"])
def pdf_to_docx():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if not file.filename.endswith(".pdf"):
        return jsonify({"error": "Invalid file format"}), 400

    pdf_path = os.path.join(UPLOAD_FOLDER, file.filename)
    docx_path = pdf_path.replace(".pdf", ".docx")
    file.save(pdf_path)

    try:
        cv = Converter(pdf_path)
        cv.convert(docx_path)
        cv.close()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return send_file(docx_path, as_attachment=True)

@app.route("/docx-to-pdf", methods=["POST"])
def docx_to_pdf():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if not file.filename.endswith(".docx"):
        return jsonify({"error": "Invalid file format"}), 400

    docx_path = os.path.join(UPLOAD_FOLDER, file.filename)
    pdf_path = docx_path.replace(".docx", ".pdf")
    file.save(docx_path)

    try:
        doc = Document(docx_path)
        pdf = canvas.Canvas(pdf_path)
        text = "\n".join([p.text for p in doc.paragraphs])
        pdf.drawString(100, 750, text)
        pdf.save()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return send_file(pdf_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
