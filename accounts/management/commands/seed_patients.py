from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import PatientProfile
from biomarkers.models import CancerType, PatientCancerProfile, CancerMarker, BiomarkerReading
from appointments.models import Appointment
from medications.models import Medication
from treatments.models import Treatment
from symptoms.models import Symptom
import datetime

def get_cancer(name):
    return CancerType.objects.filter(cancer_name__icontains=name).first()

today = datetime.date.today()

PATIENTS = [
    {
        "username": "Aarav", "password": "aarav123",
        "email": "aarav@example.com", "dob": datetime.date(1985, 3, 12),
        "blood_group": "A+", "phone": "9876501001", "address": "Mumbai, Maharashtra",
        "cancer": "Thyroid", "diagnosis_date": datetime.date(2023, 1, 10),
        "appointments": [
            {"doctor": "Dr. Mehta", "hospital": "Tata Memorial Hospital", "date": today + datetime.timedelta(days=7), "time": datetime.time(10, 30), "purpose": "Follow-up after RAI", "status": "upcoming"},
            {"doctor": "Dr. Mehta", "hospital": "Tata Memorial Hospital", "date": today - datetime.timedelta(days=90), "time": datetime.time(10, 30), "purpose": "3-month check", "status": "completed"},
        ],
        "medications": [
            {"name": "Levothyroxine", "dosage": "100mcg", "frequency": "once", "start": datetime.date(2023, 2, 1), "end": None},
            {"name": "Calcium Carbonate", "dosage": "500mg", "frequency": "twice", "start": datetime.date(2023, 2, 1), "end": None},
        ],
        "treatments": [
            {"name": "Thyroidectomy", "type": "surgery", "doctor": "Dr. Mehta", "hospital": "Tata Memorial", "start": datetime.date(2023, 1, 20), "end": datetime.date(2023, 1, 20), "total_cycles": None, "cycles_done": 0, "status": "completed"},
            {"name": "Radioactive Iodine Therapy", "type": "radioactive_iodine", "doctor": "Dr. Mehta", "hospital": "Tata Memorial", "start": datetime.date(2023, 3, 5), "end": datetime.date(2023, 3, 5), "total_cycles": None, "cycles_done": 0, "status": "completed"},
        ],
        "symptoms": [
            {"name": "Fatigue", "severity": 4, "date": today - datetime.timedelta(days=10)},
            {"name": "Weight Gain", "severity": 3, "date": today - datetime.timedelta(days=5)},
        ],
        "readings": [
            {"marker": "Thyroglobulin", "value": 8.5, "date": datetime.date(2023, 4, 1)},
            {"marker": "Thyroglobulin", "value": 4.2, "date": datetime.date(2023, 7, 1)},
            {"marker": "Thyroglobulin", "value": 1.8, "date": datetime.date(2023, 10, 1)},
            {"marker": "Thyroglobulin", "value": 0.5, "date": datetime.date(2024, 1, 1)},
            {"marker": "TSH", "value": 0.08, "date": datetime.date(2023, 4, 1)},
            {"marker": "TSH", "value": 0.05, "date": datetime.date(2023, 7, 1)},
            {"marker": "TSH", "value": 0.04, "date": datetime.date(2023, 10, 1)},
            {"marker": "TSH", "value": 0.03, "date": datetime.date(2024, 1, 1)},
            {"marker": "Anti-Thyroglobulin", "value": 85.0, "date": datetime.date(2023, 4, 1)},
            {"marker": "Anti-Thyroglobulin", "value": 52.0, "date": datetime.date(2023, 7, 1)},
            {"marker": "Anti-Thyroglobulin", "value": 28.0, "date": datetime.date(2023, 10, 1)},
            {"marker": "Anti-Thyroglobulin", "value": 12.0, "date": datetime.date(2024, 1, 1)},
        ],
    },
    {
        "username": "Priya", "password": "priya123",
        "email": "priya@example.com", "dob": datetime.date(1990, 7, 22),
        "blood_group": "B+", "phone": "9876501002", "address": "Pune, Maharashtra",
        "cancer": "Breast", "diagnosis_date": datetime.date(2022, 5, 15),
        "appointments": [
            {"doctor": "Dr. Sharma", "hospital": "Ruby Hall Clinic", "date": today + datetime.timedelta(days=14), "time": datetime.time(11, 0), "purpose": "Oncology follow-up", "status": "upcoming"},
            {"doctor": "Dr. Sharma", "hospital": "Ruby Hall Clinic", "date": today - datetime.timedelta(days=30), "time": datetime.time(11, 0), "purpose": "Post-chemo check", "status": "completed"},
        ],
        "medications": [
            {"name": "Tamoxifen", "dosage": "20mg", "frequency": "once", "start": datetime.date(2023, 1, 1), "end": None},
            {"name": "Vitamin D", "dosage": "1000IU", "frequency": "once", "start": datetime.date(2023, 1, 1), "end": None},
        ],
        "treatments": [
            {"name": "Chemotherapy (AC-T)", "type": "chemotherapy", "doctor": "Dr. Sharma", "hospital": "Ruby Hall Clinic", "start": datetime.date(2022, 7, 1), "end": datetime.date(2022, 12, 1), "total_cycles": 8, "cycles_done": 8, "status": "completed"},
            {"name": "Radiation Therapy", "type": "radiation", "doctor": "Dr. Sharma", "hospital": "Ruby Hall Clinic", "start": datetime.date(2023, 1, 10), "end": datetime.date(2023, 2, 20), "total_cycles": 25, "cycles_done": 25, "status": "completed"},
        ],
        "symptoms": [
            {"name": "Nausea", "severity": 3, "date": today - datetime.timedelta(days=20)},
            {"name": "Hair Thinning", "severity": 5, "date": today - datetime.timedelta(days=15)},
            {"name": "Fatigue", "severity": 4, "date": today - datetime.timedelta(days=8)},
        ],
        "readings": [
            {"marker": "CA 15-3", "value": 52.0, "date": datetime.date(2022, 6, 1)},
            {"marker": "CA 15-3", "value": 38.0, "date": datetime.date(2022, 9, 1)},
            {"marker": "CA 15-3", "value": 22.0, "date": datetime.date(2023, 1, 1)},
            {"marker": "CA 15-3", "value": 14.0, "date": datetime.date(2023, 6, 1)},
            {"marker": "CA 27-29", "value": 48.0, "date": datetime.date(2022, 6, 1)},
            {"marker": "CA 27-29", "value": 35.0, "date": datetime.date(2022, 9, 1)},
            {"marker": "CA 27-29", "value": 20.0, "date": datetime.date(2023, 1, 1)},
            {"marker": "CA 27-29", "value": 12.0, "date": datetime.date(2023, 6, 1)},
            {"marker": "CEA", "value": 8.2, "date": datetime.date(2022, 6, 1)},
            {"marker": "CEA", "value": 5.5, "date": datetime.date(2022, 9, 1)},
            {"marker": "CEA", "value": 3.2, "date": datetime.date(2023, 1, 1)},
            {"marker": "CEA", "value": 1.8, "date": datetime.date(2023, 6, 1)},
        ],
    },
    {
        "username": "Rohan", "password": "rohan123",
        "email": "rohan@example.com", "dob": datetime.date(1978, 11, 5),
        "blood_group": "O+", "phone": "9876501003", "address": "Delhi, India",
        "cancer": "Prostate", "diagnosis_date": datetime.date(2021, 8, 20),
        "appointments": [
            {"doctor": "Dr. Kapoor", "hospital": "AIIMS Delhi", "date": today + datetime.timedelta(days=21), "time": datetime.time(9, 0), "purpose": "PSA monitoring", "status": "upcoming"},
        ],
        "medications": [
            {"name": "Bicalutamide", "dosage": "50mg", "frequency": "once", "start": datetime.date(2021, 9, 1), "end": None},
        ],
        "treatments": [
            {"name": "Hormone Therapy", "type": "hormone", "doctor": "Dr. Kapoor", "hospital": "AIIMS Delhi", "start": datetime.date(2021, 9, 1), "end": None, "total_cycles": None, "cycles_done": 0, "status": "ongoing"},
            {"name": "Radiation Therapy", "type": "radiation", "doctor": "Dr. Kapoor", "hospital": "AIIMS Delhi", "start": datetime.date(2022, 1, 1), "end": datetime.date(2022, 3, 1), "total_cycles": 40, "cycles_done": 40, "status": "completed"},
        ],
        "symptoms": [
            {"name": "Fatigue", "severity": 3, "date": today - datetime.timedelta(days=12)},
            {"name": "Hot Flashes", "severity": 4, "date": today - datetime.timedelta(days=6)},
        ],
        "readings": [
            {"marker": "PSA", "value": 12.5, "date": datetime.date(2021, 8, 20)},
            {"marker": "PSA", "value": 6.2, "date": datetime.date(2022, 2, 1)},
            {"marker": "PSA", "value": 2.1, "date": datetime.date(2022, 8, 1)},
            {"marker": "PSA", "value": 0.8, "date": datetime.date(2023, 2, 1)},
            {"marker": "Free PSA", "value": 18.0, "date": datetime.date(2021, 8, 20)},
            {"marker": "Free PSA", "value": 22.0, "date": datetime.date(2022, 2, 1)},
            {"marker": "Free PSA", "value": 25.0, "date": datetime.date(2022, 8, 1)},
            {"marker": "Free PSA", "value": 28.0, "date": datetime.date(2023, 2, 1)},
        ],
    },
    {
        "username": "Aanya", "password": "aanya123",
        "email": "aanya@example.com", "dob": datetime.date(1995, 2, 14),
        "blood_group": "AB+", "phone": "9876501004", "address": "Bangalore, Karnataka",
        "cancer": "Blood", "diagnosis_date": datetime.date(2023, 3, 1),
        "appointments": [
            {"doctor": "Dr. Nair", "hospital": "Manipal Hospital", "date": today + datetime.timedelta(days=5), "time": datetime.time(10, 0), "purpose": "CBC review", "status": "upcoming"},
            {"doctor": "Dr. Nair", "hospital": "Manipal Hospital", "date": today - datetime.timedelta(days=60), "time": datetime.time(10, 0), "purpose": "Mid-cycle check", "status": "completed"},
        ],
        "medications": [
            {"name": "Imatinib", "dosage": "400mg", "frequency": "once", "start": datetime.date(2023, 4, 1), "end": None},
            {"name": "Allopurinol", "dosage": "300mg", "frequency": "once", "start": datetime.date(2023, 3, 15), "end": None},
        ],
        "treatments": [
            {"name": "Chemotherapy (CHOP)", "type": "chemotherapy", "doctor": "Dr. Nair", "hospital": "Manipal Hospital", "start": datetime.date(2023, 4, 1), "end": None, "total_cycles": 6, "cycles_done": 4, "status": "ongoing"},
        ],
        "symptoms": [
            {"name": "Bruising easily", "severity": 5, "date": today - datetime.timedelta(days=8)},
            {"name": "Night Sweats", "severity": 6, "date": today - datetime.timedelta(days=4)},
            {"name": "Fatigue", "severity": 7, "date": today - datetime.timedelta(days=2)},
        ],
        "readings": [
            {"marker": "WBC", "value": 48.0, "date": datetime.date(2023, 3, 1)},
            {"marker": "WBC", "value": 22.0, "date": datetime.date(2023, 5, 1)},
            {"marker": "WBC", "value": 9.5, "date": datetime.date(2023, 7, 1)},
            {"marker": "WBC", "value": 7.2, "date": datetime.date(2023, 9, 1)},
            {"marker": "RBC", "value": 2.8, "date": datetime.date(2023, 3, 1)},
            {"marker": "RBC", "value": 3.2, "date": datetime.date(2023, 5, 1)},
            {"marker": "RBC", "value": 3.8, "date": datetime.date(2023, 7, 1)},
            {"marker": "RBC", "value": 4.2, "date": datetime.date(2023, 9, 1)},
            {"marker": "Platelet", "value": 85.0, "date": datetime.date(2023, 3, 1)},
            {"marker": "Platelet", "value": 120.0, "date": datetime.date(2023, 5, 1)},
            {"marker": "Platelet", "value": 165.0, "date": datetime.date(2023, 7, 1)},
            {"marker": "Platelet", "value": 210.0, "date": datetime.date(2023, 9, 1)},
            {"marker": "LDH", "value": 480.0, "date": datetime.date(2023, 3, 1)},
            {"marker": "LDH", "value": 320.0, "date": datetime.date(2023, 5, 1)},
            {"marker": "LDH", "value": 210.0, "date": datetime.date(2023, 7, 1)},
            {"marker": "LDH", "value": 155.0, "date": datetime.date(2023, 9, 1)},
            {"marker": "Beta-2", "value": 4.8, "date": datetime.date(2023, 3, 1)},
            {"marker": "Beta-2", "value": 3.5, "date": datetime.date(2023, 5, 1)},
            {"marker": "Beta-2", "value": 2.4, "date": datetime.date(2023, 7, 1)},
            {"marker": "Beta-2", "value": 1.8, "date": datetime.date(2023, 9, 1)},
        ],
    },
    {
        "username": "Vikram", "password": "vikram123",
        "email": "vikram@example.com", "dob": datetime.date(1972, 6, 30),
        "blood_group": "A-", "phone": "9876501005", "address": "Chennai, Tamil Nadu",
        "cancer": "Lung", "diagnosis_date": datetime.date(2022, 11, 1),
        "appointments": [
            {"doctor": "Dr. Rajan", "hospital": "Apollo Hospital Chennai", "date": today + datetime.timedelta(days=10), "time": datetime.time(14, 0), "purpose": "CT scan review", "status": "upcoming"},
        ],
        "medications": [
            {"name": "Gefitinib", "dosage": "250mg", "frequency": "once", "start": datetime.date(2022, 12, 1), "end": None},
            {"name": "Ondansetron", "dosage": "8mg", "frequency": "twice", "start": datetime.date(2022, 12, 1), "end": None},
        ],
        "treatments": [
            {"name": "Targeted Therapy", "type": "targeted", "doctor": "Dr. Rajan", "hospital": "Apollo Hospital", "start": datetime.date(2022, 12, 1), "end": None, "total_cycles": None, "cycles_done": 0, "status": "ongoing"},
        ],
        "symptoms": [
            {"name": "Shortness of Breath", "severity": 5, "date": today - datetime.timedelta(days=14)},
            {"name": "Cough", "severity": 4, "date": today - datetime.timedelta(days=7)},
        ],
        "readings": [
            {"marker": "CEA", "value": 18.5, "date": datetime.date(2022, 11, 1)},
            {"marker": "CEA", "value": 12.0, "date": datetime.date(2023, 2, 1)},
            {"marker": "CEA", "value": 7.5, "date": datetime.date(2023, 5, 1)},
            {"marker": "CEA", "value": 4.2, "date": datetime.date(2023, 8, 1)},
            {"marker": "CYFRA", "value": 8.2, "date": datetime.date(2022, 11, 1)},
            {"marker": "CYFRA", "value": 5.8, "date": datetime.date(2023, 2, 1)},
            {"marker": "CYFRA", "value": 3.5, "date": datetime.date(2023, 5, 1)},
            {"marker": "CYFRA", "value": 2.1, "date": datetime.date(2023, 8, 1)},
            {"marker": "NSE", "value": 22.0, "date": datetime.date(2022, 11, 1)},
            {"marker": "NSE", "value": 16.5, "date": datetime.date(2023, 2, 1)},
            {"marker": "NSE", "value": 12.0, "date": datetime.date(2023, 5, 1)},
            {"marker": "NSE", "value": 8.5, "date": datetime.date(2023, 8, 1)},
            {"marker": "SCC Antigen", "value": 3.2, "date": datetime.date(2022, 11, 1)},
            {"marker": "SCC Antigen", "value": 2.1, "date": datetime.date(2023, 2, 1)},
            {"marker": "SCC Antigen", "value": 1.4, "date": datetime.date(2023, 5, 1)},
            {"marker": "SCC Antigen", "value": 0.9, "date": datetime.date(2023, 8, 1)},
        ],
    },
    {
        "username": "Meera", "password": "meera123",
        "email": "meera@example.com", "dob": datetime.date(1988, 9, 18),
        "blood_group": "O-", "phone": "9876501006", "address": "Hyderabad, Telangana",
        "cancer": "Ovarian", "diagnosis_date": datetime.date(2022, 2, 10),
        "appointments": [
            {"doctor": "Dr. Reddy", "hospital": "KIMS Hospital", "date": today + datetime.timedelta(days=18), "time": datetime.time(11, 30), "purpose": "CA-125 review", "status": "upcoming"},
        ],
        "medications": [
            {"name": "Olaparib", "dosage": "300mg", "frequency": "twice", "start": datetime.date(2022, 9, 1), "end": None},
        ],
        "treatments": [
            {"name": "Chemotherapy (Carboplatin + Paclitaxel)", "type": "chemotherapy", "doctor": "Dr. Reddy", "hospital": "KIMS Hospital", "start": datetime.date(2022, 3, 1), "end": datetime.date(2022, 8, 1), "total_cycles": 6, "cycles_done": 6, "status": "completed"},
        ],
        "symptoms": [
            {"name": "Bloating", "severity": 4, "date": today - datetime.timedelta(days=10)},
            {"name": "Fatigue", "severity": 5, "date": today - datetime.timedelta(days=5)},
        ],
        "readings": [
            {"marker": "CA-125", "value": 320.0, "date": datetime.date(2022, 2, 10)},
            {"marker": "CA-125", "value": 180.0, "date": datetime.date(2022, 5, 1)},
            {"marker": "CA-125", "value": 65.0, "date": datetime.date(2022, 8, 1)},
            {"marker": "CA-125", "value": 28.0, "date": datetime.date(2023, 1, 1)},
            {"marker": "HE4", "value": 185.0, "date": datetime.date(2022, 2, 10)},
            {"marker": "HE4", "value": 142.0, "date": datetime.date(2022, 5, 1)},
            {"marker": "HE4", "value": 98.0, "date": datetime.date(2022, 8, 1)},
            {"marker": "HE4", "value": 72.0, "date": datetime.date(2023, 1, 1)},
        ],
    },
    {
        "username": "Arjun", "password": "arjun123",
        "email": "arjun@example.com", "dob": datetime.date(1980, 4, 25),
        "blood_group": "B-", "phone": "9876501007", "address": "Kolkata, West Bengal",
        "cancer": "Colorectal", "diagnosis_date": datetime.date(2021, 6, 5),
        "appointments": [
            {"doctor": "Dr. Bose", "hospital": "AMRI Hospital", "date": today + datetime.timedelta(days=30), "time": datetime.time(9, 30), "purpose": "CEA monitoring", "status": "upcoming"},
        ],
        "medications": [
            {"name": "Iron Supplement", "dosage": "325mg", "frequency": "once", "start": datetime.date(2021, 7, 1), "end": None},
        ],
        "treatments": [
            {"name": "Surgery (Hemicolectomy)", "type": "surgery", "doctor": "Dr. Bose", "hospital": "AMRI Hospital", "start": datetime.date(2021, 7, 1), "end": datetime.date(2021, 7, 1), "total_cycles": None, "cycles_done": 0, "status": "completed"},
            {"name": "Chemotherapy (FOLFOX)", "type": "chemotherapy", "doctor": "Dr. Bose", "hospital": "AMRI Hospital", "start": datetime.date(2021, 8, 1), "end": datetime.date(2022, 2, 1), "total_cycles": 12, "cycles_done": 12, "status": "completed"},
        ],
        "symptoms": [
            {"name": "Abdominal Discomfort", "severity": 3, "date": today - datetime.timedelta(days=20)},
            {"name": "Fatigue", "severity": 2, "date": today - datetime.timedelta(days=10)},
        ],
        "readings": [
            {"marker": "CEA", "value": 15.2, "date": datetime.date(2021, 6, 5)},
            {"marker": "CEA", "value": 8.5, "date": datetime.date(2021, 10, 1)},
            {"marker": "CEA", "value": 4.1, "date": datetime.date(2022, 3, 1)},
            {"marker": "CEA", "value": 2.3, "date": datetime.date(2022, 9, 1)},
            {"marker": "CA 19-9", "value": 42.0, "date": datetime.date(2021, 6, 5)},
            {"marker": "CA 19-9", "value": 28.0, "date": datetime.date(2021, 10, 1)},
            {"marker": "CA 19-9", "value": 18.0, "date": datetime.date(2022, 3, 1)},
            {"marker": "CA 19-9", "value": 10.0, "date": datetime.date(2022, 9, 1)},
        ],
    },
    {
        "username": "Kavya", "password": "kavya123",
        "email": "kavya@example.com", "dob": datetime.date(1993, 12, 8),
        "blood_group": "AB-", "phone": "9876501008", "address": "Ahmedabad, Gujarat",
        "cancer": "Cervical", "diagnosis_date": datetime.date(2023, 6, 1),
        "appointments": [
            {"doctor": "Dr. Patel", "hospital": "Sterling Hospital", "date": today + datetime.timedelta(days=12), "time": datetime.time(10, 0), "purpose": "Post-radiation check", "status": "upcoming"},
        ],
        "medications": [
            {"name": "Folic Acid", "dosage": "5mg", "frequency": "once", "start": datetime.date(2023, 7, 1), "end": None},
        ],
        "treatments": [
            {"name": "Chemoradiation", "type": "radiation", "doctor": "Dr. Patel", "hospital": "Sterling Hospital", "start": datetime.date(2023, 7, 1), "end": datetime.date(2023, 9, 1), "total_cycles": 25, "cycles_done": 25, "status": "completed"},
        ],
        "symptoms": [
            {"name": "Pelvic Pain", "severity": 4, "date": today - datetime.timedelta(days=15)},
            {"name": "Fatigue", "severity": 5, "date": today - datetime.timedelta(days=7)},
        ],
        "readings": [
            {"marker": "SCC", "value": 4.8, "date": datetime.date(2023, 6, 1)},
            {"marker": "SCC", "value": 2.9, "date": datetime.date(2023, 8, 1)},
            {"marker": "SCC", "value": 1.2, "date": datetime.date(2023, 10, 1)},
            {"marker": "CEA", "value": 6.5, "date": datetime.date(2023, 6, 1)},
            {"marker": "CEA", "value": 4.2, "date": datetime.date(2023, 8, 1)},
            {"marker": "CEA", "value": 2.8, "date": datetime.date(2023, 10, 1)},
        ],
    },
    {
        "username": "Suresh", "password": "suresh123",
        "email": "suresh@example.com", "dob": datetime.date(1965, 8, 3),
        "blood_group": "A+", "phone": "9876501009", "address": "Jaipur, Rajasthan",
        "cancer": "Liver", "diagnosis_date": datetime.date(2022, 9, 14),
        "appointments": [
            {"doctor": "Dr. Gupta", "hospital": "Fortis Hospital Jaipur", "date": today + datetime.timedelta(days=8), "time": datetime.time(15, 0), "purpose": "AFP monitoring", "status": "upcoming"},
        ],
        "medications": [
            {"name": "Sorafenib", "dosage": "400mg", "frequency": "twice", "start": datetime.date(2022, 10, 1), "end": None},
        ],
        "treatments": [
            {"name": "Targeted Therapy (Sorafenib)", "type": "targeted", "doctor": "Dr. Gupta", "hospital": "Fortis Hospital", "start": datetime.date(2022, 10, 1), "end": None, "total_cycles": None, "cycles_done": 0, "status": "ongoing"},
        ],
        "symptoms": [
            {"name": "Jaundice", "severity": 4, "date": today - datetime.timedelta(days=18)},
            {"name": "Abdominal Pain", "severity": 5, "date": today - datetime.timedelta(days=9)},
            {"name": "Loss of Appetite", "severity": 6, "date": today - datetime.timedelta(days=4)},
        ],
        "readings": [
            {"marker": "AFP", "value": 850.0, "date": datetime.date(2022, 9, 14)},
            {"marker": "AFP", "value": 520.0, "date": datetime.date(2023, 1, 1)},
            {"marker": "AFP", "value": 280.0, "date": datetime.date(2023, 5, 1)},
            {"marker": "AFP", "value": 95.0, "date": datetime.date(2023, 9, 1)},
            {"marker": "ALT", "value": 85.0, "date": datetime.date(2022, 9, 14)},
            {"marker": "ALT", "value": 68.0, "date": datetime.date(2023, 1, 1)},
            {"marker": "ALT", "value": 52.0, "date": datetime.date(2023, 5, 1)},
            {"marker": "ALT", "value": 38.0, "date": datetime.date(2023, 9, 1)},
            {"marker": "AST", "value": 92.0, "date": datetime.date(2022, 9, 14)},
            {"marker": "AST", "value": 74.0, "date": datetime.date(2023, 1, 1)},
            {"marker": "AST", "value": 55.0, "date": datetime.date(2023, 5, 1)},
            {"marker": "AST", "value": 40.0, "date": datetime.date(2023, 9, 1)},
        ],
    },
    {
        "username": "Divya", "password": "divya123",
        "email": "divya@example.com", "dob": datetime.date(1983, 5, 17),
        "blood_group": "O+", "phone": "9876501010", "address": "Lucknow, Uttar Pradesh",
        "cancer": "Pancreatic", "diagnosis_date": datetime.date(2023, 4, 20),
        "appointments": [
            {"doctor": "Dr. Singh", "hospital": "SGPGI Lucknow", "date": today + datetime.timedelta(days=15), "time": datetime.time(11, 0), "purpose": "CA 19-9 review", "status": "upcoming"},
        ],
        "medications": [
            {"name": "Gemcitabine", "dosage": "1000mg/m²", "frequency": "weekly", "start": datetime.date(2023, 5, 1), "end": None},
            {"name": "Pancreatic Enzyme Supplement", "dosage": "25000 units", "frequency": "thrice", "start": datetime.date(2023, 5, 1), "end": None},
        ],
        "treatments": [
            {"name": "Chemotherapy (FOLFIRINOX)", "type": "chemotherapy", "doctor": "Dr. Singh", "hospital": "SGPGI Lucknow", "start": datetime.date(2023, 5, 1), "end": None, "total_cycles": 12, "cycles_done": 6, "status": "ongoing"},
        ],
        "symptoms": [
            {"name": "Back Pain", "severity": 6, "date": today - datetime.timedelta(days=12)},
            {"name": "Nausea", "severity": 5, "date": today - datetime.timedelta(days=6)},
            {"name": "Weight Loss", "severity": 7, "date": today - datetime.timedelta(days=3)},
        ],
        "readings": [
            {"marker": "CA 19-9", "value": 1240.0, "date": datetime.date(2023, 4, 20)},
            {"marker": "CA 19-9", "value": 780.0, "date": datetime.date(2023, 6, 1)},
            {"marker": "CA 19-9", "value": 420.0, "date": datetime.date(2023, 8, 1)},
            {"marker": "CA 19-9", "value": 185.0, "date": datetime.date(2023, 10, 1)},
            {"marker": "CEA", "value": 12.0, "date": datetime.date(2023, 4, 20)},
            {"marker": "CEA", "value": 8.5, "date": datetime.date(2023, 6, 1)},
            {"marker": "CEA", "value": 5.2, "date": datetime.date(2023, 8, 1)},
            {"marker": "CEA", "value": 3.1, "date": datetime.date(2023, 10, 1)},
        ],
    },
]


