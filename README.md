# SoniscoreData

A Python package for data processing, scoring, and visualization with a focus on sonar/score data analysis.

## Features
- **Data Ingestion**: Load data from CSV, Excel, and JSON formats
- **Data Cleaning**: Automatic handling of missing values and duplicates
- **Score Calculation**: Normalize features and calculate composite scores
- **Visualization**: Generate histograms, scatter plots, and correlation matrices
- **Export**: Save processed data and visualizations to multiple formats

## Installation

### Requirements
Python 3.8+ with the following dependencies:
```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install pandas numpy matplotlib seaborn scikit-learn
```

## Usage

### Command Line
```bash
# Basic usage
python main.py --input data.csv --output results.csv --verbose

# With custom weights
python main.py --input data.xlsx --output scores.csv --verbose
```

### As a Module
```python
from data_processor import DataProcessor
from visualizer import DataVisualizer
from config import get_config, get_data_dirs

# Initialize components
processor = DataProcessor()
visualizer = DataVisualizer()
config = get_config()

# Load and process data
df = processor.load_data('input_data.csv')
df_clean = processor.clean_data(df)
df_scored = processor.calculate_scores(df_clean)

# Create visualizations
fig1 = visualizer.plot_score_distribution(df_scored)
fig2 = visualizer.plot_top_scores(df_scored, n=10)
fig3 = visualizer.plot_correlation_matrix(df_scored)

# Save results
processor.export_results(df_scored, 'output.csv', format='csv')
visualizer.save_visualization(fig1, 'output/distribution.png')
```

## Project Structure
```
SoniscoreData/
├── main.py              # Main entry point
├── data_processor.py    # Data processing module
├── visualizer.py        # Visualization module
├── config.py            # Configuration module
├── test_processor.py    # Unit tests
├── requirements.txt     # Python dependencies
├── example_data.csv     # Sample data
├── .gitignore           # Git ignore file
└── README.md            # This file
```

## Configuration
Create a `config.yaml` file in the project root:
```yaml
data:
  input_dir: './data'
  output_dir: './output'
  default_format: 'csv'

processing:
  normalize_method: 'minmax'
  missing_value_strategy: 'median'

scoring:
  default_weight: 1.0
  score_precision: 4
```

## Running Tests
```bash
python -m pytest test_processor.py -v
```

## License
MIT License - see LICENSE file for details.

## Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request