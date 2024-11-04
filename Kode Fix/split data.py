import pandas as pd
import os

# Load CSV file
file_path = r'C:\Users\Lenovo\Documents\Deep-Learning-Project\Dataset Fix\2. Filter Data Artikel Terbaru 2020-2024.csv'
df = pd.read_csv(file_path)

# Tentukan jumlah baris per bagian
rows_per_part = len(df) // 20

# Buat folder jika belum ada
output_folder = r'C:\Users\Lenovo\Documents\Deep-Learning-Project\Split Dataset'
os.makedirs(output_folder, exist_ok=True)

# Split dan simpan dataset ke dalam 20 bagian
for i in range(20):
    start_row = i * rows_per_part
    end_row = (i + 1) * rows_per_part if i < 19 else len(df)  # Sisa baris untuk bagian terakhir
    split_df = df.iloc[start_row:end_row]
    
    # Simpan file dengan nama 'split_part_i.csv'
    output_path = os.path.join(output_folder, f'split_part_{i+1}.csv')
    split_df.to_csv(output_path, index=False)

print("Pembagian dan penyimpanan selesai.")
