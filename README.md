# 🎗️ Oncocare — Cancer Care Companion

> A Django web application designed to help cancer patients manage their recovery journey and follow-up care.

---


## 📌 About This Project

OncoCare is a Django-based healthcare management platform designed to help cancer patients organize and track their follow-up care in one place. The application provides tools for managing appointments, medications, treatments, symptoms, laboratory reports, biomarker readings, and AI-assisted support.

The idea for OncoCare was inspired by witnessing the challenges of navigating cancer care and managing important health information across multiple sources. By bringing these tools together into a single platform, OncoCare aims to make healthcare management more organized, accessible, and patient-friendly.


---

## ✨ Features

- 🔬 **Cancer-Specific Biomarker Tracking** — Log blood test results after each follow-up and see trend charts specific to your cancer type (Thyroid, Breast, Prostate, and 7 more)
- 📅 **Appointment Manager** — Track upcoming, completed, and cancelled doctor visits with email reminders
- 💊 **Medication Tracker** — Log medicines with dosage, frequency, and reminder times
- ⚕️ **Treatment Log** — Track chemotherapy cycles, radiation, surgery with a visual progress bar
- 📄 **Lab Report Upload** — Upload and store lab reports as PDF or image files
- 📓 **Symptom Diary** — Log daily symptoms with severity rating (1–10)
- 📊 **Analytics Dashboard** — Visual health summary with charts and upcoming appointments
- 🤖 **AI Health Assistant** — Chat-based assistant powered by OpenRouter API to answer general cancer care questions
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
| AI Integration | OpenRouter API |
| Environment | python-dotenv for secure API key management |

## 🗂️ Project Structure

~~~
oncocare/
│
├── accounts/        # User authentication and patient profile
├── appointments/    # Doctor appointment management
├── assistant/       # AI assistant
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

**3. Create a `.env` file** in the project root with:
```
SECRET_KEY=your-secret-key
EMAIL_HOST_USER=your-email
EMAIL_HOST_PASSWORD=your-app-password
OPENROUTER_API_KEY=your-openrouter-key
```

**4. Run migrations**
```bash
python manage.py migrate
```

**5. Seed cancer types and biomarkers**
```bash
python manage.py seed_biomarkers
```

**6. Create a superuser**
```bash
python manage.py createsuperuser
```

**7. Run the server**
```bash
python manage.py runserver
```

**8. Open in browser**
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

**Shreena Patel** is a Software Engineering student with an interest in healthcare technology and user-centered application design.

OncoCare was developed as an internship project using Python, Django, SQLite, Bootstrap, and JavaScript. The project combines healthcare domain knowledge with software engineering principles to create a practical solution for managing cancer follow-up care and treatment records.


---

## 📃 License

This project was built for educational purposes as a college internship project.

---

*Built with ❤️ and purpose by Shreena*