import os
from flask import Flask, render_template, request, redirect, url_for, session, flash

from core.data_loader import MIRAIDataLoader
from core.mfep_solver import MFEPSolver
from core.saw_solver import SAWSolver

app = Flask(__name__)
app.secret_key = 'miraizu_secret_key_sttc_2026'

data_loader = MIRAIDataLoader()

# =============================================================
# 1. PRIMARY ROUTE
# =============================================================
@app.route('/')
def index():
    return render_template('index.html')


# =============================================================
# 2. SEQUENTIAL WORKFLOW PIPELINE
# =============================================================
@app.route('/biodata', methods=['GET', 'POST'])
def biodata():
    if request.method == 'POST':
        session['mahasiswa'] = {
            'nama': request.form.get('nama'),
            'nim': request.form.get('nim'),
            'jurusan': request.form.get('jurusan'),
            'jlpt': request.form.get('jlpt'),
            'bidang_peminatan': request.form.get('bidang_peminatan'), 
            'lokasi_peminatan': request.form.get('lokasi_peminatan')  
        }
        return redirect(url_for('kuesioner'))
        
    df_gaji, _, _, _ = data_loader.load_all_datasets()
    list_bidang = []
    list_lokasi = []
    
    if df_gaji is not None:
        list_bidang = sorted(df_gaji['industri_id'].dropna().unique().tolist())
        list_lokasi = sorted(df_gaji['prefektur_en'].dropna().unique().tolist())

    return render_template('biodata.html', bidang_options=list_bidang, lokasi_options=list_lokasi)


@app.route('/kuesioner', methods=['GET', 'POST'])
def kuesioner():
    if 'mahasiswa' not in session:
        flash('Silakan isi biodata terlebih dahulu.', 'warning')
        return redirect(url_for('biodata'))

    if request.method == 'POST':
        try:
            answers = []
            for i in range(1, 13):
                val = request.form.get(f'q{i}')
                if val is None:
                    raise ValueError(f"Pertanyaan ke-{i} belum diisi.")
                answers.append(int(val))
            
            mfep = MFEPSolver()
            mfep_results = mfep.calculate_readiness(answers)
            session['mfep_results'] = mfep_results
            
            return redirect(url_for('gaji'))
            
        except Exception as e:
            flash(f"Gagal memproses kuesioner: {str(e)}", 'danger')
            return redirect(url_for('kuesioner'))

    return render_template('kuesioner.html')


# =============================================================
# 3. INTERACTIVE ANALYTICS ENGINE
# =============================================================
@app.route('/alur/analisis-gaji')
def gaji():
    if 'mfep_results' not in session:
        flash('Silakan selesaikan kuesioner internal terlebih dahulu.', 'warning')
        return redirect(url_for('kuesioner'))
        
    mhs = session['mahasiswa']
    bidang = mhs['bidang_peminatan']
    lokasi = mhs['lokasi_peminatan']
    
    df_gaji, _, _, _ = data_loader.load_all_datasets()
    top_10_render = []
    narasi = "Data analisis statistik distribusi upah tidak tersedia."
    
    if df_gaji is not None:
        df_filtered = df_gaji[df_gaji['industri_id'].str.lower() == bidang.lower()].copy()
        df_filtered = df_filtered.sort_values(by='gaji_pokok_bulanan', ascending=False).reset_index(drop=True)
        total_wilayah = len(df_filtered)
        
        rank_mhs = 0
        data_mhs = None
        for idx, row in df_filtered.iterrows():
            if row['prefektur_en'].lower() == lokasi.lower():
                rank_mhs = idx + 1
                data_mhs = row.to_dict()
                break
        
        if rank_mhs > 0:
            if rank_mhs <= 10:
                top_10_render = df_filtered.head(10).to_dict(orient='records')
            else:
                top_10_render = df_filtered.head(9).to_dict(orient='records') + [data_mhs]
            
            nilai_gaji = int(data_mhs['gaji_pokok_bulanan'])
            prefix_rank = "ke-1 (Maksimum)" if rank_mhs == 1 else f"ke-{rank_mhs} dari {total_wilayah} entitas wilayah"
            
            narasi = (
                f"Analisis komparatif pada sektor industri <strong>{bidang}</strong> menunjukkan bahwa lokasi target "
                f"pilihan Anda (<strong>{lokasi}</strong>) memproyeksikan rerata upah pokok nominal sebesar <strong>¥{nilai_gaji:,}</strong> per bulan. "
                f"Berdasarkan sebaran empiris stratifikasi pasar kerja, nilai kompensasi finansial di wilayah ini menduduki peringkat "
                f"<strong>{prefix_rank}</strong> secara nasional di Jepang. Visualisasi diagram batang di samping merepresentasikan "
                f"posisi spasial wilayah pilihan Anda dalam struktur hierarki distribusi upah makro."
            )
            
    return render_template('gaji.html', top_10=top_10_render, narasi=narasi, mhs=mhs)


