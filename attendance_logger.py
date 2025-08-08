import os
from datetime import datetime
import pandas as pd

class AttendanceLogger:
    def __init__(self):
        # Stores: {name: {"first_seen": datetime, "last_seen": datetime}}
        self.records = {}
        self.date_str = datetime.now().strftime("%Y-%m-%d")
        
        # Folder for attendance logs
        self.folder = "attendance_logs"
        os.makedirs(self.folder, exist_ok=True)

    def update(self, face_names):
        now = datetime.now()
        for name in face_names:
            if name == "Unknown":
                continue  # skip unknown faces for attendance
            if name not in self.records:
                self.records[name] = {
                    "first_seen": now,
                    "last_seen": now
                }
            else:
                self.records[name]["last_seen"] = now

    def save_to_excel(self):
        data = []
        for name, times in self.records.items():
            first_seen = times["first_seen"]
            last_seen = times["last_seen"]
            total_time = (last_seen - first_seen).total_seconds()
            
            data.append({
                "Name": name,
                "First Seen": first_seen.strftime("%H:%M:%S"),
                "Last Seen": last_seen.strftime("%H:%M:%S"),
                "Total Time (seconds)": round(total_time, 2)
            })

        df = pd.DataFrame(data)
        
        filename = os.path.join(self.folder, f"Attendance_{self.date_str}.xlsx")
        df.to_excel(filename, index=False)
        print(f"[INFO] Attendance saved to {filename}")
