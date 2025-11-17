from flask import Flask, request, send_file, send_from_directory
import os, subprocess, uuid

app = Flask(__name__, static_folder="static")

# Ruta principal: devuelve el index.html
@app.route("/")
def home():
    return send_from_directory("static", "index.html")

# Ruta que convierte código Python en EXE
@app.route("/convert", methods=["POST"])
def convert():
    data = request.get_json()
    filename = data["filename"]
    code = data["code"]

    job_id = str(uuid.uuid4())
    folder = f"temp_{job_id}"
    os.makedirs(folder)

    py_path = os.path.join(folder, filename + ".py")

    # Guardar el código en un archivo
    with open(py_path, "w", encoding="utf-8") as f:
        f.write(code)

    # Ejecutar PyInstaller
    subprocess.run(["pyinstaller", "--onefile", py_path], cwd=folder)

    # Ubicación del EXE generado
    exe_path = os.path.join(folder, "dist", filename + ".exe")

    if not os.path.exists(exe_path):
        return {"error": "Error al generar el ejecutable"}, 500

    return send_file(exe_path, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
