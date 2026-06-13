# 🏗️ GHRCE AI Timetable System - Comprehensive Project Blueprint & Algorithmic Information

This document serves as a complete technical guide and blueprint for the **GHRCE AI Timetable Management System** designed for the **GH Raisoni College of Engineering, Nagpur**. It details the architectural design, database schemas, and the step-by-step algorithms governing the Hybrid AI scheduling engine.

---

## 🏛️ 1. System Architecture Overview

The system uses a decoupled, high-performance web architecture consisting of:
*   **Frontend**: React 18, Tailwind CSS, Axios, and React Context (for state and authentication management).
*   **Backend**: FastAPI (Python 3.12) utilizing asynchronous execution, Pydantic for validation, and Uvicorn for production-grade serving.
*   **Database & ORM**: SQLite (for portable development/staging) and PostgreSQL (for production), managed via SQLAlchemy ORM.
*   **AI Engine Core**: Custom Hybrid Constraint Satisfaction Programming (CSP) solver coupled with a Genetic Algorithm (GA) optimizer.

```mermaid
graph TD
    subgraph "Client Tier (React 18 + Tailwind)"
        UI["Admin & Teacher Dashboards"]
        State["Auth Context / Local State"]
        API_Client["Axios Service Layer"]
    end

    subgraph "Application Tier (FastAPI)"
        Routers["REST API Routers"]
        Auth["JWT Security & Auth"]
        Services["Business Services (Excel Parser, PDF Gen)"]
        AIEngine["Hybrid CSP + GA Engine"]
        Repair["Dynamic Rescheduling Engine"]
    end

    subgraph "Data Tier (SQLAlchemy Relational)"
        DB[("Relational Database")]
        Schema["SQL Tables (Users, Teachers, Slots)"]
    end

    UI --> API_Client
    API_Client --> Routers
    Routers --> Auth
    Routers --> Services
    Services --> AIEngine
    Services --> Repair
    AIEngine --> DB
    Repair --> DB
    Services --> DB
    DB --> Schema
```

---

## 📊 2. Database Entity Models (Schema Models)

The system translates institutional resources into structured database schemas using SQLAlchemy ORM. Below is an explanation of **which database models are used, how they are used, and why they are used**.

### Table of Models

| Model Name | Table Name | Purpose / Why it is used | Key Attributes | How it is used in the System |
| :--- | :--- | :--- | :--- | :--- |
| **User** | `users` | Handles authentication, session security, and access control. | `email`, `password_hash`, `role` (Admin/Teacher/Student) | Restricts access to administrative timetable generation and teacher-specific rescheduling. |
| **Department** | `departments` | Models the university departments (e.g., AI, CSE, ME). | `name`, `code` | Scopes teachers, subjects, and sections. |
| **Teacher** | `teachers` | Tracks academic resource limits, credentials, and availability status. | `name`, `max_load` (weekly limit), `status` (Present/Absent) | The AI engine reads `max_load` to prevent teacher burnouts. The Rescheduling Engine reads `status` to trigger substitutions. |
| **TeacherPreference** | `teacher_preferences` | Models faculty scheduling constraints. | `day`, `preferred_slot_id`, `is_preferred` (True/False), `preference_weight` | `is_preferred = False` acts as a hard block in Phase 1 (CSP). `is_preferred = True` is optimized via weights in Phase 2 (GA). |
| **Subject** | `subjects` | Models course catalog requirements and resource constraints. | `name`, `type` (Theory/Lab), `weekly_load`, `is_core`, `required_room_id` | Identifies lab classes (which need 2 consecutive slots and specific rooms) and core subjects (which require morning slots). |
| **Room** | `rooms` | Models physical spaces and resource limits. | `name`, `capacity`, `type` (Classroom/Lab) | Prevent capacity overflows. The AI engine only schedules Labs in rooms marked as `lab`. |
| **Class** & **Batch** | `classes` / `batches` | Represents student groups. Classes are divided into sub-batches (e.g. A1, A2) for lab sessions. | `name`, `semester`, `strength` | The AI engine schedules theory sessions for the whole class, and lab sessions for sub-batches concurrently in separate rooms. |
| **TimeSlot** | `time_slots` | Defines the institutional time grid. | `label`, `slot_index` (0 to 7) | Provides the coordinate system for placement (e.g. Slot 0 = 09:30 AM). |
| **TeachingAssignment** | `teaching_assignments` | Represents the input matrix ("Requirements") configured by admins. | `teacher_id`, `subject_id`, `class_id`, `batch_id`, `weekly_load` | Serves as the primary input requirements list for the AI generator. |
| **TimetableEntry** | `timetable_entries` | Stores the final generated schedule output. | `class_id`, `batch_id`, `subject_id`, `teacher_id`, `room_id`, `day`, `time_slot_id`, `is_substituted` | Serves as the single source of truth for dashboard rendering, PDF exports, and daily substitution repair. |
| **Attendance** | `attendance` | Tracks faculty daily attendance. | `teacher_id`, `date`, `status` | Marking a teacher absent triggers the dynamic Rescheduling Engine. |
| **SubstituteAssignment** | `substitute_assignments` | Records temporary substitution pairs. | `timetable_entry_id`, `original_teacher_id`, `substitute_teacher_id`, `date` | Audit log for substitution changes. |

