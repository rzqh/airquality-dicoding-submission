import numpy as np # type: ignore
import streamlit as st # type: ignore
import pandas as pd # type: ignore
import matplotlib.pyplot as plt # type: ignore
import seaborn as sns # type: ignore
from statsmodels.tsa.seasonal import seasonal_decompose # type: ignore


# Title page
st.set_page_config(page_title="Analisis Air Quality @Wanliu oleh Rizqi Hasanuddin")

# Load dataset
data = pd.read_csv('./data/PRSA_Data_Wanliu_20130301-20170228.csv')

# Title dashboard
st.title('Dashboard Air Quality: Stasiun Wanliu')

# deskripsi singkat
st.write('Dashboard ini menyediakan cara yang lebih interaktif untuk eksplorasi data kualitas udara, khususnya yang berfokus pada tingkat PM2.5 dan korelasinya dengan berbagai kondisi cuaca.')

# about
st.markdown("""
### Tentang saya
- **Name**: Rizqi Hasanuddin
- **Email Address**: rizqih6x@gmail.com
- **Dicoding ID**: [rzqh00](https://www.dicoding.com/users/rzqh00/)

### Project Overview
Dashboard ini menyajikan analisa data kualitas udara, terutama pada tingkat PM2.5 dari stasiun Wanliu. Project ini bertujuan untuk mengungkap berbagai insight seperti dinamika, variasi musiman dan dampak berbagai kondisi cuaca terhadap kualitas udara. Insight dari analisis ini dapat bermanfaat untuk studi lingkungan dan pemantauan kesehatan pasyarakat
""")

# sidebar untuk fitur slicer 
st.sidebar.header('Fitur slicer')

selected_year = st.sidebar.selectbox('Tahun', list(data['year'].unique()))
selected_month = st.sidebar.selectbox('Bulan', list(data['month'].unique()))

# filter data based on tahun dan bulan
data_filtered = data[(data['year'] == selected_year) & (data['month'] == selected_month)].copy()

# matrix data stats
st.subheader('Data Overview')
st.write(data_filtered.describe())

# pm2.5 per hari
st.subheader('Tingkatan PM2.5 per Hari')
fig, ax = plt.subplots()
ax.plot(data_filtered['day'], data_filtered['PM2.5'])
plt.xlabel('Tanggal')
plt.ylabel('Tingkatan PM2.5')
st.pyplot(fig)

# pm2.5 per bulan
st.subheader('Tingkatan PM2.5 per Bulan')
seasonal_trends = data.groupby('month')['PM2.5'].mean()
fig, ax = plt.subplots()
seasonal_trends.plot(kind='bar', color='skyblue', ax=ax)
plt.xticks(rotation=0)
plt.title('Tingkatan PM2.5 per Bulan')
plt.xlabel('Bulan')
plt.ylabel('Tingkatan PM2.5')
st.pyplot(fig)

# Heatmap
st.subheader('Heatmap Interaktif')
selected_columns = st.multiselect('Pilih kolom korelasi yang dikehendaki', data.columns, default=['PM2.5', 'NO2', 'TEMP', 'PRES', 'DEWP'])
corr = data[selected_columns].corr()
fig, ax = plt.subplots()
sns.heatmap(corr, annot=True, ax=ax)
st.pyplot(fig)

# Dekomposisi Time-series PM2.5
st.subheader('Dekomposisi Time-series PM2.5')
try:
    data_filtered['PM2.5'].ffill(inplace=True)
    decomposed = seasonal_decompose(data_filtered['PM2.5'], model='additive', period=24) # Adjust period as necessary
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 8))
    decomposed.trend.plot(ax=ax1, title='Dinamika')
    decomposed.seasonal.plot(ax=ax2, title='Seasonality')
    decomposed.resid.plot(ax=ax3, title='Residuals')
    plt.tight_layout()
    st.pyplot(fig)
except ValueError as e:
    st.error("Unable to perform time series decomposition: " + str(e))

# Analisis Arah Angin
st.subheader('Analisis Arah Angin')
wind_data = data_filtered.groupby('wd')['PM2.5'].mean()
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, polar=True)
theta = np.linspace(0, 2 * np.pi, len(wind_data))
bars = ax.bar(theta, wind_data.values, align='center', alpha=0.5)
plt.title('Tingkatan PM2.5 berdasarkan Arah Angin')
st.pyplot(fig)

# Rainfall
st.subheader('Rainfall vs. Tingkatan PM2.5')
fig, ax = plt.subplots()
sns.scatterplot(x='RAIN', y='PM2.5', data=data_filtered, ax=ax)
plt.title('Rainfall vs. Tingkatan PM2.5')
st.pyplot(fig)

# Conclusion
st.subheader('Conclusion')
st.write("""
- Dashboard Air Quality: Stasiun Wainlu menyediakan analisis mendalam dan interaktif perihal data kualitas udara di stasiun Wainlu
- Berbagai variasi visual data menawarkan insight perihal tingkat PM2.5 dan faktor yang mempengaruhinya
- Dinamika musiman dan dampak dari kondisi cuaca dan polusi terhadap kualitas udara digambarkan dengan jelas
- Pengguna dapat eksplorasi data secara dinamis untuk memperoleh insight mendalam perihal dinamika kualitas udara
""")