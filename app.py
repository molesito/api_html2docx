from flask import Flask, request, send_file, jsonify
import pypandoc
import tempfile
import os

app = Flask(__name__)

@app.route("/convert", methods=["POST"])
def convert():
    try:
        data = request.get_json(force=True)
        html = data.get("html")
        filename = data.get("filename", "document.docx")

        if not html:
            return jsonify({"error": "Missing 'html' field"}), 400

        # Normalizar nombre
        if not filename.endswith(".docx"):
            filename += ".docx"

        # Estilos forzados para tablas y color de texto
        style = """
        <style>
            body { color: black; }
            table, th, td {
                border: 1px solid black;
                border-collapse: collapse;
                color: black;
            }
        </style>
        """
        html_with_style = f"<html><head>{style}</head><body>{html}</body></html>"

        # Crear archivo temporal
        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
            output_path = tmp.name

        # Convertir HTML a DOCX
        pypandoc.convert_text(html_with_style, "docx", format="html",
                              outputfile=output_path, extra_args=["--standalone"])

        return send_file(output_path,
                         as_attachment=True,
                         download_name=filename,
                         mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
