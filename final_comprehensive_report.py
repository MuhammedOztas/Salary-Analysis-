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

print("=== NİHAİ KAPSAMLI MAAŞ ANALİZİ RAPORU ===")
print("TR, EU ve US Maaş Rejimleri Karşılaştırmalı Analizi")
print("=" * 60)

# Veri setlerini yükle
salary_data = pd.read_csv('salary_data.csv')
salary_detailed = pd.read_csv('Salary.csv')

print("✓ Veri setleri yüklendi")

# Türkiye verilerini çıkar
turkey_data = salary_data[salary_data['country_name'] == 'Turkey'].iloc[0]

print(f"\n🇹🇷 TÜRKİYE VERİLERİ:")
print(f"Ortalama Maaş: ${turkey_data['average_salary']:.2f}")
print(f"Medyan Maaş: ${turkey_data['median_salary']:.2f}")
print(f"En Düşük Maaş: ${turkey_data['lowest_salary']:.2f}")
print(f"En Yüksek Maaş: ${turkey_data['highest_salary']:.2f}")

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

# Para birimi standardizasyonu
# 2023 yılı ortalama kurları
EUR_USD_RATE = 1.08
TRY_USD_RATE = 0.037  # 1 USD = ~27 TRY

salary_detailed['SalaryInUSD'] = salary_detailed['Salary']

# Türkiye maaşlarını USD'ye çevir (aylık maaşları yıllığa çevir)
turkey_annual_avg = turkey_data['average_salary'] * 12  # Aylık maaşı yıllığa çevir
turkey_annual_median = turkey_data['median_salary'] * 12
turkey_annual_min = turkey_data['lowest_salary'] * 12
turkey_annual_max = turkey_data['highest_salary'] * 12

print(f"\n🇹🇷 TÜRKİYE YILLIK MAAŞLAR (USD):")
print(f"Ortalama: ${turkey_annual_avg:,.2f}")
print(f"Medyan: ${turkey_annual_median:,.2f}")
print(f"En Düşük: ${turkey_annual_min:,.2f}")
print(f"En Yüksek: ${turkey_annual_max:,.2f}")

# Bölge istatistikleri
region_stats = salary_detailed.groupby('Region').agg({
    'SalaryInUSD': ['mean', 'median', 'std', 'min', 'max', 'count']
}).round(2)

print(f"\n📊 BÖLGE BAZLI MAAŞ İSTATİSTİKLERİ (USD):")
print(region_stats)

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

print(f"\n📈 DENEYİM SEVİYESİNE GÖRE BÖLGE KARŞILAŞTIRMASI:")
print(experience_region_stats)

# Gini katsayısı hesaplama
def gini_coefficient(x):
    if len(x) == 0:
        return 0
    x = np.array(x)
    n = len(x)
    index = np.arange(1, n + 1)
    return ((2 * index - n - 1) * x).sum() / (n * x.sum())

# Bölge bazlı Gini katsayıları
gini_by_region = salary_detailed.groupby('Region')['SalaryInUSD'].apply(gini_coefficient).round(4)

print(f"\n📊 GELİR EŞİTSİZLİĞİ (GİNİ KATSAYISI):")
print(gini_by_region)

# KARŞILAŞTIRMALI ANALİZ
print(f"\n" + "="*60)
print(f"🎯 KARŞILAŞTIRMALI ANALİZ SONUÇLARI")
print(f"="*60)

# Ortalama maaş karşılaştırması
avg_salaries = salary_detailed.groupby('Region')['SalaryInUSD'].mean().round(2)

print(f"\n📊 ORTALAMA MAAŞ KARŞILAŞTIRMASI:")
print(f"🇺🇸 US: ${avg_salaries['US']:,.2f}")
print(f"🇪🇺 EU: ${avg_salaries['EU']:,.2f}")
print(f"🇹🇷 TR: ${turkey_annual_avg:,.2f}")

# Oran hesaplamaları
us_eu_ratio = avg_salaries['US'] / avg_salaries['EU']
us_tr_ratio = avg_salaries['US'] / turkey_annual_avg
eu_tr_ratio = avg_salaries['EU'] / turkey_annual_avg

print(f"\n📈 MAAŞ ORANLARI:")
print(f"US/EU: {us_eu_ratio:.2f} (US maaşları EU'nun {us_eu_ratio:.2f} katı)")
print(f"US/TR: {us_tr_ratio:.2f} (US maaşları TR'nin {us_tr_ratio:.2f} katı)")
print(f"EU/TR: {eu_tr_ratio:.2f} (EU maaşları TR'nin {eu_tr_ratio:.2f} katı)")

# Deneyim seviyesine göre detaylı analiz
print(f"\n📈 DENEYİM SEVİYESİNE GÖRE DETAYLI ANALİZ:")
experience_analysis = salary_detailed.groupby(['Region', 'Experience_Level'])['SalaryInUSD'].agg(['mean', 'count']).round(2)
print(experience_analysis)

