#!/usr/bin/env python3
"""
SoniscoreData - Data processing module.
Handles data ingestion, cleaning, and transformation.
"""

import pandas as pd
import numpy as np
from typing import Optional, List, Dict, Any
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class DataProcessor:
    """Process and clean sonar/score data."""
    
    def __init__(self):
        self.stats = {}
        
    def load_data(self, file_path: str) -> pd.DataFrame:
        """Load data from various file formats."""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Data file not found: {file_path}")
        
        logger.info(f"Loading data from {file_path}")
        
        if path.suffix.lower() == '.csv':
            df = pd.read_csv(path)
        elif path.suffix.lower() in ['.xlsx', '.xls']:
            df = pd.read_excel(path)
        elif path.suffix.lower() == '.json':
            df = pd.read_json(path)
        else:
            raise ValueError(f"Unsupported file format: {path.suffix}")
        
        self.stats['rows'] = len(df)
        self.stats['columns'] = len(df.columns)
        
        return df
    
    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and preprocess the data."""
        df_clean = df.copy()
        
        # Remove duplicates
        duplicates = df_clean.duplicated().sum()
        if duplicates > 0:
            logger.info(f"Removing {duplicates} duplicate rows")
            df_clean = df_clean.drop_duplicates()
        
        # Handle missing values in numeric columns
        numeric_cols = df_clean.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            missing = df_clean[col].isna().sum()
            if missing > 0:
                median_val = df_clean[col].median()
                df_clean[col] = df_clean[col].fillna(median_val)
                logger.info(f"Filled {missing} missing values in '{col}' with median")
        
        # Handle missing values in object/string columns
        object_cols = df_clean.select_dtypes(include=['object']).columns
        for col in object_cols:
            missing = df_clean[col].isna().sum()
            if missing > 0 and missing < len(df_clean) * 0.5:  # Only if less than 50% missing
                df_clean[col] = df_clean[col].fillna(df_clean[col].mode()[0] if len(df_clean[col].mode()) > 0 else 'Unknown')
                logger.info(f"Filled {missing} missing values in '{col}' with mode")
        
        self.stats['cleaned_rows'] = len(df_clean)
        return df_clean
    
    def calculate_scores(self, df: pd.DataFrame, 
                        weight_config: Optional[Dict[str, float]] = None) -> pd.DataFrame:
        """Calculate composite scores from the data."""
        df_scored = df.copy()
        
        # Get numeric columns for scoring
        numeric_cols = df_scored.select_dtypes(include=[np.number]).columns.tolist()
        
        if not numeric_cols:
            logger.warning("No numeric columns found for scoring")
            return df_scored
        
        # Normalize columns
        for col in numeric_cols:
            min_val = df_scored[col].min()
            max_val = df_scored[col].max()
            col_range = max_val - min_val
            
            if col_range == 0:
                # All values are the same
                df_scored[f'{col}_normalized'] = 0.5
            else:
                df_scored[f'{col}_normalized'] = (df_scored[col] - min_val) / col_range
        
        # Calculate weighted composite score
        if weight_config:
            normalized_cols = [f'{col}_normalized' for col in numeric_cols]
            weights = [weight_config.get(col, 1.0/len(numeric_cols)) for col in numeric_cols]
            # Normalize weights
            weight_sum = sum(weights)
            weights = [w/weight_sum for w in weights]
            df_scored['composite_score'] = (df_scored[normalized_cols] * weights).sum(axis=1)
        else:
            # Equal weights
            normalized_cols = [f'{col}_normalized' for col in numeric_cols]
            df_scored['composite_score'] = df_scored[normalized_cols].mean(axis=1)
        
        # Add rank column
        df_scored['rank'] = df_scored['composite_score'].rank(ascending=False).astype(int)
        
        return df_scored
    
    def get_summary(self) -> Dict[str, Any]:
        """Get processing statistics."""
        return self.stats
    
    def export_results(self, df: pd.DataFrame, output_path: str, 
                      format: str = 'csv') -> None:
        """Export processed data to file."""
        path = Path(output_path)
        
        if format == 'csv':
            df.to_csv(path, index=False)
        elif format in ['xlsx', 'excel']:
            df.to_excel(path, index=False)
        elif format == 'json':
            df.to_json(path, orient='records')
        else:
            raise ValueError(f"Unsupported export format: {format}")
        
        logger.info(f"Exported {len(df)} rows to {output_path}")


if __name__ == '__main__':
    # Example usage
    processor = DataProcessor()
    print("SoniscoreData processor module loaded successfully")