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

# about
st.markdown("""
### Tentang saya
- **Name**: Rizqi Hasanuddin
- **Email Address**: rizqih6x@gmail.com
- **Dicoding ID**: [rzqh00](https://www.dicoding.com/users/rzqh00/)
""")

# project overview
st.markdown("""
### Project Overview
Dashboard ini menyajikan analisa data kualitas udara, terutama pada tingkat PM2.5 dari stasiun Wanliu. Project ini bertujuan untuk mengungkap berbagai insight seperti dinamika, variasi musiman dan dampak berbagai kondisi cuaca terhadap kualitas udara. Insight dari analisis ini dapat bermanfaat untuk studi lingkungan dan pemantauan kesehatan pasyarakat
""")

# pertanyaan analisis
st.markdown("""
### Pertanyaan Analisis
1. Apakah ada korelasi antara kadar PM2.5 dengan berbagai kondisi cuaca serta berbagai polutan udara lainnya (PM10 & CO) di Stasiun Wanliu dalam kurun tahun 2013 hingga 2017?
2. Bagaimana tren atau pola kadar PM2.5 setiap tahunnya di Stasiun Wanliu dari tahun 2013 hingga 2017?        
""")

# sidebar untuk fitur slicer 
st.sidebar.header('Fitur slicer')

default_year = 2015
default_month = 6
years = list(data['year'].unique())
months = list(data['month'].unique())
default_year_index = years.index(default_year)
default_month_index = months.index(default_month)
selected_year = st.sidebar.selectbox('Tahun', years, index=default_year_index)
selected_month = st.sidebar.selectbox('Bulan', months, index=default_month_index)

# filter data based on tahun dan bulan
data_filtered = data[(data['year'] == selected_year) & (data['month'] == selected_month)].copy()

# matrix data stats
st.subheader('Data Overview')
st.write(data.describe())

st.subheader('Grafik Wajib')

# Heatmap
st.subheader('Heatmap Korelasi Interaktif')
selected_columns = st.multiselect('Pilih kolom korelasi yang dikehendaki', data.columns, default=['PM2.5', 'PM10', 'CO', 'O3', 'TEMP', 'PRES', 'RAIN'])
corr = data[selected_columns].corr()
fig, ax = plt.subplots()
sns.heatmap(corr, annot=True, ax=ax)
st.pyplot(fig)

# pm2.5 dan pm10 time series
st.subheader('Tingkatan Rata-Rata PM2.5 dan PM10 per Tahun')
annual_data = data.groupby('year')[['PM2.5', 'PM10']].mean()
fig, ax = plt.subplots()
ax.plot(annual_data.index, annual_data['PM2.5'], label='PM2.5', color='blue')
ax.plot(annual_data.index, annual_data['PM10'], label='PM10', color='green')
ax.axvline(x=annual_data.index[int(len(annual_data) / 2)], color='gray', linestyle='--', linewidth=0.5)
plt.xlabel('Tahun')
plt.ylabel('Rata-Rata Tingkatan PM')
plt.legend()
st.pyplot(fig)

# Conclusion
st.subheader('Kesimpulan')
st.write("""
1. Berdasarkan korelasi negatif antara tingkatan PM2.5 dengan tingkatan suhu, menunjukkan tingkat polusi yang lebih tinggi pada cuaca yang lebih dingin. Lalu ditemukan pula korelasi positif dengan kadar PM10 dan CO yang ternyata saling berhubungan karena bersumber dari beberapa emisi yang sama.
2. Line chart Tingkatan Rata-Rata PM2.5 dan PM10 per tahun menunjukkan tren antara PM2.5 dan PM10 pada 2013-2017. 
        Berdasarkan line chart tersebut dapat disimpulkan terdapat pola tren yang selaras beriringan dari 2015-2017
         
Dari kedua kesimpulan tersebut dapat ditarik garis besar bahwasannya korelasi positif antara kadar PM2.5 dengan kadar PM10 disertai dinamikanya yang kian meningkat pada suhu yang lebih rendah, maka dari itu perlu pengembangan strategi pengendalian polusi yang efektif untuk melindungi kesehatan masyarakat
""")

st.divider()

# pertanyaan tambahan
st.subheader('Pertanyaan Tambahan')
st.write("""
1. Bagaimana lonjakan PM2.5 pada bulan Juni serta pada bulan selanjutnya pada tahun 2015 di Stasiun Wanliu?
2. Bagaimana pola curah hujan pada tahun 2015 yang mempengaruhi fluktuasi PM2.5 dalam kurun waktu setiap bulan di Stasiun Wanliu?
""")

st.subheader("Grafik Interaktif Tambahan dengan Fitur Slicer")

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

# Rainfall
st.subheader('Rainfall vs Tingkatan PM2.5')
fig, ax = plt.subplots()
sns.scatterplot(x='RAIN', y='PM2.5', data=data_filtered, ax=ax)
plt.title('Rainfall vs Tingkatan PM2.5')
st.pyplot(fig)

# Conclusion
st.subheader('Kesimpulan Tambahan')
st.write("""
1. Pada Juni 2015, tingkatan PM2.5 mengalami fluktuasi dari tanggal 1-20 yang kemudian mengalami pelonjakan yang sangat pesat hingga tanggal 29
         Lalu pada bulan selanjutnya di tahun 2015, tingkatan PM2.5 cenderung rendah pada musim kemarau dan mengalami pelonjakan saat musim hujan yang dapat disimpulkan bahwa pelonjakan PM2.5 beriringan dengan suhu dingin pada musim hujan
3. Meski tingkatan PM2.5 cenderung tinggi pada cuaca yang lebih dingin, ternyata berdasarkan grafik Rainfall vs Tingkatan PM2.5 menunjukkan bahwa dengan curah hujan yang tinggi maka dapat menurunkan tingkatan PM2.5
""")