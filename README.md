
# Fluid Replacement Calculator for Nurses and Midwives
**Author**: Peter Mvuma  
**Program**: MSc Health Informatics  
**University**: Michigan Technological University  

## Problem Statement
Nurses in remote health centers often struggle with:
- Time-consuming manual fluid calculations
- Lack of immediate access to pediatric dehydration protocols
- Overburdened workflow and decision fatigue
   **This tool provides an evidence-based, automated solution that improves both *efficiency* and *patient outcomes**.

## Project Overview
In many rural areas of Malawi and other resource-limited settings, nurses and midwives often manage patients with dehydration without reliable access to digital tools or standardized fluid calculation aids. This project addresses that gap by providing an **offline, Python-based desktop application** that automates **fluid replacement calculations** based on **WHO guidelines**.

The Fluid Replacement Calculator is specifically tailored to support clinical decision-making by calculating;
- Fluid deficit volumes
- Maintenance fluid requirements
- Administration duration and hourly rates

The program simplifies manual processes, reduces errors and improves the quality of care especially for patients particulary in settings nurse to patient ratios is poor.

## Features
- **Graphical User Interface (GUI)** built with `tkinter`
- **Visual trend graphs** using `matplotlib`
- **Patient data management** with `MySQL`
- **Exportable reports** in PDF format
- **Data validation** to ensure input accuracy
- **Time-based scheduling** of fluid administration
- WHO-compliant dehydration management logic (Plan A, B, C)
- Works **entirely offline**

## Technologies and Libraries Used

| Module        | Purpose                                      |
|---------------|----------------------------------------------|
| `tkinter`, `ttk`, `tkcalendar.DateEntry` | GUI and date inputs |
| `MySQL`       | Patient record storage                       |
| `matplotlib`  | Plotting fluid volume vs time                |
| `datetime`    | Treatment duration and timestamp tracking    |
| `csv`, `os`   | File system access and CSV export            |
| `re`          | Input validation                             |
| `reportlab` / `fpdf` | PDF generation for printable session summaries for an individual patient|

## Sample Workflow
1. Launch application via desktop shortcut.
2. Log in and open the patient input form.
3. Enter:
   - Patient name
   - Age
   - Weight (kg)
   - Level of dehydration (mild, moderate, severe)
4. Click **Calculate** to receive:
   - Total fluid volume (mL)
   - Duration (e.g., 4 hours)
   - Recommended infusion rate (e.g., 375 mL/hour)
5. Optionally:
   - View fluid schedule plot
   - Save session to database
   - Export session report as PDF

## Input and Output
### Inputs
- Patient Name
- Age
- Weight (kg)
- Dehydration Level
### Outputs
- Total fluid volume required (mL)
- Duration and hourly rate for administration
- Visual fluid schedule (optional)
- PDF session summary
- MySQL data log for audit/review

## Impact & Way Forward
This tool is a step toward **digitally empowering nurses** in remote clinics to:
- Make faster, evidence-based decisions
- Reduce human error
- Track treatment data for quality improvement

### Potential Future Improvements
- Improve the design of the application including outlook
- EHR data integration 
- Integrate barcode scanning for patient ID
- Mobile version for Android tablets

## License
This project is developed as part of an academic requirement. Future iterations may adopt an open-source license to promote collaboration and deployment in underserved health settings.

## Acknowledgments
   **Special thanks to**
- Weihua Zhou, Assistant Professor - Health Informatics & Applied Computing, Michigan Technological University
- Nurses and midwives in Malawi whose work inspired me to develop this ditital tool
- WHO for their fluid replacement guidelines
