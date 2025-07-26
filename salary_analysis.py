#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kapsamlı Uluslararası Maaş Analizi
TR, EU, US Bölgeleri Karşılaştırması
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import requests
import json
from datetime import datetime
import re

# Türkçe karakterler için encoding ayarı
import locale
import os
os.environ['LANG'] = 'en_US.UTF-8'

warnings.filterwarnings('ignore')

# Grafik ayarları
plt.style.use('seaborn-v0_8')
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10
sns.set_palette("husl")

class SalaryAnalyzer:
    def __init__(self):
        self.df_combined = None
        self.exchange_rates = {
            'TRY_USD': None,
            'EUR_USD': None,
            'data_year': None
        }
        
    def load_data(self):
        """Veri setlerini yükle ve temel bilgileri göster"""
        print("=== VERİ YÜKLEME VE KEŞİF AŞAMASI ===\n")
        
        # İlk veri seti
        try:
            df1 = pd.read_csv('salary_data.csv')
            print(f"salary_data.csv yüklendi: {df1.shape}")
            print("Sütunlar:", list(df1.columns))
            print("\nİlk 3 satır:")
            print(df1.head(3))
            print("\nVeri tipleri:")
            print(df1.dtypes)
            print("\nEksik veriler:")
            print(df1.isnull().sum())
            print("\n" + "="*80 + "\n")
        except Exception as e:
            print(f"salary_data.csv yüklenirken hata: {e}")
            df1 = pd.DataFrame()
        
        # İkinci veri seti
        try:
            df2 = pd.read_csv('Salary.csv')
            print(f"Salary.csv yüklendi: {df2.shape}")
            print("Sütunlar:", list(df2.columns))
            print("\nİlk 3 satır:")
            print(df2.head(3))
            print("\nVeri tipleri:")
            print(df2.dtypes)
            print("\nEksik veriler:")
            print(df2.isnull().sum())
            print("\n" + "="*80 + "\n")
        except Exception as e:
            print(f"Salary.csv yüklenirken hata: {e}")
            df2 = pd.DataFrame()
        
        return df1, df2
    
    def detect_data_year(self, df1, df2):
        """Verinin hangi yıla ait olduğunu tespit et"""
        print("=== VERİ YILI TESPİTİ ===\n")
        
        # Tarih sütunlarını ara
        date_columns = []
        for df, name in [(df1, 'salary_data.csv'), (df2, 'Salary.csv')]:
            if not df.empty:
                for col in df.columns:
                    if any(word in col.lower() for word in ['date', 'year', 'time', 'work_year']):
                        date_columns.append((name, col))
                        print(f"{name} - {col} sütunu bulundu:")
                        print(f"Örnek değerler: {df[col].dropna().unique()[:5]}")
        
        # Eğer tarih sütunu varsa yılı çıkar
        data_year = None
        if date_columns:
            for file_name, col in date_columns:
                df = df1 if file_name == 'salary_data.csv' else df2
                sample_values = df[col].dropna().unique()
                for val in sample_values:
                    if isinstance(val, (int, float)) and 2015 <= val <= 2024:
                        data_year = int(val)
                        break
                    elif isinstance(val, str):
                        # Tarih string'inden yıl çıkar
                        year_match = re.search(r'(20\d{2})', str(val))
                        if year_match:
                            data_year = int(year_match.group(1))
                            break
                if data_year:
                    break
        
        # Eğer bulamazsa 2023 varsayılan olsun
        if data_year is None:
            data_year = 2023
            print("Veri yılı otomatik tespit edilemedi. 2023 varsayıldı.")
        else:
            print(f"Veri yılı tespit edildi: {data_year}")
        
        self.exchange_rates['data_year'] = data_year
        print(f"\nAnaliz {data_year} yılı döviz kurları ile yapılacak.\n")
        return data_year
    
    def get_exchange_rates(self, year):
        """Belirtilen yıl için ortalama döviz kurlarını al"""
        print(f"=== {year} YILI DÖVİZ KURLARI ===\n")
        
        # Sabit kurlar (yıllık ortalamalar - gerçek veriler)
        historical_rates = {
            2020: {'TRY_USD': 7.01, 'EUR_USD': 1.14},
            2021: {'TRY_USD': 8.85, 'EUR_USD': 1.18},
            2022: {'TRY_USD': 16.55, 'EUR_USD': 1.05},
            2023: {'TRY_USD': 19.07, 'EUR_USD': 1.08},
            2024: {'TRY_USD': 32.20, 'EUR_USD': 1.09}
        }
        
        if year in historical_rates:
            rates = historical_rates[year]
            print(f"{year} yılı ortalama kurlar:")
            print(f"TRY/USD: {rates['TRY_USD']}")
            print(f"EUR/USD: {rates['EUR_USD']}")
        else:
            # Varsayılan kurlar
            rates = {'TRY_USD': 19.07, 'EUR_USD': 1.08}
            print(f"⚠️  {year} yılı için kur bulunamadı. 2023 kurları kullanılıyor:")
            print(f"TRY/USD: {rates['TRY_USD']}")
            print(f"EUR/USD: {rates['EUR_USD']}")
        
        self.exchange_rates.update(rates)
        print()
        return rates
    
    def preprocess_data(self, df1, df2):
        """Veri ön işleme ve birleştirme"""
        print("=== VERİ ÖN İŞLEME ===\n")
        
        combined_data = []
        
        # salary_data.csv işleme (Ülke bazında maaş verileri)
        if not df1.empty:
            print("salary_data.csv işleniyor...")
            df1_processed = df1.copy()
            
            # Bu veri seti ülke bazında genel maaş bilgileri içeriyor
            # Ortalama maaşı kullanacağız
            df1_processed['job_title'] = 'General Average'  # Genel ortalama
            df1_processed['salary_local'] = df1_processed['average_salary']
            df1_processed['experience_level'] = 'Unknown'
            df1_processed['location'] = df1_processed['country_name']
            
            # Bölge bilgisi ekle
            df1_processed['region'] = df1_processed['location'].apply(self.map_location_to_region)
            df1_processed['source'] = 'salary_data'
            
            # Sütun seçimi
            keep_cols = ['job_title', 'salary_local', 'experience_level', 'location', 'region', 'source']
            df1_processed = df1_processed[keep_cols]
            
            print(f"  İşlenen kayıt sayısı: {len(df1_processed)}")
            combined_data.append(df1_processed)
        
        # Salary.csv işleme (Detaylı bireysel maaş verileri)
        if not df2.empty:
            print("Salary.csv işleniyor...")
            df2_processed = df2.copy()
            
            # Sütun isimlerini standartlaştır
            df2_processed['job_title'] = df2_processed['Job Title']
            df2_processed['salary_local'] = df2_processed['Salary']
            df2_processed['location'] = df2_processed['Country']
            
            # Deneyim seviyesi - Years of Experience ve Senior bilgisini kullan
            def determine_experience(row):
                years = row['Years of Experience']
                is_senior = row['Senior']
                
                if is_senior == 1:
                    return 'Senior'
                elif years <= 2:
                    return 'Entry Level'
                elif years <= 5:
                    return 'Mid Level'
                else:
                    return 'Senior'
            
            df2_processed['experience_level'] = df2_processed.apply(determine_experience, axis=1)
            
            # Bölge bilgisi ekle
            df2_processed['region'] = df2_processed['location'].apply(self.map_location_to_region)
            df2_processed['source'] = 'Salary'
            
            # Sütun seçimi
            keep_cols = ['job_title', 'salary_local', 'experience_level', 'location', 'region', 'source']
            df2_processed = df2_processed[keep_cols]
            
            print(f"  İşlenen kayıt sayısı: {len(df2_processed)}")
            combined_data.append(df2_processed)
        
        # Veri setlerini birleştir
        if combined_data:
            self.df_combined = pd.concat(combined_data, ignore_index=True)
            print(f"\nBirleştirilmiş veri seti: {self.df_combined.shape}")
            print("Bölge dağılımı:")
            print(self.df_combined['region'].value_counts())
            print("\nKaynak dağılımı:")
            print(self.df_combined['source'].value_counts())
        else:
            print("❌ Hiçbir veri seti işlenemedi!")
            return None
        
        return self.df_combined
    
    def map_location_to_region(self, location):
        """Konum bilgisini bölgeye eşle"""
        if pd.isna(location):
            return 'Unknown'
        
        location_str = str(location).upper()
        
        # Türkiye
        turkey_codes = ['TR', 'TUR', 'TURKEY', 'TÜRKİYE', 'TURKIYE']
        if any(code in location_str for code in turkey_codes):
            return 'TR'
        
        # ABD
        us_codes = ['US', 'USA', 'UNITED STATES', 'AMERICA', 'CALIFORNIA', 'NEW YORK', 'TEXAS', 'FLORIDA']
        if any(code in location_str for code in us_codes):
            return 'US'
        
        # AB ülkeleri
        eu_codes = ['DE', 'FR', 'IT', 'ES', 'NL', 'BE', 'AT', 'PT', 'IE', 'GR', 'FI', 'DK', 'SE', 
                   'GERMANY', 'FRANCE', 'ITALY', 'SPAIN', 'NETHERLANDS', 'BELGIUM', 'AUSTRIA',
                   'PORTUGAL', 'IRELAND', 'GREECE', 'FINLAND', 'DENMARK', 'SWEDEN', 'EU', 'EUR']
        if any(code in location_str for code in eu_codes):
            return 'EU'
        
        return 'Other'
    
    def convert_to_usd(self, df):
        """Tüm maaşları USD'ye çevir"""
        print("=== MAAŞ STANDARDIZASYONU (USD) ===\n")
        
        # salary_local sütunundaki maaşları bölgeye göre USD'ye çevir
        if 'salary_local' in df.columns:
            df['SalaryInUSD'] = df.apply(self.estimate_and_convert_currency, axis=1)
            print("Yerel para birimleri bölgeye göre USD'ye çevrildi")
        else:
            print("❌ Maaş verisi bulunamadı!")
            return df
        
        # Eksik USD değerleri varsa temizle
        initial_count = len(df)
        df = df.dropna(subset=['SalaryInUSD'])
        df = df[df['SalaryInUSD'] > 0]
        final_count = len(df)
        
        print(f"Maaş verisi olan kayıt sayısı: {initial_count} → {final_count}")
        
        if final_count > 0:
            print(f"USD Maaş İstatistikleri:")
            print(f"Ortalama: ${df['SalaryInUSD'].mean():,.0f}")
            print(f"Medyan: ${df['SalaryInUSD'].median():,.0f}")
            print(f"Min: ${df['SalaryInUSD'].min():,.0f}")
            print(f"Max: ${df['SalaryInUSD'].max():,.0f}")
        print()
        
        return df
    
    def convert_currency_to_usd(self, row):
        """Satır bazında para birimi çevirisi"""
        if pd.isna(row['salary_local']):
            return np.nan
        
        salary = float(row['salary_local'])
        currency = str(row.get('currency', '')).upper()
        
        if currency in ['USD', 'US', 'DOLLAR']:
            return salary
        elif currency in ['EUR', 'EURO']:
            return salary * self.exchange_rates['EUR_USD']
        elif currency in ['TRY', 'TL', 'LIRA']:
            return salary / self.exchange_rates['TRY_USD']
        else:
            # Bilinmeyen para birimi - bölgeye göre tahmin et
            return self.estimate_and_convert_currency(row)
    
    def estimate_and_convert_currency(self, row):
        """Bölgeye göre para birimi tahmin et ve çevir"""
        if pd.isna(row['salary_local']):
            return np.nan
        
        salary = float(row['salary_local'])
        region = row.get('region', 'Unknown')
        location = str(row.get('location', '')).upper()
        
        # Bölgeye göre para birimi tahmin et ve çevir
        if region == 'US':
            return salary  # USD varsayımı
        elif region == 'EU':
            return salary * self.exchange_rates['EUR_USD']  # EUR varsayımı
        elif region == 'TR':
            return salary / self.exchange_rates['TRY_USD']  # TRY varsayımı
        elif 'UK' in location or 'BRITAIN' in location:
            # İngiltere için GBP varsayımı (yaklaşık 1.27 GBP/USD 2023)
            return salary * 1.27
        elif 'CANADA' in location:
            # Kanada için CAD varsayımı (yaklaşık 0.74 CAD/USD 2023)
            return salary * 0.74
        elif 'AUSTRALIA' in location:
            # Avustralya için AUD varsayımı (yaklaşık 0.67 AUD/USD 2023)
            return salary * 0.67
        else:
            return salary  # USD varsayımı
    
    def normalize_job_titles(self, df):
        """Meslek unvanlarını normalize et"""
        print("=== MESLEK UNVANLARI NORMALİZASYONU ===\n")
        
        if 'job_title' not in df.columns:
            print("❌ job_title sütunu bulunamadı!")
            return df
        
        # Normalizasyon kuralları
        normalization_rules = {
            # Senior Software Engineer varyasyonları
            r'senior\s+software\s+engineer': 'Senior Software Engineer',
            r'sr\.?\s+software\s+engineer': 'Senior Software Engineer',
            r'senior\s+software\s+developer': 'Senior Software Engineer',
            
            # Data Scientist varyasyonları
            r'data\s+scientist': 'Data Scientist',
            r'senior\s+data\s+scientist': 'Senior Data Scientist',
            r'sr\.?\s+data\s+scientist': 'Senior Data Scientist',
            
            # Software Engineer varyasyonları
            r'software\s+engineer': 'Software Engineer',
            r'software\s+developer': 'Software Engineer',
            
            # Data Engineer varyasyonları
            r'data\s+engineer': 'Data Engineer',
            r'senior\s+data\s+engineer': 'Senior Data Engineer',
            
            # Product Manager varyasyonları
            r'product\s+manager': 'Product Manager',
            r'senior\s+product\s+manager': 'Senior Product Manager',
            
            # Machine Learning Engineer varyasyonları
            r'machine\s+learning\s+engineer': 'Machine Learning Engineer',
            r'ml\s+engineer': 'Machine Learning Engineer',
        }
        
        df['job_title_normalized'] = df['job_title'].copy()
        
        for pattern, replacement in normalization_rules.items():
            mask = df['job_title_normalized'].str.contains(pattern, case=False, na=False, regex=True)
            df.loc[mask, 'job_title_normalized'] = replacement
        
        print("En yaygın meslek unvanları (normalize edilmiş):")
        top_jobs = df['job_title_normalized'].value_counts().head(10)
        for job, count in top_jobs.items():
            print(f"  {job}: {count}")
        print()
        
        return df
    
    def normalize_experience_levels(self, df):
        """Deneyim seviyelerini normalize et"""
        print("=== DENEYİM SEVİYELERİ NORMALİZASYONU ===\n")
        
        if 'experience_level' not in df.columns:
            print("❌ experience_level sütunu bulunamadı!")
            df['experience_level_normalized'] = 'Unknown'
            return df
        
        def normalize_experience(exp):
            if pd.isna(exp):
                return 'Unknown'
            
            exp_str = str(exp).lower().strip()
            
            # Entry Level / Junior
            if any(word in exp_str for word in ['entry', 'junior', 'jr', 'beginner', 'new grad', 'en', '0-2']):
                return 'Entry Level'
            
            # Senior
            elif any(word in exp_str for word in ['senior', 'sr', 'lead', 'principal', 'se', '5+']):
                return 'Senior'
            
            # Mid Level
            elif any(word in exp_str for word in ['mid', 'intermediate', 'regular', 'mi', '2-5']):
                return 'Mid Level'
            
            # Executive
            elif any(word in exp_str for word in ['executive', 'director', 'vp', 'ex', 'chief', 'head']):
                return 'Executive'
            
            # Sayısal deneyim yılları
            elif exp_str.isdigit():
                years = int(exp_str)
                if years <= 2:
                    return 'Entry Level'
                elif years <= 5:
                    return 'Mid Level'
                else:
                    return 'Senior'
            
            else:
                return 'Unknown'
        
        df['experience_level_normalized'] = df['experience_level'].apply(normalize_experience)
        
        print("Deneyim seviyesi dağılımı:")
        exp_dist = df['experience_level_normalized'].value_counts()
        for level, count in exp_dist.items():
            print(f"  {level}: {count}")
        print()
        
        return df
    
    def perform_regional_analysis(self):
        """Bölgesel analiz gerçekleştir"""
        print("=== BÖLGESEL MAAŞ ANALİZİ ===\n")
        
        df = self.df_combined
        
        # TR, EU, US filtresi
        target_regions = ['TR', 'EU', 'US']
        df_filtered = df[df['region'].isin(target_regions)].copy()
        
        if len(df_filtered) == 0:
            print("❌ TR, EU, US bölgelerinde veri bulunamadı!")
            return None
        
        print(f"Analiz edilen toplam kayıt: {len(df_filtered)}")
        print("Bölge bazında kayıt sayıları:")
        for region in target_regions:
            count = len(df_filtered[df_filtered['region'] == region])
            print(f"  {region}: {count}")
        print()
        
        # Genel istatistikler
        print("GENEL MAAŞ İSTATİSTİKLERİ (USD):")
        print("="*50)
        
        region_stats = df_filtered.groupby('region')['SalaryInUSD'].agg([
            'count', 'mean', 'median', 'std', 'min', 'max'
        ]).round(0)
        
        print(region_stats)
        print()
        
        # Ortak meslekleri bul
        common_jobs = self.find_common_jobs(df_filtered, target_regions)
        print(f"Ortak meslekler ({len(common_jobs)} adet):")
        for job in common_jobs:
            print(f"  - {job}")
        print()
        
        return df_filtered, common_jobs
    
    def find_common_jobs(self, df, regions):
        """Bölgeler arasında ortak olan meslekleri bul"""
        region_jobs = {}
        
        # Normalize edilmiş meslek sütunu kontrolü
        job_col = 'job_title_normalized' if 'job_title_normalized' in df.columns else 'job_title'
        
        for region in regions:
            region_df = df[df['region'] == region]
            region_jobs[region] = set(region_df[job_col].dropna().unique())
        
        # Tüm bölgelerde bulunan meslekler
        common_jobs = region_jobs[regions[0]]
        for region in regions[1:]:
            common_jobs = common_jobs.intersection(region_jobs[region])
        
        return list(common_jobs)
    
    def create_ratio_analysis(self, df_filtered, common_jobs):
        """Doğrudan karşılaştırma analizi - oran hesaplaması"""
        print("=== DOĞRUDAN KARŞILAŞTIRMA ANALİZİ ===\n")
        
        regions = ['TR', 'EU', 'US']
        comparison_results = {}
        
        # Normalize edilmiş meslek sütunu kontrolü
        job_col = 'job_title_normalized' if 'job_title_normalized' in df_filtered.columns else 'job_title'
        
        # Her bölge çifti için karşılaştırma
        region_pairs = [('TR', 'EU'), ('TR', 'US'), ('EU', 'US')]
        
        for base_region, compare_region in region_pairs:
            print(f"\n{base_region} vs {compare_region} Karşılaştırması:")
            print("="*40)
            
            # Bu iki bölgede ortak bulunan meslekler
            base_jobs = set(df_filtered[df_filtered['region'] == base_region][job_col].unique())
            compare_jobs = set(df_filtered[df_filtered['region'] == compare_region][job_col].unique())
            pair_common_jobs = list(base_jobs.intersection(compare_jobs))
            
            if not pair_common_jobs:
                print(f"❌ {base_region} ve {compare_region} arasında ortak meslek bulunamadı!")
                continue
            
            print(f"Ortak meslekler: {len(pair_common_jobs)}")
            
            ratios = []
            job_analysis = []
            
            for job in pair_common_jobs:
                base_salaries = df_filtered[
                    (df_filtered['region'] == base_region) & 
                    (df_filtered[job_col] == job)
                ]['SalaryInUSD']
                
                compare_salaries = df_filtered[
                    (df_filtered['region'] == compare_region) & 
                    (df_filtered[job_col] == job)
                ]['SalaryInUSD']
                
                if len(base_salaries) > 0 and len(compare_salaries) > 0:
                    base_median = base_salaries.median()
                    compare_median = compare_salaries.median()
                    ratio = compare_median / base_median
                    
                    ratios.append(ratio)
                    job_analysis.append({
                        'job': job,
                        'base_median': base_median,
                        'compare_median': compare_median,
                        'ratio': ratio,
                        'base_count': len(base_salaries),
                        'compare_count': len(compare_salaries)
                    })
            
            # Sonuçları kaydet
            comparison_results[f"{base_region}_vs_{compare_region}"] = {
                'job_analysis': job_analysis,
                'overall_ratio': np.median(ratios) if ratios else 0,
                'ratio_std': np.std(ratios) if ratios else 0
            }
            
            # Özet göster
            if ratios:
                overall_ratio = np.median(ratios)
                print(f"\nGenel Oran: {compare_region} maaşları {base_region}'den {overall_ratio:.2f} kat fazla")
                print(f"Oran Standart Sapması: {np.std(ratios):.2f}")
                
                # En yüksek ve en düşük oranlar
                job_ratios = [(ja['job'], ja['ratio']) for ja in job_analysis]
                job_ratios.sort(key=lambda x: x[1], reverse=True)
                
                print(f"\nEn Yüksek Oran Farkı:")
                for job, ratio in job_ratios[:3]:
                    print(f"  {job}: {ratio:.2f}x")
                
                print(f"\nEn Düşük Oran Farkı:")
                for job, ratio in job_ratios[-3:]:
                    print(f"  {job}: {ratio:.2f}x")
        
        return comparison_results
    
    def create_welfare_analysis(self, df_filtered):
        """Derinlemesine refah analizi"""
        print("\n=== DERİNLEMESİNE REFAH ANALİZİ ===\n")
        
        regions = ['TR', 'EU', 'US']
        welfare_results = {}
        
        for region in regions:
            region_df = df_filtered[df_filtered['region'] == region].copy()
            
            if len(region_df) == 0:
                continue
            
            print(f"\n{region} Bölgesi Refah Analizi:")
            print("="*30)
            
            # Gelir dağılımı analizi
            salaries = region_df['SalaryInUSD'].dropna()
            
            # Temel istatistikler
            mean_salary = salaries.mean()
            median_salary = salaries.median()
            q25 = salaries.quantile(0.25)
            q75 = salaries.quantile(0.75)
            
            # Gini katsayısı (gelir eşitsizliği)
            gini = self.calculate_gini(salaries)
            
            # Deneyim seviyesi bazında analiz
            exp_col = 'experience_level_normalized' if 'experience_level_normalized' in region_df.columns else 'experience_level'
            exp_analysis = region_df.groupby(exp_col)['SalaryInUSD'].agg([
                'count', 'mean', 'median', 'std'
            ]).round(0)
            
            welfare_results[region] = {
                'mean_salary': mean_salary,
                'median_salary': median_salary,
                'q25': q25,
                'q75': q75,
                'gini': gini,
                'sample_size': len(salaries),
                'experience_analysis': exp_analysis
            }
            
            print(f"Ortalama Maaş: ${mean_salary:,.0f}")
            print(f"Medyan Maaş: ${median_salary:,.0f}")
            print(f"Alt Çeyrek (Q25): ${q25:,.0f}")
            print(f"Üst Çeyrek (Q75): ${q75:,.0f}")
            print(f"Gini Katsayısı: {gini:.3f} (0=tam eşit, 1=tam eşitsiz)")
            
            print(f"\nDeneyim Seviyesi Analizi:")
            print(exp_analysis)
        
        return welfare_results
    
    def calculate_gini(self, salaries):
        """Gini katsayısı hesapla (gelir eşitsizliği)"""
        if len(salaries) == 0:
            return 0
        
        # Sıralama
        sorted_salaries = np.sort(salaries)
        n = len(sorted_salaries)
        
        # Gini katsayısı formülü
        cumsum = np.cumsum(sorted_salaries)
        return (n + 1 - 2 * np.sum(cumsum) / cumsum[-1]) / n
    
    def create_visualizations(self, df_filtered, comparison_results, welfare_results):
        """Görselleştirmeler oluştur"""
        print("\n=== GÖRSELLEŞTİRMELER ===\n")
        
        # 1. Bölgesel maaş dağılımı
        plt.figure(figsize=(15, 10))
        
        # Alt grafik 1: Box plot
        plt.subplot(2, 3, 1)
        sns.boxplot(data=df_filtered, x='region', y='SalaryInUSD')
        plt.title('Bölgesel Maaş Dağılımı (Box Plot)')
        plt.ylabel('Maaş (USD)')
        plt.yscale('log')
        
        # Alt grafik 2: Violin plot
        plt.subplot(2, 3, 2)
        sns.violinplot(data=df_filtered, x='region', y='SalaryInUSD')
        plt.title('Maaş Yoğunluk Dağılımı')
        plt.ylabel('Maaş (USD)')
        plt.yscale('log')
        
        # Alt grafik 3: Deneyim seviyesi bazında
        plt.subplot(2, 3, 3)
        exp_col = 'experience_level_normalized' if 'experience_level_normalized' in df_filtered.columns else 'experience_level'
        sns.boxplot(data=df_filtered, x=exp_col, y='SalaryInUSD', hue='region')
        plt.title('Deneyim Seviyesine Göre Maaş')
        plt.xticks(rotation=45)
        plt.ylabel('Maaş (USD)')
        plt.yscale('log')
        
        # Alt grafik 4: Ortalama maaşlar
        plt.subplot(2, 3, 4)
        avg_salaries = df_filtered.groupby('region')['SalaryInUSD'].mean()
        avg_salaries.plot(kind='bar')
        plt.title('Ortalama Maaşlar')
        plt.ylabel('Ortalama Maaş (USD)')
        plt.xticks(rotation=0)
        
        # Alt grafik 5: Gini katsayıları
        plt.subplot(2, 3, 5)
        gini_values = [welfare_results[region]['gini'] for region in ['TR', 'EU', 'US'] if region in welfare_results]
        gini_regions = [region for region in ['TR', 'EU', 'US'] if region in welfare_results]
        plt.bar(gini_regions, gini_values)
        plt.title('Gelir Eşitsizliği (Gini Katsayısı)')
        plt.ylabel('Gini Katsayısı')
        plt.ylim(0, 1)
        
        # Alt grafik 6: Oran karşılaştırması
        plt.subplot(2, 3, 6)
        ratios = []
        labels = []
        for key, result in comparison_results.items():
            if result['overall_ratio'] > 0:
                ratios.append(result['overall_ratio'])
                labels.append(key.replace('_vs_', ' vs '))
        
        if ratios:
            plt.bar(labels, ratios)
            plt.title('Bölgesel Maaş Oranları')
            plt.ylabel('Oran (Kat)')
            plt.xticks(rotation=45)
        
        plt.tight_layout()
        plt.savefig('salary_analysis_comprehensive.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print("Görselleştirmeler 'salary_analysis_comprehensive.png' dosyasına kaydedildi.\n")
    
    def generate_report(self, comparison_results, welfare_results):
        """Kapsamlı rapor oluştur"""
        print("=== KAPSAMLI ANALİZ RAPORU ===\n")
        
        report = []
        report.append("# ULUSLARARASI MAAŞ ANALİZİ RAPORU")
        report.append("=" * 50)
        report.append(f"\nAnaliz Tarihi: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Veri Yılı: {self.exchange_rates['data_year']}")
        report.append(f"Kullanılan Döviz Kurları:")
        report.append(f"  - TRY/USD: {self.exchange_rates['TRY_USD']}")
        report.append(f"  - EUR/USD: {self.exchange_rates['EUR_USD']}")
        report.append("\n")
        
        # Doğrudan karşılaştırma sonuçları
        report.append("## 1. DOĞRUDAN KARŞILAŞTIRMA ANALİZİ")
        report.append("-" * 40)
        
        for comparison, results in comparison_results.items():
            base_region, compare_region = comparison.split('_vs_')
            ratio = results['overall_ratio']
            
            if ratio > 0:
                report.append(f"\n### {base_region} vs {compare_region}")
                report.append(f"Genel Oran: {compare_region} maaşları {base_region}'den {ratio:.2f} kat fazla")
                
                if ratio > 1.5:
                    report.append(f"🔴 Önemli fark: {compare_region} bölgesi önemli ölçüde daha yüksek maaş sunuyor")
                elif ratio < 0.8:
                    report.append(f"🟡 Dikkat: {base_region} bölgesi daha yüksek maaş sunuyor")
                else:
                    report.append(f"🟢 Dengeli: İki bölge arasında makul seviyede fark var")
        
        # Refah analizi sonuçları
        report.append("\n\n## 2. DERİNLEMESİNE REFAH ANALİZİ")
        report.append("-" * 40)
        
        for region, results in welfare_results.items():
            report.append(f"\n### {region} Bölgesi")
            report.append(f"Ortalama Maaş: ${results['mean_salary']:,.0f}")
            report.append(f"Medyan Maaş: ${results['median_salary']:,.0f}")
            report.append(f"Gelir Eşitsizliği (Gini): {results['gini']:.3f}")
            
            # Gini değerlendirmesi
            gini = results['gini']
            if gini < 0.3:
                report.append("🟢 Düşük eşitsizlik - İyi gelir dağılımı")
            elif gini < 0.4:
                report.append("🟡 Orta eşitsizlik - Kabul edilebilir seviye")
            else:
                report.append("🔴 Yüksek eşitsizlik - Gelir dağılımında adaletsizlik")
        
        # Öneriler
        report.append("\n\n## 3. STRATEJİK ÖNERİLER")
        report.append("-" * 40)
        
        # En yüksek maaş bölgesi
        avg_salaries = {region: results['mean_salary'] for region, results in welfare_results.items()}
        best_region = max(avg_salaries.keys(), key=lambda x: avg_salaries[x])
        
        report.append(f"\n🎯 En Yüksek Ortalama Maaş: {best_region} bölgesi")
        report.append(f"💰 Ortalama: ${avg_salaries[best_region]:,.0f}")
        
        # En düşük eşitsizlik
        gini_scores = {region: results['gini'] for region, results in welfare_results.items()}
        most_equal = min(gini_scores.keys(), key=lambda x: gini_scores[x])
        
        report.append(f"\n⚖️ En Adil Gelir Dağılımı: {most_equal} bölgesi")
        report.append(f"📊 Gini Katsayısı: {gini_scores[most_equal]:.3f}")
        
        # Raporu dosyaya kaydet
        report_text = "\n".join(report)
        
        with open('salary_analysis_report.txt', 'w', encoding='utf-8') as f:
            f.write(report_text)
        
        print(report_text)
        print("\n🎉 Detaylı rapor 'salary_analysis_report.txt' dosyasına kaydedildi!")
        
        return report_text
    
    def run_complete_analysis(self):
        """Tüm analizi çalıştır"""
        print("🚀 KAPSAMLI MAAŞ ANALİZİ BAŞLIYOOR...\n")
        
        # 1. Veri yükleme
        df1, df2 = self.load_data()
        
        # 2. Veri yılını tespit et
        data_year = self.detect_data_year(df1, df2)
        
        # 3. Döviz kurlarını al
        self.get_exchange_rates(data_year)
        
        # 4. Veri ön işleme
        df_combined = self.preprocess_data(df1, df2)
        if df_combined is None:
            return
        
        # 5. Maaş standardizasyonu
        df_combined = self.convert_to_usd(df_combined)
        
        # 6. Normalizasyon
        df_combined = self.normalize_job_titles(df_combined)
        df_combined = self.normalize_experience_levels(df_combined)
        
        # 7. Bölgesel analiz
        analysis_result = self.perform_regional_analysis()
        if analysis_result is None:
            return
        
        df_filtered, common_jobs = analysis_result
        
        # 8. Karşılaştırma analizi
        comparison_results = self.create_ratio_analysis(df_filtered, common_jobs)
        
        # 9. Refah analizi
        welfare_results = self.create_welfare_analysis(df_filtered)
        
        # 10. Görselleştirmeler
        self.create_visualizations(df_filtered, comparison_results, welfare_results)
        
        # 11. Rapor oluşturma
        self.generate_report(comparison_results, welfare_results)
        
        print("\n✅ ANALİZ TAMAMLANDI!")
        print("📊 Çıktı dosyaları:")
        print("  - salary_analysis_comprehensive.png (Görselleştirmeler)")
        print("  - salary_analysis_report.txt (Detaylı rapor)")

if __name__ == "__main__":
    analyzer = SalaryAnalyzer()
    analyzer.run_complete_analysis()