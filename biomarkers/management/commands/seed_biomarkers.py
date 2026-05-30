"""
Oncocare — Biomarker Seed Command
Usage:  python manage.py seed_biomarkers

Place this file at:
  biomarkers/management/__init__.py          (empty)
  biomarkers/management/commands/__init__.py (empty)
  biomarkers/management/commands/seed_biomarkers.py  ← this file

Then run:
  python manage.py seed_biomarkers
"""

from django.core.management.base import BaseCommand
from biomarkers.models import CancerType, CancerMarker


# ── ALL CANCER DATA ──────────────────────────────────────────────────────────

CANCER_DATA = [

    {
        "cancer_name": "Thyroid Cancer",
        "description": (
            "Thyroid cancer originates in the thyroid gland. "
            "The most common types are papillary and follicular. "
            "After treatment (surgery/RAI), blood markers are monitored "
            "to detect any recurrence or residual disease."
        ),
        "markers": [
            {
                "marker_name": "Thyroglobulin (Tg)",
                "unit": "ng/mL",
                "expected_trend": "decrease",
                "guidance_text": (
                    "Thyroglobulin is a protein made only by thyroid cells. "
                    "After thyroid removal, your Tg should drop to near zero. "
                    "A rising Tg may indicate recurrence and should be discussed "
                    "with your oncologist immediately."
                ),
            },
            {
                "marker_name": "TSH (Thyroid Stimulating Hormone)",
                "unit": "mIU/L",
                "expected_trend": "suppress",
                "guidance_text": (
                    "For thyroid cancer patients, TSH is intentionally kept low "
                    "(suppressed) using levothyroxine therapy. This prevents any "
                    "remaining cancer cells from growing. Your target TSH range "
                    "will be set by your doctor based on your risk level."
                ),
            },
            {
                "marker_name": "Anti-Thyroglobulin Antibody (Anti-Tg)",
                "unit": "IU/mL",
                "expected_trend": "decrease",
                "guidance_text": (
                    "Anti-Tg antibodies can interfere with the Tg test and make "
                    "it unreliable. High Anti-Tg levels should gradually fall after "
                    "successful treatment. If they remain high or rise, it may signal "
                    "persistent disease even when Tg appears normal."
                ),
            },
        ],
    },

    {
        "cancer_name": "Breast Cancer",
        "description": (
            "Breast cancer is the most common cancer in women. "
            "Tumour markers help monitor treatment response and detect recurrence. "
            "They are not used alone for diagnosis but are valuable for tracking."
        ),
        "markers": [
            {
                "marker_name": "CA 15-3",
                "unit": "U/mL",
                "expected_trend": "decrease",
                "guidance_text": (
                    "CA 15-3 is the most commonly used breast cancer marker. "
                    "Normal range is below 30 U/mL. Falling levels during treatment "
                    "suggest the cancer is responding well. Rising levels may indicate "
                    "disease progression or recurrence."
                ),
            },
            {
                "marker_name": "CEA (Carcinoembryonic Antigen)",
                "unit": "ng/mL",
                "expected_trend": "decrease",
                "guidance_text": (
                    "CEA is a general cancer marker elevated in many cancer types "
                    "including breast cancer. Normal is below 5 ng/mL in non-smokers. "
                    "Decreasing CEA during treatment is a positive sign. It is used "
                    "alongside CA 15-3 for a more complete picture."
                ),
            },
            {
                "marker_name": "CA 27-29",
                "unit": "U/mL",
                "expected_trend": "decrease",
                "guidance_text": (
                    "CA 27-29 is similar to CA 15-3 and specifically measures "
                    "breast cancer activity. Normal is below 38 U/mL. It is used "
                    "to monitor for recurrence in women who have been treated for "
                    "stage II or III breast cancer."
                ),
            },
        ],
    },

    {
        "cancer_name": "Prostate Cancer",
        "description": (
            "Prostate cancer is the most common cancer in men. "
            "PSA is the primary marker used to screen, diagnose, and monitor "
            "prostate cancer treatment and recurrence."
        ),
        "markers": [
            {
                "marker_name": "PSA (Prostate Specific Antigen)",
                "unit": "ng/mL",
                "expected_trend": "decrease",
                "guidance_text": (
                    "PSA is produced by prostate cells. After treatment, PSA should "
                    "drop significantly. After surgery it should reach near-zero. "
                    "After radiation, a gradual decline is expected. A rising PSA "
                    "after treatment (biochemical recurrence) needs evaluation. "
                    "Normal in healthy men is typically below 4 ng/mL, though "
                    "post-treatment targets are much lower."
                ),
            },
            {
                "marker_name": "Free PSA Ratio",
                "unit": "%",
                "expected_trend": "normalize",
                "guidance_text": (
                    "Free PSA is PSA not bound to proteins. A low free-to-total PSA "
                    "ratio suggests a higher likelihood of cancer. This ratio helps "
                    "distinguish prostate cancer from benign prostate enlargement "
                    "when total PSA is in the borderline range (4–10 ng/mL)."
                ),
            },
        ],
    },

    {
        "cancer_name": "Lung Cancer",
        "description": (
            "Lung cancer is broadly divided into small cell (SCLC) and non-small "
            "cell (NSCLC) types. Several markers help monitor treatment response, "
            "though no single marker is definitive for lung cancer."
        ),
        "markers": [
            {
                "marker_name": "CEA (Carcinoembryonic Antigen)",
                "unit": "ng/mL",
                "expected_trend": "decrease",
                "guidance_text": (
                    "CEA is elevated in many NSCLC patients, especially adenocarcinoma. "
                    "Normal is below 5 ng/mL. Falling CEA during treatment indicates "
                    "response. A rising CEA during or after treatment may signal "
                    "progression or recurrence."
                ),
            },
            {
                "marker_name": "CYFRA 21-1",
                "unit": "ng/mL",
                "expected_trend": "decrease",
                "guidance_text": (
                    "CYFRA 21-1 is a fragment of cytokeratin 19, elevated in NSCLC "
                    "especially squamous cell carcinoma. Normal is below 3.3 ng/mL. "
                    "It is useful for monitoring treatment response and prognosis. "
                    "Declining levels indicate the treatment is working."
                ),
            },
            {
                "marker_name": "NSE (Neuron Specific Enolase)",
                "unit": "ng/mL",
                "expected_trend": "decrease",
                "guidance_text": (
                    "NSE is the primary marker for small cell lung cancer (SCLC). "
                    "Normal is below 16.3 ng/mL. It is used to monitor SCLC treatment "
                    "and detect relapse. Very high NSE at diagnosis usually indicates "
                    "extensive-stage SCLC."
                ),
            },
            {
                "marker_name": "SCC Antigen (Squamous Cell Carcinoma)",
                "unit": "ng/mL",
                "expected_trend": "decrease",
                "guidance_text": (
                    "SCC antigen is elevated in squamous cell carcinoma of the lung. "
                    "Normal is below 1.5 ng/mL. Used to monitor treatment response "
                    "and detect recurrence in squamous cell type specifically."
                ),
            },
        ],
    },

    {
        "cancer_name": "Blood Cancer (Leukaemia / Lymphoma)",
        "description": (
            "Blood cancers affect the production and function of blood cells. "
            "Complete blood count (CBC) markers are the primary way to monitor "
            "treatment response, recovery of normal blood cell production, and "
            "disease activity."
        ),
        "markers": [
            {
                "marker_name": "WBC (White Blood Cell Count)",
                "unit": "×10⁹/L",
                "expected_trend": "normalize",
                "guidance_text": (
                    "Normal WBC is 4.0–11.0 × 10⁹/L. In leukaemia, WBC can be "
                    "extremely high (too many abnormal cells) or low (bone marrow "
                    "failure). After chemotherapy, WBC typically drops before recovering. "
                    "The goal is for WBC to normalise within healthy range."
                ),
            },
            {
                "marker_name": "RBC (Red Blood Cell Count)",
                "unit": "×10¹²/L",
                "expected_trend": "normalize",
                "guidance_text": (
                    "Normal RBC is 4.2–5.4 × 10¹²/L for men and 3.6–5.0 for women. "
                    "Low RBC causes anaemia (fatigue, breathlessness). After treatment, "
                    "RBC should gradually return to normal as bone marrow recovers. "
                    "Transfusions may be needed during treatment."
                ),
            },
            {
                "marker_name": "Platelet Count",
                "unit": "×10⁹/L",
                "expected_trend": "normalize",
                "guidance_text": (
                    "Normal platelets are 150–400 × 10⁹/L. Low platelets (below 50) "
                    "increase bleeding risk. Chemotherapy temporarily lowers platelets. "
                    "Recovering platelet counts after treatment is a positive sign. "
                    "Your team will monitor this closely during active treatment."
                ),
            },
            {
                "marker_name": "LDH (Lactate Dehydrogenase)",
                "unit": "U/L",
                "expected_trend": "decrease",
                "guidance_text": (
                    "LDH is released when cells are damaged or destroyed. Normal is "
                    "140–280 U/L. High LDH in lymphoma indicates rapid cell turnover "
                    "and is a marker of disease burden and prognosis. Falling LDH "
                    "during treatment is a strong indicator of response."
                ),
            },
            {
                "marker_name": "Beta-2 Microglobulin (B2M)",
                "unit": "mg/L",
                "expected_trend": "decrease",
                "guidance_text": (
                    "B2M is elevated in multiple myeloma and some lymphomas. "
                    "Normal is below 2.5 mg/L. High levels indicate higher disease "
                    "burden and worse prognosis. Falling B2M during treatment "
                    "indicates the cancer is responding."
                ),
            },
        ],
    },

    {
        "cancer_name": "Liver Cancer (Hepatocellular Carcinoma)",
        "description": (
            "Hepatocellular carcinoma (HCC) is the most common primary liver cancer, "
            "often arising in the context of cirrhosis. AFP is the key marker, "
            "alongside liver function tests."
        ),
        "markers": [
            {
                "marker_name": "AFP (Alpha-Fetoprotein)",
                "unit": "ng/mL",
                "expected_trend": "decrease",
                "guidance_text": (
                    "AFP is the main liver cancer marker. Normal is below 10 ng/mL. "
                    "Very high AFP (above 400 ng/mL) strongly suggests HCC. After "
                    "surgery or ablation, AFP should drop dramatically. A rising AFP "
                    "during monitoring suggests recurrence."
                ),
            },
            {
                "marker_name": "ALT (Alanine Aminotransferase)",
                "unit": "U/L",
                "expected_trend": "decrease",
                "guidance_text": (
                    "ALT is a liver enzyme. Normal is 7–56 U/L. Elevated ALT indicates "
                    "liver cell damage. During liver cancer treatment, ALT may fluctuate. "
                    "Persistently high ALT indicates ongoing liver stress and should "
                    "be discussed with your doctor."
                ),
            },
            {
                "marker_name": "AST (Aspartate Aminotransferase)",
                "unit": "U/L",
                "expected_trend": "decrease",
                "guidance_text": (
                    "AST is another liver enzyme. Normal is 10–40 U/L. Like ALT, "
                    "high AST indicates liver damage. Monitoring AST alongside ALT "
                    "gives a fuller picture of liver health during and after treatment."
                ),
            },
        ],
    },

    {
        "cancer_name": "Ovarian Cancer",
        "description": (
            "Ovarian cancer is often detected at a late stage. CA-125 and HE4 are "
            "the primary markers used to monitor treatment response and detect "
            "recurrence after initial therapy."
        ),
        "markers": [
            {
                "marker_name": "CA-125",
                "unit": "U/mL",
                "expected_trend": "decrease",
                "guidance_text": (
                    "CA-125 is the standard ovarian cancer marker. Normal is below "
                    "35 U/mL. Levels fall during chemotherapy if it is working. "
                    "After remission, a rising CA-125 is often the first sign of "
                    "recurrence — sometimes months before symptoms appear."
                ),
            },
            {
                "marker_name": "HE4 (Human Epididymis Protein 4)",
                "unit": "pmol/L",
                "expected_trend": "decrease",
                "guidance_text": (
                    "HE4 is more specific than CA-125 and is less affected by "
                    "endometriosis or benign conditions. Normal is below 140 pmol/L "
                    "in premenopausal women. Used alongside CA-125, it improves "
                    "the accuracy of recurrence monitoring."
                ),
            },
        ],
    },

    {
        "cancer_name": "Colorectal Cancer",
        "description": (
            "Colorectal cancer includes cancers of the colon and rectum. "
            "CEA is the primary marker used for monitoring after surgery and "
            "detecting recurrence."
        ),
        "markers": [
            {
                "marker_name": "CEA (Carcinoembryonic Antigen)",
                "unit": "ng/mL",
                "expected_trend": "decrease",
                "guidance_text": (
                    "CEA is the standard marker for colorectal cancer. Normal is "
                    "below 5 ng/mL (below 2.5 in non-smokers). After surgery, CEA "
                    "should drop to normal within 4–6 weeks. A rising CEA during "
                    "follow-up is a strong indicator of recurrence and requires "
                    "immediate investigation."
                ),
            },
            {
                "marker_name": "CA 19-9",
                "unit": "U/mL",
                "expected_trend": "decrease",
                "guidance_text": (
                    "CA 19-9 can be elevated in colorectal cancer and is used as a "
                    "supplementary marker alongside CEA. Normal is below 37 U/mL. "
                    "It is less specific but can be useful when CEA alone is not "
                    "elevated despite disease activity."
                ),
            },
        ],
    },

    {
        "cancer_name": "Pancreatic Cancer",
        "description": (
            "Pancreatic cancer is often diagnosed at an advanced stage. "
            "CA 19-9 is the primary marker used to monitor treatment response "
            "and detect recurrence."
        ),
        "markers": [
            {
                "marker_name": "CA 19-9",
                "unit": "U/mL",
                "expected_trend": "decrease",
                "guidance_text": (
                    "CA 19-9 is the main pancreatic cancer marker. Normal is below "
                    "37 U/mL. Very high levels (above 1000 U/mL) usually indicate "
                    "unresectable disease. Falling CA 19-9 during chemotherapy "
                    "indicates response. After surgery, levels should normalise. "
                    "A rising CA 19-9 suggests recurrence."
                ),
            },
            {
                "marker_name": "CEA (Carcinoembryonic Antigen)",
                "unit": "ng/mL",
                "expected_trend": "decrease",
                "guidance_text": (
                    "CEA is used as a supplementary marker in pancreatic cancer. "
                    "Normal is below 5 ng/mL. Used alongside CA 19-9 for a more "
                    "complete monitoring picture, especially when CA 19-9 is not "
                    "elevated due to certain blood type factors."
                ),
            },
        ],
    },

    {
        "cancer_name": "Cervical Cancer",
        "description": (
            "Cervical cancer is caused primarily by HPV infection. "
            "SCC antigen is the main marker for squamous cell type, "
            "the most common form."
        ),
        "markers": [
            {
                "marker_name": "SCC Antigen (Squamous Cell Carcinoma Antigen)",
                "unit": "ng/mL",
                "expected_trend": "decrease",
                "guidance_text": (
                    "SCC antigen is elevated in squamous cell cervical cancer. "
                    "Normal is below 1.5 ng/mL. Levels fall with successful "
                    "treatment (surgery or chemoradiation). Rising SCC after "
                    "treatment suggests recurrence. Monitored at each follow-up visit."
                ),
            },
            {
                "marker_name": "CEA (Carcinoembryonic Antigen)",
                "unit": "ng/mL",
                "expected_trend": "decrease",
                "guidance_text": (
                    "CEA may be elevated in adenocarcinoma of the cervix. "
                    "Normal is below 5 ng/mL. Used alongside SCC antigen to give "
                    "a fuller picture, especially for the rarer adenocarcinoma type."
                ),
            },
        ],
    },

]


