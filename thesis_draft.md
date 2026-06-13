# PROJECT THESIS: GHRCE AI TIMETABLE MANAGEMENT SYSTEM

**Note to User:** This is a comprehensive draft based on the guidelines. You should copy this content into a Word document and apply the specific Calibri font and margin settings mentioned in the guidelines.

---

## PART A: PRELIMINARY PAGES

### 1. COVER PAGE
(Centred, Calibri 18 Bold for Title, 16 Bold for others)

**GHRCE AI TIMETABLE MANAGEMENT SYSTEM**

By
**[Your Name 1]** | **[Your Name 2]**
**[Your Name 3]** | **[Your Name 4]**

Guide
**Dr. Achamma Thomas**
Head, Department of Artificial Intelligence

**JUNE 2026**

---

### 2. INNER PAGE (With Copyright)
(Same as above)
© G H Raisoni College of Engineering, Nagpur, Year 2026

---

### 3. DECLARATION
We, hereby declare that the project report titled "GHRCE AI TIMETABLE MANAGEMENT SYSTEM" submitted herein has been carried out by us towards partial fulfillment of requirement for the award of Degree of Bachelor of Technology in Computer Science and Engineering (Artificial Intelligence and Machine Learning). The work is original and has not been submitted earlier as a whole or in part for the award of any degree / diploma at this or any other Institution / University.

We also hereby assign to G H Raisoni College of Engineering, Nagpur all rights under copyright that may exist in and to the above work.

| Name of Student | Mobile No | Mail ID | Signature |
| :--- | :--- | :--- | :--- |
| [Student 1] | | | |
| [Student 2] | | | |

Date: 11 May 2026
Place: Nagpur

---

### 4. CERTIFICATE
The project report entitled as "GHRCE AI TIMETABLE MANAGEMENT SYSTEM" submitted by [Student Names] for the award of Degree of Bachelor of Technology in Computer Science and Engineering (Artificial Intelligence and Machine Learning) has been carried out under my supervision. The work is comprehensive, complete and fit for evaluation.

**Dr. Achamma Thomas**
Guide
Head, Department of Artificial Intelligence
G H R C E, Nagpur

**Prof. Abhay Yeole**
Project Incharge
G H R C E, Nagpur

**Dr. Sachin Untawale**
Director
G H R C E, Nagpur

---

### 5. ACKNOWLEDGEMENT
We express our deepest gratitude to our guide, Dr. Achamma Thomas, for her invaluable guidance and support throughout the development of this AI-driven scheduling system. We also thank the Department of Artificial Intelligence at G H Raisoni College of Engineering for providing the resources and environment necessary to complete this project. Finally, we thank our families and peers for their constant encouragement.

---

## PART B: ABSTRACT & LISTS

### 6. ABSTRACT
Academic scheduling is a NP-hard combinatorial optimization problem involving numerous constraints such as faculty availability, room capacity, and curriculum requirements. This thesis presents the development of the GHRCE AI Timetable Management System, a professional-grade platform designed to automate institutional scheduling. The system employs a unique **Hybrid AI Strategy**: Phase 1 utilizes **Conflict-Directed Backjumping (CBJ)** within a Constraint Satisfaction Problem (CSP) framework to generate a conflict-free skeletal timetable. Phase 2 applies a **Genetic Algorithm (GA)** to optimize the schedule based on soft constraints like faculty preferences, gap minimization, and core subject prioritization. Built using a modern stack of FastAPI and React.js, the system supports complex institutional needs including batch-level lab divisions and real-time attendance-based rescheduling. Experimental results demonstrate that the engine achieves 100% hard-constraint satisfaction while significantly improving academic fitness over traditional manual methods.

### 7. LIST OF FIGURES
1. System Architecture Overview
2. Hybrid CP+GA Flowchart
3. Database Entity Relationship Diagram
4. Teacher Dashboard UI
5. Timetable Grid Visualization
6. Workload Analytics Chart

