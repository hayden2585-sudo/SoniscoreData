# SoniscoreData Setup Guide

## Project Overview
SoniscoreData is a Python package for data processing, scoring, and visualization with a focus on sonar/score data analysis. The project includes:

- **Data Processing**: Load, clean, and transform data from multiple formats
- **Score Calculation**: Normalize features and calculate composite scores
- **Visualization**: Generate charts and statistical visualizations
- **CLI Interface**: Command-line tool for easy data processing
- **Testing**: Unit tests for core functionality

## Current Status
✅ Repository cloned from https://github.com/hayden2585-sudo/SoniscoreData
✅ Project structure created with core modules
✅ README documentation updated
✅ Unit tests added
✅ GitHub authentication helper created

⚠️ **Authentication Required**: To push changes to GitHub, you need to authenticate.

## Authentication Setup

### Option 1: GitHub CLI (Recommended)
```bash
cd /Users/haydenjohnson/.agnes/temporary/2026-08-24/20260824_1/work/SoniscoreData
python github_auth_helper.py
```

Follow the prompts to authenticate with GitHub CLI.

### Option 2: Personal Access Token
1. Go to https://github.com/settings/tokens
2. Generate a new token with `repo` and `workflow` scopes
3. Copy the token
4. Update git remote:
   ```bash
   git remote set-url origin https://<TOKEN>@github.com/hayden2585-sudo/SoniscoreData.git
   ```

### Option 3: SSH Keys
1. Add SSH public key to GitHub:
   ```bash
   cat ~/.ssh/id_ed25519.pub
   ```
   Copy the output and add at: https://github.com/settings/ssh/new

2. Update remote to SSH:
   ```bash
   git remote set-url origin git@github.com:hayden2585-sudo/SoniscoreData.git
   ```

## Testing the Setup
```bash
cd /Users/haydenjohnson/.agnes/temporary/2026-08-24/20260824_1/work/SoniscoreData

# Test authentication
python github_auth_helper.py

# Or manually test push
git push origin main
```

## Project Structure
```
SoniscoreData/
├── main.py              # Main entry point with CLI
├── data_processor.py    # Data processing module
├── visualizer.py        # Visualization module
├── config.py            # Configuration management
├── test_processor.py    # Unit tests
├── github_auth_helper.py # GitHub authentication helper
├── setup_github_auth.sh # Shell script for auth setup
├── requirements.txt     # Python dependencies
├── example_data.csv     # Sample data
├── .gitignore           # Git ignore file
├── README.md            # Main documentation
└── SETUP_GUIDE.md       # This file
```

## Usage Examples

### Command Line
```bash
# Process example data
python main.py --input example_data.csv --output results.csv --verbose

# Process with custom settings
python main.py --input data.xlsx --output scores.csv
```

### As a Module
```python
from data_processor import DataProcessor
from visualizer import DataVisualizer

# Initialize
processor = DataProcessor()
visualizer = DataVisualizer()

# Process data
df = processor.load_data('data.csv')
df_clean = processor.clean_data(df)
df_scored = processor.calculate_scores(df_clean)

# Visualize
fig = visualizer.plot_score_distribution(df_scored)
visualizer.save_visualization(fig, 'output/distribution.png')
```

## Next Steps
1. Set up GitHub authentication (choose one option above)
2. Push changes to GitHub
3. Add more features as needed:
   - Support for additional data formats
   - More sophisticated scoring algorithms
   - Interactive web interface
   - Docker support

## Dependencies
```
pandas>=1.3.0
numpy>=1.21.0
matplotlib>=3.4.0
seaborn>=0.11.0
scikit-learn>=0.24.0
requests>=2.25.0
```

## License
MIT License