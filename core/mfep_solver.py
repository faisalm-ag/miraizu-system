class MFEPSolver:
    def __init__(self):
        # Criteria weight initialization based on system specification
        self.weights = {
            'bahasa': 0.30,
            'mental': 0.25,
            'ekonomi': 0.20,
            'fisik': 0.15,
            'akademik': 0.10
        }
        
        # Questionnaire index mapping (0-11) for each readiness criteria
        self.mapping_pertanyaan = {
            'bahasa': [0, 1, 2],      # Questions 1, 2, 3
            'mental': [3, 4, 5],      # Questions 4, 5, 6
            'fisik': [6, 7],          # Questions 7, 8
            'ekonomi': [8, 9],        # Questions 9, 10
            'akademik': [10, 11]      # Questions 11, 12
        }

    def calculate_readiness(self, answers):
        """
        Computes student internal readiness values using the Multi-Attribute Factor Evaluation Process (MFEP).
        
        Parameters:
        answers (list): Array of 12 integers/floats representing Likert scale values (1-5).
                        
        Returns:
        dict: Synthesized analytical results containing final readiness percentages and dimensional scores.
        """
        if not answers or len(answers) != 12:
            raise ValueError("Input must strictly contain exactly 12 questionnaire responses.")

        max_scale_value = 5.0
        factor_ratings = {}
        evaluation_values = {}
        total_mfep_score = 0.0

        for faktor, indeks_list in self.mapping_pertanyaan.items():
            faktor_answers = [float(answers[i]) for i in indeks_list]
            
            # Compute the mean response score for the designated factor
            rata_rata_skor = sum(faktor_answers) / len(faktor_answers)
            
            # Factor Rating: Scale the mean score to a percentage format (0 - 100)
            factor_rating = (rata_rata_skor / max_scale_value) * 100
            factor_ratings[faktor] = round(factor_rating, 2)
            
            # Evaluation Value: Apply criteria weighting to the scaled Factor Rating
            bobot = self.weights[faktor]
            evaluation_value = factor_rating * bobot
            evaluation_values[faktor] = round(evaluation_value, 2)
            
            # Synthesize final cumulative score
            total_mfep_score += evaluation_value

        results = {
            'total_readiness_percentage': round(total_mfep_score, 2),
            'factor_ratings': factor_ratings,
            'evaluation_values': evaluation_values,
            'status': 'Siap' if total_mfep_score >= 80.0 else 'Kurang Siap'
        }
        
        return results