"""
Database Service Layer for FixFlowDB (SSMS 22 / SQL Server)
Project: Repair Request and Tracking System for UC Main Facilities
"""

import pyodbc
from datetime import datetime

# Connection string for Microsoft SQL Server Express
DB_CONFIG = {
    "server": r"localhost\SQLEXPRESS",
    "database": "FixFlowDB",
    "driver": "{ODBC Driver 18 for SQL Server}",
    "trusted_connection": "yes",
    "trust_server_certificate": "yes"
}

def get_connection():
    """Establish and return an active pyodbc connection to FixFlowDB."""
    conn_str = (
        f"DRIVER={DB_CONFIG['driver']};"
        f"SERVER={DB_CONFIG['server']};"
        f"DATABASE={DB_CONFIG['database']};"
        f"Trusted_Connection={DB_CONFIG['trusted_connection']};"
        f"TrustServerCertificate={DB_CONFIG['trust_server_certificate']};"
    )
    return pyodbc.connect(conn_str)

def row_to_dict(cursor, row):
    """Convert pyodbc.Row to a standard Python dictionary."""
    if not row:
        return None
    columns = [column[0] for column in cursor.description]
    return dict(zip(columns, row))

def rows_to_dicts(cursor, rows):
    """Convert a list of pyodbc.Row to standard Python dictionaries."""
    if not rows:
        return []
    columns = [column[0] for column in cursor.description]
    return [dict(zip(columns, row)) for row in rows]

# ==============================================================================
# SEED INITIAL DATA IF TABLES ARE EMPTY
# ==============================================================================

