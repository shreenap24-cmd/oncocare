# 🎗️ Oncocare — Cancer Care Companion

> A Django web application designed to help cancer patients manage their recovery journey and follow-up care.

---

## 📌 About This Project

Being a cancer patient myself, I understand how overwhelming it is to keep track of appointments, medications, blood test results, and treatment cycles. Most patients manage this through paper notes and memory. It shouldn't be this hard.

Oncocare is a meaningful healthcare web application that brings everything into one organized place — helping cancer patients focus on recovery instead of paperwork.

---

## ✨ Features

- 🔬 **Cancer-Specific Biomarker Tracking** — Log blood test results after each follow-up and see trend charts specific to your cancer type (Thyroid, Breast, Prostate, and 7 more)
- 📅 **Appointment Manager** — Track upcoming, completed, and cancelled doctor visits with email reminders
- 💊 **Medication Tracker** — Log medicines with dosage, frequency, and reminder times
- ⚕️ **Treatment Log** — Track chemotherapy cycles, radiation, surgery with a visual progress bar
- 📄 **Lab Report Upload** — Upload and store lab reports as PDF or image files
- 📓 **Symptom Diary** — Log daily symptoms with severity rating (1–10)
- 📊 **Analytics Dashboard** — Visual health summary with charts and upcoming appointments
- 📥 **PDF Health Summary** — Download a clean printable summary to share with your doctor
- 🔒 **Private & Secure** — Your data is never shared or sold

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python + Django |
| Database | SQLite |
| Frontend | HTML, CSS, Bootstrap 5 |
| Charts | Chart.js |
| PDF Generation | ReportLab |
| Icons | Bootstrap Icons |
| Fonts | Playfair Display + DM Sans |

## 🗂️ Project Structure

~~~
oncocare/
│
├── accounts/        # User authentication and patient profile
├── appointments/    # Doctor appointment management
├── medications/     # Medication tracking
├── treatments/      # Treatment and cycle tracking
├── reports/         # Lab report file uploads
├── symptoms/        # Symptom diary
├── biomarkers/      # Cancer-specific biomarker tracking
├── dashboard/       # Main analytics dashboard
├── home/            # Landing page and privacy policy
└── templates/       # All HTML templates
~~~

## 🚀 Setup Instructions

**1. Clone the repository**
```bash
git clone https://github.com/shreenap24-cmd/oncocare.git
cd oncocare
```

**2. Install dependencies**
```bash
pip install django reportlab
```

**3. Run migrations**
```bash
python manage.py migrate
```

**4. Seed cancer types and biomarkers**
```bash
python manage.py seed_biomarkers
```

**5. Create a superuser**
```bash
python manage.py createsuperuser
```

**6. Run the server**
```bash
python manage.py runserver
```

**7. Open in browser**
http://localhost:8000

---

## 🔬 Supported Cancer Types & Biomarkers

| Cancer Type | Key Markers |
|---|---|
| Thyroid Cancer | Thyroglobulin (Tg), TSH, Anti-Tg |
| Breast Cancer | CA 15-3, CEA, CA 27-29 |
| Prostate Cancer | PSA, Free PSA Ratio |
| Lung Cancer | CEA, CYFRA 21-1, NSE, SCC |
| Blood Cancer | WBC, RBC, Platelets, LDH, B2M |
| Liver Cancer | AFP, ALT, AST |
| Ovarian Cancer | CA-125, HE4 |
| Colorectal Cancer | CEA, CA 19-9 |
| Pancreatic Cancer | CA 19-9, CEA |
| Cervical Cancer | SCC Antigen, CEA |

---

## 👩‍💻 About the Developer

**Shreena** — Cancer patient and software engineering student.

This project was built as a Django internship project. The biomarker tracking feature was designed from personal experience — as a thyroid cancer patient, I know that Thyroglobulin levels should trend downward after treatment. That kind of cancer-specific knowledge is what makes Oncocare different from a generic health tracker.

---

## 📃 License

This project was built for educational purposes as a college internship project.

---

*Built with ❤️ and purpose by Shreena*