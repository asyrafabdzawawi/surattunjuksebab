from flask import Flask, render_template, request, send_file
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import Table
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import Image
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Paragraph
from reportlab.platypus import Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Table
from reportlab.platypus import TableStyle
import os

app = Flask(__name__)

@app.route('/')
def form():
    return render_template('form.html')

@app.route('/generate', methods=['POST'])
def generate_pdf():
    nama = request.form['nama']
    kelas = request.form['kelas']
    tarikh_mula = request.form['tarikh_mula']
    tarikh_akhir = request.form['tarikh_akhir']
    sebab = request.form['sebab']
    nama_waris = request.form['nama_waris']

    filename = f"Surat_Tidak_Hadir_{nama}.pdf"
    filepath = os.path.join("temp.pdf")

    doc = SimpleDocTemplate(filepath)
    elements = []
    styles = getSampleStyleSheet()

    elements.append(Paragraph("SURAT TIDAK HADIR KE SEKOLAH", styles['Title']))
    elements.append(Spacer(1, 0.5 * inch))

    text = f"""
    Saya ingin memaklumkan bahawa anak saya {nama} dari kelas {kelas}
    tidak dapat hadir ke sekolah bermula {tarikh_mula} hingga {tarikh_akhir}
    kerana {sebab}.
    """

    elements.append(Paragraph(text, styles['Normal']))
    elements.append(Spacer(1, 0.5 * inch))
    elements.append(Paragraph("Sekian, terima kasih.", styles['Normal']))
    elements.append(Spacer(1, 0.5 * inch))
    elements.append(Paragraph(f"Yang benar,", styles['Normal']))
    elements.append(Paragraph(nama_waris, styles['Normal']))

    doc.build(elements)

    return send_file(filepath, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
