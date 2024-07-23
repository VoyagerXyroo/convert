from flask import Flask, request, send_file, render_template
import os
import tempfile
import pdfkit


app = Flask(__name__)

# Path ke wkhtmltopdf (sesuaikan path dengan instalasi Anda)
path_wkhtmltopdf = 'wkhtmltopdf/bin/wkhtmltopdf' # Sesuaikan path jika berbeda
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

@app.route('/')
def index():
    return render_template('convert.html')

@app.route('/convert', methods=['POST'])
def convert():
    url = request.form.get('url')
    filename = request.form.get('filename')

    if not url or not filename:
        return "URL dan nama file harus diisi.", 400

    # Sanitasi nama file
    filename = filename.replace('/', '_').replace('\\', '_').strip()
    if not filename:
        filename = 'output'

    output_file = f'{filename}.pdf'

    # Menggunakan file temporer untuk menyimpan PDF
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            temp_file_path = temp_file.name

        pdfkit.from_url(url, temp_file_path, configuration=config)

        response = send_file(temp_file_path, as_attachment=True, attachment_filename=output_file, mimetype='application/pdf')
        response.headers['Content-Disposition'] = f'attachment; filename="{output_file}"'
        response.headers['Content-Type'] = 'application/pdf'
        return response

    except Exception as e:
        return f"Terjadi kesalahan saat mengonversi website: {e}", 500

    finally:
        if os.path.exists(temp_file_path):
            try:
                os.remove(temp_file_path)
            except Exception as e:
                print(f"Terjadi kesalahan saat menghapus file: {e}")

if __name__ == '__main__':
    app.run(debug=True)
