# Proyek Analisis Data: Air Quality @Wanliu

## Live Dashboard
[Klik di sini!](https://rzqh-airquality-dicoding-submission.streamlit.app/)

## Project Overview
Dashboard ini menyajikan analisa data kualitas udara, terutama pada tingkat PM2.5 dari stasiun Wanliu. Project ini bertujuan untuk mengungkap berbagai insight seperti dinamika, variasi musiman dan dampak berbagai kondisi cuaca terhadap kualitas udara. Insight dari analisis ini dapat bermanfaat untuk studi lingkungan dan pemantauan kesehatan pasyarakat

## How to Run the Dashboard
Untuk menjalankan Air Quality Analysis Dashboard, ikuti step berikut:
### Setup Environment 
```
python -m venv venv-airquality
source venv-airquality/bin/activate # Jika menggunakan Mac/Linux
`venv-airquality/Scripts/activate # Jika menggunakana Windows

```

### Setup Environment - Shell/Terminal
```
pip install -r requirements.txt
```

### Run steamlit app
```
streamlit run dashboard/dashboard.py
```