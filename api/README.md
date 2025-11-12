# KickCheck API

Flask API server for serving campaign and report data from the database.

## Setup

1. Install dependencies:
```bash
pip3 install -r requirements.txt
```

2. Make sure the database is initialized and seeded:
```bash
cd ../database
python3 init_db.py
python3 seed_data.py
```

3. Run the API server:
```bash
python3 app.py
```

The API will be available at `http://localhost:5000`

## API Endpoints

### GET /api/campaigns
Get all campaigns, optionally filtered by search query.

**Query Parameters:**
- `q` (optional): Search query to filter campaigns by name or creator

**Response:**
```json
[
  {
    "name": "Campaign Name",
    "creator": "Creator Name",
    "grade": "A",
    "verified": true,
    "kickstarterUrl": "https://...",
    "reportUrl": "report.html?id=..."
  }
]
```

### GET /api/campaigns/<campaign_id>
Get a single campaign by ID.

### GET /api/reports/<campaign_id>
Get full report data for a campaign.

**Response:**
```json
{
  "title": "Campaign Name",
  "creator": "Creator Name",
  "grade": "A",
  "overallScore": 92,
  "scores": {
    "Business Legitimacy": 25,
    "Track Record": 23,
    ...
  },
  "manufacturingScores": {
    "partners": 22,
    "timeline": 20,
    "financial": 18
  },
  "campaignHistory": [...]
}
```

## Development

The API runs in debug mode by default. For production, set `debug=False` in `app.py`.