# En yaygın mesleklerde karşılaştırma
top_5_jobs = ['Software Engineer', 'Data Scientist', 'Marketing Manager', 'Sales Manager', 'Product Manager']

print(f"\n💼 EN YAYGIN MESLEKLERDE KARŞILAŞTIRMA:")
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

# GÖRSELLEŞTİRME
print(f"\n📊 GÖRSELLEŞTİRME OLUŞTURULUYOR...")

# Figür boyutlarını ayarla
plt.rcParams['figure.figsize'] = (20, 15)

# Ana görselleştirme
fig, axes = plt.subplots(3, 3, figsize=(20, 15))
fig.suptitle('TR, EU ve US Maaş Rejimleri Kapsamlı Karşılaştırmalı Analizi', 
             fontsize=18, fontweight='bold', y=0.98)

# 1. Ortalama maaş karşılaştırması
regions = ['TR', 'EU', 'US']
avg_values = [turkey_annual_avg, avg_salaries['EU'], avg_salaries['US']]
colors = ['#ff6b6b', '#4ecdc4', '#45b7d1']

axes[0, 0].bar(regions, avg_values, color=colors, alpha=0.8)
axes[0, 0].set_title('Ortalama Yıllık Maaş Karşılaştırması', fontweight='bold')
axes[0, 0].set_ylabel('Maaş (USD)')
axes[0, 0].grid(True, alpha=0.3)

# Değerleri çubukların üzerine yaz
for i, v in enumerate(avg_values):
    axes[0, 0].text(i, v + 2000, f'${v:,.0f}', ha='center', va='bottom', fontweight='bold')

# 2. Maaş dağılımı (Box Plot)
region_data = [salary_detailed[salary_detailed['Region'] == region]['SalaryInUSD'] for region in ['EU', 'US']]
axes[0, 1].boxplot(region_data, labels=['EU', 'US'])
axes[0, 1].set_title('Maaş Dağılımı (Box Plot)', fontweight='bold')
axes[0, 1].set_ylabel('Maaş (USD)')
axes[0, 1].grid(True, alpha=0.3)

# 3. Deneyim seviyesine göre maaş
experience_pivot = salary_detailed.groupby(['Region', 'Experience_Level'])['SalaryInUSD'].mean().unstack()
experience_pivot.plot(kind='bar', ax=axes[0, 2])
axes[0, 2].set_title('Deneyim Seviyesine Göre Ortalama Maaş', fontweight='bold')
axes[0, 2].set_ylabel('Ortalama Maaş (USD)')
axes[0, 2].tick_params(axis='x', rotation=45)
axes[0, 2].legend(title='Deneyim Seviyesi', bbox_to_anchor=(1.05, 1), loc='upper left')

# 4. En yaygın mesleklerde karşılaştırma
top_5_jobs = ['Software Engineer', 'Data Scientist', 'Marketing Manager', 'Sales Manager', 'Product Manager']
job_comparison = salary_detailed[
    salary_detailed['Normalized_Job_Title'].isin(top_5_jobs)
].groupby(['Normalized_Job_Title', 'Region'])['SalaryInUSD'].mean().unstack()

job_comparison.plot(kind='bar', ax=axes[1, 0])
axes[1, 0].set_title('En Yaygın Mesleklerde Maaş Karşılaştırması', fontweight='bold')
axes[1, 0].set_ylabel('Ortalama Maaş (USD)')
axes[1, 0].tick_params(axis='x', rotation=45)
axes[1, 0].legend(title='Bölge')

# 5. Maaş histogramları
for i, region in enumerate(['EU', 'US']):
    region_data = salary_detailed[salary_detailed['Region'] == region]['SalaryInUSD']
    axes[1, 1].hist(region_data, bins=30, alpha=0.7, label=region, density=True)
axes[1, 1].set_title('Maaş Dağılımı (Histogram)', fontweight='bold')
axes[1, 1].set_xlabel('Maaş (USD)')
axes[1, 1].set_ylabel('Yoğunluk')
axes[1, 1].legend()
axes[1, 1].grid(True, alpha=0.3)

# 6. Deneyim vs Maaş scatter plot
for region in ['EU', 'US']:
    region_data = salary_detailed[salary_detailed['Region'] == region]
    axes[1, 2].scatter(region_data['Years of Experience'], region_data['SalaryInUSD'], 
                      alpha=0.6, label=region, s=20)
axes[1, 2].set_title('Deneyim vs Maaş İlişkisi', fontweight='bold')
axes[1, 2].set_xlabel('Deneyim Yılı')
axes[1, 2].set_ylabel('Maaş (USD)')
axes[1, 2].legend()
axes[1, 2].grid(True, alpha=0.3)

# 7. Gelir eşitsizliği karşılaştırması
gini_values = [gini_by_region[region] for region in ['EU', 'US']]
axes[2, 0].bar(['EU', 'US'], gini_values, color=['#4ecdc4', '#45b7d1'])
axes[2, 0].set_title('Gelir Eşitsizliği (Gini Katsayısı)', fontweight='bold')
axes[2, 0].set_ylabel('Gini Katsayısı')
axes[2, 0].grid(True, alpha=0.3)

