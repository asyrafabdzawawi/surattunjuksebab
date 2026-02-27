from flask import Flask, render_template, request, send_file
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from datetime import datetime
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
    alamat_waris = request.form['alamat_waris']

    # ===== Mapping Alamat Sekolah Ikut Kelas =====
    alamat_map = {
        "4 AMBER": "Guru Kelas 4 AMBER\nSekolah Kebangsaan Ulu Manding\nSarawak",
        "5 AMBER": "Guru Kelas 5 AMBER\nSekolah Kebangsaan Ulu Manding\nSarawak",
        "6 AMBER": "Guru Kelas 6 AMBER\nSekolah Kebangsaan Ulu Manding\nSarawak"
    }

    alamat_sekolah = alamat_map.get(kelas, "")

    filename = f"Surat_Tidak_Hadir_{nama}.pdf"
    filepath = "temp.pdf"

    doc = SimpleDocTemplate(
        filepath,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    elements = []
    styles = getSampleStyleSheet()

    style_normal = ParagraphStyle(
        'normal',
        parent=styles['Normal'],
        fontSize=12,
        leading=18,
        alignment=TA_JUSTIFY
    )

    style_right = ParagraphStyle(
        'right',
        parent=styles['Normal'],
        fontSize=12,
        leading=18,
        alignment=TA_RIGHT
    )

    # Format tarikh Malaysia
    tarikh_hari_ini = datetime.today().strftime("%d %B %Y")

    # ===== Alamat Waris =====
    elements.append(Paragraph(nama_waris, styles['Normal']))
    elements.append(Paragraph(alamat_waris.replace("\n", "<br/>"), styles['Normal']))
    elements.append(Spacer(1, 0.5 * inch))

    # ===== Tarikh =====
    elements.append(Paragraph(tarikh_hari_ini, style_right))
    elements.append(Spacer(1, 0.5 * inch))

    # ===== Alamat Sekolah =====
    elements.append(Paragraph(alamat_sekolah.replace("\n", "<br/>"), styles['Normal']))
    elements.append(Spacer(1, 0.3 * inch))

    # ===== Tajuk =====
    elements.append(Paragraph("<b>PER: MAKLUMAN TIDAK HADIR KE SEKOLAH</b>", styles['Normal']))
    elements.append(Spacer(1, 0.3 * inch))

    # ===== Isi Surat =====
    isi = f"""
    Dengan segala hormatnya perkara di atas adalah dirujuk.

    2. Saya {nama_waris} ingin memaklumkan bahawa anak saya {nama}
    dari kelas {kelas} tidak dapat hadir ke sekolah bermula
    {tarikh_mula} hingga {tarikh_akhir} kerana {sebab}.

    3. Sehubungan itu, saya memohon agar pihak tuan/puan dapat
    memberikan pelepasan kepada anak saya sepanjang tempoh tersebut.

    Kerjasama dan perhatian pihak tuan/puan amatlah dihargai.
    """

    elements.append(Paragraph(isi, style_normal))
    elements.append(Spacer(1, 0.5 * inch))

    # ===== Penutup =====
    elements.append(Paragraph("Sekian, terima kasih.", styles['Normal']))
    elements.append(Spacer(1, 0.6 * inch))

    elements.append(Paragraph("Yang benar,", styles['Normal']))
    elements.append(Spacer(1, 0.8 * inch))

    elements.append(Paragraph(f"<b>({nama_waris})</b>", styles['Normal']))

    doc.build(elements)

    return send_file(filepath, as_attachment=True, download_name=filename)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
