AI-Based Master Timetable is an enterprise-grade academic scheduling and management platform designed to automate and optimize the complex task of college timetable generation. Built specifically to handle the intricate, multi-departmental constraints of G.H. Raisoni College of Engineering (GHRCE), the system replaces manual scheduling efforts with a high-performance algorithmic solver.

At its core, the application utilizes a custom-built Constraint Satisfaction Problem (CSP) Solver with Backtracking to generate collision-free timetables in seconds. Beyond initial creation, it features a dynamic Smart Rescheduling Engine that automatically detects teacher absences, evaluates qualified substitutes, and updates the active timetable on-the-fly without disrupting other classes.

🚀 Key Technical Highlights & Capabilities
⚡ Automated CSP-Backtracking Engine: Formulates scheduling as a constraint network. Enforces both hard constraints (e.g., zero double-booking for rooms, classes, or teachers) and soft/preference constraints (e.g., workload balancing, specific lab slots, and department-specific hours).
🔄 Instant Absentee Rescheduling: Allows administrators to mark teacher attendance. If a teacher is absent, the system's heuristic matching algorithm finds the most qualified, non-conflicting substitute and updates the schedule in real-time.
📊 Interactive Admin & Faculty Dashboards: Built with React and interactive charts (powered by Recharts) to provide clear visualizations of teacher workloads, department capacities, room utilization, and live activity feeds.
📁 Robust Data Processing: Includes a smart Excel parser to rapidly ingest department syllabus, faculty details, and course layouts.
🔒 Secure Role-Based Access Control (RBAC): Implements state-of-the-art JWT authentication with bcrypt password hashing, isolating administrative controls from teacher portals.