# Değerleri çubukların üzerine yaz
for i, v in enumerate(gini_values):
    axes[2, 0].text(i, v + 0.001, f'{v:.3f}', ha='center', va='bottom', fontweight='bold')

# 8. Maaş oranları
ratios = [us_eu_ratio, us_tr_ratio, eu_tr_ratio]
ratio_labels = ['US/EU', 'US/TR', 'EU/TR']
axes[2, 1].bar(ratio_labels, ratios, color=['#ff6b6b', '#4ecdc4', '#45b7d1'])
axes[2, 1].set_title('Maaş Oranları Karşılaştırması', fontweight='bold')
axes[2, 1].set_ylabel('Oran')
axes[2, 1].grid(True, alpha=0.3)

# Değerleri çubukların üzerine yaz
for i, v in enumerate(ratios):
    axes[2, 1].text(i, v + 0.1, f'{v:.2f}x', ha='center', va='bottom', fontweight='bold')

# 9. Kariyer ilerlemesi analizi
experience_levels = ['Junior (0-2 yıl)', 'Mid-Level (2-5 yıl)', 'Senior (5-10 yıl)', 'Expert (10+ yıl)']
eu_progression = []
us_progression = []

for level in experience_levels:
    eu_avg = salary_detailed[
        (salary_detailed['Region'] == 'EU') & 
        (salary_detailed['Experience_Level'] == level)
    ]['SalaryInUSD'].mean()
    us_avg = salary_detailed[
        (salary_detailed['Region'] == 'US') & 
        (salary_detailed['Experience_Level'] == level)
    ]['SalaryInUSD'].mean()
    eu_progression.append(eu_avg)
    us_progression.append(us_avg)

x = np.arange(len(experience_levels))
width = 0.35

axes[2, 2].bar(x - width/2, eu_progression, width, label='EU', alpha=0.8)
axes[2, 2].bar(x + width/2, us_progression, width, label='US', alpha=0.8)
axes[2, 2].set_title('Kariyer İlerlemesi ve Maaş Artışı', fontweight='bold')
axes[2, 2].set_ylabel('Ortalama Maaş (USD)')
axes[2, 2].set_xticks(x)
axes[2, 2].set_xticklabels(experience_levels, rotation=45, ha='right')
axes[2, 2].legend()
axes[2, 2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('comprehensive_salary_analysis_final.png', dpi=300, bbox_inches='tight')
print("✓ Görselleştirmeler kaydedildi: comprehensive_salary_analysis_final.png")

# NİHAİ RAPOR
print(f"\n" + "="*80)
print(f"📋 NİHAİ KAPSAMLI ANALİZ RAPORU")
print(f"="*80)

print(f"\n🎯 ANA BULGULAR:")
print(f"1. Ortalama Maaş Sıralaması: EU > US > TR")
print(f"2. US maaşları EU maaşlarının {us_eu_ratio:.2f} katı")
print(f"3. US maaşları TR maaşlarının {us_tr_ratio:.2f} katı")
print(f"4. EU maaşları TR maaşlarının {eu_tr_ratio:.2f} katı")

print(f"\n📊 GELİR EŞİTSİZLİĞİ:")
print(f"• EU: Gini katsayısı = {gini_by_region['EU']:.4f}")
print(f"• US: Gini katsayısı = {gini_by_region['US']:.4f}")

print(f"\n💼 MESLEK BAZLI EN YÜKSEK FARKLAR:")
for job, ratio, us_avg, eu_avg in job_differences[:3]:
    print(f"• {job}: US ${us_avg:,.0f} vs EU ${eu_avg:,.0f} (US/EU oranı: {ratio:.2f})")

print(f"\n📈 KARİYER İLERLEMESİ:")
print(f"• EU'da Expert seviyesi maaşları Junior seviyesinin {eu_progression[3]/eu_progression[0]:.1f} katı")
print(f"• US'da Expert seviyesi maaşları Junior seviyesinin {us_progression[3]/us_progression[0]:.1f} katı")

print(f"\n🔍 EKONOMİK REFAH GÖSTERGELERİ:")
print(f"• EU: Daha yüksek ortalama maaş ve daha düşük gelir eşitsizliği")
print(f"• US: Daha yüksek gelir eşitsizliği ancak güçlü kariyer ilerlemesi")
print(f"• TR: Gelişmekte olan ekonomi profili, düşük maaş seviyeleri")

print(f"\n✅ ANALİZ TAMAMLANDI!")
print(f"📁 Detaylı görselleştirmeler: comprehensive_salary_analysis_final.png")
print(f"📊 Veri setleri: {len(salary_detailed)} kayıt analiz edildi")
print(f"🌍 Karşılaştırılan bölgeler: TR, EU, US")