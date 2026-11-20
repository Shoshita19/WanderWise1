# WanderWise – Smart India Travel Planner 🧭

> **Explore India. Your Budget. Your Journey.**

WanderWise is an intelligent, India-only travel planning web application built with **Python** and **Streamlit**. It recommends the most suitable Indian destinations based on your budget, trip duration, starting location, and travel interests. WanderWise calculates detailed cost estimates, builds practical day-wise itineraries, suggests verified hotels and attractions, and generates a downloadable, professionally formatted PDF travel report.

---

## 🌟 Key Features

1. **Authentic India-Only Recommendations**:
   - Curated dataset covering top destinations across Indian states (Himachal Pradesh, Uttarakhand, Rajasthan, Goa, Kerala, Karnataka, Tamil Nadu, Maharashtra, Sikkim, Meghalaya, and more).
   - Multi-factor recommendation algorithm scoring destinations based on interest overlap, budget fit, and duration suitability.

2. **Realistic Cost Estimation & Budget Analysis**:
   - Itemized expense breakdown across 6 essential categories:
     - Intercity Transportation
     - Accommodation
     - Food & Dining
     - Local Transportation
     - Sightseeing & Activities
     - Miscellaneous Buffer (~7%)
   - Automated budget status alerts: **Within Budget**, **Slightly Over Budget**, or **Over Budget**.
   - Displays total cost, cost per person, daily average expense, and remaining balance.

3. **Personalized Day-Wise Itinerary**:
   - Automatically generates structured schedules for morning, afternoon, and evening.
   - Geographically sensible pacing connecting top local attractions.

4. **Hotels & Nearby Attractions**:
   - Real, verified hotels across Budget, Standard, and Luxury tiers with price per night and location.
   - Sights and monuments with visiting hours and entry fees in Indian Rupees (₹).

5. **Destination-Specific Travel Tips**:
   - Best visiting season, climate and clothing advice, local culinary specialties, transportation guidance, and smart packing checklists.

6. **Executive Travel Dashboard**:
   - Clean, graphical-chart-free dashboard utilizing metric cards, structured tables, and travel readiness indicators.

7. **Instant PDF Report Generation & Browser Printing**:
   - High-resolution, multi-page PDF generated via **ReportLab** with dynamic page numbering, cost tables, itinerary, and travel disclaimers.
   - Direct browser print button (`window.print()`) for quick printing or saving.

---

## 📁 Project Folder Structure

WanderWise follows a clean, minimalist 4-file structure:

```
wander/
│
├── README.md            # Project overview, installation, and deployment documentation
├── destinations.csv     # Verified Indian destinations dataset (costs, hotels, sights, tips)
├── app.py               # Complete Streamlit application and recommendation engine
└── requirements.txt     # Python dependencies
```

---

## 🚀 How to Run Locally

### 1. Prerequisites
Ensure you have **Python 3.10+** installed on your system.

### 2. Clone or Navigate to the Project Folder
Open your terminal or PowerShell and navigate to the project directory:
```bash
cd wander
```

### 3. Create a Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies
Install all required libraries using `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 5. Launch the Application
Run the Streamlit app:
```bash
streamlit run app.py
```
The website will open automatically in your browser at `http://localhost:8501`.

---

## ☁️ How to Push to GitHub & Deploy on Streamlit Cloud

### Step 1: Initialize Git and Push to GitHub
1. Create a new public repository on [GitHub](https://github.com) named `wanderwise`.
2. In your terminal inside the `wander` folder, run:
```bash
git init
git add .
git commit -m "Initial commit - WanderWise India Travel Planner"
git branch -M main
git remote add origin https://github.com/<YOUR_GITHUB_USERNAME>/wanderwise.git
git push -u origin main
```

### Step 2: Deploy on Streamlit Community Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io) and log in with your GitHub account.
2. Click **New app**.
3. Select your repository: `wanderwise`.
4. Set the branch to `main`.
5. Set the Main file path to `app.py`.
6. Click **Deploy!**

Your website will be live with a shareable URL within 1-2 minutes!

---

## 🛠️ Technology Stack

- **Frontend & UI**: Streamlit, Custom Responsive CSS
- **Backend & Logic**: Python 3
- **Data Processing**: Pandas, NumPy
- **PDF Generation**: ReportLab
- **Data Storage**: CSV (`destinations.csv`)

---

## 📝 Disclaimers
All price estimates, hotel tariffs, and attraction fees are realistic approximations compiled from authentic Indian travel sources. Live market rates may vary based on holiday seasons, booking lead times, and local tariffs.
