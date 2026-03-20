#!/bin/bash

# Sales Forecasting API - Quick Setup Script
# Run this script to set up and test the API locally

echo "=========================================="
echo "🚀 Sales Forecasting API - Setup Script"
echo "=========================================="
echo ""

# Check Python
echo "✓ Checking Python..."
python --version

# Create virtual environment
echo ""
echo "✓ Creating virtual environment..."
python -m venv venv

# Activate virtual environment
echo "✓ Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Upgrade pip
echo "✓ Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "✓ Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "=========================================="
echo "✅ Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Run the API:"
echo "   python app.py"
echo ""
echo "2. Open browser:"
echo "   http://localhost:8000"
echo "   http://localhost:8000/docs (Interactive Docs)"
echo ""
echo "3. Test endpoints:"
echo "   curl http://localhost:8000/stats"
echo "   curl -X POST http://localhost:8000/forecast/arima?periods=30"
echo ""
echo "4. To run web dashboard:"
echo "   pip install streamlit plotly"
echo "   streamlit run streamlit_app.py"
echo ""
echo "=========================================="