@app.route('/alur/analisis-biaya-hidup')
def biayahidup():
    if 'mfep_results' not in session:
        flash('Sesi pengujian tidak valid, silakan ulangi langkah.', 'warning')
        return redirect(url_for('kuesioner'))
        
    mhs = session['mahasiswa']
    lokasi = mhs['lokasi_peminatan']
    
    _, df_hidup, _, _ = data_loader.load_all_datasets()
    top_10_render = []
    narasi = "Data komponen pengeluaran konsumsi domestik tidak tersedia."
    
    if df_hidup is not None:
        df_filtered = df_hidup.sort_values(by='biaya_hidup_nominal_yen', ascending=True).reset_index(drop=True)
        total_wilayah = len(df_filtered)
        
        rank_mhs = 0
        data_mhs = None
        for idx, row in df_filtered.iterrows():
            if row['prefektur_en'].lower() == lokasi.lower():
                rank_mhs = idx + 1
                data_mhs = row.to_dict()
                break
                
        if rank_mhs > 0:
            if rank_mhs <= 10:
                top_10_render = df_filtered.head(10).to_dict(orient='records')
            else:
                top_10_render = df_filtered.head(9).to_dict(orient='records') + [data_mhs]
                
            nilai_hidup = int(data_mhs['biaya_hidup_nominal_yen'])
            narasi = (
                f"Berdasarkan agregasi data statistik pengeluaran agregat bulanan (tidak termasuk instrumen sewa akomodasi), "
                f"prefektur <strong>{lokasi}</strong> mencatatkan nilai ambang batas konsumsi finansial sebesar <strong>¥{nilai_hidup:,}</strong> per bulan. "
                f"Indikator ini menempatkan wilayah amatan Anda pada peringkat <strong>{rank_mhs} dari {total_wilayah} prefektur</strong> "
                f"dalam spektrum efisiensi biaya (diurutkan dari klaster paling minimum). Parameter ini diintegrasikan sebagai kriteria biaya "
                f"(<em>cost</em>) dalam fungsi objektif pembobotan algoritma SAW."
            )

    return render_template('biayahidup.html', top_10=top_10_render, narasi=narasi, mhs=mhs)


