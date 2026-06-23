# Miraizu System - Internship Recommendation Platform

<p align="center">
  <a href="#-bahasa-indonesia">Bahasa Indonesia</a> •
  <a href="#-english">English</a> •
  <a href="#-日本語">日本語</a>
</p>

---

## 🇮🇩 Bahasa Indonesia

### 📋 Deskripsi Proyek
Miraizu System adalah platform pengambilan keputusan berbasis web yang dirancang untuk membantu mahasiswa mengevaluasi kesiapan internal mereka sekaligus mencocokkan mereka dengan prefektur target di Jepang secara objektif. Sistem ini menggabungkan dua algoritma utama:
1. **MFEP (Factor Evaluation Process):** Digunakan untuk mengolah data kuesioner internal guna mengukur skor total kesiapan mahasiswa berdasarkan bobot regulasi magang Jepang.
2. **SAW (Simple Additive Weighting):** Digunakan untuk melakukan perankingan alternatif prefektur terbaik berdasarkan optimasi kriteria makro ekonomi seperti standar gaji (*benefit*), biaya hidup (*cost*), biaya sewa tempat tinggal (*cost*), dan rasio lowongan kerja (*benefit*).

### 📁 Struktur Direktori
```text
.
├── core/                       # Modul Logika Utama & Solver Algoritma
│   ├── __init__.py
│   ├── data_loader.py          # Pengolah & pemuat dataset CSV
│   ├── mfep_solver.py          # Logika kalkulasi evaluasi kesiapan
│   └── saw_solver.py           # Logika kalkulasi perankingan matriks SAW
├── data/                       # Penyimpanan Data Terpusat
│   ├── processed/              # Dataset final hasil pembersihan (siap pakai)
│   └── raw/                    # Dataset mentah makro ekonomi Jepang
├── notebook/                   # Eksperimen Analisis Data & Pra-pemrosesan
├── static/                     # Aset Statis Frontend (CSS/JS)
├── templates/                  # Antarmuka Halaman Web (Jinja2 Templates)
├── app.py                      # Aplikasi Flask Utama (Gateway/Controller)
├── requirements.txt            # Daftar dependensi pustaka Python
└── readme.md                   # Dokumentasi proyek

```

### Cara Menjalankan Aplikasi

1. **Klon Repositori & Masuk ke Direktori Proyek:**
```bash
git clone [https://github.com/username/miraizu-system.git](https://github.com/username/miraizu-system.git)
cd miraizu-system

```


2. **Instal Seluruh Dependensi:**
```bash
pip install -r requirements.txt

```


3. **Jalankan Server Flask:**
```bash
python app.py

```


4. **Buka Aplikasi di Browser:**
Akses `http://127.0.0.1:5000`

---

## 🇬🇧 English

### 📋 Project Description

Miraizu System is a web-based decision support system designed to help students evaluate their internal readiness and objectively match them with target prefectures in Japan. This system integrates two core algorithms:

1. **MFEP (Factor Evaluation Process):** Utilized to process internal questionnaire data to compute the student's total readiness score relative to Japanese internship regulations.
2. **SAW (Simple Additive Weighting):** Utilized to rank prefecture alternatives through the optimization of macroeconomic criteria, specifically Average Salary (*benefit*), Cost of Living (*cost*), Rent Index (*cost*), and Job Vacancy Ratio (*benefit*).

### 📁 Directory Structure

```text
.
├── core/                       # Core Logic Modules & Algorithm Solvers
│   ├── __init__.py
│   ├── data_loader.py          # CSV Dataset loader and parser
│   ├── mfep_solver.py          # Readiness evaluation calculation logic
│   └── saw_solver.py           # SAW matrix ranking calculation logic
├── data/                       # Centralized Data Storage
│   ├── processed/              # Cleaned and finalized datasets (production-ready)
│   └── raw/                    # Raw macroeconomic datasets of Japan
├── notebook/                   # Data Analysis & Preprocessing Experiments
├── static/                     # Frontend Static Assets (CSS/JS)
├── templates/                  # Web Interface Views (Jinja2 Templates)
├── app.py                      # Main Flask Application (Gateway/Controller)
├── requirements.txt            # Python library dependency declarations
└── readme.md                   # Project documentation

```

### How to Run

1. **Clone the Repository & Navigate to Project Directory:**
```bash
git clone [https://github.com/username/miraizu-system.git](https://github.com/username/miraizu-system.git)
cd miraizu-system

```


2. **Install Dependencies:**
```bash
pip install -r requirements.txt

```


3. **Run the Flask Server:**
```bash
python app.py

```


4. **Access the Web App:**
Open your browser and type `http://127.0.0.1:5000`

---

## 🇯🇵 日本語

### 📋 プロジェクト概要

Miraizu System（ミライズ・システム）は、学生が自身の内部的な準備状況を評価し、日本の目的の都道府県客観的にマッチングできるように設計された、ウェブベースの意思決定支援システムです。本システムは主に2つのアルゴリズムを統合しています：

1. **MFEP (因子評価プロセス):** 内部アンケートデータを処理し、日本のインターンシップ・技能実習制度の規制に基づく学生の総合的な準備状況スコアを算出します。
2. **SAW (単純加算重み付け法):** 平均賃金（メリット）、生活費（コスト）、家賃インフラ（コスト）、および有効求人倍率（メリット）といったマクロ経済基準を最適化することにより、最適な都道府県のランキングを生成します。

### 📁 ディレクトリ構造

```text
.
├── core/                       # コアロジックモジュール & アルゴリズムソルバー
│   ├── __init__.py
│   ├── data_loader.py          # CSVデータセットの読み込みと解析
│   ├── mfep_solver.py          # 準備状態評価の計算ロジック
│   └── saw_solver.py           # SAWマトリクスランキングの計算ロジック
├── data/                       # データストレージ
│   ├── processed/              # クリーニング済みの確定データセット（本番用）
│   └── raw/                    # 日本のマクロ経済生データ
├── notebook/                   # データ分析・前処理実験用ノートブック
├── static/                     # フロントエンド静的アセット（CSS/JS）
├── templates/                  # Webインターフェース画面（Jinja2 テンプレート）
├── app.py                      # メイン Flask アプリケーション（コントローラー）
├── requirements.txt            # Pythonライブラリ依存関係一覧
└── readme.md                   # プロジェクトドキュメント

```

### 起動方法

1. **リポジトリのクローンとプロジェクトディレクトリへの移動:**
```bash
git clone [https://github.com/username/miraizu-system.git](https://github.com/username/miraizu-system.git)
cd miraizu-system

```


2. **依存関係のインストール:**
```bash
pip install -r requirements.txt

```


3. **Flaskサーバーの起動:**
```bash
python app.py

```


4. **ブラウザでアクセス:**
URL `http://127.0.0.1:5000` を開きます。

```