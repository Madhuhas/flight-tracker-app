# Flight Tracker Dashboard 🛬

A lightweight, real-time flight tracking web app built with:

- 📊 Flask backend with Excel integration
- 🌐 Frontend in HTML/CSS/JS
- 🔁 Live flight status from AeroDataBox API (cached to avoid rate limits)

---

## 🚀 Features

- Upload an Excel file with passenger + flight details
- Fetches real-time flight statuses (e.g. "Landed", "Scheduled")
- Responsive web dashboard with live highlighting
- Smart caching to avoid API rate limits
- Configurable for any airport or airline

## 📦 Project Structure

flight-tracker-app/ ├── backend/ │ ├── app.py # Flask API │ ├── flight_status.py # Live status fetcher │ ├── refresh_status.py # Background status cache builder │ ├── status_cache.json # Auto-generated flight status cache │ └── flights.xlsx # Your Excel source file ├── frontend/ │ ├── index.html │ ├── style.css │ └── script.js └── README.md


---

## 🛠️ Setup Instructions

📁 1. Clone this repo:
```bash
git clone https://github.com/Madhuhas/flight-tracker-app.git
cd flight-tracker-app/backend
🐍 2. Install Python packages:
bash
pip install flask flask-cors requests pandas openpyxl
💾 3. Add your flights.xlsx file
Ensure it has these column headers:

First and Last Name | Phone Number | Check-Out Date | Check-Out Time | 
Arriving Airlines Name | Flight Number | Number Of Passenger | Arrival Airport
🔄 4. Build flight status cache
bash
python refresh_status.py
This saves live status info to status_cache.json

▶️ 5. Run the backend
bash
python app.py
It starts on http://localhost:5000/api/flights

🌐 6. View your dashboard
Open frontend/index.html in your browser.

⏱️ Optional: Schedule Automatic Refresh
Use Task Scheduler (Windows) or cron (Linux/macOS) to run refresh_status.py every 10–15 minutes so your dashboard stays fresh.

📄 License
This project is open-source under the MIT License. Customize and build on it freely!

🙌 Credits
Created by Madhuhas Guided by Microsoft Copilot 💬 Powered by AeroDataBox