def init_db_seed():
    """Seeds lookup tables and initial records into SSMS if empty."""
    conn = get_connection()
    cur = conn.cursor()
    try:
        # Check if DEPARTMENT is empty
        cur.execute("SELECT COUNT(*) FROM DEPARTMENT")
        if cur.fetchone()[0] == 0:
            print("[SEED] Seeding DEPARTMENT table...")
            departments = [
                ("College of Allied Engineering", "CAE Department at UC Main"),
                ("College of Arts and Sciences", "CAS Department at UC Main"),
                ("College of Business and Accountancy", "CBA Department at UC Main"),
                ("College of Computer Studies", "CCS Department at UC Main"),
                ("College of Criminal Justice", "CCJ Department at UC Main"),
                ("College of Customs and Administration", "CCA Department at UC Main"),
                ("College of Engineering", "COE Department at UC Main"),
                ("College of Hospitality Management", "CHM Department at UC Main"),
                ("College of Nursing", "CON Department at UC Main"),
                ("College of Social Work", "CSW Department at UC Main"),
                ("College of Teacher Education", "CTE Department at UC Main"),
                ("Facilities & Physical Plant Office", "Maintenance and Campus Operations"),
                ("General Services Office", "Custodial and Campus Services"),
            ]
            cur.executemany("INSERT INTO DEPARTMENT (department_name, department_desc) VALUES (?, ?)", departments)

        # Check if ROLE is empty
        cur.execute("SELECT COUNT(*) FROM ROLE")
        if cur.fetchone()[0] == 0:
            print("[SEED] Seeding ROLE table...")
            roles = [("Admin",), ("Staff",), ("Faculty",), ("Student",)]
            cur.executemany("INSERT INTO ROLE (role_name) VALUES (?)", roles)

        # Check if CATEGORIES is empty
        cur.execute("SELECT COUNT(*) FROM CATEGORIES")
        if cur.fetchone()[0] == 0:
            print("[SEED] Seeding CATEGORIES table...")
            categories = [
                ("Air Conditioning / HVAC", "Aircon repair, maintenance, cleaning, and temperature control"),
                ("Electrical", "Lighting, power outlets, circuit breakers, wiring issues"),
                ("Plumbing & Restroom", "Water leaks, clogged pipes, broken faucets, CR fixtures"),
                ("Carpentry & Furniture", "Broken desks, chairs, doors, locks, whiteboards, windows"),
                ("IT & AV Equipment", "Projectors, sound system, lab computers, network cabling"),
                ("General Facilities", "Wall paint, floor damage, ceiling leaks, physical hazards"),
            ]
            cur.executemany("INSERT INTO CATEGORIES (category_name, description) VALUES (?, ?)", categories)

        # Check if STATUS is empty
        cur.execute("SELECT COUNT(*) FROM STATUS")
        if cur.fetchone()[0] == 0:
            print("[SEED] Seeding STATUS table...")
            statuses = [
                ("Pending", "Request submitted and awaiting review/assignment"),
                ("Assigned", "Assigned to a maintenance technician"),
                ("In Progress", "Technician is actively working on the repair"),
                ("Completed", "Repair has been verified and resolved"),
                ("Cancelled", "Request was cancelled or marked as duplicate"),
            ]
            cur.executemany("INSERT INTO STATUS (status_name, description) VALUES (?, ?)", statuses)

        # Check if FLOOR is empty
        cur.execute("SELECT COUNT(*) FROM FLOOR")
        if cur.fetchone()[0] == 0:
            print("[SEED] Seeding FLOOR table...")
            floors = [
                ("Main Building", "Ground Floor"),
                ("Main Building", "2nd Floor"),
                ("Main Building", "3rd Floor"),
                ("Main Building", "4th Floor"),
                ("Main Building", "5th Floor"),
                ("Engineering Building", "1st Floor"),
                ("Engineering Building", "2nd Floor"),
            ]
            cur.executemany("INSERT INTO FLOOR (building, floor_name) VALUES (?, ?)", floors)

        # Check if LOCATION is empty
        cur.execute("SELECT COUNT(*) FROM LOCATION")
        if cur.fetchone()[0] == 0:
            print("[SEED] Seeding LOCATION table...")
            locations = [
                ("Main Building", "Room 101", 1),
                ("Main Building", "Faculty Room G/F", 1),
                ("Main Building", "Room 205 (Lecture)", 2),
                ("Main Building", "Room 208", 2),
                ("Main Building", "CCS Computer Lab 1", 3),
                ("Main Building", "CCS Computer Lab 2", 3),
                ("Main Building", "Male Comfort Room 3F", 3),
                ("Main Building", "Room 401", 4),
                ("Main Building", "Audio Visual Hall", 4),
                ("Engineering Building", "Circuits Lab 1F", 6),
                ("Engineering Building", "Drawing Room 2F", 7),
            ]
            cur.executemany("INSERT INTO LOCATION (building, room, floor_id) VALUES (?, ?, ?)", locations)

        # Check if USERS is empty
        cur.execute("SELECT COUNT(*) FROM USERS")
        if cur.fetchone()[0] == 0:
            print("[SEED] Seeding USERS table...")
            users = [
                ("Engr. Roberto", "Santos", "EMP-0012", "rsantos@uc.edu.ph", "hash_admin", "09171112233", 4, 1), # Admin
                ("Mark", "Fernandez", "TECH-104", "mfernandez@uc.edu.ph", "hash_staff1", "09185556677", 4, 2), # Electrician Staff
                ("Danilo", "Gomez", "TECH-109", "dgomez@uc.edu.ph", "hash_staff2", "09198889900", 4, 2), # HVAC Staff
                ("Althea", "Mercado", "22-0491-102", "amercado@uc.edu.ph", "hash_student", "09204445566", 1, 4), # Student
            ]
            cur.executemany(
                "INSERT INTO USERS (first_name, last_name, school_id_no, email, password_hash, contact_no, department_id, role_id) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                users
            )

        # Check if REQUEST is empty
        cur.execute("SELECT COUNT(*) FROM REQUEST")
        if cur.fetchone()[0] == 0:
            print("[SEED] Seeding sample REQUEST tickets...")
            sample_requests = [
                (4, 1, 5, 3, 1, datetime.now(), "Wall-mounted AC unit not blowing cold air", "The split-type aircon in front row only blows room temperature air.", "High"),
                (4, 2, 3, 1, 1, datetime.now(), "Fluorescent lighting flickering continuously", "Two fixtures keep blinking and buzzing during lectures.", "Medium"),
                (4, 3, 7, 1, 2, datetime.now(), "Severe faucet leak flooding floor", "Third faucet won't shut off completely; water spilling to hallway.", "Urgent"),
                (4, 4, 4, 4, 1, datetime.now(), "Broken wooden armchairs (5 units)", "Writing tablets detached from student chairs.", "Low"),
            ]
            cur.executemany(
                "INSERT INTO REQUEST (user_id, category_id, location_id, status_id, occurrence, request_date, description_label, description, priority) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                sample_requests
            )

        # Check if ASSIGNMENT is empty
        cur.execute("SELECT COUNT(*) FROM ASSIGNMENT")
        if cur.fetchone()[0] == 0:
            print("[SEED] Seeding sample ASSIGNMENT records...")
            sample_assignments = [
                (datetime.now(), datetime.now(), None, "Inspect capacitor and clean clogged coil.", 1, 3), # req 1 -> Danilo Gomez
                (datetime.now(), datetime.now(), datetime.now(), "Reinforced brackets and re-screwed tablets.", 4, 2), # req 4 -> Mark Fernandez
            ]
            cur.executemany(
                "INSERT INTO ASSIGNMENT (date_assigned, date_started, date_completed, remarks, request_id, staff_id) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                sample_assignments
            )

        conn.commit()
        print("[SUCCESS] FixFlowDB initial seed check complete.")
    except Exception as e:
        conn.rollback()
        print("[ERROR] Seed check error:", e)
    finally:
        cur.close()
        conn.close()

