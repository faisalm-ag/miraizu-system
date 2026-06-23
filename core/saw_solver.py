import pandas as pd
import numpy as np

class SAWSolver:
    def __init__(self):
        # Criteria weights initialization based on system specification
        self.weights = {
            'gaji': 0.30,
            'biaya_hidup': 0.25,
            'biaya_sewa': 0.20,
            'rasio_kerja': 0.25
        }

    def calculate_saw(self, df_merged):
        """
        Computes the Simple Additive Weighting (SAW) preference values for each prefecture alternative.
        
        Parameters:
        df_merged (DataFrame): Joined dataset from MIRAIDataLoader.get_merged_saw_matrix
        
        Returns:
        DataFrame: Ranked alternatives containing synthesized SAW percentage scores.
        """
        if df_merged is None or df_merged.empty:
            return None

        df_matrix = df_merged.copy()

        # STEP 1: Extract Extremum Values for Criteria Optimization
        # Benefit Criteria (Maximal)
        max_gaji = df_matrix['gaji_pokok_bulanan'].max()
        max_rasio = df_matrix['rasio_lowongan_kerja'].max()
        
        # Cost Criteria (Minimal)
        min_hidup = df_matrix['biaya_hidup_nominal_yen'].min()
        min_sewa = df_matrix['biaya_sewa_nominal_yen'].min()

        # STEP 2: Matrix Normalization (R)
        # Benefit Formula: r_ij = x_ij / max(x_j)
        df_matrix['R_gaji'] = df_matrix['gaji_pokok_bulanan'] / max_gaji if max_gaji != 0 else 0
        df_matrix['R_rasio'] = df_matrix['rasio_lowongan_kerja'] / max_rasio if max_rasio != 0 else 0
        
        # Cost Formula: r_ij = min(x_j) / x_ij
        df_matrix['R_hidup'] = min_hidup / df_matrix['biaya_hidup_nominal_yen']
        df_matrix['R_sewa'] = min_sewa / df_matrix['biaya_sewa_nominal_yen']

        # STEP 3: Preference Value Synthesis (V) & Percentage Scaling
        df_matrix['saw_score'] = (
            (df_matrix['R_gaji'] * self.weights['gaji']) +
            (df_matrix['R_hidup'] * self.weights['biaya_hidup']) +
            (df_matrix['R_sewa'] * self.weights['biaya_sewa']) +
            (df_matrix['R_rasio'] * self.weights['rasio_kerja'])
        )

        # Scale preference values to a percentage format (0% - 100%) for MFEP compatibility
        df_matrix['saw_score_percentage'] = round(df_matrix['saw_score'] * 100, 2)

        # STEP 4: Alternative Ranking & Column Selection
        df_result = df_matrix.sort_values(by='saw_score_percentage', ascending=False).reset_index(drop=True)
        
        columns_to_return = [
            'prefektur_en', 
            'industri_id', 
            'gaji_pokok_bulanan', 
            'bonus_tahunan_rata_rata', 
            'biaya_hidup_nominal_yen', 
            'biaya_sewa_nominal_yen', 
            'rasio_lowongan_kerja', 
            'saw_score_percentage'
        ]
        
        return df_result[columns_to_return]