# ── COMMAND ──────────────────────────────────────────────────────────────────

class Command(BaseCommand):
    help = "Seeds all cancer types and their biomarkers into the database."

    def handle(self, *args, **kwargs):
        self.stdout.write("\n🔬  Oncocare — Seeding Biomarker Data\n")
        self.stdout.write("─" * 45 + "\n")

        created_types   = 0
        skipped_types   = 0
        created_markers = 0
        skipped_markers = 0

        for cancer in CANCER_DATA:

            # Create or get cancer type
            ct, ct_created = CancerType.objects.get_or_create(
                cancer_name=cancer["cancer_name"],
                defaults={"description": cancer["description"]},
            )

            if ct_created:
                created_types += 1
                self.stdout.write(
                    self.style.SUCCESS(f"  ✓ Created: {ct.cancer_name}")
                )
            else:
                skipped_types += 1
                self.stdout.write(
                    f"  → Already exists: {ct.cancer_name}"
                )

            # Create markers for this cancer type
            for m in cancer["markers"]:
                marker, m_created = CancerMarker.objects.get_or_create(
                    cancer_type=ct,
                    marker_name=m["marker_name"],
                    defaults={
                        "unit":           m["unit"],
                        "expected_trend": m["expected_trend"],
                        "guidance_text":  m["guidance_text"],
                    },
                )

                if m_created:
                    created_markers += 1
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"      ✓ Marker: {marker.marker_name} ({marker.unit})"
                        )
                    )
                else:
                    skipped_markers += 1
                    self.stdout.write(
                        f"      → Already exists: {marker.marker_name}"
                    )

        self.stdout.write("\n" + "─" * 45)
        self.stdout.write(
            self.style.SUCCESS(
                f"\n✅  Done!\n"
                f"    Cancer types  — created: {created_types}, skipped: {skipped_types}\n"
                f"    Markers       — created: {created_markers}, skipped: {skipped_markers}\n"
            )
        )
        self.stdout.write(
            "    You can re-run this command safely at any time.\n"
            "    Existing records will be skipped, not duplicated.\n\n"
        )