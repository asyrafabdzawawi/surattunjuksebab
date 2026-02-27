from flask import Flask, render_template, request, send_file
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_JUSTIFY
from datetime import datetime
from reportlab.platypus import HRFlowable
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

    # ===== AUTO GENERATE SENARAI KELAS SK LABU BESAR =====
    tahun_list = [1, 2, 3, 4, 5, 6]
    aliran_list = ["Amber", "Amethyst", "Aquamarine"]

    alamat_map = {}

    for tahun in tahun_list:
        for aliran in aliran_list:
            nama_kelas_auto = f"{tahun} {aliran}"
            alamat_map[nama_kelas_auto] = f"""Guru Kelas {nama_kelas_auto}
Sekolah Kebangsaan Labu Besar
Kg Padang Ubi
09010 Kulim"""

    alamat_sekolah = alamat_map.get(kelas.strip(), "")

    filename = f"Surat_Tidak_Hadir_{nama}.pdf"
    filepath = f"/tmp/{filename}"

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
        leading=20,
        alignment=TA_JUSTIFY
    )

    style_left = ParagraphStyle(
        'left',
        parent=styles['Normal'],
        fontSize=12,
        leading=20,
        alignment=TA_LEFT
    )

    style_right = ParagraphStyle(
        'right',
        parent=styles['Normal'],
        fontSize=12,
        leading=20,
        alignment=TA_RIGHT
    )

    # ===== FORMAT TARIKH BM =====
    bulan_bm = {
        1: "Januari", 2: "Februari", 3: "Mac", 4: "April",
        5: "Mei", 6: "Jun", 7: "Julai", 8: "Ogos",
        9: "September", 10: "Oktober", 11: "November", 12: "Disember"
    }

    today = datetime.today()
    tarikh_hari_ini = f"{today.day} {bulan_bm[today.month]} {today.year}"

    # ===== ALAMAT WARIS =====
    elements.append(Paragraph(nama_waris, style_left))
    elements.append(Paragraph(alamat_waris.replace("\n", "<br/>"), style_left))
    elements.append(Spacer(1, 0.2 * inch))

    # ===== GARIS PANJANG =====
    elements.append(HRFlowable(
        width="100%",
        thickness=1,
        lineCap='round',
        color="black",
        spaceBefore=1,
        spaceAfter=1
    ))
    elements.append(Spacer(1, 0.3 * inch))

    # ===== TARIKH (KANAN) =====
    elements.append(Paragraph(tarikh_hari_ini, style_right))
    elements.append(Spacer(1, 0.35 * inch))

    # ===== ALAMAT SEKOLAH =====
    elements.append(Paragraph(alamat_sekolah.replace("\n", "<br/>"), style_left))
    elements.append(Spacer(1, 0.2 * inch))

    # ===== TUAN / PUAN =====
    elements.append(Paragraph("Tuan / Puan,", style_left))
    elements.append(Spacer(1, 0.3 * inch))

    # ===== PERKARA =====
    elements.append(Paragraph("<b>PER: MAKLUMAN TIDAK HADIR KE SEKOLAH</b>", style_left))
    elements.append(Spacer(1, 0.3 * inch))

    # ===== PERENGGAN 1 =====
    elements.append(Paragraph("Dengan segala hormatnya perkara di atas adalah dirujuk.", style_normal))
    elements.append(Spacer(1, 0.4 * inch))

    # ===== PERENGGAN 2 =====
    perenggan2 = f"""
    2. Saya {nama_waris} ingin memaklumkan bahawa anak saya {nama}
    dari kelas {kelas} tidak dapat hadir ke sekolah bermula
    {tarikh_mula} hingga {tarikh_akhir} kerana {sebab}.
    """
    elements.append(Paragraph(perenggan2, style_normal))
    elements.append(Spacer(1, 0.4 * inch))

    # ===== PERENGGAN 3 =====
    perenggan3 = """
    3. Sehubungan itu, saya memohon agar pihak tuan/puan dapat
    memberikan pelepasan kepada anak saya sepanjang tempoh tersebut.
    """
    elements.append(Paragraph(perenggan3, style_normal))
    elements.append(Spacer(1, 0.5 * inch))

    elements.append(Paragraph("Kerjasama dan perhatian pihak tuan/puan amatlah dihargai.", style_normal))
    elements.append(Spacer(1, 0.6 * inch))

    # ===== PENUTUP =====
    elements.append(Paragraph("Sekian, terima kasih.", style_left))
    elements.append(Spacer(1, 0.6 * inch))

    elements.append(Paragraph("Yang benar,", style_left))
    elements.append(Spacer(1, 0.8 * inch))

    # ===== GARIS TANDATANGAN =====
    elements.append(Paragraph("______________________________", style_left))
    elements.append(Paragraph(f"({nama_waris})", style_left))

    doc.build(elements)

    return send_file(filepath, as_attachment=True, download_name=filename)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
