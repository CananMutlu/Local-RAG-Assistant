<div align="center">
  <h1>🌟 Foundry Local RAG Assistant</h1>
  <p><i>100% Çevrimdışı, Gizlilik Odaklı ve Güvenli Belge Asistanı</i></p>

  ![Python](https://img.shields.io/badge/Python-3.8+-blue.svg?style=for-the-badge)
  ![Streamlit](https://img.shields.io/badge/Streamlit-Premium_UI-FF4B4B.svg?style=for-the-badge)
  ![Foundry Local](https://img.shields.io/badge/LLM-Foundry_Local-purple.svg?style=for-the-badge)
  ![SQLite](https://img.shields.io/badge/Database-SQLite-003B57.svg?style=for-the-badge)
</div>

<br>

Bu proje, verilerinizi internete veya herhangi bir bulut sunucusuna göndermeden, **tamamen kendi bilgisayarınızda** çalışan modern bir RAG (Retrieval-Augmented Generation) mimarisidir. Kurumsal belgelerinizi (PDF/TXT) okur, analiz eder ve sorularınızı **sadece** bu belgelere dayanarak yüksek doğrulukla yanıtlar.

---

## 🎥 Proje Sunumu ve Canlı Demo

Sistemin nasıl çalıştığını, mimarisini ve modern Streamlit arayüzü üzerindeki canlı demomuzu aşağıdaki bağlantıdan izleyebilirsiniz:

👉 **[Proje Demo Videosunu İzlemek İçin Tıklayın](https://drive.google.com/file/d/1wp8qrgQy_5gMEjzc-aQwC_fwIW5h94l1/view?usp=sharing)**

---

## ✨ Öne Çıkan Özellikler

* **🔒 %100 Veri Gizliliği:** Sistem internet bağlantısına ihtiyaç duymaz. Hiçbir veriniz OpenAI, Google veya başka bir dış sunucuya gönderilmez. Tamamen yerel (local) çalışır.
* **🎯 Sıfır Halüsinasyon (Dürüst Yapay Zeka):** Sistem gelişmiş prompt mühendisliği ile sıkıca sınırlandırılmıştır. Bilmediği veya veritabanında (belgelerinizde) olmayan bir soru sorulduğunda içerik uydurmaz, şeffaf bir şekilde "Bilmiyorum" yanıtını verir.
* **🎨 Premium Kullanıcı Arayüzü:** Özel CSS ile tasarlanmış, "Dark Mode" destekli, estetik ve akıcı bir Streamlit web arayüzü sunar.
* **🔍 Kaynak Şeffaflığı:** Asistanın verdiği her cevabın altında, o bilginin hangi belgeden alındığı net bir şekilde referans olarak gösterilir.

---

## 🛠️ Kullanılan Teknolojiler

Modern ve hafif bir mimari tercih edilmiştir:

| Bileşen | Teknoloji | Açıklama |
| :--- | :--- | :--- |
| **Kullanıcı Arayüzü** | `Streamlit` | Özel CSS giydirilmiş web arayüzü |
| **Veritabanı** | `SQLite` | Vektörlerin ve metin parçalarının yerel depolanması |
| **Vektörleştirme (Embedding)**| `Qwen3-Embedding-0.6b` | Foundry Local üzerinden çalışan yerel embedding modeli |
| **LLM Motoru** | `Phi-3.5-mini / Qwen2.5`| Foundry Local ile çalışan, RAG için optimize edilmiş dil modelleri |

---

## 🚀 Kurulum ve Çalıştırma

Projeyi kendi bilgisayarınızda çalıştırmak için aşağıdaki adımları izleyin:

### 1. Projeyi Klonlayın
```bash
git clone <repo-url-adresiniz>
cd RAG_Sistemleri
```

### 2. Gerekli Kütüphaneleri Yükleyin
*(Sanal ortam (virtual environment) kullanmanız tavsiye edilir)*
```bash
pip install -r requirements.txt
```

### 3. Uygulamayı Başlatın
```bash
streamlit run app.py
```

Uygulama çalıştıktan sonra tarayıcınızda otomatik olarak `http://localhost:8501` adresinde açılacaktır. Sol menüden PDF veya TXT belgelerinizi yükleyip asistanınızla sohbete başlayabilirsiniz!

---
<div align="center">
  <i>Geliştirici tarafından ❤️ ile yapılmıştır.</i>
</div>
