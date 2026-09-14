"""
PDF Generator: Project Architecture & Data Folder Guide
Explains what each folder does, why it was created, how data flows through it,
and how the project mirrors professional human software and data engineering standards.
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
        
        # Header (pages 2+)
        if self._pageNumber > 1:
            self.drawString(54, 750, "Customer Churn Analytics | Project Architecture & Folder Guide")
            self.setStrokeColor(colors.HexColor("#cbd5e1"))
            self.setLineWidth(0.5)
            self.line(54, 744, 558, 744)
            
        # Footer (all pages)
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.5)
        self.line(54, 42, 558, 42)
        self.drawString(54, 30, "Technical Reference Document | Software Architecture & Data Governance")
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 30, page_text)
            
        self.restoreState()


def build_folder_guide_pdf(output_pdf_path):
    doc = SimpleDocTemplate(
        output_pdf_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=50,
        bottomMargin=48
    )
    
    styles = getSampleStyleSheet()
    
    # Color Palette
    c_primary = colors.HexColor("#1e3a8a")     # Deep Navy
    c_secondary = colors.HexColor("#0f172a")   # Dark Slate
    c_accent = colors.HexColor("#2563eb")      # Royal Blue
    c_success = colors.HexColor("#16a34a")     # Emerald Green
    c_warning = colors.HexColor("#d97706")     # Amber
    c_bg_light = colors.HexColor("#f8fafc")    # Slate Light
    c_text = colors.HexColor("#1e293b")        # Slate Body Text
    c_border = colors.HexColor("#cbd5e1")      # Border Grey
    
    title_style = ParagraphStyle(
        'DocTitle', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=22, leading=26,
        textColor=c_primary, spaceAfter=2
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle', parent=styles['Normal'],
        fontName='Helvetica', fontSize=10.5, leading=14,
        textColor=colors.HexColor("#475569"), spaceAfter=6
    )
    
    h1_style = ParagraphStyle(
        'Heading1Custom', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=12.5, leading=16,
        textColor=c_primary, spaceBefore=8, spaceAfter=4,
        keepWithNext=True
    )
    
    h2_style = ParagraphStyle(
        'Heading2Custom', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=10.5, leading=14,
        textColor=c_secondary, spaceBefore=6, spaceAfter=3,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'BodyCustom', parent=styles['Normal'],
        fontName='Helvetica', fontSize=8.5, leading=11.5,
        textColor=c_text, spaceAfter=4
    )
    
    bullet_style = ParagraphStyle(
        'BulletCustom', parent=body_style,
        leftIndent=10, firstLineIndent=-6, spaceAfter=2.5
    )
    
    table_text = ParagraphStyle(
        'TableTextCustom', parent=styles['Normal'],
        fontName='Helvetica', fontSize=8, leading=10,
        textColor=c_text
    )
    
    table_header = ParagraphStyle(
        'TableHeaderCustom', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=8, leading=10,
        textColor=colors.white
    )
    
    caption_style = ParagraphStyle(
        'CaptionCustom', parent=styles['Normal'],
        fontName='Helvetica-Oblique', fontSize=7.5, leading=9,
        textColor=colors.HexColor("#64748b"), alignment=TA_CENTER,
        spaceAfter=4
    )

    story = []
    
    # =============================================================
    # PAGE 1: TITLE, PURPOSE & ARCHITECTURE OVERVIEW
    # =============================================================
    story.append(Paragraph("Project Architecture & Folder Guide", title_style))
    story.append(Paragraph("Comprehensive Technical Reference: Directory Responsibilities, Engineering Rationale & Data Lifecycle", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2, color=c_primary, spaceBefore=1, spaceAfter=6))
    
    # Metadata Badge Strip
    meta_table = Table([[
        Paragraph("<b>Project:</b> Customer Churn & Retention Analytics", table_text),
        Paragraph("<b>Architecture Pattern:</b> Modular Pipeline & Decoupled Storage", table_text),
        Paragraph("<b>Standard:</b> Human Data Engineering Best Practices", table_text)
    ]], colWidths=[180, 180, 144])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_bg_light),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 6))
    
    story.append(Paragraph("1. Executive Summary: Why Architecture & Folder Structure Matter", h1_style))
    story.append(Paragraph(
        "A common pitfall in novice data science projects is dumping data, exploratory code, generated graphs, trained models, "
        "and final reports into a single cluttered directory. This causes naming collisions, breaks reproducibility, risks accidental "
        "overwrites of raw data, and makes the project inaccessible to team members or hiring managers.",
        body_style
    ))
    story.append(Paragraph(
        "This project adopts the <b>Separation of Concerns (SoC)</b> architectural standard utilized by senior data engineers and "
        "production ML teams. Every directory has a strictly defined single responsibility, creating a transparent, auditable pipeline "
        "from raw transactional ingestion to executive decision-making:",
        body_style
    ))
    story.append(Spacer(1, 3))
    
    # Quick Architecture Summary Table
    folder_summary_data = [
        [Paragraph("<b>Directory / Layer</b>", table_header), Paragraph("<b>Primary Function (What It Does)</b>", table_header), Paragraph("<b>Engineering Rationale (Why We Create It)</b>", table_header)],
        [Paragraph("<b><code>data/</code></b>", table_text), Paragraph("Houses raw inputs and cleansed analytical datasets.", table_text), Paragraph("Preserves immutable raw data; prevents irreversible corruption.", table_text)],
        [Paragraph("<b><code>src/</code></b>", table_text), Paragraph("Contains modular, testable Python source code.", table_text), Paragraph("Eliminates 'spaghetti code'; enables automated CLI pipeline execution.", table_text)],
        [Paragraph("<b><code>notebooks/</code></b>", table_text), Paragraph("Step-by-step narrative notebooks (Audit & Modeling).", table_text), Paragraph("Facilitates interactive visual storytelling and methodology verification.", table_text)],
        [Paragraph("<b><code>models/</code></b>", table_text), Paragraph("Stores serialized ML pipelines (<code>.joblib</code>).", table_text), Paragraph("Decouples model training from real-time API or dashboard inference.", table_text)],
        [Paragraph("<b><code>visualizations/</code></b>", table_text), Paragraph("Stores high-resolution (300 DPI) exported charts.", table_text), Paragraph("Separates visual assets from code; ready for reports and slide decks.", table_text)],
        [Paragraph("<b><code>sql/</code></b>", table_text), Paragraph("Enterprise ANSI SQL schema DDL and analytical queries.", table_text), Paragraph("Enables direct execution inside Postgres, Snowflake, or BigQuery.", table_text)],
        [Paragraph("<b><code>tableau/</code></b>", table_text), Paragraph("Tableau extract and calculated field documentation.", table_text), Paragraph("Bridges data science with executive BI dashboard authoring.", table_text)],
        [Paragraph("<b><code>reports/</code></b>", table_text), Paragraph("Executive summaries and interactive web applications.", table_text), Paragraph("Packages strategic takeaways and ROI models for business stakeholders.", table_text)]
    ]
    fs_table = Table(folder_summary_data, colWidths=[90, 204, 210])
    fs_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(fs_table)
    story.append(Spacer(1, 8))
    
    story.append(Paragraph("2. End-to-End Data Lifecycle & Flow", h1_style))
    story.append(Paragraph(
        "Data moves through the repository in a strictly unidirectional flow, ensuring full traceability and zero data leakage:",
        body_style
    ))
    
    flow_steps = [
        "<b>1. Raw Ingestion (<code>data/raw_...csv</code>):</b> Represents untouched operational records as received from production billing systems.",
        "<b>2. Cleansing & Validation (<code>src/data_cleansing.py</code>):</b> Audits formatting, handles missing values, and writes <code>data/cleaned_...csv</code>.",
        "<b>3. Feature Engineering & Modeling (<code>src/train_models.py</code>):</b> Reads clean data, encodes features, and saves models to <code>models/</code>.",
        "<b>4. Asset & Plot Generation (<code>src/eda_visualizations.py</code>):</b> Exports visual plots to <code>visualizations/</code> without modifying data.",
        "<b>5. Business Reporting (<code>reports/</code> & <code>generate_pdf_report.py</code>):</b> Consumes clean data, models, and charts to generate stakeholder artifacts."
    ]
    for fs in flow_steps:
        story.append(Paragraph(f"• {fs}", bullet_style))
        
    story.append(PageBreak())

    # =============================================================
    # PAGE 2: DEEP DIVE INTO DATA, SRC, AND NOTEBOOKS
    # =============================================================
    story.append(Paragraph("3. Deep-Dive: Directory Responsibilities & Engineering Rationale", h1_style))
    
    # FOLDER 1: DATA
    story.append(Paragraph("Folder 1: <code>data/</code> (The Data Storage Layer)", h2_style))
    data_folder_desc = [
        [Paragraph("<b>Component</b>", table_header), Paragraph("<b>Detailed Specification</b>", table_header)],
        [Paragraph("<b>Key Files</b>", table_text), Paragraph("<code>raw_customer_churn_data.csv</code> (10k raw uncleaned records)<br/><code>cleaned_customer_churn_data.csv</code> (Generated post-cleansing)", table_text)],
        [Paragraph("<b>What It Does</b>", table_text), Paragraph("Serves as the dedicated repository for data files across different lifecycle states: pristine raw data and certified clean data.", table_text)],
        [Paragraph("<b>Why We Create It</b>", table_text), Paragraph("<b>Principle of Immutability:</b> Raw data must never be manually edited or overwritten. By separating raw from cleaned files, any data scientist can re-run the pipeline from scratch and reproduce identical results. It also prevents production databases from being queried repeatedly.", table_text)],
        [Paragraph("<b>Handling Defects</b>", table_text), Paragraph("The raw dataset deliberately contains realistic defects (266 records with whitespace charges in <code>Total_Charges</code>). The clean dataset is created only after running the cleansing module, proving data hygiene.", table_text)]
    ]
    t_data = Table(data_folder_desc, colWidths=[120, 384])
    t_data.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_data)
    story.append(Spacer(1, 6))

    # FOLDER 2: SRC
    story.append(Paragraph("Folder 2: <code>src/</code> (The Production Source Code Layer)", h2_style))
    src_folder_desc = [
        [Paragraph("<b>Component</b>", table_header), Paragraph("<b>Detailed Specification</b>", table_header)],
        [Paragraph("<b>Key Modules</b>", table_text), Paragraph("<code>data_generator.py</code>, <code>data_cleansing.py</code>, <code>data_cleansing_visualizer.py</code>, <code>feature_engineering.py</code>, <code>eda_visualizations.py</code>, <code>train_models.py</code>, <code>retention_strategy.py</code>, <code>__init__.py</code>", table_text)],
        [Paragraph("<b>What It Does</b>", table_text), Paragraph("Contains modular, object-oriented, and functional Python code powering each analytical phase. Each file is an executable module and importable library.", table_text)],
        [Paragraph("<b>Why We Create It</b>", table_text), Paragraph("<b>Modularity & Testability:</b> Notebooks are great for exploration but terrible for automated deployment. Packaging logic into Python scripts allows unit testing, CLI execution, integration into CI/CD pipelines, and re-use across multiple notebooks without code duplication.", table_text)],
        [Paragraph("<b>Design Standard</b>", table_text), Paragraph("Follows PEP 8 standards with descriptive docstrings, type validation, parameterization, and isolated side effects.", table_text)]
    ]
    t_src = Table(src_folder_desc, colWidths=[120, 384])
    t_src.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_src)
    story.append(Spacer(1, 6))

    # FOLDER 3: NOTEBOOKS
    story.append(Paragraph("Folder 3: <code>notebooks/</code> (The Interactive Research Layer)", h2_style))
    nb_folder_desc = [
        [Paragraph("<b>Component</b>", table_header), Paragraph("<b>Detailed Specification</b>", table_header)],
        [Paragraph("<b>Notebooks</b>", table_text), Paragraph("<code>01_data_cleansing_and_audit.ipynb</code> (Data Quality Audit)<br/><code>02_customer_churn_and_retention.ipynb</code> (Full EDA, ML & Retention Strategy)", table_text)],
        [Paragraph("<b>What It Does</b>", table_text), Paragraph("Provides rich, interactive computational environments combining executable Python code with Markdown narratives, LaTeX math, and inline visualizations.", table_text)],
        [Paragraph("<b>Why We Create It</b>", table_text), Paragraph("<b>Auditing & Scientific Storytelling:</b> Stakeholders and technical evaluators can run code cell-by-cell, observe intermediate tables, and verify hypotheses interactively without running terminal commands. Splitting into two notebooks ensures clean separation between data engineering and modeling.", table_text)]
    ]
    t_nb = Table(nb_folder_desc, colWidths=[120, 384])
    t_nb.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_nb)
    story.append(PageBreak())

    # =============================================================
    # PAGE 3: DEEP DIVE INTO MODELS, VISUALIZATIONS, SQL, TABLEAU & REPORTS
    # =============================================================
    # FOLDER 4: MODELS
    story.append(Paragraph("Folder 4: <code>models/</code> (The Serialized Artifacts Layer)", h2_style))
    models_folder_desc = [
        [Paragraph("<b>Component</b>", table_header), Paragraph("<b>Detailed Specification</b>", table_header)],
        [Paragraph("<b>Key Artifact</b>", table_text), Paragraph("<code>best_churn_model.joblib</code> (Starts empty with <code>.gitkeep</code>; saved during training)", table_text)],
        [Paragraph("<b>What It Does</b>", table_text), Paragraph("Stores serialized Scikit-Learn pipelines containing fitted scalers, encoders, and the trained classifier weights.", table_text)],
        [Paragraph("<b>Why We Create It</b>", table_text), Paragraph("<b>Inference Decoupling:</b> Retraining machine learning models is computationally expensive. Persisting models enables instant inference (scoring new customer accounts in milliseconds) for batch jobs or web applications without retraining.", table_text)]
    ]
    t_models = Table(models_folder_desc, colWidths=[120, 384])
    t_models.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_models)
    story.append(Spacer(1, 6))

    # FOLDER 5: VISUALIZATIONS
    story.append(Paragraph("Folder 5: <code>visualizations/</code> (The Visual Evidence Layer)", h2_style))
    viz_folder_desc = [
        [Paragraph("<b>Component</b>", table_header), Paragraph("<b>Detailed Specification</b>", table_header)],
        [Paragraph("<b>Exported Assets</b>", table_text), Paragraph("<code>data_cleansing_audit.png</code>, <code>churn_by_contract.png</code>, <code>churn_by_support_tickets.png</code>, <code>churn_by_payment_method.png</code>, <code>churn_by_tenure_band.png</code>, <code>model_roc_curves.png</code>, <code>feature_importance.png</code>, <code>confusion_matrices.png</code>, <code>retention_campaign_roi.png</code>", table_text)],
        [Paragraph("<b>What It Does</b>", table_text), Paragraph("Stores publication-ready 300 DPI image assets generated during EDA and model evaluation.", table_text)],
        [Paragraph("<b>Why We Create It</b>", table_text), Paragraph("<b>Asset Decoupling:</b> External documents (PDF reports, executive slide decks, web dashboards) require static image files. Housing charts in a dedicated folder ensures they can be embedded cleanly without re-executing notebooks.", table_text)]
    ]
    t_viz = Table(viz_folder_desc, colWidths=[120, 384])
    t_viz.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_viz)
    story.append(Spacer(1, 6))

    # FOLDER 6: SQL
    story.append(Paragraph("Folder 6: <code>sql/</code> (The Enterprise Database Layer)", h2_style))
    sql_folder_desc = [
        [Paragraph("<b>Component</b>", table_header), Paragraph("<b>Detailed Specification</b>", table_header)],
        [Paragraph("<b>Key Script</b>", table_text), Paragraph("<code>churn_analysis.sql</code> (ANSI SQL schema, CTEs, Window functions, Cohort retention)", table_text)],
        [Paragraph("<b>What It Does</b>", table_text), Paragraph("Houses enterprise SQL queries that execute churn analytics directly within relational databases or cloud data warehouses.", table_text)],
        [Paragraph("<b>Why We Create It</b>", table_text), Paragraph("<b>Database Native Analytics:</b> Not all analytics run in Python. Data analysts and SQL engineers need direct database queries. This script proves advanced SQL competence (CTEs, <code>ROW_NUMBER()</code>, <code>MIN() OVER()</code>, partitioned sums) for database warehouses.", table_text)]
    ]
    t_sql = Table(sql_folder_desc, colWidths=[120, 384])
    t_sql.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_sql)
    story.append(Spacer(1, 6))

    # FOLDER 7: TABLEAU
    story.append(Paragraph("Folder 7: <code>tableau/</code> (The Business Intelligence Layer)", h2_style))
    tableau_folder_desc = [
        [Paragraph("<b>Component</b>", table_header), Paragraph("<b>Detailed Specification</b>", table_header)],
        [Paragraph("<b>Key Files</b>", table_text), Paragraph("<code>tableau_calculated_fields.md</code> (Calculated fields guide & LOD expressions)<br/><code>tableau_churn_dataset.csv</code> (Enriched flat extract generated during pipeline execution)", table_text)],
        [Paragraph("<b>What It Does</b>", table_text), Paragraph("Provides ready-to-import data extracts and formulas for building interactive BI dashboards in Tableau or PowerBI.", table_text)],
        [Paragraph("<b>Why We Create It</b>", table_text), Paragraph("<b>BI Enablement:</b> Bridges data science with non-technical business users. Business analysts can immediately build dashboards using pre-engineered dimensions without needing to re-implement Python transformation logic.", table_text)]
    ]
    t_tableau = Table(tableau_folder_desc, colWidths=[120, 384])
    t_tableau.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_tableau)
    story.append(Spacer(1, 6))

    # FOLDER 8: REPORTS
    story.append(Paragraph("Folder 8: <code>reports/</code> (The Stakeholder Delivery Layer)", h2_style))
    reports_folder_desc = [
        [Paragraph("<b>Component</b>", table_header), Paragraph("<b>Detailed Specification</b>", table_header)],
        [Paragraph("<b>Key Files</b>", table_text), Paragraph("<code>executive_summary.md</code>, <code>interactive_dashboard.html</code>, <code>model_benchmarks.json</code>, <code>retention_financial_summary.json</code>", table_text)],
        [Paragraph("<b>What It Does</b>", table_text), Paragraph("Contains executive-facing summaries, machine-readable JSON metrics, and the single-page HTML interactive simulator.", table_text)],
        [Paragraph("<b>Why We Create It</b>", table_text), Paragraph("<b>Actionable Decision Making:</b> Corporate executives care about financial outcomes (MRR lost, CLV saved, campaign ROI) rather than code lines. This folder consolidates high-level business intelligence into easily digestible formats.", table_text)]
    ]
    t_reports = Table(reports_folder_desc, colWidths=[120, 384])
    t_reports.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_reports)
    story.append(PageBreak())

    # =============================================================
    # PAGE 4: ORCHESTRATION & HOW A HUMAN DEPLOYER RUNS IT
    # =============================================================
    story.append(Paragraph("4. Root Files & Pipeline Orchestration", h1_style))
    story.append(Paragraph(
        "The repository root contains five essential configuration and execution files that tie all directories together:",
        body_style
    ))
    
    root_files_desc = [
        [Paragraph("<b>File</b>", table_header), Paragraph("<b>Function & Purpose</b>", table_header)],
        [Paragraph("<b><code>main.py</code></b>", table_text), Paragraph("<b>Master CLI Orchestrator:</b> Single entry point to run all pipeline steps sequentially (clean, eda, train, strategy, report) or execute individual steps via <code>--step</code>.", table_text)],
        [Paragraph("<b><code>generate_pdf_report.py</code></b>", table_text), Paragraph("<b>Automated PDF Compiler:</b> Compiles the 5-page executive report embedding generated charts and financial metrics with auto-prerequisite checking.", table_text)],
        [Paragraph("<b><code>customer_churn_analytics.json</code></b>", table_text), Paragraph("<b>Project Blueprint:</b> Defines business objectives, dataset schema, key metrics, and empirical findings to validate.", table_text)],
        [Paragraph("<b><code>requirements.txt</code></b>", table_text), Paragraph("<b>Dependency Manifest:</b> Specifies exact library versions (<code>pandas</code>, <code>scikit-learn</code>, <code>xgboost</code>, <code>seaborn</code>, <code>matplotlib</code>, <code>reportlab</code>).", table_text)],
        [Paragraph("<b><code>README.md</code></b>", table_text), Paragraph("<b>Project Portfolio Documentation:</b> Explains business context, findings, model comparisons, and human-written execution instructions.", table_text)]
    ]
    t_root = Table(root_files_desc, colWidths=[140, 364])
    t_root.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
    ]))
    story.append(t_root)
    story.append(Spacer(1, 8))

    story.append(Paragraph("5. Step-by-Step Execution Guide for Evaluators", h1_style))
    story.append(Paragraph(
        "To experience the project exactly as designed, run the following commands in order from your terminal:",
        body_style
    ))
    
    exec_steps = [
        "<b>Step 1: Install Dependencies</b><br/><code>pip install -r requirements.txt</code> (Installs pandas, scikit-learn, xgboost, seaborn, reportlab).",
        "<b>Step 2: Execute Data Cleansing</b><br/><code>python main.py --step clean</code><br/>Reads <code>data/raw_customer_churn_data.csv</code>, resolves whitespace defects, and generates <code>data/cleaned_customer_churn_data.csv</code>.",
        "<b>Step 3: Run Exploratory Data Analysis</b><br/><code>python main.py --step eda</code><br/>Generates high-res visual plots in <code>visualizations/</code> verifying the 4x contract risk and 81.7% ticket cliff.",
        "<b>Step 4: Train Machine Learning Classifiers</b><br/><code>python main.py --step train</code><br/>Trains Logistic Regression, Random Forest, and XGBoost; exports <code>models/best_churn_model.joblib</code>.",
        "<b>Step 5: Compute Business Retention Strategy</b><br/><code>python main.py --step strategy</code><br/>Calculates MRR Lost ($231.9K), CLV ($1,848), and models the 175.5% ROI campaign.",
        "<b>Step 6: Generate Executive PDF Reports</b><br/><code>python main.py --step report</code> (Compiles the 5-page executive intelligence report)."
    ]
    for es in exec_steps:
        story.append(Paragraph(f"• {es}", bullet_style))
        story.append(Spacer(1, 1.5))
        
    story.append(Spacer(1, 8))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=4, spaceAfter=4))
    story.append(Paragraph(
        "<b>Customer Churn & Retention Analytics</b> | Data Engineering & Architecture Reference Guide",
        caption_style
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully compiled Folder Guide PDF to: {output_pdf_path}")

if __name__ == '__main__':
    project_dir = os.path.dirname(os.path.abspath(__file__))
    target_pdf = os.path.join(project_dir, 'Project_Architecture_and_Folder_Guide.pdf')
    build_folder_guide_pdf(target_pdf)
    
    reports_pdf = os.path.join(project_dir, 'reports', 'Project_Architecture_and_Folder_Guide.pdf')
    shutil.copy2(target_pdf, reports_pdf)
    print(f"Copied folder guide to: {reports_pdf}")