# ==============================================================================
# DATA QUERY FUNCTIONS (1-to-1 WITH FixFlowDB SCHEMA)
# ==============================================================================

def get_departments():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT department_id, department_name, department_desc FROM DEPARTMENT ORDER BY department_id")
    res = rows_to_dicts(cur, cur.fetchall())
    conn.close()
    return res

def get_categories():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT category_id, category_name, description FROM CATEGORIES ORDER BY category_id")
    res = rows_to_dicts(cur, cur.fetchall())
    conn.close()
    return res

def get_floors():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT floor_id, building, floor_name FROM FLOOR ORDER BY floor_id")
    res = rows_to_dicts(cur, cur.fetchall())
    conn.close()
    return res

def get_locations():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT location_id, building, room, floor_id FROM LOCATION ORDER BY floor_id, room")
    res = rows_to_dicts(cur, cur.fetchall())
    conn.close()
    return res

def get_or_create_location(floor_id, room_no):
    """
    Finds or creates a LOCATION record for a room number (1-800) on a given floor.
    Ensures any room number from 1 to 800 links cleanly into FixFlowDB.
    """
    conn = get_connection()
    cur = conn.cursor()
    try:
        # Normalize room label (e.g. '304' -> 'Room 304')
        room_str = f"Room {room_no}" if not str(room_no).lower().startswith("room") else str(room_no)
        
        # Look up building from FLOOR table
        cur.execute("SELECT building FROM FLOOR WHERE floor_id = ?", (floor_id,))
        floor_row = cur.fetchone()
        building = floor_row[0] if floor_row else "Main Building"

        # Check if already exists in LOCATION table
        cur.execute("SELECT location_id FROM LOCATION WHERE floor_id = ? AND (room = ? OR room = ?)", 
                    (floor_id, room_str, str(room_no)))
        loc_row = cur.fetchone()
        if loc_row:
            return loc_row[0]

        # Insert new room into LOCATION table
        cur.execute(
            """
            INSERT INTO LOCATION (building, room, floor_id)
            OUTPUT INSERTED.location_id
            VALUES (?, ?, ?)
            """,
            (building, room_str, floor_id)
        )
        new_loc_id = cur.fetchone()[0]
        conn.commit()
        return new_loc_id
    finally:
        cur.close()
        conn.close()

def get_staff_users():
    conn = get_connection()
    cur = conn.cursor()
    query = """
        SELECT u.user_id, u.first_name, u.last_name, u.school_id_no, u.email, u.contact_no,
               u.department_id, d.department_name, u.role_id, r.role_name
        FROM USERS u
        JOIN DEPARTMENT d ON u.department_id = d.department_id
        JOIN ROLE r ON u.role_id = r.role_id
        WHERE r.role_name IN ('Staff', 'Admin')
        ORDER BY u.first_name
    """
    cur.execute(query)
    res = rows_to_dicts(cur, cur.fetchall())
    conn.close()
    return res

