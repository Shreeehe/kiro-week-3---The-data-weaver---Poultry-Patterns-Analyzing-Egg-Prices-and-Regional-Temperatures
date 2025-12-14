# 🐣 Poultry & Patterns: Analyzing Egg Prices and Regional Temperatures

A comprehensive Streamlit web application that analyzes correlations between regional temperature patterns and egg prices across major Indian cities. This project explores how meteorological factors influence agricultural commodity pricing in the poultry industry.

## 🌟 Features

### 📊 Interactive Data Analysis

- **Multi-City Comparison**: Analyze data from 8 major Indian cities
- **Time Series Visualization**: Track temperature and egg price trends over time
- **Correlation Analysis**: Statistical analysis with Pearson correlation coefficients
- **Date Range Filtering**: Customize analysis periods from 2017-2024

### 📈 Advanced Visualizations

- **Temperature Trends**: Interactive line charts showing regional temperature patterns
- **Egg Price Trends**: Price fluctuation analysis across different markets
- **Correlation Scatter Plots**: Visual representation of temperature-price relationships
- **Statistical Insights**: Automated generation of key findings and trends

### 🔧 Technical Features

- **Real-time Processing**: Fast data loading with Streamlit caching
- **Export Functionality**: Download filtered data and analysis results
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Error Handling**: Robust data validation and user-friendly error messages

## 🏙️ Cities Covered

| City                | Region      | Climate Zone         |
| ------------------- | ----------- | -------------------- |
| **Ahmedabad** | Gujarat     | Semi-arid            |
| **Bengaluru** | Karnataka   | Tropical savanna     |
| **Chennai**   | Tamil Nadu  | Tropical wet and dry |
| **Delhi**     | NCR         | Humid subtropical    |
| **Hyderabad** | Telangana   | Semi-arid            |
| **Kolkata**   | West Bengal | Tropical wet and dry |
| **Mumbai**    | Maharashtra | Tropical monsoon     |
| **Pune**      | Maharashtra | Semi-arid            |

## 📁 Project Structure

```
poultry-patterns/
├── 📱 app.py                    # Main Streamlit application
├── 🔧 data_processor.py         # Data loading and processing
├── 📊 visualizations.py         # Chart creation and plotting
├── 📈 statistics.py             # Statistical analysis functions
├── 🛠️ utils.py                  # Utility and helper functions
├── 🧪 test_data_loading.py      # Data loading tests
├── 📋 requirements.txt          # Python dependencies
├── 📚 README.md                 # Project documentation
├── 🧹 Data_Cleaning.ipynb       # Data preprocessing and cleaning notebook
├── 📂 csv/                      # Processed data files
│   ├── 🌡️ temperature.csv       # Monthly temperature data (processed)
│   └── 🥚 egg prices.csv        # Monthly egg price data (processed)
├── 📂 .kiro/                    # Kiro IDE specifications
│   └── specs/data-weaver-dashboard/
│       ├── requirements.md      # Project requirements
│       ├── design.md           # Technical design
│       └── tasks.md            # Implementation tasks
└── 📂 Weather Data/             # Raw weather data files
    ├── Information.txt          # Data source information
    └── [City].csv files         # Individual city weather data
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**

```bash
git clone <repository-url>
cd poultry-patterns
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Run the application**

```bash
streamlit run app.py
```

4. **Open your browser**
   Navigate to `http://localhost:8501` to access the dashboard

## 📊 Data Sources

### 🥚 Egg Price Data