@app.route('/alur/analisis-biaya-sewa')
def biayasewa():
    if 'mfep_results' not in session:
        flash('Sesi pengujian tidak valid, silakan ulangi langkah.', 'warning')
        return redirect(url_for('kuesioner'))
        
    mhs = session['mahasiswa']
    lokasi = mhs['lokasi_peminatan']
    
    _, _, df_sewa, _ = data_loader.load_all_datasets()
    top_10_render = []
    narasi = "Data indeks nilai sewa akomodasi tidak tersedia."
    
    if df_sewa is not None:
        df_filtered = df_sewa.sort_values(by='biaya_sewa_nominal_yen', ascending=True).reset_index(drop=True)
        total_wilayah = len(df_filtered)
        
        rank_mhs = 0
        data_mhs = None
        for idx, row in df_filtered.iterrows():
            if row['prefektur_en'].lower() == lokasi.lower():
                rank_mhs = idx + 1
                data_mhs = row.to_dict()
                break
                
        if rank_mhs > 0:
            if rank_mhs <= 10:
                top_10_render = df_filtered.head(10).to_dict(orient='records')
            else:
                top_10_render = df_filtered.head(9).to_dict(orient='records') + [data_mhs]
                
            nilai_sewa = int(data_mhs['biaya_sewa_nominal_yen'])
            narasi = (
                f"Estimasi nilai rerata spasial untuk alokasi akomodasi dan asrama program internship di prefektur "
                f"<strong>{lokasi}</strong> berada pada ekuilibrium <strong>¥{nilai_sewa:,}</strong> per bulan. Berdasarkan penelaahan "
                f"secara komprehensif pada skala nasional, indeks biaya akomodasi wilayah sasaran Anda menempati peringkat "
                f"ke-<strong>{rank_mhs} dari {total_wilayah} regional</strong> (dihitung dari ambang ekonomi paling kompetitif). "
                f"Koefisien sewa pasar yang lebih rendah secara linier akan mengoptimalkan nilai preferensi akhir kriteria biaya pada pemodelan SAW."
            )

    return render_template('biayasewa.html', top_10=top_10_render, narasi=narasi, mhs=mhs)


@app.route('/alur/analisis-rasio-lowongan')
def lowongan():
    if 'mfep_results' not in session:
        flash('Sesi pengujian tidak valid, silakan ulangi langkah.', 'warning')
        return redirect(url_for('kuesioner'))
        
    mhs = session['mahasiswa']
    lokasi = mhs['lokasi_peminatan']
    
    _, _, _, df_kerja = data_loader.load_all_datasets()
    top_10_render = []
    avg_nasional = 0.0
    narasi = "Data indeks koefisien ketersediaan lapangan kerja tidak tersedia."
    
    if df_kerja is not None:
        avg_nasional = round(float(df_kerja['rasio_lowongan_kerja'].mean()), 2)
        df_filtered = df_kerja.sort_values(by='rasio_lowongan_kerja', ascending=False).reset_index(drop=True)
        total_wilayah = len(df_filtered)
        
        rank_mhs = 0
        data_mhs = None
        for idx, row in df_filtered.iterrows():
            if row['prefektur_en'].lower() == lokasi.lower():
                rank_mhs = idx + 1
                data_mhs = row.to_dict()
                break
                
        if rank_mhs > 0:
            if rank_mhs <= 10:
                top_10_render = df_filtered.head(10).to_dict(orient='records')
            else:
                top_10_render = df_filtered.head(9).to_dict(orient='records') + [data_mhs]
                
            ratio_mhs = float(data_mhs['rasio_lowongan_kerja'])
            keterangan_pasar = "mengalami saturasi positif (tingkat penyerapan tenaga kerja tinggi)" if ratio_mhs > avg_nasional else "berada pada fase restriktif (tingkat kompetisi tinggi)"
            
            narasi = (
                f"Indeks rasio lowongan kerja (<em>Active Job Openings Ratio</em>) di prefektur <strong>{lokasi}</strong> "
                f"mencatatkan koefisien sebesar <strong>{ratio_mhs}</strong>, sedangkan nilai rerata parameter nasional berada pada "
                f"angka <strong>{avg_nasional}</strong>. Karakateristik makro pasar kerja pada wilayah sasaran dinilai "
                f"<strong>{keterangan_pasar}</strong>, memposisikan wilayah tersebut pada urutan ke-<strong>{rank_mhs} dalam pemetaan "
                f"kapasitas absorbsi tenaga kerja</strong> di Jepang."
            )

    return render_template('lowongan.html', top_10=top_10_render, avg_nasional=avg_nasional, narasi=narasi, mhs=mhs)


