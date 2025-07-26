import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Türkçe karakter desteği için
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

print("=== MAAŞ ANALİZİ BAŞLATILIYOR ===")
print("Veri setleri yükleniyor...")

# Veri setlerini yükle
try:
    salary_data = pd.read_csv('salary_data.csv')
    salary_detailed = pd.read_csv('Salary.csv')
    print("✓ Veri setleri başarıyla yüklendi")
except Exception as e:
    print(f"❌ Veri yükleme hatası: {e}")
    exit()

print("\n=== VERİ SETİ YAPILARI ===")
print("\n1. salary_data.csv yapısı:")
print(salary_data.info())
print("\nİlk 5 satır:")
print(salary_data.head())

print("\n2. Salary.csv yapısı:")
print(salary_detailed.info())
print("\nİlk 5 satır:")
print(salary_detailed.head())

print("\n=== VERİ KEŞFİ ===")
print(f"\nSalary.csv'deki ülkeler: {salary_detailed['Country'].unique()}")
print(f"Salary.csv'deki meslek sayısı: {salary_detailed['Job Title'].nunique()}")
print(f"Salary.csv'deki toplam kayıt sayısı: {len(salary_detailed)}")

print("\n=== BÖLGE SINIFLANDIRMASI ===")
# Bölge sınıflandırması
def classify_region(country):
    if country == 'Turkey':
        return 'TR'
    elif country in ['UK', 'Germany', 'France', 'Italy', 'Spain', 'Netherlands', 'Belgium', 'Austria', 'Sweden', 'Denmark', 'Norway', 'Finland', 'Switzerland']:
        return 'EU'
    elif country in ['USA', 'Canada']:
        return 'US'
    else:
        return 'Other'

# Salary.csv'ye bölge sütunu ekle
salary_detailed['Region'] = salary_detailed['Country'].apply(classify_region)

print("Bölge dağılımı:")
print(salary_detailed['Region'].value_counts())

print("\n=== MESLEK NORMALİZASYONU ===")
# Meslek unvanlarını normalize et
def normalize_job_title(title):
    title = str(title).lower().strip()
    
    # Software Engineer varyasyonları
    if any(keyword in title for keyword in ['software engineer', 'software developer', 'developer']):
        return 'Software Engineer'
    
    # Data Scientist varyasyonları
    if any(keyword in title for keyword in ['data scientist', 'data analyst']):
        return 'Data Scientist'
    
    # Product Manager varyasyonları
    if any(keyword in title for keyword in ['product manager', 'product development manager']):
        return 'Product Manager'
    
    # Marketing varyasyonları
    if any(keyword in title for keyword in ['marketing manager', 'marketing analyst', 'marketing coordinator', 'marketing specialist']):
        return 'Marketing Manager'
    
    # Project Manager varyasyonları
    if any(keyword in title for keyword in ['project manager', 'project coordinator']):
        return 'Project Manager'
    
    # Financial varyasyonları
    if any(keyword in title for keyword in ['financial analyst', 'financial manager', 'financial advisor']):
        return 'Financial Analyst'
    
    # HR varyasyonları
    if any(keyword in title for keyword in ['hr manager', 'hr generalist', 'human resources']):
        return 'HR Manager'
    
    # Sales varyasyonları
    if any(keyword in title for keyword in ['sales manager', 'sales representative', 'sales associate']):
        return 'Sales Manager'
    
    # Operations varyasyonları
    if any(keyword in title for keyword in ['operations manager', 'operations analyst']):
        return 'Operations Manager'
    
    # Business Analyst varyasyonları
    if any(keyword in title for keyword in ['business analyst', 'business intelligence analyst']):
        return 'Business Analyst'
    
    return title.title()

salary_detailed['Normalized_Job_Title'] = salary_detailed['Job Title'].apply(normalize_job_title)

print("En yaygın meslekler:")
print(salary_detailed['Normalized_Job_Title'].value_counts().head(10))

print("\n=== PARA BİRİMİ STANDARDİZASYONU ===")
# 2023 yılı ortalama kurları (yaklaşık değerler)
# Bu değerler gerçek analizde güvenilir kaynaklardan alınmalıdır
EXCHANGE_RATES = {
    'TRY': 1/30.0,  # 1 USD = 30 TRY (2023 ortalama)
    'EUR': 1.08,    # 1 EUR = 1.08 USD (2023 ortalama)
    'GBP': 1.27,    # 1 GBP = 1.27 USD (2023 ortalama)
    'USD': 1.0      # Baz para birimi
}

# Salary.csv'deki maaşları USD'ye çevir
# Bu veri setinde maaşlar zaten USD cinsinden görünüyor
salary_detailed['SalaryInUSD'] = salary_detailed['Salary']

# salary_data.csv'deki maaşları USD'ye çevir
# Bu veri setinde maaşlar muhtemelen yerel para biriminde
# Türkiye için TRY, diğer ülkeler için EUR/GBP varsayımı
def convert_to_usd(row):
    country = row['country_name']
    median_salary = row['median_salary']
    
    if country == 'Turkey':
        return median_salary * EXCHANGE_RATES['TRY']
    elif country in ['UK', 'Ireland']:
        return median_salary * EXCHANGE_RATES['GBP']
    else:
        return median_salary * EXCHANGE_RATES['EUR']

salary_data['SalaryInUSD'] = salary_data.apply(convert_to_usd, axis=1)

print("Para birimi dönüşümü tamamlandı")

print("\n=== ORTAK MESLEK ANALİZİ ===")
# TR, EU, US bölgelerindeki ortak meslekleri bul
tr_jobs = set(salary_detailed[salary_detailed['Region'] == 'TR']['Normalized_Job_Title'].unique())
eu_jobs = set(salary_detailed[salary_detailed['Region'] == 'EU']['Normalized_Job_Title'].unique())
us_jobs = set(salary_detailed[salary_detailed['Region'] == 'US']['Normalized_Job_Title'].unique())

common_jobs_tr_eu = tr_jobs.intersection(eu_jobs)
common_jobs_tr_us = tr_jobs.intersection(us_jobs)
common_jobs_eu_us = eu_jobs.intersection(us_jobs)
common_jobs_all = tr_jobs.intersection(eu_jobs).intersection(us_jobs)

print(f"TR-EU ortak meslekler: {len(common_jobs_tr_eu)}")
print(f"TR-US ortak meslekler: {len(common_jobs_tr_us)}")
print(f"EU-US ortak meslekler: {len(common_jobs_eu_us)}")
print(f"Tüm bölgelerde ortak meslekler: {len(common_jobs_all)}")

if len(common_jobs_all) > 0:
    print(f"Ortak meslekler: {list(common_jobs_all)}")

print("\n=== ANALİZ HAZIRLIK ===")
print("Veri setleri analiz için hazırlandı.")
print("Bir sonraki adımda detaylı karşılaştırmalı analizler yapılacak.")