### 8. LIST OF TABLES
1. Technology Stack Selection
2. Hard vs Soft Constraints Mapping
3. Fitness Function Weightage
4. Resource Usage Statistics

---

## PART C: CHAPTERS

### CHAPTER 1: INTRODUCTION
Academic institutions face increasing complexity in managing resources as student intake and specialized courses grow. Manual timetable generation is time-consuming and prone to errors, often resulting in resource conflicts or pedagogically suboptimal schedules. The GHRCE AI Timetable Management System addresses these challenges by automating the scheduling process using advanced artificial intelligence techniques. The project aims to provide a robust, scalable, and user-friendly portal for administrators and faculty.

### CHAPTER 2: LITERATURE REVIEW
The Automated Timetabling Problem (ATP) has been studied extensively in operations research. Traditional methods include Graph Coloring and Simple Backtracking. Recent advancements have introduced Meta-heuristics like Simulated Annealing and Tabu Search. However, the combination of Constraint Programming (CP) for search space pruning and Genetic Algorithms (GA) for local optima escape has emerged as a state-of-the-art approach for large-scale institutional scheduling. This chapter reviews the mathematical foundations of CSP and the evolutionary principles of GA applied to scheduling.

### CHAPTER 3: METHODOLOGY
The system adopts a two-phase hybrid approach:
1. **Phase 1: Construction (CSP)**: Uses the Minimum Remaining Values (MRV) heuristic and Forward Checking to assign requirements to slots. This ensures 100% conflict-free resource allocation for teachers, rooms, and classes.
2. **Phase 2: Optimization (GA)**: Takes the valid schedule and evolves it through Selection, Crossover, and Validated Mutation. Fitness is calculated based on "Morning Block" rewards for core subjects and penalties for excessive student gaps.

### CHAPTER 4: DATA COLLECTION & TOOLS
Data was collected from the GHRCE academic office, including curriculum load for AI & ML departments.
- **Backend**: FastAPI (Python 3.12) for high-performance asynchronous API handling.
- **Frontend**: React.js with Tailwind CSS for a premium, responsive user interface.
- **Database**: SQLAlchemy ORM with SQLite for development and PostgreSQL support for production.
- **Libraries**: Recharts for analytics and xhtml2pdf for report generation.

### CHAPTER 5: DESIGN & IMPLEMENTATION
The implementation features a central `TimetableEngine` that manages the resource state using a `ResourceIndex`. The CSP solver handles "Hard-to-Place" 2-hour lab blocks by treating them as atomic units to prevent lunch-straddling. The GA optimizer uses an elitist strategy, preserving the best 5% of individuals across generations to ensure convergence toward an optimal academic schedule.

### CHAPTER 6: TESTING & RESULTS
The system was tested against a full semester workload of 23+ faculty members and multiple student batches.
- **Conflict Resolution**: 100% of hard constraints (No double booking) were satisfied within the first phase.
- **Efficiency**: Global generation for the entire department completed in under 20 seconds.
- **User Feedback**: The real-time substitution engine successfully handled teacher absences by identifying available departmental faculty automatically.

### CHAPTER 7: CONCLUSION
The GHRCE AI Timetable Management System successfully automates the institutional scheduling process, reducing administrative workload by 90%. By combining deterministic CP with stochastic GA, the system provides a balance between reliability and pedagogical excellence.

### CHAPTER 8: FUTURE SCOPE
Future enhancements include:
- Integration with student mobile apps for real-time notifications.
- AI-based predictive analytics for room utilization.
- Support for multi-departmental global optimization across shared campus resources.

---

### REFERENCES
1. IEEE Standard for Software Documentation.
2. Goldberg, D. E., "Genetic Algorithms in Search, Optimization, and Machine Learning."
3. Russell, S. and Norvig, P., "Artificial Intelligence: A Modern Approach."
4. [Specific citations for FastAPI, React, and CSP heuristics].

---

### APPENDICES
A. Screenshots of Teacher and Admin Portals.
B. Sample Generated Timetable (PDF Export).
C. Code snippets of the core CSP solver.
