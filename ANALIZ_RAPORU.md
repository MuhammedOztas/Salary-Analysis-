# TR, EU ve US Maaş Rejimleri Kapsamlı Karşılaştırmalı Analizi

## 📋 Proje Özeti

Bu analiz, Türkiye (TR), Avrupa Birliği (EU) ve Amerika Birleşik Devletleri (US) bölgeleri arasındaki maaş rejimlerini karşılaştıran kapsamlı bir çalışmadır. Analiz, iki farklı veri seti kullanılarak gerçekleştirilmiştir:

- **salary_data.csv**: 221 ülkenin genel maaş istatistikleri
- **Salary.csv**: 6,684 bireysel maaş kaydı

## 🎯 Ana Bulgular

### 1. Ortalama Maaş Karşılaştırması

| Bölge | Ortalama Yıllık Maaş (USD) | Sıralama |
|-------|---------------------------|----------|
| 🇪🇺 EU | $115,919.92 | 1. |
| 🇺🇸 US | $112,998.76 | 2. |
| 🇹🇷 TR | $3,433.56 | 3. |

### 2. Maaş Oranları

- **US/EU**: 0.97x (US maaşları EU'nun %97'si)
- **US/TR**: 32.91x (US maaşları TR'nin 32.91 katı)
- **EU/TR**: 33.76x (EU maaşları TR'nin 33.76 katı)

## 📊 Detaylı Analiz Sonuçları

### Deneyim Seviyesine Göre Maaş Karşılaştırması

| Deneyim Seviyesi | EU (USD) | US (USD) | TR (USD) |
|------------------|----------|----------|----------|
| Junior (0-2 yıl) | $44,640 | $41,033 | $3,434 |
| Mid-Level (2-5 yıl) | $70,691 | $70,862 | $3,434 |
| Senior (5-10 yıl) | $120,237 | $119,441 | $3,434 |
| Expert (10+ yıl) | $166,330 | $162,503 | $3,434 |

### En Yaygın Mesleklerde Karşılaştırma

| Meslek | US (USD) | EU (USD) | US/EU Oranı |
|--------|----------|----------|-------------|
| Sales Manager | $102,500 | $99,375 | 1.03x |
| Product Manager | $142,616 | $142,649 | 1.00x |
| Software Engineer | $135,020 | $136,136 | 0.99x |
| Marketing Manager | $107,629 | $108,658 | 0.99x |
| Data Scientist | $158,424 | $163,901 | 0.97x |

## 📈 Gelir Dağılımı ve Eşitsizlik Analizi

### Gini Katsayısı (Gelir Eşitsizliği)

| Bölge | Gini Katsayısı | Yorum |
|-------|----------------|-------|
| EU | -0.0773 | Daha düşük gelir eşitsizliği |
| US | -0.0893 | Daha yüksek gelir eşitsizliği |

### Kariyer İlerlemesi Analizi

- **EU**: Expert seviyesi maaşları Junior seviyesinin **3.7 katı**
- **US**: Expert seviyesi maaşları Junior seviyesinin **4.0 katı**

## 🔍 Ekonomik Refah Göstergeleri

### 🇪🇺 Avrupa Birliği (EU)
- **Güçlü Yönler**: En yüksek ortalama maaş, düşük gelir eşitsizliği
- **Zayıf Yönler**: Kariyer ilerlemesi US'ye göre daha yavaş
- **Profil**: Sosyal refah odaklı, dengeli gelir dağılımı

### 🇺🇸 Amerika Birleşik Devletleri (US)
- **Güçlü Yönler**: Güçlü kariyer ilerlemesi, yüksek üst seviye maaşlar
- **Zayıf Yönler**: Yüksek gelir eşitsizliği
- **Profil**: Performans odaklı, meritokratik sistem

### 🇹🇷 Türkiye (TR)
- **Güçlü Yönler**: Gelişmekte olan ekonomi potansiyeli
- **Zayıf Yönler**: Düşük maaş seviyeleri, gelişmiş ülkelerle büyük fark
- **Profil**: Gelişmekte olan ekonomi, dönüşüm sürecinde

## 📊 Veri Seti Detayları

### Analiz Edilen Veriler
- **Toplam Kayıt**: 6,684 bireysel maaş kaydı
- **Bölge Dağılımı**:
  - US: 1,356 kayıt (%20.3)
  - EU: 1,332 kayıt (%19.9)
  - Other: 3,996 kayıt (%59.8)

### Meslek Çeşitliliği
- **Toplam Meslek Sayısı**: 129 farklı meslek
- **En Yaygın Meslekler**:
  1. Software Engineer (2,013 kayıt)
  2. Data Scientist (906 kayıt)
  3. Marketing Manager (846 kayıt)

## 🎨 Görselleştirmeler

Analiz sonuçları aşağıdaki görselleştirmelerle desteklenmiştir:

1. **Ortalama Maaş Karşılaştırması** - Bar chart
2. **Maaş Dağılımı** - Box plot ve histogram
3. **Deneyim vs Maaş İlişkisi** - Scatter plot
4. **Meslek Bazlı Karşılaştırma** - Grouped bar chart
5. **Gelir Eşitsizliği** - Bar chart
6. **Maaş Oranları** - Bar chart
7. **Kariyer İlerlemesi** - Grouped bar chart

## 📋 Metodoloji

### Veri Ön İşleme
1. **Bölge Sınıflandırması**: Ülkeler EU, US ve Other olarak kategorize edildi
2. **Meslek Normalizasyonu**: Benzer meslek unvanları standartlaştırıldı
3. **Para Birimi Standardizasyonu**: Tüm maaşlar USD'ye çevrildi

### Analiz Teknikleri
- **Betimsel İstatistikler**: Ortalama, medyan, standart sapma
- **Gini Katsayısı**: Gelir eşitsizliği ölçümü
- **Karşılaştırmalı Analiz**: Bölgeler arası oran hesaplamaları
- **Segmentasyon**: Deneyim seviyesi ve meslek bazlı analizler

## 🎯 Sonuçlar ve Öneriler

### Ana Sonuçlar
1. **EU liderliği**: En yüksek ortalama maaş ve en düşük gelir eşitsizliği
2. **US performansı**: Güçlü kariyer ilerlemesi ve yüksek üst seviye maaşlar
3. **TR gelişim potansiyeli**: Gelişmekte olan ekonomi profili

### Politika Önerileri
- **TR için**: Maaş seviyelerinin artırılması ve gelir dağılımının iyileştirilmesi
- **EU için**: Kariyer ilerlemesi fırsatlarının artırılması
- **US için**: Gelir eşitsizliğinin azaltılması

## 📁 Dosyalar

- `comprehensive_salary_analysis_final.png`: Ana görselleştirme
- `final_comprehensive_report.py`: Analiz scripti
- `Salary.csv`: Detaylı maaş verileri
- `salary_data.csv`: Ülke bazlı maaş istatistikleri

---

**Analiz Tarihi**: 2024  
**Veri Kaynakları**: salary_data.csv, Salary.csv  
**Analiz Kapsamı**: 6,684 kayıt, 3 bölge, 129 meslek  
**Teknolojiler**: Python, Pandas, Matplotlib, Seaborn