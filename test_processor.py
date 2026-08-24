#!/usr/bin/env python3
"""
SoniscoreData - Unit tests for data processor.
"""

import unittest
import pandas as pd
import numpy as np
from data_processor import DataProcessor


class TestDataProcessor(unittest.TestCase):
    """Test cases for DataProcessor class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.processor = DataProcessor()
        self.test_data = pd.DataFrame({
            'id': [1, 2, 3, 4, 5],
            'value1': [10, 20, 30, 40, 50],
            'value2': [15, 25, 35, 45, 55],
            'value3': [20, 30, 40, 50, 60],
            'name': ['A', 'B', 'C', 'D', 'E']
        })
    
    def test_load_csv(self):
        """Test loading CSV file."""
        import tempfile
        import os
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            self.test_data.to_csv(f, index=False)
            temp_path = f.name
        
        try:
            df = self.processor.load_data(temp_path)
            self.assertEqual(len(df), 5)
            self.assertEqual(list(df.columns), ['id', 'value1', 'value2', 'value3', 'name'])
        finally:
            os.unlink(temp_path)
    
    def test_clean_data(self):
        """Test data cleaning functionality."""
        # Add some missing values and duplicates
        df_with_issues = self.test_data.copy()
        df_with_issues.loc[2, 'value1'] = np.nan
        df_with_issues.loc[3, 'value2'] = np.nan
        df_with_issues = pd.concat([df_with_issues, self.test_data.iloc[0:1]])
        
        cleaned = self.processor.clean_data(df_with_issues)
        
        # Check no missing values
        self.assertFalse(cleaned.isnull().any().any())
        # Check no duplicates
        self.assertEqual(len(cleaned), len(df_with_issues) - 1)
    
    def test_calculate_scores(self):
        """Test score calculation."""
        df_scored = self.processor.calculate_scores(self.test_data)
        
        # Check that composite_score column exists
        self.assertIn('composite_score', df_scored.columns)
        # Check that rank column exists
        self.assertIn('rank', df_scored.columns)
        # Check that scores are normalized (0 to 1)
        self.assertTrue((df_scored['composite_score'] >= 0).all())
        self.assertTrue((df_scored['composite_score'] <= 1).all())
    
    def test_export_csv(self):
        """Test exporting to CSV."""
        import tempfile
        import os
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            temp_path = f.name
        
        try:
            self.processor.export_results(self.test_data, temp_path, format='csv')
            
            # Verify file was created and can be read
            df = pd.read_csv(temp_path)
            self.assertEqual(len(df), 5)
        finally:
            os.unlink(temp_path)


if __name__ == '__main__':
    unittest.main()