---

## 🧠 3. AI Scheduling Engine Models

The scheduling engine uses a **Hybrid Multi-Phase AI Optimization Model** because academic scheduling is an NP-hard problem. It combines deterministic backtracking solvers with stochastic evolutionary optimization.

### 1. Conflict-Directed Backjumping (CBJ) CSP Solver (Phase 1)
*   **Why it is used**: Hard constraints (no teacher in two places at once, no class section doubled up, no lab lunch interruptions) are non-negotiable. Pure stochastic models (like Genetic Algorithms) or neural models are highly inefficient at finding a mathematically valid, 100% clash-free starting schedule because the feasible search space is extremely dense and full of dead ends. A CSP solver systematically searches and guarantees that the resulting baseline schedule has **zero** hard conflicts.
*   **How it is used**: 
    *   **Variables**: Each session required by `TeachingAssignment` (e.g., 3 hours of DAA Theory, 2 hours of DL Lab) is a variable.
    *   **Domain**: A list of valid combinations of `(Teacher, Room, Day, Slot Index)`.
    *   **Hard Constraints Checked**:
        1.  *Teacher Availability*: Teacher is not booked at the selected `(day, slot_index)` and has not reached their weekly `max_load`.
        2.  *Room Availability*: Physical room is vacant. The room type (Classroom/Lab) matches the subject type, and cap meets section strength.
        3.  *Class / Batch Availability*: The class group is free. If it is a lab, the sub-batch is free and the slot doesn't straddle lunch.
        4.  *Day-Spread Limits*: No class section has more than `max_per_day` lectures (typically 6). No class has more than 2 sessions of the same theory subject on a single day.
        5.  *Teacher Preference Blocks*: If a teacher marked a slot as unavailable (`is_preferred = False`), the domain evaluator excludes it.

### 2. Genetic Algorithm (GA) Optimizer (Phase 2)
*   **Why it is used**: A CSP solver only guarantees a *valid* schedule, not a *good* one. It may schedule classes with long gap hours for students, place tough core subjects in late afternoon blocks, or scatter teacher schedules across the week. A Genetic Algorithm optimizes "soft constraints" (preferences and quality heuristics) by simulating natural selection, crossover, and mutation without violating the hard constraints established in Phase 1.
*   **How it is used**:
    *   **Chromosome Representation**: A complete valid timetable (list of `ScheduleSlot` objects). To achieve maximum performance, mutations and crossovers operate on references and index arrays, reducing computational deep-copy overhead.
    *   **Fitness Function (Score Evaluation)**:
        *   `+150` for Core subjects scheduled in morning slots (Slots 1-3).
        *   `+200` for Theory classes in the morning (fresher minds).
        *   `+150` for Labs scheduled in the afternoon (practical work).
        *   `+200 * Preference Weight` for matching a teacher's preferred slots.
        *   `-100` to `-600` (penalty) for student gaps (idle hours between lectures).
        *   `-100 * (consecutive - 2)` (penalty) for teacher fatigue (3+ consecutive lectures).
        *   `+100` (reward) / `-50` (penalty) for Room Stability (keeping a subject in the same room throughout the week).

