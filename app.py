from flask import Flask, render_template, request, send_file
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from datetime import datetime
from reportlab.platypus import Table, TableStyle

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
    filepath = "temp.pdf"

    doc = SimpleDocTemplate(
        filepath,
        pagesize=A4,
        rightMargin=72,
        leftMargin=72,
        topMargin=60,
        bottomMargin=60
    )

    elements = []
    styles = getSampleStyleSheet()

    normal = styles['Normal']
    bold = styles['Heading4']

    # Nama & alamat atas
    elements.append(Paragraph(f"{nama_waris}", normal))
    elements.append(Paragraph("Taman Selasih", normal))
    elements.append(Spacer(1, 12))

    # Garisan pendek (tak full page)
    line = Table([[""]], colWidths=350)
    line.setStyle(TableStyle([
        ('LINEBELOW', (0,0), (-1,-1), 1, colors.black),
    ]))
    elements.append(line)
    elements.append(Spacer(1, 20))

    # Tarikh kanan
    tarikh_hari_ini = datetime.now().strftime("%d %B %Y")
    elements.append(Paragraph(f"{tarikh_hari_ini}", normal))
    elements.append(Spacer(1, 20))

    # Penerima
    elements.append(Paragraph(f"Guru Kelas {kelas}", normal))
    elements.append(Paragraph("Sekolah Kebangsaan Ulu Manding", normal))
    elements.append(Paragraph("Sarawak", normal))
    elements.append(Spacer(1, 20))

    elements.append(Paragraph("Tuan / Puan,", normal))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("<b>PER: MAKLUMAN TIDAK HADIR KE SEKOLAH</b>", normal))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("Dengan segala hormatnya perkara di atas adalah dirujuk.", normal))
    elements.append(Spacer(1, 12))

    isi = f"""
    2. Saya ingin memaklumkan bahawa anak saya {nama} dari kelas {kelas}
    tidak dapat hadir ke sekolah bermula {tarikh_mula} hingga {tarikh_akhir}
    kerana {sebab}.
    """
    elements.append(Paragraph(isi, normal))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("Kerjasama dan perhatian pihak tuan/puan amatlah dihargai.", normal))
    elements.append(Spacer(1, 20))

    elements.append(Paragraph("Sekian, terima kasih.", normal))
    elements.append(Spacer(1, 40))

    elements.append(Paragraph("Yang benar,", normal))
    elements.append(Spacer(1, 40))
    elements.append(Paragraph(f"({nama_waris})", normal))

    doc.build(elements)

    return send_file(filepath, as_attachment=True)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