class Command(BaseCommand):
    help = "Seeds 10 sample patients with full data"

    def handle(self, *args, **kwargs):
        self.stdout.write("\n👥  Oncocare — Seeding Patient Data\n")
        self.stdout.write("─" * 45 + "\n")

        today = datetime.date.today()

        for p in PATIENTS:
            username = p["username"].capitalize()

            if User.objects.filter(username=username).exists():
                self.stdout.write(f"  → Already exists: {username}, skipping.")
                continue

            # User
            user = User.objects.create_user(
                username=username,
                password=p["password"],
                email=p["email"],
                first_name=username,
            )

            # Patient Profile
            profile = PatientProfile.objects.create(
                user=user,
                phone=p["phone"],
                date_of_birth=p["dob"],
                blood_group=p["blood_group"],
                address=p["address"],
            )

            # Cancer Profile
            cancer_type = get_cancer(p["cancer"])
            if cancer_type:
                cancer_profile = PatientCancerProfile.objects.create(
                    patient=profile,
                    cancer_type=cancer_type,
                    diagnosis_date=p["diagnosis_date"],
                )

                # Biomarker Readings
                for r in p["readings"]:
                    marker = CancerMarker.objects.filter(
                        cancer_type=cancer_type,
                        marker_name__icontains=r["marker"]
                    ).first()
                    if marker:
                        BiomarkerReading.objects.create(
                            cancer_profile=cancer_profile,
                            marker=marker,
                            value=r["value"],
                            reading_date=r["date"],
                        )
            else:
                self.stdout.write(
                    self.style.WARNING(f"  ⚠️  Cancer type not found for {username}: {p['cancer']}")
                )

            # Appointments
            for a in p["appointments"]:
                Appointment.objects.create(
                    patient=profile,
                    doctor_name=a["doctor"],
                    hospital_name=a["hospital"],
                    appointment_date=a["date"],
                    appointment_time=a["time"],
                    purpose=a["purpose"],
                    status=a["status"],
                )

            # Medications
            for m in p["medications"]:
                Medication.objects.create(
                    patient=profile,
                    medicine_name=m["name"],
                    dosage=m["dosage"],
                    frequency=m["frequency"],
                    start_date=m["start"],
                    end_date=m["end"],
                )

            # Treatments
            for t in p["treatments"]:
                Treatment.objects.create(
                    patient=profile,
                    treatment_name=t["name"],
                    treatment_type=t["type"],
                    doctor_name=t["doctor"],
                    hospital_name=t["hospital"],
                    start_date=t["start"],
                    end_date=t["end"],
                    total_cycles=t["total_cycles"],
                    cycles_completed=t["cycles_done"],
                    status=t["status"],
                )

            # Symptoms
            for s in p["symptoms"]:
                Symptom.objects.create(
                    patient=profile,
                    symptom_name=s["name"],
                    severity=s["severity"],
                    symptom_date=s["date"],
                )

            self.stdout.write(
                self.style.SUCCESS(f"  ✓ Created: {username} / {p['password']}")
            )

        self.stdout.write("\n" + "─" * 45)
        self.stdout.write(self.style.SUCCESS("\n✅  All patients seeded successfully!\n"))