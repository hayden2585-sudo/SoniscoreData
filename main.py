#!/usr/bin/env python3
"""
SoniscoreData - Main entry point for data processing and analysis.
"""

import pandas as pd
import numpy as np
import argparse
import sys
from pathlib import Path


def load_data(file_path: str) -> pd.DataFrame:
    """Load data from CSV or Excel file."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Data file not found: {file_path}")
    
    if path.suffix.lower() == '.csv':
        return pd.read_csv(path)
    elif path.suffix.lower() in ['.xlsx', '.xls']:
        return pd.read_excel(path)
    else:
        raise ValueError(f"Unsupported file format: {path.suffix}")


def process_data(df: pd.DataFrame) -> pd.DataFrame:
    """Process and clean the data."""
    # Basic data cleaning
    df_clean = df.copy()
    
    # Remove duplicates
    df_clean = df_clean.drop_duplicates()
    
    # Handle missing values
    numeric_cols = df_clean.select_dtypes(include=[np.number]).columns
    df_clean[numeric_cols] = df_clean[numeric_cols].fillna(df_clean[numeric_cols].median())
    
    return df_clean


def calculate_scores(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate composite scores from the data."""
    df_scored = df.copy()
    
    # Example: Create a composite score from numeric columns
    numeric_cols = df_scored.select_dtypes(include=[np.number]).columns
    
    if len(numeric_cols) > 0:
        # Normalize each numeric column
        for col in numeric_cols:
            min_val = df_scored[col].min()
            max_val = df_scored[col].max()
            if max_val != min_val:
                df_scored[f'{col}_normalized'] = (df_scored[col] - min_val) / (max_val - min_val)
            else:
                df_scored[f'{col}_normalized'] = 0.5
        
        # Calculate composite score (simple average)
        normalized_cols = [f'{col}_normalized' for col in numeric_cols]
        df_scored['composite_score'] = df_scored[normalized_cols].mean(axis=1)
    
    return df_scored


def main():
    parser = argparse.ArgumentParser(description='SoniscoreData - Data processing and scoring')
    parser.add_argument('--input', '-i', required=True, help='Input data file (CSV or Excel)')
    parser.add_argument('--output', '-o', default='output.csv', help='Output file for processed data')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose output')
    
    args = parser.parse_args()
    
    try:
        if args.verbose:
            print(f"Loading data from {args.input}...")
        
        # Load and process data
        df = load_data(args.input)
        df_processed = process_data(df)
        
        if args.verbose:
            print(f"Processed {len(df_processed)} records")
        
        # Calculate scores
        df_scored = calculate_scores(df_processed)
        
        # Save results
        df_scored.to_csv(args.output, index=False)
        
        if args.verbose:
            print(f"Results saved to {args.output}")
        
        print(f"Successfully processed data and calculated scores")
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()