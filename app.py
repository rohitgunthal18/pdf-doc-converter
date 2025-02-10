from flask import Flask, request, send_file, render_template
from pdf2docx import Converter
from docx import Document
from reportlab.pdfgen import canvas
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/pdf-to-docx", methods=["POST"])
def pdf_to_docx():
    file = request.files["file"]
    if file.filename.endswith(".pdf"):
        pdf_path = os.path.join(UPLOAD_FOLDER, file.filename)
        docx_path = pdf_path.replace(".pdf", ".docx")
        file.save(pdf_path)

        cv = Converter(pdf_path)
        cv.convert(docx_path)
        cv.close()

        return send_file(docx_path, as_attachment=True)

@app.route("/docx-to-pdf", methods=["POST"])
def docx_to_pdf():
    file = request.files["file"]
    if file.filename.endswith(".docx"):
        docx_path = os.path.join(UPLOAD_FOLDER, file.filename)
        pdf_path = docx_path.replace(".docx", ".pdf")
        file.save(docx_path)

        doc = Document(docx_path)
        pdf = canvas.Canvas(pdf_path)
        text = "\n".join([p.text for p in doc.paragraphs])
        pdf.drawString(100, 750, text)
        pdf.save()

        return send_file(pdf_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
