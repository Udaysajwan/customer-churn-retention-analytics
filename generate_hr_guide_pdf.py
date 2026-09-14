# -*- coding: utf-8 -*-
"""
PDF Generator: HR & Interview Discussion Guide
Equips the candidate to present, explain, and defend the Customer Churn & Retention Analytics
project across HR recruiter screenings, hiring manager interviews, and technical deep dives.
"""

import os
import shutil
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfgen import canvas


class NumberedCanvas(canvas.Canvas):
    """Canvas that calculates total page count and adds running headers/footers."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))
        
        # Running Header (pages 2+)
        if self._pageNumber > 1:
            self.drawString(54, 750, "Customer Churn Analytics | HR & Technical Interview Discussion Playbook")
            self.setStrokeColor(colors.HexColor("#cbd5e1"))
            self.setLineWidth(0.5)
            self.line(54, 744, 558, 744)
            
        # Running Footer (all pages)
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.5)
        self.line(54, 42, 558, 42)
        self.drawString(54, 30, "Candidate Interview Reference Guide | Customer Churn & Retention Analytics")
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 30, page_text)
            
        self.restoreState()


def create_callout(text, style, bg_color="#f1f5f9", border_color="#2563eb", width=504):
    """Creates a professional callout box with a colored left accent border."""
    p = Paragraph(text, style)
    t = Table([[p]], colWidths=[width])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor(bg_color)),
        ('LINELEFT', (0, 0), (0, -1), 3.5, colors.HexColor(border_color)),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    return t


def build_hr_guide_pdf(output_pdf_path):
    doc = SimpleDocTemplate(
        output_pdf_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=50,
        bottomMargin=48
    )
    
    styles = getSampleStyleSheet()
    
    # Custom Color Palette
    c_primary = colors.HexColor("#0f172a")      # Slate Dark
    c_accent = colors.HexColor("#1e40af")       # Deep Blue
    c_teal = colors.HexColor("#0369a1")         # Ocean Blue
    c_emerald = colors.HexColor("#047857")      # Forest Emerald
    c_amber = colors.HexColor("#b45309")        # Dark Amber
    c_text = colors.HexColor("#1e293b")         # Body Charcoal
    c_text_muted = colors.HexColor("#475569")   # Slate Muted
    c_bg_light = colors.HexColor("#f8fafc")     # Light Grey
    c_border = colors.HexColor("#cbd5e1")       # Border Slate
    
    # Custom Typography Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=c_primary,
        alignment=TA_LEFT
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=c_accent,
        alignment=TA_LEFT
    )
    
    meta_style = ParagraphStyle(
        'DocMeta',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=c_text_muted,
        alignment=TA_LEFT
    )
    
    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=c_accent,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )
    
    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.8,
        leading=13,
        textColor=c_primary,
        spaceBefore=6,
        spaceAfter=2,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'BodyMain',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=c_text,
        alignment=TA_LEFT,
        spaceAfter=3
    )
    
    script_style = ParagraphStyle(
        'ScriptBox',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.2,
        leading=11.6,
        textColor=colors.HexColor("#0f172a"),
        alignment=TA_LEFT
    )
    
    table_hdr = ParagraphStyle(
        'TableHdr',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.8,
        leading=10,
        textColor=colors.white,
        alignment=TA_LEFT
    )
    
    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=10,
        textColor=c_text,
        alignment=TA_LEFT
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=10,
        textColor=c_primary,
        alignment=TA_LEFT
    )
    
    story = []
    
    # -------------------------------------------------------------
    # PAGE 1: TITLE, PURPOSE, & ELEVATOR PITCHES
    # -------------------------------------------------------------
    story.append(Paragraph("Customer Churn & Retention Analytics", title_style))
    story.append(Spacer(1, 2))
    story.append(Paragraph("HR & Technical Interview Discussion Playbook: End-to-End Candidate Guide", subtitle_style))
    story.append(Spacer(1, 2))
    story.append(Paragraph(
        "<b>Target Audience:</b> HR Recruiters, Talent Acquisition, Hiring Managers, and Technical Leads &nbsp;|&nbsp; "
        "<b>Focus:</b> Subscriber Intelligence, Predictive Risk Modeling, SQL Analytics & Financial ROI",
        meta_style
    ))
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width="100%", thickness=1.2, color=c_accent, spaceBefore=2, spaceAfter=6))
    
    # Purpose Banner
    intro_callout = (
        "<b>Why This Playbook Exists:</b> This document translates every line of code, machine learning algorithm, "
        "SQL query, and financial metric in the <i>Customer Churn & Retention Analytics</i> project into high-impact talking points. "
        "Whether speaking to a non-technical HR screener testing communication and business acumen, or a lead data scientist probing "
        "classification trade-offs, this guide provides calibrated, battle-tested explanations."
    )
    story.append(create_callout(intro_callout, body_style, bg_color="#eff6ff", border_color="#1e40af"))
    story.append(Spacer(1, 7))
    
    # Section 1: Elevator Pitches
    story.append(Paragraph("1. The Elevator Pitches: How to Introduce the Project", h1_style))
    story.append(Paragraph(
        "When an interviewer asks: <i>\"Tell me about a key data project on your resume\"</i> or <i>\"Can you walk me through your customer churn analytics project?\"</i>, "
        "use the appropriate version below based on time and audience:",
        body_style
    ))
    story.append(Spacer(1, 3))
    
    pitch_30 = (
        "<b>THE 30-SECOND RECRUITER HOOK (Ideal for HR Screenings & Quick Intros):</b><br/>"
        "\"In my Customer Churn & Retention Analytics project, I built an end-to-end subscriber intelligence pipeline "
        "analyzing 10,000 telecommunications accounts leaking over <b>$231,000 in monthly recurring revenue</b>. I audited dirty billing data, "
        "discovered that customer support friction is the single greatest tipping point for cancellation, and trained a predictive machine learning model "
        "that intercepts <b>75% of at-risk subscribers</b> before they leave. Most importantly, I translated predictions into a targeted <b>$85 concierge retention campaign</b> "
        "that preserves <b>$78,000 in annual revenue</b> at an audited <b>175% net ROI</b>.\""
    )
    story.append(create_callout(pitch_30, script_style, bg_color="#f8fafc", border_color="#059669"))
    story.append(Spacer(1, 5))
    
    pitch_2m = (
        "<b>THE 2-MINUTE DEEP DIVE (Ideal for Hiring Managers & Technical Leads):</b><br/>"
        "\"The goal of this project was to solve a high-stakes business problem: in subscription telecom, customer acquisition costs 5 to 7 times more "
        "than retention. I built a production-grade data science workflow starting from raw billing and usage telemetry.<br/>"
        "• <b>Data Engineering & Cleansing:</b> I discovered a hidden formatting defect where 266 new signups contained blank whitespace in Total Charges. Rather than naively deleting them, I investigated the root cause, established they were month-zero accounts, and imputed $0.00 to prevent survivorship bias.<br/>"
        "• <b>Exploratory Data Analysis:</b> I uncovered empirical behavioral cliffs: subscribers submitting >3 support tickets experienced an 81.7% churn cliff, and month-to-month contracts had a 4.0x churn hazard compared to two-year agreements.<br/>"
        "• <b>Predictive ML & Cost Matrix:</b> I trained Logistic Regression, Random Forest, and XGBoost. Crucially, because the business cost of a false negative (losing an $1,848 lifetime value customer) dwarfs a false positive (a $15-$25 retention offer), I prioritized <b>Recall</b>. Logistic Regression achieved <b>74.88% Recall and 0.787 ROC-AUC</b> with full interpretability.<br/>"
        "• <b>Executive Impact:</b> I authored ANSI SQL window functions for cohort retention, built an interactive browser dashboard simulator, and designed a concierge retention campaign saving 87 accounts and $78,060 annually with a 175.5% net campaign ROI.\""
    )
    story.append(create_callout(pitch_2m, script_style, bg_color="#f8fafc", border_color="#1e40af"))
    story.append(Spacer(1, 7))
    
    # Section 2: STAR Framework Overview
    story.append(Paragraph("2. The STAR Method Breakdown (Behavioral & Competency Alignment)", h1_style))
    story.append(Paragraph(
        "Recruiters evaluate candidates on structured problem solving. Here is how this project maps directly to the standard STAR methodology:",
        body_style
    ))
    
    star_data = [
        [Paragraph("<b>Stage</b>", table_hdr), Paragraph("<b>Project Realization & Evidence</b>", table_hdr)],
        [
            Paragraph("<b>Situation</b>", table_cell_bold),
            Paragraph("Telecommunications subscription model experiencing a <b>26.5% baseline churn rate</b>, resulting in <b>$231,895 lost in monthly recurring revenue</b> (a 34.8% revenue loss ratio). High Customer Acquisition Cost (CAC) made replacing lost accounts unsustainable.", table_cell)
        ],
        [
            Paragraph("<b>Task</b>", table_cell_bold),
            Paragraph("Audit raw uncleaned subscriber logs, engineer predictive behavioral features, benchmark machine learning models to identify at-risk subscribers prior to billing cycles, and model a financially viable retention strategy with positive net ROI.", table_cell)
        ],
        [
            Paragraph("<b>Action</b>", table_cell_bold),
            Paragraph("• Isolated 266 hidden whitespace charge records; imputed $0.00 for tenure-zero accounts.<br/>"
                      "• Engineered domain features: <i>Average_Monthly_Spend</i>, <i>Support_Ticket_Frequency</i>, and tenure cohorts.<br/>"
                      "• Evaluated Logistic Regression, Random Forest, and XGBoost under class-weighted loss.<br/>"
                      "• Authored ANSI SQL CTEs/window functions and designed an interactive web simulator and Tableau data model.", table_cell)
        ],
        [
            Paragraph("<b>Result</b>", table_cell_bold),
            Paragraph("• Deployed Logistic Regression delivering <b>74.88% Recall</b> and <b>0.7869 ROC-AUC</b>.<br/>"
                      "• Formulated targeted retention campaign for early-tenure high-friction subscribers rescuing <b>87 accounts</b>, preserving <b>$78,060 in annual revenue</b> at a <b>175.51% net campaign ROI</b>.", table_cell)
        ]
    ]
    t_star = Table(star_data, colWidths=[65, 439])
    t_star.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_accent),
        ('GRID', (0, 0), (-1, -1), 0.5, c_border),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_bg_light])
    ]))
    story.append(t_star)
    
    # -------------------------------------------------------------
    # PAGE 2: TOUGH QUESTIONS & MODEL ANSWERS (PART 1)
    # -------------------------------------------------------------
    story.append(PageBreak())
    story.append(Paragraph("3. Anticipated Interview Questions & High-Impact Model Answers", h1_style))
    story.append(Paragraph(
        "Below are the 6 most challenging questions interviewers ask regarding this project, paired with exact word-for-word talking points:",
        body_style
    ))
    story.append(Spacer(1, 3))
    
    # Q1: Data Quality & Cleansing
    story.append(Paragraph("Q1: \"Tell me about a time you handled dirty, missing, or malformed data in this project.\"", h2_style))
    q1_ans = (
        "<b>What the Interviewer is Testing:</b> Do you understand real-world data quality, or do you just blindly run <code>dropna()</code>?<br/>"
        "<b>Your Model Response:</b><br/>"
        "\"In this project, the raw dataset appeared clean at first glance with zero NaN values in standard automated checks. "
        "However, when I inspected data types, <code>Total_Charges</code> was stored as an <code>object</code> rather than numeric. "
        "I wrote a regex diagnostic script and discovered <b>266 rows containing blank whitespace strings</b> (<code>' '</code>).<br/>"
        "Rather than dropping these rows—which would have created survivorship bias—I cross-tabulated them against all other features. "
        "I discovered a <b>100% mathematical correlation with <code>Tenure_Months == 0</code></b>: these were brand-new subscribers who had signed up but had not yet received their first monthly billing cycle. "
        "Because they had consumed zero months of service, their accumulated total spend was legitimately <b>$0.00</b>. "
        "I imputed $0.00, converted the column to float64, and verified the distribution before and after. This preserved 100% of new-customer records and prevented our churn model from being blind to early onboarding behavior.\""
    )
    story.append(create_callout(q1_ans, script_style, bg_color="#f8fafc", border_color="#0284c7"))
    story.append(Spacer(1, 6))
    
    # Q2: Algorithm Selection & Cost Matrix
    story.append(Paragraph("Q2: \"Why did you choose Logistic Regression when XGBoost and Random Forest are more advanced algorithms?\"", h2_style))
    q2_ans = (
        "<b>What the Interviewer is Testing:</b> Do you understand business trade-offs, evaluation metrics, and the cost matrix of classification errors?<br/>"
        "<b>Your Model Response:</b><br/>"
        "\"I evaluated Logistic Regression, Random Forest, and XGBoost on a held-out test set with balanced class weighting. "
        "While Random Forest achieved slightly higher accuracy (71.90% vs 71.65%), <b>accuracy is the wrong metric for churn prediction</b> due to class imbalance.<br/>"
        "In customer retention, the business cost matrix is asymmetric: a <b>False Negative</b> (failing to identify an at-risk customer) means losing their entire <b>$1,848 average lifetime value</b>. In contrast, a <b>False Positive</b> (flagging a safe customer) only costs <b>$15 to $25</b> in targeted retention messaging.<br/>"
        "Therefore, our primary optimization goal was <b>Recall (Sensitivity)</b>. <b>Logistic Regression achieved 74.88% Recall and 0.7869 ROC-AUC</b>, outperforming XGBoost (68.10% Recall) and Random Forest (64.56% Recall). "
        "Additionally, Logistic Regression offers exact odds ratios and complete transparency, allowing customer success leaders to clearly understand <i>why</i> a customer is flagged (e.g. ticket frequency and month-to-month contracts) without dealing with black-box complexity.\""
    )
    story.append(create_callout(q2_ans, script_style, bg_color="#f8fafc", border_color="#1e40af"))
    story.append(Spacer(1, 6))

    # Q3: Business Impact & Unit Economics
    story.append(Paragraph("Q3: \"How did you connect your machine learning predictions to actual business revenue and ROI?\"", h2_style))
    q3_ans = (
        "<b>What the Interviewer is Testing:</b> Are you just a code writer, or do you understand business economics, P&L, and ROI?<br/>"
        "<b>Your Model Response:</b><br/>"
        "\"Predictive models are useless unless paired with an economically viable intervention. I established key unit economics: "
        "average Monthly Recurring Revenue (MRR) was <b>$64.76</b>, average Customer Lifetime Value (CLV) was <b>$1,848</b>, and baseline churn leaked <b>$231,895 MRR</b>.<br/>"
        "Rather than spamming all 10,000 customers with discounts, I used our EDA findings to isolate the highest-friction, early-tenure cohort: subscribers with <b>tenure under 12 months who logged more than 3 support tickets</b> (306 accounts with an 81.7% churn rate).<br/>"
        "I modeled a <b>Customer Retention Cost (CRC) of $85.00 per account</b>—consisting of a $25 proactive Tier-3 Concierge Support intervention plus a $20/month bill credit for three months. "
        "Total campaign budget was <b>$26,010</b>. Assuming a conservative 35% rescue rate, the campaign rescues <b>87 accounts</b>, preserving <b>$78,060 in annual recurring revenue</b> and <b>$71,659 in residual CLV</b>. "
        "Subtracting the campaign cost yields a <b>$45,649 net profit</b>, or an audited <b>175.51% net campaign ROI</b>.\""
    )
    story.append(create_callout(q3_ans, script_style, bg_color="#f8fafc", border_color="#059669"))

    # -------------------------------------------------------------
    # PAGE 3: TOUGH QUESTIONS (PART 2) & SQL / ARCHITECTURE
    # -------------------------------------------------------------
    story.append(PageBreak())
    
    # Q4: SQL & Data Engineering
    story.append(Paragraph("Q4: \"How did you utilize SQL, and why was it necessary alongside Python?\"", h2_style))
    q4_ans = (
        "<b>What the Interviewer is Testing:</b> Are your SQL skills limited to simple <code>SELECT *</code>, or do you write production-grade analytical SQL?<br/>"
        "<b>Your Model Response:</b><br/>"
        "\"While Python is ideal for statistical modeling and scikit-learn pipelines, in an enterprise data warehouse like Snowflake, BigQuery, or Redshift, heavy aggregations should occur at the database layer to minimize compute latency and data egress costs.<br/>"
        "I authored a dedicated ANSI SQL analytics suite (<code>sql/churn_analysis.sql</code>) employing advanced SQL patterns:<br/>"
        "• <b>Common Table Expressions (CTEs):</b> Structured multi-stage cohort segmentation and clean categorical transformations.<br/>"
        "• <b>Window Functions:</b> Used <code>ROW_NUMBER() OVER (PARTITION BY ... ORDER BY ...)</code> to isolate highest-risk accounts and <code>AVG() OVER ()</code> for cross-cohort spend comparisons.<br/>"
        "• <b>Cohort Analysis:</b> Segmented subscriber retention curves by contract type, tenure buckets (0-12m, 13-24m, 25-48m, 49-72m), and payment methods, proving directly in SQL that automatic billing reduces churn by 27.8%.\""
    )
    story.append(create_callout(q4_ans, script_style, bg_color="#f8fafc", border_color="#b45309"))
    story.append(Spacer(1, 6))

    # Q5: Communication & BI Deliverables
    story.append(Paragraph("Q5: \"How do you communicate analytical findings to non-technical executive stakeholders?\"", h2_style))
    q5_ans = (
        "<b>What the Interviewer is Testing:</b> Can you translate complex data into executive decision-making tools?<br/>"
        "<b>Your Model Response:</b><br/>"
        "\"Executive leaders rarely look at Jupyter notebooks or code repositories. To make this project consumable across the organization, I built three distinct delivery channels:<br/>"
        "1. <b>Executive 5-Page PDF Intelligence Report:</b> Created an automated C-suite document containing high-level KPI cards, data audit breakdowns, charts, model benchmark comparison tables, and retention ROI projections.<br/>"
        "2. <b>Interactive Web Dashboard Simulator:</b> Developed a responsive web app (<code>interactive_dashboard.html</code>) with Chart.js plots and a live slider widget where product managers can adjust retention budgets and rescue rates to see real-time ROI forecasts.<br/>"
        "3. <b>Tableau Enterprise Data Model:</b> Exported an enriched dataset and documented Level of Detail (LOD) formulas (e.g. <code>{FIXED [Contract_Type]: AVG([Churn])}</code>) to enable business intelligence teams to drag-and-drop live metrics into corporate Tableau dashboards.\""
    )
    story.append(create_callout(q5_ans, script_style, bg_color="#f8fafc", border_color="#0284c7"))
    story.append(Spacer(1, 6))

    # Q6: Production Scaling & Future Improvements
    story.append(Paragraph("Q6: \"What would you do differently or improve if putting this into a 10-million subscriber production system?\"", h2_style))
    q6_ans = (
        "<b>What the Interviewer is Testing:</b> Do you understand production ML architecture, latency, streaming, and model maintenance?<br/>"
        "<b>Your Model Response:</b><br/>"
        "\"If deploying this pipeline at enterprise scale for 10 million active users, I would introduce three key architectural upgrades:<br/>"
        "1. <b>Real-Time Event Streaming:</b> Ingest support ticket creations and payment failures through <b>Apache Kafka</b> to update churn probability scores within seconds rather than waiting for nightly batch ETL.<br/>"
        "2. <b>Feature Store & Model Drift Monitoring:</b> Implement a feature store like <b>Feast</b> for consistent offline training and online inference, and integrate <b>Evidently AI or MLflow</b> to track concept drift and covariate shift in subscriber behavior.<br/>"
        "3. <b>Explainability at the Edge (SHAP):</b> Compute tree-based SHAP values during scoring and inject individual risk drivers directly into the frontline customer support CRM (e.g. Salesforce / Zendesk), telling the agent: <i>'This subscriber is at 84% churn risk due to 4 open router tickets—offer immediate equipment replacement.'</i>\""
    )
    story.append(create_callout(q6_ans, script_style, bg_color="#f8fafc", border_color="#1e40af"))

    # -------------------------------------------------------------
    # PAGE 4: CANDIDATE'S METRIC FLASHCARDS & ROLE-SPECIFIC PITCH
    # -------------------------------------------------------------
    story.append(PageBreak())
    story.append(Paragraph("4. Candidate's Metric Flashcards: Key Numbers to Quote Confidently", h1_style))
    story.append(Paragraph(
        "Memorize these verified metrics so you can quote them naturally and authoritatively during discussions:",
        body_style
    ))
    story.append(Spacer(1, 3))
    
    metrics_table_data = [
        [Paragraph("<b>Metric Domain</b>", table_hdr), Paragraph("<b>Exact Value</b>", table_hdr), Paragraph("<b>Business / Technical Meaning</b>", table_hdr)],
        [Paragraph("<b>Total Dataset Size</b>", table_cell_bold), Paragraph("10,000 Records", table_cell), Paragraph("Telecom subscriber records across contracts, billing & telemetry.", table_cell)],
        [Paragraph("<b>Baseline Churn Rate</b>", table_cell_bold), Paragraph("26.50% (2,650 users)", table_cell), Paragraph("Historical proportion of accounts that cancelled their subscription.", table_cell)],
        [Paragraph("<b>Monthly Revenue Lost</b>", table_cell_bold), Paragraph("$231,895.20 / mo", table_cell), Paragraph("Total MRR at risk from churned subscribers (34.8% revenue loss ratio).", table_cell)],
        [Paragraph("<b>Average CLV</b>", table_cell_bold), Paragraph("$1,848.00 / user", table_cell), Paragraph("Calculated customer lifetime value across subscriber lifespans.", table_cell)],
        [Paragraph("<b>Data Anomaly</b>", table_cell_bold), Paragraph("266 whitespace rows", table_cell), Paragraph("100% matched Tenure=0; imputed $0.00 to preserve new-account behavior.", table_cell)],
        [Paragraph("<b>Contract Multiplier</b>", table_cell_bold), Paragraph("4.0x Churn Hazard", table_cell), Paragraph("Month-to-month (43.5%) vs Two-Year contract churn rate (10.8%).", table_cell)],
        [Paragraph("<b>Support Friction Cliff</b>", table_cell_bold), Paragraph("81.70% Churn Rate", table_cell), Paragraph("Churn probability jumps dramatically once support tickets exceed 3.", table_cell)],
        [Paragraph("<b>Auto-Pay Impact</b>", table_cell_bold), Paragraph("27.8% Relative Drop", table_cell), Paragraph("Auto-billing churn is 25.2% vs 34.9% for manual check/paper billing.", table_cell)],
        [Paragraph("<b>Best Model Recall</b>", table_cell_bold), Paragraph("<b>74.88%</b> (LogReg)", table_cell), Paragraph("Intercepts ~3 out of 4 churning accounts prior to cancellation.", table_cell)],
        [Paragraph("<b>Model ROC-AUC</b>", table_cell_bold), Paragraph("<b>0.7869</b> (LogReg)", table_cell), Paragraph("High discriminative ranking capability across probability thresholds.", table_cell)],
        [Paragraph("<b>Target Campaign Cohort</b>", table_cell_bold), Paragraph("306 Accounts", table_cell), Paragraph("High-risk, early-tenure subscribers (Tenure < 12m & Tickets > 3).", table_cell)],
        [Paragraph("<b>Customer Retention Cost</b>", table_cell_bold), Paragraph("$85.00 / account", table_cell), Paragraph("$25 Concierge Support desk routing + $20/mo billing credit for 3 mos.", table_cell)],
        [Paragraph("<b>Total Campaign Budget</b>", table_cell_bold), Paragraph("$26,010.00", table_cell), Paragraph("Targeted budget allocation for the 306 high-risk accounts.", table_cell)],
        [Paragraph("<b>Rescued Revenue & ROI</b>", table_cell_bold), Paragraph("<b>$78,060 & 175.51%</b>", table_cell), Paragraph("87 rescued accounts; $45,649 net profit above campaign cost.", table_cell)],
    ]
    t_metrics = Table(metrics_table_data, colWidths=[110, 114, 280])
    t_metrics.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_accent),
        ('GRID', (0, 0), (-1, -1), 0.5, c_border),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_bg_light])
    ]))
    story.append(t_metrics)
    story.append(Spacer(1, 6))
    
    # Section 5: Role-Specific Adaptations
    story.append(Paragraph("5. Role-Specific Interview Customizations", h1_style))
    story.append(Paragraph(
        "Adjust your emphasis depending on the exact position you are interviewing for:",
        body_style
    ))
    story.append(Spacer(1, 3))
    
    pitch_ds = (
        "<b>FOR DATA SCIENTIST & ML ROLES:</b> Lead with class imbalance weighting, ROC-AUC vs Recall trade-offs, "
        "the asymmetric cost matrix (cost of false negatives vs false positives), feature transformation of skewed charges, "
        "and probability calibration for operational decision thresholds."
    )
    story.append(create_callout(pitch_ds, body_style, bg_color="#eff6ff", border_color="#1e40af"))
    story.append(Spacer(1, 3))
    
    pitch_bi = (
        "<b>FOR DATA ANALYST & BUSINESS INTELLIGENCE ROLES:</b> Lead with SQL window functions, cohort retention analysis, "
        "Tableau Level of Detail (LOD) expressions, the raw-to-clean data auditing methodology, and translating complex churn "
        "distributions into executive KPI dashboards."
    )
    story.append(create_callout(pitch_bi, body_style, bg_color="#f0fdf4", border_color="#047857"))
    story.append(Spacer(1, 3))
    
    pitch_biz = (
        "<b>FOR PRODUCT & REVENUE OPERATIONS ROLES:</b> Lead with unit economics: Monthly Recurring Revenue (MRR) preservation, "
        "Customer Acquisition Cost (CAC) vs Customer Retention Cost (CRC), the 81.7% support ticket cliff, and the 175.51% net campaign ROI."
    )
    story.append(create_callout(pitch_biz, body_style, bg_color="#fffbeb", border_color="#b45309"))
    
    # Build Document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated HR & Interview Discussion Guide PDF at: {output_pdf_path}")


if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.abspath(__file__))
    root_pdf = os.path.join(base_dir, "HR_and_Interview_Discussion_Guide.pdf")
    reports_pdf = os.path.join(base_dir, "reports", "HR_and_Interview_Discussion_Guide.pdf")
    
    build_hr_guide_pdf(root_pdf)
    
    # Ensure reports copy exists
    os.makedirs(os.path.join(base_dir, "reports"), exist_ok=True)
    shutil.copy2(root_pdf, reports_pdf)
    print(f"Successfully duplicated to: {reports_pdf}")
