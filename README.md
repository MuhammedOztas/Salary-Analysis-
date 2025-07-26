# 🎯 Uluslararası Maaş Analizi - Kapsamlı Web Sitesi

## 📋 Proje Hakkında

Bu proje, Türkiye, Avrupa Birliği ve Amerika Birleşik Devletleri arasında kapsamlı maaş karşılaştırması ve gelir eşitsizliği analizi sunan modern, bilimsel ve estetik bir web sitesidir. Site, 6,905 veri kaydı üzerinden yapılan detaylı analizleri interaktif ve kullanıcı dostu bir şekilde sunmaktadır.

## ✨ Özellikler

### 🎨 Modern Tasarım
- **Bilimsel Estetik**: Profesyonel ve akademik görünüm
- **Responsive Tasarım**: Tüm cihazlarda mükemmel görüntü
- **Glassmorphism Efektleri**: Modern şeffaflık ve blur efektleri
- **Smooth Animasyonlar**: CSS ve JavaScript ile gelişmiş animasyonlar
- **Dark/Light Theme Uyumlu**: Sistem tercihleri destekli

### 📊 İnteraktif Görselleştirmeler
- **Chart.js Entegrasyonu**: Profesyonel grafik kütüphanesi
- **Çoklu Grafik Türleri**: Bar, Doughnut, Radar, Line grafikleri
- **Tab-based Navigation**: Farklı analiz türleri arasında geçiş
- **Responsive Charts**: Mobil uyumlu grafik boyutlandırma

### 🧭 Gelişmiş Navigasyon
- **Smooth Scrolling**: Yumuşak sayfa geçişleri
- **Active Link Tracking**: Otomatik aktif bölüm takibi
- **Mobile Menu**: Hamburger menü ile mobil navigasyon
- **Keyboard Navigation**: Erişilebilirlik odaklı klavye desteği

### 📱 Responsive & Accessible
- **Mobile-First Approach**: Önce mobil tasarım prensibi
- **WCAG Guidelines**: Web erişilebilirlik standartları
- **Screen Reader Support**: Ekran okuyucu uyumluluğu
- **Keyboard Navigation**: Tam klavye desteği

## 🗂️ Dosya Yapısı

```
📁 Salary Analysis Website/
├── 📄 index.html              # Ana HTML dosyası
├── 🎨 styles.css              # Tüm CSS stilleri
├── ⚡ script.js               # JavaScript işlevselliği
├── 📊 salary_analysis.py      # Python analiz kodu
├── 📈 salary_analysis_comprehensive.png # Detaylı grafikler
├── 📄 salary_analysis_report.txt # Teknik rapor
├── 📋 MASTER_SALARY_ANALYSIS_SUMMARY.md # Master özet
├── 📊 salary_data.csv         # Veri dosyası (223 kayıt)
├── 📊 Salary.csv             # Ana veri dosyası (6,686 kayıt)
└── 📖 README.md              # Bu dosya
```

## 🚀 Kullanım

### 🌐 Web Sitesini Çalıştırma

1. **Dosyaları İndirin**: Tüm dosyaları aynı klasöre yerleştirin
2. **Web Sunucusu**: Bir web sunucusu çalıştırın (Live Server, XAMPP, vs.)
3. **Tarayıcıda Açın**: `index.html` dosyasını tarayıcınızda açın

```bash
# Python ile basit sunucu
python -m http.server 8000

# Node.js ile live-server
npx live-server

# PHP ile yerleşik sunucu
php -S localhost:8000
```

### 📱 Tarayıcı Desteği

- ✅ Chrome 80+
- ✅ Firefox 75+
- ✅ Safari 13+
- ✅ Edge 80+
- ✅ Mobile Browsers

## 🎯 Site Bölümleri

### 🏠 Ana Sayfa (Hero Section)
- **İstatistik Kartları**: Temel veri özetleri
- **Call-to-Action Butonları**: Hızlı erişim linkleri
- **İnteraktif Grafik**: Doughnut chart ile veri özeti
- **Gradient Background**: Çekici görsel tasarım

