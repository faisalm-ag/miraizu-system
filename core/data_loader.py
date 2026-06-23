import os
import pandas as pd

class MIRAIDataLoader:
    def __init__(self, base_dir=None):
        """
        Initializes dataset file paths using absolute path resolution 
        relative to the directory structure.
        """
        if base_dir is None:
            self.base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        else:
            self.base_dir = base_dir
            
        self.path_gaji = os.path.join(self.base_dir, 'data', 'processed', 'dataset_gaji_final.csv')
        self.path_hidup = os.path.join(self.base_dir, 'data', 'processed', 'dataset_biaya_hidup_final.csv')
        self.path_sewa = os.path.join(self.base_dir, 'data', 'processed', 'dataset_biaya_sewa_final.csv')
        self.path_kerja = os.path.join(self.base_dir, 'data', 'processed', 'dataset_kondisi_kerja_final.csv')

    def load_all_datasets(self):
        """
        Loads processed CSV datasets into memory using pandas DataFrames.
        
        Returns:
        tuple: Four pandas DataFrames containing macroeconomic indicators.
        """
        try:
            df_gaji = pd.read_csv(self.path_gaji)
            df_hidup = pd.read_csv(self.path_hidup)
            df_sewa = pd.read_csv(self.path_sewa)
            df_kerja = pd.read_csv(self.path_kerja)
            return df_gaji, df_hidup, df_sewa, df_kerja
        except Exception as e:
            print(f"Data ingestion failure: {e}")
            return None, None, None, None

    def get_merged_saw_matrix(self, bidang_terpilih):
        """
        Filters and integrates datasets based on user sector selection 
        to construct the evaluation matrix for SAW optimization.
        
        Parameters:
        bidang_terpilih (str): Designated industrial sector ID.
        
        Returns:
        DataFrame: Synthesized multi-criteria evaluation matrix.
        """
        df_gaji, df_hidup, df_sewa, df_kerja = self.load_all_datasets()
        
        if df_gaji is None:
            return None

        df_gaji_filtered = df_gaji[df_gaji['industri_id'] == bidang_terpilih].copy()
        
        if df_gaji_filtered.empty:
            return None

        base_matrix = df_gaji_filtered[[
            'prefektur_en', 
            'industri_id', 
            'gaji_pokok_bulanan', 
            'bonus_tahunan_rata_rata'
        ]]
        
        # Sequentially perform relational inner-joins across multidimensional parameters
        merged_df = pd.merge(base_matrix, df_hidup[['prefektur_en', 'biaya_hidup_nominal_yen']], on='prefektur_en', how='inner')
        merged_df = pd.merge(merged_df, df_sewa[['prefektur_en', 'biaya_sewa_nominal_yen']], on='prefektur_en', how='inner')
        merged_df = pd.merge(merged_df, df_kerja[['prefektur_en', 'rasio_lowongan_kerja']], on='prefektur_en', how='inner')
        
        return merged_df