# =============================================================
# 4. DECISION SUPPORT SYNTHESIS (MFEP VS SAW)
# =============================================================
@app.route('/rekomendasi')
def rekomendasi():
    if 'mahasiswa' not in session or 'mfep_results' not in session:
        flash('Lengkapi seluruh instrumen pengujian kesiapan terlebih dahulu.', 'warning')
        return redirect(url_for('biodata'))

    mhs_data = session['mahasiswa']
    mfep_data = session['mfep_results']
    
    bidang = mhs_data['bidang_peminatan']
    lokasi_target = mhs_data['lokasi_peminatan']

    df_merged = data_loader.get_merged_saw_matrix(bidang)
    
    if df_merged is None or df_merged.empty:
        flash(f"Data untuk bidang '{bidang}' tidak tersedia di dataset.", 'danger')
        return redirect(url_for('biodata'))

    saw = SAWSolver()
    df_saw_result = saw.calculate_saw(df_merged)

    target_row = df_saw_result[df_saw_result['prefektur_en'].str.lower() == lokasi_target.lower()]
    
    saw_target_score = 0.0
    detail_target = None
    
    if not target_row.empty:
        saw_target_score = target_row.iloc[0]['saw_score_percentage']
        detail_target = target_row.iloc[0].to_dict()

    mfep_score = mfep_data['total_readiness_percentage']
    is_recommended = mfep_score >= saw_target_score
    
    if is_recommended:
        narasi = (
            f"Berdasarkan sintesis komparatif antarmetode, variabel kesiapan internal subjek (MFEP) mencapai koefisien {mfep_score}%. "
            f"Capaian kuantitatif tersebut berhasil melampaui indeks ambang kelayakan lingkungan eksternal (SAW) yang ditetapkan pada prefektur "
            f"target <strong>{lokasi_target}</strong> untuk bidang <strong>{bidang}</strong>, dengan nilai ambang kebutuhan sebesar {saw_target_score}%. "
            f"Melalui penelaahan berbasis optimasi parameter tersebut, keputusan alokasi penempatan wilayah ini dinyatakan "
            f"<strong>SANGAT LAYAK & DIREKOMENDASIKAN</strong> bagi implementasi program internship mahasiswa."
        )
    else:
        narasi = (
            f"Berdasarkan hasil kalkulasi dan sintesis multikriteria, parameter kesiapan internal subjek (MFEP) saat ini berada pada tingkat {mfep_score}%. "
            f"Di sisi lain, tuntutan indeks kelayakan makro lingkungan eksternal (SAW) untuk bidang pekerjaan <strong>{bidang}</strong> di prefektur "
            f"sasaran <strong>{lokasi_target}</strong> menetapkan standar batas yang signifikan, yaitu sebesar {saw_target_score}%. Dikarenakan "
            f"kapasitas kesiapan internal subjek secara empiris berada di bawah ambang batas (<em>under-threshold</em>) kebutuhan regional, "
            f"maka penempatan di prefektur ini dinyatakan **TIDAK DIREKOMENDASIKAN**. Hal ini ditujukan guna memitigasi risiko kegagalan adaptasi "
            f"sosio-finansial maupun mental subjek di lapangan. Sistem merekomendasikan peninjauan ulang terhadap klaster alternatif di bawah "
            f"yang memiliki indeks kecocokan lebih realistis."
        )

    tabel_alternatif = df_saw_result.to_dict(orient='records')

    return render_template(
        'rekomendasi.html',
        mahasiswa=mhs_data,
        mfep=mfep_data,
        saw_target_score=saw_target_score,
        detail_target=detail_target,
        narasi=narasi,
        is_recommended=is_recommended,
        tabel_alternatif=tabel_alternatif
    )


# =============================================================
# 5. CORE SESSION MANAGEMENT
# =============================================================
@app.route('/reset')
def reset():
    session.clear()
    flash('Data pengujian telah di-reset secara bersih. Silakan mulai kembali.', 'info')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, port=5000)