### 🔍 Önemli Bulgular
- **4 Ana Bulgu Kartı**: Kilit sonuçlar
- **Hover Efektleri**: İnteraktif kart animasyonları
- **Renkli Kodlama**: Görsel veri kategorileri
- **Trend İndikatörleri**: Yön göstergeleri

### 🎯 Yönetici Özeti
- **Maaş Karşılaştırma Tablosu**: Detaylı sayısal veriler
- **Gini Katsayısı Analizi**: Gelir eşitsizliği metrikleri
- **Stratejik Çıkarımlar**: İş dünyası için öneriler
- **Badge Sistemi**: Görsel durum göstergeleri

### 📊 Detaylı Analiz
- **Doğrudan Karşılaştırmalar**: Ülke/bölge oranları
- **Deneyim Seviyesi Analizi**: Kariyer basamakları
- **Breakdown Detayları**: Alt kategori analizleri
- **Alert Sistemleri**: Önemli uyarılar

### 🔬 Veri Keşfi
- **İnteraktif Tab Sistemi**: 3 farklı grafik türü
- **Chart.js Entegrasyonu**: Profesyonel grafikler
- **Veri İstatistikleri**: Özet metrikler
- **Responsive Charts**: Mobil uyumlu görselleştirme

### 🧪 Metodoloji
- **Teknik Detaylar**: Analiz yöntemleri
- **Code Snippets**: Python kod örnekleri
- **Veri Toplama**: Süreç açıklamaları
- **Bilimsel Yaklaşım**: Akademik metodoloji

## 🎨 Tasarım Sistemi

### 🎨 Renk Paleti
```css
/* Ana Renkler */
--primary-color: #2563eb      /* Mavi */
--success-color: #10b981      /* Yeşil */
--warning-color: #f59e0b      /* Turuncu */
--danger-color: #dc2626       /* Kırmızı */

/* Gradient'ler */
--gradient-primary: linear-gradient(135deg, #667eea 0%, #764ba2 100%)
--gradient-hero: linear-gradient(135deg, #667eea 0%, #764ba2 100%)
```

### 📝 Typography
```css
/* Font Aileleri */
--font-primary: 'Inter'       /* Genel metin */
--font-mono: 'JetBrains Mono' /* Kod ve sayısal veriler */

/* Font Boyutları */
Hero Title: 3.5rem (56px)
Section Title: 2.5rem (40px)
Block Title: 1.5rem (24px)
Body Text: 1rem (16px)
```

### 📏 Spacing System
```css
/* Container */
--container-max-width: 1200px

/* Border Radius */
--border-radius: 12px
--border-radius-lg: 20px

/* Shadows */
--box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1)
--box-shadow-lg: 0 20px 25px -5px rgba(0, 0, 0, 0.1)
```

## ⚡ JavaScript Özellikleri

### 🧭 Navigasyon
- **Smooth Scrolling**: Yumuşak sayfa geçişleri
- **Active Link Tracking**: Otomatik bölüm takibi
- **Mobile Menu**: Responsive hamburger menü
- **Navbar Blur**: Scroll bazlı şeffaflık efekti

### 📊 Chart İşlevselliği
```javascript
// Grafik türleri
- Doughnut Chart (Hero)
- Bar Chart (Salary Comparison)
- Radar Chart (Gini Analysis)
- Line Chart (Experience Breakdown)
```

### 🎬 Animasyonlar
- **Scroll Reveal**: Sayfa kaydırma animasyonları
- **Counter Animation**: Sayısal veri animasyonları
- **Hover Effects**: Fare üzerine gelme efektleri
- **Loading States**: Yükleme durumu göstergeleri

### 📱 Responsive Behavior
- **Breakpoints**: 768px, 480px
- **Grid Adaptations**: Responsive grid düzenleri
- **Mobile Optimizations**: Dokunmatik optimizasyonlar

## 🛠️ Teknik Detaylar

### 📚 Kütüphaneler
- **Chart.js**: Grafik görselleştirmeleri
- **Font Awesome**: İkon kütüphanesi
- **Google Fonts**: Inter & JetBrains Mono fontları

### 🌐 CDN Linkler
```html
<!-- Font Awesome -->
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">

<!-- Google Fonts -->
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500">

<!-- Chart.js -->
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
```

