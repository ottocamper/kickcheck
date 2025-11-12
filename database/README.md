# KickCheck Database

SQLite database for storing campaign verification data.

## Setup

1. Initialize the database:
```bash
python3 init_db.py
```

2. Seed with sample data:
```bash
python3 seed_data.py
```

## Database Structure

- **campaigns**: Stores all Kickstarter campaigns
- **reports**: Stores verification reports linked to campaigns
- **score_breakdown**: Detailed scores for each report category
- **campaign_history**: Previous campaign history for creators
- **manufacturing_scores**: Manufacturing-specific sub-scores

## Usage

### Query campaigns:
```python
from db_api import get_all_campaigns, get_campaign_by_id, search_campaigns

# Get all campaigns
campaigns = get_all_campaigns()

# Get verified campaigns only
verified = get_all_campaigns(verified_only=True)

# Search campaigns
results = search_campaigns("Smart")

# Get specific campaign
campaign = get_campaign_by_id("nexus-hub")
```

### Get full report:
```python
from db_api import get_report_by_campaign_id

report = get_report_by_campaign_id("nexus-hub")
```

### Export to JSON:
```python
from db_api import export_to_json

export_to_json("data.json")
```

## File: kickcheck.db

The SQLite database file will be created in this directory after running `init_db.py`.

