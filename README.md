# KickCheck

KickCheck independently verifies Kickstarter campaigns, giving backers confidence that projects can actually deliver.

## Project Structure

- `index.html` - Main landing page with hero section, comparison, pricing, and process
- `browse.html` - Campaign browser where backers can search and view verified campaigns
- `report.html` - Detailed verification reports with scores and methodology

## Features

- **Landing Page**: Modern, responsive design with verification process explanation
- **Campaign Browser**: Searchable list of campaigns with verification status
- **Detailed Reports**: Comprehensive verification reports with:
  - Numerical scores for each component
  - Campaign history tracking
  - Visual indicators for delays
  - Methodology modal

## Getting Started

### 1. Initialize Database

First, set up the database:
```bash
cd database
python3 init_db.py
python3 seed_data.py
```

### 2. Start the API Server

Install dependencies and start the API:
```bash
cd api
pip3 install -r requirements.txt
python3 app.py
```

The API will run on `http://localhost:5000`

### 3. Open the Frontend

Open `index.html` in a web browser to view the landing page.

**Note:** The frontend requires the API server to be running to display campaign data.

## Development

All changes should be committed and pushed to GitHub:

```bash
git add .
git commit -m "Your commit message"
git push origin main
```