### 🚀 Performance
- **CSS Optimizasyonu**: Minifikasyon ve gzip uyumluluğu
- **JavaScript Optimizasyonu**: Debounced scroll events
- **Image Optimization**: Modern format desteği
- **Lazy Loading**: Görsel yükleme optimizasyonu

## 📊 Veri Yapısı

### 📈 Ana Veriler
```javascript
salaryData = {
    regions: {
        'US': { averageSalary: 112431, gini: 0.268 },
        'TR': { averageSalary: 5991, gini: 0.274 },
        'EU': { averageSalary: 2770, gini: 0.451 }
    }
}
```

### 🔄 Veri Akışı
1. **CSV Dosyaları** → Python Analizi
2. **Python Çıktısı** → JavaScript Veri Objesi
3. **JavaScript** → Chart.js Görselleştirme
4. **Chart.js** → İnteraktif Grafikler

## 🎯 Kullanıcı Deneyimi (UX)

### 👆 Etkileşim Tasarımı
- **Micro-interactions**: Küçük animasyonlar
- **Visual Feedback**: Anlık geri bildirimler
- **Progressive Disclosure**: Kademeli bilgi açılımı
- **Consistent Navigation**: Tutarlı navigasyon sistemi

### 📱 Mobile Experience
- **Touch-friendly**: Dokunmatik uyumlu boyutlar
- **Swipe Gestures**: Kaydırma hareketleri
- **Mobile Charts**: Mobil optimize grafikler
- **Thumb-zone Optimization**: Parmak erişim alanları

### ♿ Erişilebilirlik
- **ARIA Labels**: Ekran okuyucu etiketleri
- **Keyboard Navigation**: Tam klavye desteği
- **Color Contrast**: WCAG AA uyumlu kontrastlar
- **Focus Management**: Odak yönetimi

## 🔧 Geliştirme

### 🛠️ Local Development
```bash
# Repository'yi klonlayın
git clone [repository-url]

# Klasöre gidin
cd salary-analysis-website

# Live server başlatın
npx live-server
```

### 🎨 CSS Customization
```css
/* CSS değişkenleri ile kolay özelleştirme */
:root {
    --primary-color: #your-color;
    --font-primary: 'Your-Font';
}
```

### ⚡ JavaScript Extension
```javascript
// Yeni grafik türü ekleme
function createCustomChart(ctx) {
    // Chart.js implementasyonu
}
```

## 📈 Analiz Sonuçları

### 🏆 Kilit Bulgular
1. **ABD Liderliği**: $112,431 ortalama maaş
2. **Gelir Adaleti**: ABD en düşük Gini (0.268)
3. **Türkiye Dengesi**: Düşük maaş, adil dağılım
4. **AB Paradoksu**: Yüksek eşitsizlik sorunu

### 📊 İstatistiksel Metrikler
- **Toplam Kayıt**: 6,905 veri
- **Analiz Edilen Bölge**: 3 (TR, EU, US)
- **Döviz Kurları**: TRY/USD: 19.07, EUR/USD: 1.08
- **Veri Yılı**: 2023

## 🤝 Katkıda Bulunma

Bu proje açık kaynaklıdır ve katkılara açıktır:

1. 🍴 **Fork** edin
2. 🌿 **Branch** oluşturun
3. ✨ **Geliştirmeler** yapın
4. 📝 **Commit** edin
5. 🚀 **Pull Request** gönderin

## 📞 İletişim

- 📧 **Email**: [your-email@domain.com]
- 🐙 **GitHub**: [your-github-profile]
- 💼 **LinkedIn**: [your-linkedin-profile]

## 📄 Lisans

Bu proje MIT Lisansı altında lisanslanmıştır. Detaylar için `LICENSE` dosyasına bakınız.

---

## 🙏 Teşekkürler

Bu proje şu teknolojiler sayesinde geliştirilmiştir:
- **Chart.js** - Grafik kütüphanesi
- **Font Awesome** - İkon seti
- **Google Fonts** - Typography
- **Modern CSS** - Grid & Flexbox
- **Vanilla JavaScript** - İnteraktivite

---

**© 2025 Uluslararası Maaş Analizi. Tüm hakları saklıdır.**