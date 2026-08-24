#!/usr/bin/env python3
"""
SoniscoreData - Data visualization module.
Creates charts and visualizations for score analysis.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class DataVisualizer:
    """Create visualizations for score data."""
    
    def __init__(self, style: str = 'darkgrid'):
        self.style = style
        # Validate style
        valid_styles = ['white', 'dark', 'whitegrid', 'darkgrid', 'ticks']
        if style not in valid_styles:
            print(f"Warning: Invalid style '{style}', using 'darkgrid'")
            style = 'darkgrid'
        sns.set_style(style)
        plt.rcParams['figure.figsize'] = (12, 8)
        
    def plot_score_distribution(self, df: pd.DataFrame, 
                               score_col: str = 'composite_score',
                               title: str = 'Score Distribution') -> plt.Figure:
        """Plot histogram of composite scores."""
        fig, ax = plt.subplots()
        
        # Create histogram
        ax.hist(df[score_col], bins=30, alpha=0.7, color='steelblue', edgecolor='white')
        ax.set_xlabel(score_col, fontsize=12)
        ax.set_ylabel('Frequency', fontsize=12)
        ax.set_title(title, fontsize=14)
        
        # Add mean line
        mean_score = df[score_col].mean()
        ax.axvline(x=mean_score, color='red', linestyle='--', 
                  label=f'Mean: {mean_score:.2f}')
        ax.legend()
        
        plt.tight_layout()
        return fig
    
    def plot_top_scores(self, df: pd.DataFrame, 
                       n: int = 10,
                       title: str = 'Top N Scores') -> plt.Figure:
        """Plot top N scores with their ranks."""
        fig, ax = plt.subplots()
        
        # Get top N scores
        top_scores = df.nlargest(n, 'composite_score')[['rank', 'composite_score']]
        
        # Create bar chart
        colors = plt.cm.viridis(np.linspace(0.2, 0.8, len(top_scores)))
        bars = ax.barh(range(len(top_scores)), top_scores['composite_score'], color=colors)
        
        # Add labels and formatting
        ax.set_yticks(range(len(top_scores)))
        ax.set_yticklabels([f"Rank {rank}" for rank in top_scores['rank']])
        ax.set_xlabel('Composite Score', fontsize=12)
        ax.set_title(title, fontsize=14)
        
        # Add value labels on bars
        for i, (bar, score) in enumerate(zip(bars, top_scores['composite_score'])):
            ax.text(score + 0.01, i, f'{score:.2f}', va='center', fontsize=9)
        
        plt.tight_layout()
        return fig
    
    def plot_score_vs_features(self, df: pd.DataFrame, 
                              feature_cols: list = None,
                              title: str = 'Score vs Features') -> plt.Figure:
        """Plot scatter plots of scores vs individual features."""
        if feature_cols is None:
            feature_cols = [col for col in df.columns if 'normalized' in col]
        
        num_features = min(len(feature_cols), 4)  # Limit to 4 for readability
        cols = num_features // 2 if num_features > 1 else 1
        rows = (num_features + 1) // 2
        
        fig, axes = plt.subplots(rows, cols, figsize=(5*cols, 5*rows))
        if rows == 1 and cols == 1:
            axes = [axes]
        elif rows == 1:
            axes = axes.flatten()
        elif cols == 1:
            axes = axes.reshape(-1, 1)
        else:
            axes = axes.flatten()
        
        for i, col in enumerate(feature_cols[:num_features]):
            ax = axes[i]
            
            # Create scatter plot
            ax.scatter(df[col], df['composite_score'], alpha=0.6, s=50, color='steelblue')
            ax.set_xlabel(col.replace('_normalized', ''), fontsize=10)
            ax.set_ylabel('Composite Score', fontsize=10)
            ax.set_title(f'{col.replace("_normalized", "")} vs Score', fontsize=12)
            
            # Add trend line
            z = np.polyfit(df[col], df['composite_score'], 1)
            p = np.poly1d(z)
            x_range = np.linspace(df[col].min(), df[col].max(), 100)
            ax.plot(x_range, p(x_range), "r--", alpha=0.8, linewidth=2)
        
        # Hide any unused subplots
        for i in range(num_features, len(axes)):
            axes[i].set_visible(False)
        
        plt.tight_layout()
        return fig
    
    def plot_correlation_matrix(self, df: pd.DataFrame, 
                               title: str = 'Feature Correlation Matrix') -> plt.Figure:
        """Plot correlation matrix heatmap."""
        fig, ax = plt.subplots()
        
        # Calculate correlation
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        corr_matrix = df[numeric_cols].corr()
        
        # Create heatmap
        mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
        sns.heatmap(corr_matrix, mask=mask, annot=True, fmt='.2f', 
                   cmap='RdYlBu_r', center=0, square=True, 
                   ax=ax, cbar_kws={"shrink": .8})
        
        ax.set_title(title, fontsize=14)
        plt.tight_layout()
        return fig
    
    def save_visualization(self, fig: plt.Figure, output_path: str) -> None:
        """Save visualization to file."""
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(path, dpi=150, bbox_inches='tight')
        plt.close(fig)
        logger.info(f"Visualization saved to {output_path}")


if __name__ == '__main__':
    # Example usage
    visualizer = DataVisualizer()
    print("SoniscoreData visualizer module loaded successfully")