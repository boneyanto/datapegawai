import pandas as pd
import json
import os

# Baca file Excel dari URL
file_url = "https://docs.google.com/spreadsheets/d/1-kKhJJi2QrNnKVJUnbwXAXjmE8PpxuLu/edit?gid=535977766#gid=535977766"
df = pd.read_excel(file_url)

# Convert date columns to string
date_columns = ['TANGGAL LAHIR', 'tmt_sk', 'tst_sk', 'tgl_mulai', 'tgl_selesai', 'TMT']
for col in date_columns:
    if col in df.columns:
        df[col] = pd.to_datetime(df[col], errors='coerce').dt.strftime('%Y-%m-%d')

# Select main fields
main_fields = [
    'NIP', 'NAMA', 'GELAR DEPAN', 'GELAR BELAKANG',
    'TEMPAT LAHIR', 'TANGGAL LAHIR', 'JENKEL',
    'Status Kepegawaian',
    'PANGKAT', 'UNIT KERJA', 'TMT', 'MASA KERJA'
]
main_data = df[main_fields]

# Pastikan kolom "MASA KERJA" adalah nilai yang dihasilkan oleh formula, bukan formula itu sendiri
main_data['MASA KERJA'] = main_data['MASA KERJA'].astype(str)

# Select "RIWAYAT JABATAN" fields
riwayat_fields = ['nm_jabatan', 'tmt_sk', 'tst_sk', 'tgl_mulai', 'tgl_selesai', 'jns_jabatan']
riwayat_data = df[riwayat_fields]

# Combine main fields with "RIWAYAT JABATAN"
result = []
for i in range(len(main_data)):
    main_record = main_data.iloc[i].to_dict()
    main_record["RIWAYAT JABATAN"] = riwayat_data.iloc[i].to_dict()
    result.append(main_record)

# Save as JSON file
output_file = 'data-pegawai.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=4)

print(f"File {output_file} has been created.")