- **Source**: [Kaggle - Egg Dataset India States 1982 to 2025](https://www.kaggle.com/datasets/youtubepremium123/egg-dataset-india-states-1982-to-2025)
- **Original Period**: 1982-2025
- **Processed Period**: 2017-2024 (filtered for analysis)
- **Format**: CSV with columns: Year, Month, Location, Average_Price_Per_Egg_INR_Monthly, Date
- **Coverage**: State-wise egg prices across India
- **Market Type**: Wholesale market prices in Indian Rupees per egg

### 🌡️ Temperature Data

- **Source**: [OpenCity.in - Daily Temperature 70 Years Data for Major Indian Cities](https://data.opencity.in/dataset/daily-temperature-70-years-data-for-major-indian-cities)
- **Original Period**: 1951-2024 (70 years of daily data)
- **Processed Period**: 2017-2024 (aggregated to monthly averages)
- **Format**: CSV with columns: Year, Month, Location, amonthly_average_temp, Date
- **Coverage**: 8 major Indian metropolitan cities
- **Measurement**: Daily temperature readings aggregated to monthly averages

### 🧹 Data Processing

- **Cleaning Notebook**: `Data_Cleaning.ipynb` (included in project directory)
- **Processing Tools**: Pandas for data manipulation and cleaning
- **Transformations Applied**:
  - Date standardization and alignment
  - Monthly aggregation of daily temperature data
  - Missing value handling and interpolation
  - City name standardization across datasets
  - Data type optimization and validation

## 🔬 Methodology

### Data Integration Process
1. **Raw Data Extraction**: Downloaded datasets from Kaggle and OpenCity.in
2. **Data Cleaning**: Used Pandas in Jupyter notebook (`Data_Cleaning.ipynb`) to:
   - Remove inconsistencies and outliers
   - Standardize date formats across datasets
   - Aggregate daily temperature to monthly averages
   - Filter data to common time period (2017-2024)
3. **Data Alignment**: Synchronized datasets by city and month for correlation analysis
4. **Quality Validation**: Implemented data quality checks and validation rules

### Analysis Framework
- **Statistical Method**: Pearson correlation coefficient for linear relationships
- **Significance Testing**: P-value analysis with α = 0.05 threshold
- **Visualization**: Interactive time series and scatter plot analysis
- **Insight Generation**: Automated pattern recognition and trend identification

## 🎯 Use Cases

### 🔬 Research Applications

- **Agricultural Economics**: Study price volatility in poultry markets
- **Climate Impact Analysis**: Understand weather effects on food production
- **Market Forecasting**: Identify seasonal patterns and trends
- **Policy Making**: Data-driven insights for agricultural policies

### 👥 Target Users

- **Agricultural Researchers**: Academic and industry professionals
- **Policy Makers**: Government officials and agricultural departments
- **Farmers and Producers**: Poultry industry stakeholders
- **Data Analysts**: Business intelligence and market research teams

## 📈 Key Insights

The application automatically generates insights such as:

- **Correlation Strength**: Statistical significance of temperature-price relationships
- **Regional Variations**: How different climate zones affect pricing
- **Seasonal Patterns**: Monthly and yearly trends in both metrics
- **Extreme Weather Impact**: Price volatility during temperature extremes

## 🛠️ Technology Stack

| Component                 | Technology      | Purpose                               |
| ------------------------- | --------------- | ------------------------------------- |
| **Frontend**        | Streamlit       | Interactive web interface             |
| **Data Processing** | Pandas          | Data manipulation and analysis        |
| **Visualization**   | Plotly          | Interactive charts and graphs         |
| **Statistics**      | SciPy, NumPy    | Correlation analysis and calculations |
| **Deployment**      | Streamlit Cloud | Cloud hosting and sharing             |

## 📱 Usage Guide

### 1. Select Cities

Use the sidebar to choose which cities to include in your analysis. You can select multiple cities for comparison.

### 2. Set Date Range

Pick start and end dates to focus on specific time periods. The application supports data from May 2017 onwards.

### 3. Analyze Correlations

View the correlation coefficient and statistical significance between temperature and egg prices.

### 4. Explore Visualizations

- **Time Series**: Track trends over time
- **Scatter Plots**: See direct temperature-price relationships
- **City Comparisons**: Compare patterns across regions

### 5. Export Results

Download your filtered data and analysis results for further research or reporting.

## 🔍 Statistical Methods

### Correlation Analysis

- **Pearson Correlation Coefficient**: Measures linear relationships
- **P-Value Testing**: Statistical significance at α = 0.05
- **Sample Size Validation**: Ensures reliable statistical inference

### Data Quality

- **Missing Value Handling**: Robust data cleaning procedures
- **Outlier Detection**: Statistical methods to identify anomalies
- **Date Alignment**: Precise temporal matching of datasets

## 🤝 Contributing

We welcome contributions to improve the analysis and add new features!

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test thoroughly
4. Submit a pull request with detailed description

### Areas for Contribution

- Additional weather metrics (humidity, rainfall)
- More cities and regions
- Advanced statistical models
- Machine learning predictions
- Mobile app development

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **AI for Bharat**: Week 3 Challenge - "The Data Weaver"
- **Data Sources**: 
  - [Kaggle](https://www.kaggle.com/datasets/youtubepremium123/egg-dataset-india-states-1982-to-2025) for comprehensive egg price dataset
  - [OpenCity.in](https://data.opencity.in/dataset/daily-temperature-70-years-data-for-major-indian-cities) for 70 years of temperature data
- **Kiro IDE**: Development environment and project management
- **Streamlit Community**: Framework and deployment platform
- **Pandas Community**: Data processing and analysis tools

## 🔮 Future Enhancements

- [ ] **Machine Learning Models**: Predictive analytics for price forecasting
- [ ] **Real-time Data**: Live feeds from weather stations and markets
- [ ] **Mobile App**: Native iOS and Android applications
- [ ] **API Integration**: RESTful API for external data access
- [ ] **Advanced Analytics**: Seasonal decomposition and trend analysis
- [ ] **Geographic Mapping**: Interactive maps with regional data
- [ ] **Alert System**: Notifications for significant price changes

---

**Built with ❤️ for agricultural research and data-driven decision making**

