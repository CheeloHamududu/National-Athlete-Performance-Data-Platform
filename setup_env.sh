#!/bin/bash

# Create virtual environment
python3 -m venv athlete_env

# Activate environment
source athlete_env/bin/activate

# Install requirements
pip install -r requirements.txt

echo "Environment setup complete!"
echo "To activate: source athlete_env/bin/activate"
echo "To run dashboard: streamlit run streamlit_dashboard.py"