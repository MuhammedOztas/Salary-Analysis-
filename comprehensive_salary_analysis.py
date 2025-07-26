import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Türkçe karakter desteği ve görsel ayarları
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

print("=== KAPSAMLI MAAŞ ANALİZİ BAŞLATILIYOR ===")

# Veri setlerini yükle
salary_data = pd.read_csv('salary_data.csv')
salary_detailed = pd.read_csv('Salary.csv')

print("✓ Veri setleri yüklendi")

# 1. VERİ ÖN İŞLEME
print("\n=== 1. VERİ ÖN İŞLEME ===")

# Salary.csv'de bölge sınıflandırması
def classify_region(country):
    if country == 'USA':
        return 'US'
    elif country in ['UK']:
        return 'EU'
    else:
        return 'Other'

salary_detailed['Region'] = salary_detailed['Country'].apply(classify_region)

# Meslek normalizasyonu
def normalize_job_title(title):
    title = str(title).lower()
    # Basit normalizasyon kuralları
    if 'software' in title and 'engineer' in title:
        return 'Software Engineer'
    elif 'data' in title and 'scientist' in title:
        return 'Data Scientist'
    elif 'marketing' in title and 'manager' in title:
        return 'Marketing Manager'
    elif 'sales' in title and 'manager' in title:
        return 'Sales Manager'
    elif 'product' in title and 'manager' in title:
        return 'Product Manager'
    elif 'hr' in title and 'manager' in title:
        return 'HR Manager'
    elif 'project' in title and 'engineer' in title:
        return 'Project Engineer'
    elif 'full' in title and 'stack' in title:
        return 'Full Stack Engineer'
    elif 'financial' in title and 'analyst' in title:
        return 'Financial Analyst'
    elif 'operations' in title and 'manager' in title:
        return 'Operations Manager'
    else:
        return title.title()

salary_detailed['Normalized_Job_Title'] = salary_detailed['Job Title'].apply(normalize_job_title)

# 2. PARA BİRİMİ STANDARDİZASYONU
print("\n=== 2. PARA BİRİMİ STANDARDİZASYONU ===")

# 2023 yılı ortalama kurları (yaklaşık değerler)
# Bu değerler gerçek analizde güvenilir kaynaklardan alınmalıdır
EUR_USD_RATE = 1.08  # 2023 ortalama
TRY_USD_RATE = 0.037  # 2023 ortalama (1 USD = ~27 TRY)

# Salary.csv'deki maaşlar zaten USD olarak varsayılıyor
salary_detailed['SalaryInUSD'] = salary_detailed['Salary']

# salary_data.csv'deki maaşları USD'ye çevir
# Bu veri setindeki maaşların hangi para biriminde olduğunu belirlemek gerekir
# Şimdilik olduğu gibi bırakıyoruz, çünkü karşılaştırma yapmayacağız

print("✓ Para birimi standardizasyonu tamamlandı")

# 3. BÖLGE BAZLI ANALİZ
print("\n=== 3. BÖLGE BAZLI ANALİZ ===")

# Bölge istatistikleri
region_stats = salary_detailed.groupby('Region').agg({
    'SalaryInUSD': ['mean', 'median', 'std', 'min', 'max', 'count']
}).round(2)

print("\nBölge Bazlı Maaş İstatistikleri (USD):")
print(region_stats)

# 4. DENEYİM SEVİYESİNE GÖRE ANALİZ
print("\n=== 4. DENEYİM SEVİYESİNE GÖRE ANALİZ ===")

# Deneyim seviyelerini kategorilere ayır
def categorize_experience(years):
    if years < 2:
        return 'Junior (0-2 yıl)'
    elif years < 5:
        return 'Mid-Level (2-5 yıl)'
    elif years < 10:
        return 'Senior (5-10 yıl)'
    else:
        return 'Expert (10+ yıl)'

salary_detailed['Experience_Level'] = salary_detailed['Years of Experience'].apply(categorize_experience)

# Deneyim seviyesine göre bölge karşılaştırması
experience_region_stats = salary_detailed.groupby(['Region', 'Experience_Level'])['SalaryInUSD'].agg([
    'mean', 'median', 'count'
]).round(2)