def get_all_requests():
    """Fetches all repair requests with full joins to display on Admin & Public Portal."""
    conn = get_connection()
    cur = conn.cursor()
    query = """
        SELECT 
            r.request_id,
            CONVERT(VARCHAR(16), r.request_date, 120) AS request_date,
            r.description_label,
            r.description,
            r.priority,
            r.occurrence,
            r.image_url,
            s.status_id,
            s.status_name,
            c.category_id,
            c.category_name,
            l.location_id,
            l.room,
            l.building,
            f.floor_name,
            u.user_id,
            ISNULL(u.first_name, 'Anonymous') AS first_name,
            ISNULL(u.last_name, '') AS last_name,
            ISNULL(u.school_id_no, 'N/A') AS school_id_no,
            d.department_name,
            a.assignment_id,
            a.staff_id,
            CONCAT(staff.first_name, ' ', staff.last_name) AS staff_name,
            CONVERT(VARCHAR(16), a.date_assigned, 120) AS date_assigned,
            CONVERT(VARCHAR(16), a.date_started, 120) AS date_started,
            CONVERT(VARCHAR(16), a.date_completed, 120) AS date_completed,
            a.remarks
        FROM REQUEST r
        JOIN CATEGORIES c ON r.category_id = c.category_id
        JOIN LOCATION l ON r.location_id = l.location_id
        JOIN FLOOR f ON l.floor_id = f.floor_id
        JOIN STATUS s ON r.status_id = s.status_id
        LEFT JOIN USERS u ON r.user_id = u.user_id
        LEFT JOIN DEPARTMENT d ON u.department_id = d.department_id
        LEFT JOIN ASSIGNMENT a ON r.request_id = a.request_id
        LEFT JOIN USERS staff ON a.staff_id = staff.user_id
        ORDER BY r.request_id DESC
    """
    cur.execute(query)
    res = rows_to_dicts(cur, cur.fetchall())
    conn.close()
    return res

def get_request_by_id(query_str):
    """Finds a single request by Request ID or School ID number."""
    conn = get_connection()
    cur = conn.cursor()
    clean_id = query_str.replace("REQ-", "").replace("req-", "").strip()

    base_query = """
        SELECT 
            r.request_id,
            CONVERT(VARCHAR(16), r.request_date, 120) AS request_date,
            r.description_label,
            r.description,
            r.priority,
            r.occurrence,
            r.image_url,
            s.status_id,
            s.status_name,
            c.category_id,
            c.category_name,
            l.location_id,
            l.room,
            l.building,
            f.floor_name,
            u.user_id,
            u.first_name,
            u.last_name,
            u.school_id_no,
            d.department_name,
            a.assignment_id,
            a.staff_id,
            CONCAT(staff.first_name, ' ', staff.last_name) AS staff_name,
            CONVERT(VARCHAR(16), a.date_assigned, 120) AS date_assigned,
            CONVERT(VARCHAR(16), a.date_started, 120) AS date_started,
            CONVERT(VARCHAR(16), a.date_completed, 120) AS date_completed,
            a.remarks
        FROM REQUEST r
        JOIN CATEGORIES c ON r.category_id = c.category_id
        JOIN LOCATION l ON r.location_id = l.location_id
        JOIN FLOOR f ON l.floor_id = f.floor_id
        JOIN STATUS s ON r.status_id = s.status_id
        LEFT JOIN USERS u ON r.user_id = u.user_id
        LEFT JOIN DEPARTMENT d ON u.department_id = d.department_id
        LEFT JOIN ASSIGNMENT a ON r.request_id = a.request_id
        LEFT JOIN USERS staff ON a.staff_id = staff.user_id
    """

    if clean_id.isdigit():
        cur.execute(base_query + " WHERE r.request_id = ?", (int(clean_id),))
        row = cur.fetchone()
        if row:
            res = row_to_dict(cur, row)
            conn.close()
            return res

    # Otherwise query by school_id_no
    cur.execute(base_query + " WHERE u.school_id_no = ? ORDER BY r.request_id DESC", (query_str.strip(),))
    row = cur.fetchone()
    res = row_to_dict(cur, row) if row else None
    conn.close()
    return res

def create_request(reporter_info, request_info):
    """
    Inserts reporter into USERS (if not yet registered)
    and logs a new record into REQUEST.
    """
    conn = get_connection()
    cur = conn.cursor()
    try:
        school_id_no = reporter_info.get("school_id_no", "").strip()
        first_name = reporter_info.get("first_name", "").strip()
        last_name = reporter_info.get("last_name", "").strip()
        email = reporter_info.get("email", "").strip()
        contact_no = reporter_info.get("contact_no", "").strip()
        department_id = int(reporter_info.get("department_id", 1))

        # Check existing user
        user_id = None
        if school_id_no:
            cur.execute("SELECT user_id FROM USERS WHERE school_id_no = ?", (school_id_no,))
            user_row = cur.fetchone()
            if user_row:
                user_id = user_row[0]

        if not user_id:
            # Create user
            cur.execute(
                """
                INSERT INTO USERS (first_name, last_name, school_id_no, email, password_hash, contact_no, department_id, role_id)
                OUTPUT INSERTED.user_id
                VALUES (?, ?, ?, ?, 'default_hash', ?, ?, 4)
                """,
                (first_name, last_name, school_id_no, email, contact_no, department_id)
            )
            user_id = cur.fetchone()[0]

        # Insert REQUEST
        cur.execute(
            """
            INSERT INTO REQUEST (user_id, category_id, location_id, status_id, occurrence, request_date, description_label, description, priority, image_url)
            OUTPUT INSERTED.request_id
            VALUES (?, ?, ?, 1, 1, GETDATE(), ?, ?, ?, ?)
            """,
            (
                user_id,
                int(request_info.get("category_id")),
                int(request_info.get("location_id")),
                request_info.get("description_label"),
                request_info.get("description"),
                request_info.get("priority", "Medium"),
                request_info.get("image_url")
            )
        )
        new_request_id = cur.fetchone()[0]
        conn.commit()
        return new_request_id
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        conn.close()

