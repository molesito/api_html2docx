from flask import Flask, request, send_file, jsonify
import pypandoc
import tempfile
import os
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/convert", methods=["POST"])
def convert():
    try:
        data = request.get_json(force=True)
        html = data.get("html")
        filename = data.get("filename", "document.docx")

        if not html:
            return jsonify({"error": "Missing 'html' field"}), 400

        if not filename.endswith(".docx"):
            filename += ".docx"

        # Procesar HTML con BeautifulSoup
        soup = BeautifulSoup(html, "html.parser")

        # Forzar texto negro en todo
        for tag in soup.find_all(True):  # True = todos los tags
            old_style = tag.get("style", "")
            if "color" not in old_style:
                tag["style"] = old_style + "; color: black;"

        # Forzar bordes en tablas
        for table in soup.find_all("table"):
            table["style"] = table.get("style", "") + "; border-collapse: collapse; border: 1px solid black;"
        for td in soup.find_all(["td", "th"]):
            td["style"] = td.get("style", "") + "; border: 1px solid black;"

        html_processed = str(soup)

        # Crear archivo temporal
        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
            output_path = tmp.name

        # Convertir HTML a DOCX
        pypandoc.convert_text(html_processed, "docx", format="html",
                              outputfile=output_path, extra_args=["--standalone"])

        return send_file(output_path,
                         as_attachment=True,
                         download_name=filename,
                         mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