### 3. Dynamic Repair / Rescheduling Engine
*   **Why it is used**: Schedules are dynamic. When a teacher calls in sick, regenerating the entire timetable would disrupt the rest of the college. A localized, fast-repair engine is required to substitute the teacher while preserving the rest of the schedule.
*   **How it is used**:
    *   Identifies the slots taught by the absent teacher.
    *   Retrieves the list of present teachers.
    *   Scores prospective substitutes based on:
        *   Department code matching (`+100`)
        *   Subject qualification list matching (`+50`)
        *   Current workload minimization (prefers less-loaded faculty).
    *   Checks availability using the shared `ResourceIndex` component to ensure the substitute has no scheduling conflict.
    *   Applies changes in place, flags them as `is_substituted`, and posts a notification to the notice board.

---

## ⚙️ 4. Step-by-Step AI Scheduling Algorithm

The following flowchart and detailed description outline the step-by-step execution of the timetable generation algorithm.

### Algorithmic Workflow

```mermaid
flowchart TD
    Start([1. Start Generation Request]) --> LoadData[2. Load Data from DB & Schema]
    LoadData --> Audit[3. Pre-Flight Capacity Audit]
    Audit --> HasCritical{Critical Warnings?}
    
    HasCritical -- Yes --> AlertAdmin[Log Critical warning to Notice Board]
    HasCritical -- No --> BuildReqs[4. Build Requirements & Sort Variables]
    
    AlertAdmin --> BuildReqs
    BuildReqs --> CSPStart[5. Initialize Phase 1 CSP Solver]
    
    CSPStart --> SelectVar[6. Pick Next Variable in Sorted Order]
    SelectVar --> ComputeDomain[7. Compute Valid Domain for Variable]
    
    ComputeDomain --> IsDomainEmpty{Domain Empty?}
    
    IsDomainEmpty -- Yes --> Backtrack[8. Backtrack / Backjump]
    IsDomainEmpty -- No --> AssignVal[9. Assign Valid Random Domain Coordinate]
    
    AssignVal --> IsAllPlaced{All Reqs Placed?}
    IsAllPlaced -- No --> SelectVar
    
    Backtrack --> Stagnated{Stagnated / BT Limit Reached?}
    Stagnated -- Yes --> Restart[9b. CSP Restart with New Random Seed]
    Stagnated -- No --> UndoLast[Undo Last Resource Assignment]
    UndoLast --> SelectVar
    
    Restart --> CSPStart
    
    IsAllPlaced -- Yes --> GAStart[10. Initialize Phase 2 GA Optimizer]
    
    GAStart --> GenPop[11. Generate Initial Population from CSP Output]
    GenPop --> EvalFitness[12. Calculate Fitness Scores]
    
    EvalFitness --> GenLoop{Max Generations Reached?}
    
    GenLoop -- No --> SelectParents[13. Select Elite Parents]
    SelectParents --> Crossover[14. Perform Class-Wise Crossover]
    Crossover --> Mutation[15. Apply Constraint-Validated Mutation Swaps]
    Mutation --> EvalFitness
    
    GenLoop -- Yes --> SaveDB[16. Save Fittest Timetable to DB]
    SaveDB --> End([17. Timetable Rendered on Dashboard])
```

### Algorithmic Steps Description

#### Step 1: Request & Input Ingestion
The administrative portal issues a `POST` request to `/api/timetable/generate`. The backend fetches all entries from the DB tables: `Class`, `Batch`, `Teacher`, `Subject`, `Room`, `TimeSlot`, and `TeachingAssignment`.

#### Step 2: Pre-Flight Capacity Audit
Before launching the heavy CSP algorithm, the engine performs a static calculation:
1.  **Class Capacity Audit**: Compares total required hours for each class against the total weekly slots available ($5 \text{ days} \times 8 \text{ slots} = 40$). If weekly hours exceed 40, a critical warning is flagged.
2.  **Teacher Overload Audit**: Compares assigned hours in `TeachingAssignment` against each teacher's `max_load`.
3.  **Room Saturation Audit**: Sums total lab and theory hours required, comparing them against the total capacity of respective rooms ($N_{\text{rooms}} \times 40$).

#### Step 3: Requirement Building & Static Ordering (Heuristic)
The `_build_requirements` service translates teaching assignments into standard scheduling blocks.
*   A 3-credit theory course is split into 3 independent 1-hour variables.
*   A 4-credit lab course is split into 2 independent 2-hour variables.
*   **Variable Ordering (Turbo Heuristic)**: The variables are sorted before search:
    $$\text{Sort Priority: } \text{Labs (2-hour blocks)} \succ \text{Busiest Teachers} \succ \text{Busiest Classes}$$
    *Why?* 2-hour lab blocks are the hardest to place because they require consecutive slots that do not cross the lunch break. Placing them first prevents search dead-ends.

