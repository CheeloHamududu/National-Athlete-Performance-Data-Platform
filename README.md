# National Athlete Performance Platform

A centralized, digital performance and analytics platform to support national sports federations and youth training centers in optimizing athlete development, monitoring, and talent identification.

## Features

- **Real-time Performance Monitoring**: Track physical performance, physiological metrics, training load & recovery
- **Injury Prevention**: Data-driven insights to reduce injury risk through proactive monitoring
- **Talent Identification**: Objective analytics to uncover high-potential youth athletes
- **Personalized Training**: Tailored programs to improve athlete performance and career longevity

## Project Structure

```
├── National_Athlete_Performance_Platform.ipynb  # Main analysis notebook
├── Sports_Training_Analysis.ipynb               # Additional training analysis
├── streamlit_dashboard.py                       # Interactive web dashboard
├── Athlete_Training_Recovery_Tracker_Dataset.csv # Primary dataset
├── sports_training_dataset.csv                 # Secondary dataset
├── requirements.txt                             # Python dependencies
├── setup_env.sh                                # Environment setup script
└── athlete_env/                                # Virtual environment
```

## Quick Start

### Prerequisites

- Python 3.8+
- pip package manager

### Installation

1. Clone or download this repository
2. Navigate to the project directory:

3. Set up the environment:
   ```bash
   chmod +x setup_env.sh
   ./setup_env.sh
   ```

4. Activate the virtual environment:
   ```bash
   source athlete_env/bin/activate
   ```

5. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Usage

#### Jupyter Notebook Analysis
```bash
jupyter notebook National_Athlete_Performance_Platform.ipynb
```

#### Interactive Dashboard
```bash
streamlit run streamlit_dashboard.py
```

## Data Overview

The platform analyzes athlete performance data including:
- Training hours and intensity
- Sleep patterns and recovery metrics
- Nutrition scores
- Fatigue levels
- Performance scores
- Injury risk assessments

## Key Metrics

- **Performance Score**: Overall athlete performance rating (0-100)
- **Recovery Index**: Recovery status indicator (0-100)
- **Injury Risk**: Categorized as Low, Medium, or High
- **Training Load**: Combination of hours and intensity

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](#license) section below.

---

## License

MIT License

Copyright (c) 2025 National Athlete Performance Platform

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
