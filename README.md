# Repair Request and Tracking System for UC Main Facilities
**Database:** `FixFlowDB` (Microsoft SQL Server / SSMS 22)  
**Theme:** University of Cebu (UC) Royal Blue & Clean White  
**Stack:** Python (Flask) + Modern HTML5, Tailwind CSS, FontAwesome  

---

## 🏛️ Project Overview
This web-based system facilitates maintenance reporting and real-time repair tracking for facilities across the **University of Cebu (UC) Main Campus**. 

The system maps directly to the exact database schema:
* `DEPARTMENT` — Academic and administrative divisions (CCS, Engineering, Facilities Office).
* `ROLE` — User permissions (Admin, Staff, Faculty, Student).
* `CATEGORIES` — Aircon/HVAC, Electrical, Plumbing, Carpentry, IT/AV, General Facilities.
* `STATUS` — Pending, Assigned, In Progress, Completed, Cancelled.
* `FLOOR` & `LOCATION` — Building, floor level, and specific classroom/lab rooms.
* `USERS` — Campus reporters and physical plant maintenance technicians.
* `REQUEST` — Repair ticket information, urgency/priority, issue labels, and occurrence counters.
* `ASSIGNMENT` — Work order dispatching, assigned technician, timestamps, and resolution remarks.

---

## 🎨 Three Core Interfaces

1. **Campus User Portal (`/`)**
   * **Submit Repair Form**: Dynamic floor-to-room cascading selector, urgency priority flags, and detailed descriptions.
   * **Real-time Ticket Tracker**: Enter Request ID (e.g. `101`) to view a 4-step live progress timeline (*Submitted → Assigned → In Progress → Completed*).

2. **Facilities Coordinator & Admin Dispatch (`/admin`)**
   * Operational KPI metrics (Total Requests, Pending Review, In Progress, Resolved).
   * Search and filter by Building, Room, Urgency, Category, and Status.
   * **Staff Assignment Modal**: Dispatch work orders directly to technicians.

3. **Technician / Maintenance Staff View (`/staff-dashboard`)**
   * Active work orders list for maintenance staff.
   * Action triggers: *"Start Repair Work"* (logs start time) and *"Mark as Completed"* (logs resolution remarks).

---

## 🚀 How to Run the System

1. Open your terminal in this project folder:
   ```powershell
   cd C:\Users\Jurelyn\OneDrive\Desktop\DBYSYS-PROJECT
   ```

2. Start the server:
   ```powershell
   python app.py
   ```
   *(Or double-click `run.bat`)*

3. Open your browser and navigate to:
   * **Public / Student Portal:** [http://127.0.0.1:5000](http://127.0.0.1:5000)
   * **Admin Dispatch Hub:** [http://127.0.0.1:5000/admin](http://127.0.0.1:5000/admin)
   * **Technician Work Orders:** [http://127.0.0.1:5000/staff-dashboard](http://127.0.0.1:5000/staff-dashboard)