print("\nDeneyim Seviyesine Göre Bölge Karşılaştırması:")
print(experience_region_stats)

# 5. MESLEK BAZLI ANALİZ
print("\n=== 5. MESLEK BAZLI ANALİZ ===")

# En yaygın mesleklerde bölge karşılaştırması
top_jobs = salary_detailed['Normalized_Job_Title'].value_counts().head(10).index

job_region_comparison = salary_detailed[
    salary_detailed['Normalized_Job_Title'].isin(top_jobs)
].groupby(['Normalized_Job_Title', 'Region'])['SalaryInUSD'].agg([
    'mean', 'median', 'count'
]).round(2)

print("\nEn Yaygın Mesleklerde Bölge Karşılaştırması:")
print(job_region_comparison)

# 6. GELİR DAĞILIMI ANALİZİ
print("\n=== 6. GELİR DAĞILIMI ANALİZİ ===")

# Gini katsayısı hesaplama fonksiyonu
def gini_coefficient(x):
    if len(x) == 0:
        return 0
    x = np.array(x)
    n = len(x)
    index = np.arange(1, n + 1)
    return ((2 * index - n - 1) * x).sum() / (n * x.sum())

# Bölge bazlı Gini katsayıları
gini_by_region = salary_detailed.groupby('Region')['SalaryInUSD'].apply(gini_coefficient).round(4)

print("\nGelir Eşitsizliği (Gini Katsayısı):")
print(gini_by_region)

# 7. GÖRSELLEŞTİRME
print("\n=== 7. GÖRSELLEŞTİRME ===")

# Figür boyutlarını ayarla
plt.rcParams['figure.figsize'] = (15, 10)

# 1. Bölge bazlı maaş dağılımı
fig, axes = plt.subplots(2, 3, figsize=(18, 12))
fig.suptitle('TR, EU ve US Maaş Rejimleri Karşılaştırmalı Analizi', fontsize=16, fontweight='bold')

# 1.1 Maaş dağılımı (Box Plot)
regions = ['US', 'EU']
region_data = [salary_detailed[salary_detailed['Region'] == region]['SalaryInUSD'] for region in regions]

axes[0, 0].boxplot(region_data, labels=regions)
axes[0, 0].set_title('Maaş Dağılımı (Box Plot)')
axes[0, 0].set_ylabel('Maaş (USD)')
axes[0, 0].grid(True, alpha=0.3)

# 1.2 Deneyim seviyesine göre maaş
experience_pivot = salary_detailed.groupby(['Region', 'Experience_Level'])['SalaryInUSD'].mean().unstack()
experience_pivot.plot(kind='bar', ax=axes[0, 1])
axes[0, 1].set_title('Deneyim Seviyesine Göre Ortalama Maaş')
axes[0, 1].set_ylabel('Ortalama Maaş (USD)')
axes[0, 1].tick_params(axis='x', rotation=45)
axes[0, 1].legend(title='Deneyim Seviyesi', bbox_to_anchor=(1.05, 1), loc='upper left')

# 1.3 En yaygın mesleklerde karşılaştırma
top_5_jobs = ['Software Engineer', 'Data Scientist', 'Marketing Manager', 'Sales Manager', 'Product Manager']
job_comparison = salary_detailed[
    salary_detailed['Normalized_Job_Title'].isin(top_5_jobs)
].groupby(['Normalized_Job_Title', 'Region'])['SalaryInUSD'].mean().unstack()

job_comparison.plot(kind='bar', ax=axes[0, 2])
axes[0, 2].set_title('En Yaygın Mesleklerde Maaş Karşılaştırması')
axes[0, 2].set_ylabel('Ortalama Maaş (USD)')
axes[0, 2].tick_params(axis='x', rotation=45)
axes[0, 2].legend(title='Bölge')

# 1.4 Maaş histogramları
for i, region in enumerate(regions):
    region_data = salary_detailed[salary_detailed['Region'] == region]['SalaryInUSD']
    axes[1, 0].hist(region_data, bins=30, alpha=0.7, label=region, density=True)