def assign_staff(request_id, staff_id, remarks):
    """Assigns staff in ASSIGNMENT and sets REQUEST status to 'Assigned' (status_id = 2)."""
    conn = get_connection()
    cur = conn.cursor()
    try:
        # Update Request Status to Assigned (2)
        cur.execute("UPDATE REQUEST SET status_id = 2 WHERE request_id = ?", (request_id,))

        # Check if an assignment record already exists
        cur.execute("SELECT assignment_id FROM ASSIGNMENT WHERE request_id = ?", (request_id,))
        existing = cur.fetchone()

        if existing:
            cur.execute(
                """
                UPDATE ASSIGNMENT 
                SET staff_id = ?, remarks = ?, date_assigned = GETDATE()
                WHERE request_id = ?
                """,
                (staff_id, remarks, request_id)
            )
        else:
            cur.execute(
                """
                INSERT INTO ASSIGNMENT (date_assigned, remarks, request_id, staff_id)
                VALUES (GETDATE(), ?, ?, ?)
                """,
                (remarks, request_id, staff_id)
            )

        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        conn.close()

def update_job_status(assignment_id, request_id, action, remarks=None):
    """Updates work order progress: 'start' (In Progress = 3) or 'complete' (Completed = 4)."""
    conn = get_connection()
    cur = conn.cursor()
    try:
        if action == "start":
            cur.execute("UPDATE REQUEST SET status_id = 3 WHERE request_id = ?", (request_id,))
            cur.execute("UPDATE ASSIGNMENT SET date_started = GETDATE() WHERE assignment_id = ?", (assignment_id,))
        elif action == "complete":
            cur.execute("UPDATE REQUEST SET status_id = 4 WHERE request_id = ?", (request_id,))
            if remarks:
                cur.execute(
                    """
                    UPDATE ASSIGNMENT 
                    SET date_completed = GETDATE(), 
                        remarks = CONCAT(ISNULL(remarks, ''), ' | Resolution: ', ?)
                    WHERE assignment_id = ?
                    """,
                    (remarks, assignment_id)
                )
            else:
                cur.execute("UPDATE ASSIGNMENT SET date_completed = GETDATE() WHERE assignment_id = ?", (assignment_id,))

        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        conn.close()

def get_staff_jobs(staff_id):
    """Fetches all work orders assigned to a specific technician."""
    conn = get_connection()
    cur = conn.cursor()
    query = """
        SELECT 
            r.request_id,
            CONVERT(VARCHAR(16), r.request_date, 120) AS request_date,
            r.description_label,
            r.description,
            r.priority,
            r.image_url,
            s.status_name,
            c.category_name,
            l.room,
            l.building,
            f.floor_name,
            a.assignment_id,
            a.staff_id,
            CONVERT(VARCHAR(16), a.date_assigned, 120) AS date_assigned,
            CONVERT(VARCHAR(16), a.date_started, 120) AS date_started,
            CONVERT(VARCHAR(16), a.date_completed, 120) AS date_completed,
            a.remarks
        FROM ASSIGNMENT a
        JOIN REQUEST r ON a.request_id = r.request_id
        JOIN STATUS s ON r.status_id = s.status_id
        JOIN CATEGORIES c ON r.category_id = c.category_id
        JOIN LOCATION l ON r.location_id = l.location_id
        JOIN FLOOR f ON l.floor_id = f.floor_id
        WHERE a.staff_id = ?
        ORDER BY a.assignment_id DESC
    """
    cur.execute(query, (staff_id,))
    res = rows_to_dicts(cur, cur.fetchall())
    conn.close()
    return res