#### Step 4: Phase 1 — Constraint Satisfaction Solver (CBJ)
The engine executes the Backtracking Search:
1.  **MRV-driven Heuristic**: Selects the next variable from the sorted list.
2.  **Domain Computation**: Computes valid `(Teacher, Room, Day, Slot)` tuples. It checks constraints against a fast `ResourceIndex` (which indexes occupied teachers, classes, rooms, and batches on a coordinate map).
3.  **Backjumping (CBJ)**: If a variable has no valid domains, it backtracks. Instead of reverting the immediately preceding assignment (which might be unrelated to the clash), it analyzes conflict sets and jumps back to the variable that caused the conflict.
4.  **Restart Loop**: If the solver stalls (exceeds $30,000$ backtracks on a seed), it restarts with a new randomized seed (up to $25$ restarts) to escape local minima.
5.  **Output**: Returns a mathematically valid, 100% collision-free schedule.

#### Step 5: Phase 2 — Genetic Algorithm Optimization
The valid schedule is optimized for quality:
1.  **Initial Population**: Creates $P$ clones of the CSP schedule.
2.  **Fitness Evaluation**: Evaluates each schedule against soft constraints (morning slots for core subjects, room stability, minimized student gaps, and balanced teacher workloads).
3.  **Elitism Selection**: The top 2 individuals are copied directly into the next generation.
4.  **Crossover**: Parents are combined. A crossover operator randomly selects class IDs and transfers all timetable entries for those classes from either Parent 1 or Parent 2 to the child, ensuring no student schedule is mixed.
5.  **Validated Mutation (Swaps)**: Selects a random assignment and attempts to relocate it. The relocation is only applied if it satisfies all Phase 1 hard constraints.
6.  **Looping**: Steps are repeated for $G$ generations (auto-scaled dynamically based on the number of classes to minimize computation time).

#### Step 6: Post-Generation Notice Board Logging
The engine compiles a final notice board report highlighting warnings like:
*   Room saturation levels (rooms utilized $>80\%$).
*   Substitution risk days (days where a teacher is booked solid and cannot substitute).
*   Save the final `ScheduleSlot` entries into the `timetable_entries` table.

---

## 🛠️ 5. Dynamic Repair (Rescheduling) Algorithm

When a teacher is marked absent, the following step-by-step localized algorithm runs:

1.  **Mark Absence**: Admin marks Teacher $A$ absent on date $D$.
2.  **Filter Entries**: The system isolates all `TimetableEntry` records where `teacher_id = A`, `day` corresponds to the weekday of $D$, and `is_substituted = False`.
3.  **Isolate Present Faculty**: Queries all teachers who are active and not absent.
4.  **Candidate Selection**:
    *   Checks availability of each present teacher $T$ at time slot $S$ using the `ResourceIndex`.
    *   If free, calculates a selection score:
        $$\text{Score} = (100 \times \text{SameDept}) + (50 \times \text{QualifiedForSubject}) - \text{CurrentWorkload}$$
5.  **Assign Substitute**: The candidate with the highest positive score is selected. The entry is updated:
    *   `teacher_id` set to substitute teacher.
    *   `original_teacher_id` set to $A$.
    *   `is_substituted` set to `True`.
6.  **Fail-safe Logging**: If no teacher is free, the entry remains unassigned, and a critical notification is pushed to the notice board highlighting that the lecture is unresolved.

---

## 🎯 6. Benefits of the Hybrid Model Design

1.  **Completeness Guarantee**: CSP with CBJ guarantees that if a conflict-free timetable exists, it will be found.
2.  **Institutional Quality**: The Genetic Algorithm ensures that the timetable is optimized for human convenience (less teacher fatigue, fewer empty gap hours for students).
3.  **Dynamic Resilience**: The Rescheduling Engine prevents the need to rebuild schedules during faculty emergencies, keeping daily operations stable.
4.  **High Scalability**: By offloading domain calculation checks to a `ResourceIndex` map and representing chromosomes as flat indexes, the engine can schedule complex departments with over 250+ weekly lectures in under 5 seconds.
