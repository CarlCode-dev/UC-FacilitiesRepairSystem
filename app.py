"""
Repair Request and Tracking System for UC Main Facilities
Database: FixFlowDB on Microsoft SQL Server (SSMS 22)
Theme: University of Cebu Royal Blue & Clean White
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import db

app = Flask(__name__)

# Ensure seed data is present in SSMS on startup
try:
    db.init_db_seed()
except Exception as e:
    print("[WARN] Database init check:", e)

@app.route('/uc-logo.png')
def serve_root_logo():
    """Serves uc-logo.png directly if requested from root."""
    return send_from_directory(os.path.dirname(__file__), 'uc-logo.png')

# ==============================================================================
# FLASK WEB ROUTES
# ==============================================================================

@app.route('/')
def index():
    """Campus User Portal - Submit Repair Request & Track Status"""
    requests_list = db.get_all_requests()
    pending_count = sum(1 for r in requests_list if r["status_name"] == "Pending")
    completed_count = sum(1 for r in requests_list if r["status_name"] == "Completed")

    return render_template(
        'index.html',
        active_page='portal',
        departments=db.get_departments(),
        categories=db.get_categories(),
        floors=db.get_floors(),
        locations=db.get_locations(),
        requests=requests_list,
        pending_count=pending_count,
        completed_count=completed_count
    )

@app.route('/admin')
def admin_dashboard():
    """Facilities Admin & Dispatch Dashboard"""
    requests_list = db.get_all_requests()
    staff_users = db.get_staff_users()

    pending_count = sum(1 for r in requests_list if r["status_name"] == "Pending")
    in_progress_count = sum(1 for r in requests_list if r["status_name"] == "In Progress")
    completed_count = sum(1 for r in requests_list if r["status_name"] == "Completed")

    return render_template(
        'admin_dashboard.html',
        active_page='admin',
        requests=requests_list,
        categories=db.get_categories(),
        staff_users=staff_users,
        pending_count=pending_count,
        in_progress_count=in_progress_count,
        completed_count=completed_count
    )

@app.route('/staff-dashboard')
def staff_dashboard():
    """Technician / Maintenance Staff View"""
    staff_users = db.get_staff_users()
    default_staff_id = staff_users[0]["user_id"] if staff_users else 2
    staff_id_param = request.args.get('staff_id', default=default_staff_id, type=int)
    
    assigned_jobs = db.get_staff_jobs(staff_id_param)

    return render_template(
        'staff_dashboard.html',
        active_page='staff',
        assigned_jobs=assigned_jobs,
        staff_users=staff_users,
        current_staff_id=staff_id_param
    )

# ==============================================================================
# REST API ENDPOINTS (CONNECTED DIRECTLY TO SQL SERVER FixFlowDB)
# ==============================================================================

@app.route('/api/submit-request', methods=['POST'])
def api_submit_request():
    """Submits a new repair request directly into SQL Server FixFlowDB."""
    data = request.get_json() or {}

    reporter_info = {
        "first_name": data.get("first_name", "").strip(),
        "last_name": data.get("last_name", "").strip(),
        "school_id_no": data.get("school_id_no", "").strip(),
        "email": data.get("email", "").strip(),
        "contact_no": data.get("contact_no", "").strip(),
        "department_id": data.get("department_id", 1)
    }

    # Handle optional image attachment
    image_url = None
    image_data = data.get("image_data")
    if image_data and image_data.startswith("data:image/"):
        import base64
        import time
        try:
            header, encoded = image_data.split(",", 1)
            ext = "jpg"
            if "png" in header:
                ext = "png"
            elif "webp" in header:
                ext = "webp"
            filename = f"issue_{int(time.time())}_{data.get('location_id', 1)}.{ext}"
            upload_dir = os.path.join(os.path.dirname(__file__), "static", "uploads")
            os.makedirs(upload_dir, exist_ok=True)
            filepath = os.path.join(upload_dir, filename)
            with open(filepath, "wb") as f:
                f.write(base64.b64decode(encoded))
            image_url = f"/static/uploads/{filename}"
        except Exception as img_err:
            print("[WARN] Image save failed:", img_err)

    # Resolve location from room_no input (1 - 800) and floor_id
    location_id = data.get("location_id")
    room_no = data.get("room_no")
    floor_id = data.get("floor_id")

    if room_no and floor_id:
        try:
            location_id = db.get_or_create_location(int(floor_id), str(room_no).strip())
        except Exception as loc_err:
            print("[WARN] Error resolving location:", loc_err)
            location_id = 1
    elif not location_id:
        location_id = 1

    request_info = {
        "location_id": location_id,
        "category_id": data.get("category_id"),
        "description_label": data.get("description_label", "").strip(),
        "description": data.get("description", "").strip(),
        "priority": data.get("priority", "Medium"),
        "image_url": image_url
    }

    if not request_info["description_label"] or not request_info["description"]:
        return jsonify({"success": False, "message": "Problem label and detailed description are required."}), 400

    try:
        new_request_id = db.create_request(reporter_info, request_info)
        return jsonify({
            "success": True,
            "request_id": new_request_id,
            "message": "Repair request successfully recorded in FixFlowDB."
        })
    except Exception as e:
        return jsonify({"success": False, "message": f"Database error: {str(e)}"}), 500

@app.route('/api/track/<query>', methods=['GET'])
def api_track_request(query):
    """Queries SQL Server FixFlowDB by request_id (e.g. 1) or school_id_no."""
    try:
        match_req = db.get_request_by_id(query)
        if not match_req:
            return jsonify({"success": False, "message": f"No ticket found matching '{query}' in FixFlowDB."}), 404

        return jsonify({
            "success": True,
            "request": match_req
        })
    except Exception as e:
        return jsonify({"success": False, "message": f"Query error: {str(e)}"}), 500

@app.route('/api/assign', methods=['POST'])
def api_assign_staff():
    """Updates ASSIGNMENT table and sets REQUEST status to 'Assigned' in SQL Server."""
    data = request.get_json() or {}
    try:
        request_id = int(data.get("request_id"))
        staff_id = int(data.get("staff_id"))
        remarks = data.get("remarks", "")

        db.assign_staff(request_id, staff_id, remarks)
        return jsonify({"success": True, "message": "Technician successfully assigned in FixFlowDB."})
    except Exception as e:
        return jsonify({"success": False, "message": f"Assignment error: {str(e)}"}), 500

@app.route('/api/update-job-status', methods=['POST'])
def api_update_job_status():
    """Updates work order progress in SQL Server FixFlowDB."""
    data = request.get_json() or {}
    try:
        assignment_id = int(data.get("assignment_id"))
        request_id = int(data.get("request_id"))
        action = data.get("action") # 'start' or 'complete'
        remarks = data.get("remarks", "")

        db.update_job_status(assignment_id, request_id, action, remarks)
        return jsonify({"success": True, "message": "Work order status updated in FixFlowDB."})
    except Exception as e:
        return jsonify({"success": False, "message": f"Update error: {str(e)}"}), 500

# ==============================================================================
# MAIN ENTRYPOINT
# ==============================================================================

if __name__ == '__main__':
    print("=" * 70)
    print("  Repair Request and Tracking System for UC Main Facilities")
    print("  Database: FixFlowDB (LIVE ON SSMS / SQLEXPRESS)")
    print("  Theme: UC Royal Blue & Clean White")
    print("  Server running at: http://127.0.0.1:5000")
    print("=" * 70)
    app.run(debug=True, port=5000)