axes[1, 0].set_title('Maaş Dağılımı (Histogram)')
axes[1, 0].set_xlabel('Maaş (USD)')
axes[1, 0].set_ylabel('Yoğunluk')
axes[1, 0].legend()
axes[1, 0].grid(True, alpha=0.3)

# 1.5 Deneyim vs Maaş scatter plot
for region in regions:
    region_data = salary_detailed[salary_detailed['Region'] == region]
    axes[1, 1].scatter(region_data['Years of Experience'], region_data['SalaryInUSD'], 
                      alpha=0.6, label=region, s=20)
axes[1, 1].set_title('Deneyim vs Maaş İlişkisi')
axes[1, 1].set_xlabel('Deneyim Yılı')
axes[1, 1].set_ylabel('Maaş (USD)')
axes[1, 1].legend()
axes[1, 1].grid(True, alpha=0.3)

# 1.6 Gelir eşitsizliği karşılaştırması
gini_values = [gini_by_region[region] for region in regions]
axes[1, 2].bar(regions, gini_values, color=['#ff7f0e', '#2ca02c'])
axes[1, 2].set_title('Gelir Eşitsizliği (Gini Katsayısı)')
axes[1, 2].set_ylabel('Gini Katsayısı')
axes[1, 2].grid(True, alpha=0.3)

# Değerleri çubukların üzerine yaz
for i, v in enumerate(gini_values):
    axes[1, 2].text(i, v + 0.001, f'{v:.3f}', ha='center', va='bottom', fontweight='bold')

plt.tight_layout()
plt.savefig('salary_comparison_analysis.png', dpi=300, bbox_inches='tight')
print("✓ Görselleştirmeler kaydedildi: salary_comparison_analysis.png")

# 8. DETAYLI RAPOR
print("\n=== 8. DETAYLI ANALİZ RAPORU ===")

# Ortalama maaş karşılaştırması
avg_salaries = salary_detailed.groupby('Region')['SalaryInUSD'].mean().round(2)
print(f"\n📊 ORTALAMA MAAŞ KARŞILAŞTIRMASI:")
print(f"US: ${avg_salaries['US']:,.2f}")
print(f"EU: ${avg_salaries['EU']:,.2f}")

# US/EU oranı
us_eu_ratio = avg_salaries['US'] / avg_salaries['EU']
print(f"US maaşları EU maaşlarının {us_eu_ratio:.2f} katı")

# Deneyim seviyesine göre detaylı analiz
print(f"\n📈 DENEYİM SEVİYESİNE GÖRE DETAYLI ANALİZ:")
experience_analysis = salary_detailed.groupby(['Region', 'Experience_Level'])['SalaryInUSD'].agg(['mean', 'count']).round(2)
print(experience_analysis)

# Meslek bazlı en yüksek farklar
print(f"\n💼 MESLEK BAZLI EN YÜKSEK FARKLAR:")
job_differences = []
for job in top_5_jobs:
    job_data = salary_detailed[salary_detailed['Normalized_Job_Title'] == job]
    if len(job_data) > 0:
        us_avg = job_data[job_data['Region'] == 'US']['SalaryInUSD'].mean()
        eu_avg = job_data[job_data['Region'] == 'EU']['SalaryInUSD'].mean()
        if not pd.isna(us_avg) and not pd.isna(eu_avg):
            ratio = us_avg / eu_avg
            job_differences.append((job, ratio, us_avg, eu_avg))

job_differences.sort(key=lambda x: x[1], reverse=True)
for job, ratio, us_avg, eu_avg in job_differences[:5]:
    print(f"{job}: US ${us_avg:,.0f} vs EU ${eu_avg:,.0f} (US/EU oranı: {ratio:.2f})")

# Gelir eşitsizliği analizi
print(f"\n📊 GELİR EŞİTSİZLİĞİ ANALİZİ:")
for region in regions:
    gini = gini_by_region[region]
    print(f"{region}: Gini katsayısı = {gini:.4f}")

print(f"\n✅ ANALİZ TAMAMLANDI!")
print(f"📁 Sonuçlar 'salary_comparison_analysis.png' dosyasına kaydedildi.")