#!/usr/bin/env python3
"""
Database API for KickCheck
Provides functions to query the database
"""

import sqlite3
import os
import json
from typing import List, Dict, Optional

DB_PATH = os.path.join(os.path.dirname(__file__), 'kickcheck.db')

def get_db_connection():
    """Get database connection"""
    return sqlite3.connect(DB_PATH)

def get_all_campaigns(verified_only: bool = False) -> List[Dict]:
    """Get all campaigns, optionally filtered by verification status"""
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    if verified_only:
        cursor.execute('''
            SELECT * FROM campaigns WHERE verified = 1 ORDER BY name
        ''')
    else:
        cursor.execute('''
            SELECT * FROM campaigns ORDER BY verified DESC, name
        ''')
    
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_campaign_by_id(campaign_id: str) -> Optional[Dict]:
    """Get a single campaign by ID"""
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM campaigns WHERE id = ?', (campaign_id,))
    row = cursor.fetchone()
    conn.close()
    
    return dict(row) if row else None

def get_report_by_campaign_id(campaign_id: str) -> Optional[Dict]:
    """Get full report data for a campaign"""
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Get report
    cursor.execute('''
        SELECT * FROM reports WHERE campaign_id = ?
    ''', (campaign_id,))
    report = cursor.fetchone()
    
    if not report:
        conn.close()
        return None
    
    report_dict = dict(report)
    report_id = report_dict['id']
    
    # Get score breakdown
    cursor.execute('''
        SELECT category, score, max_score FROM score_breakdown WHERE report_id = ?
    ''', (report_id,))
    scores = [dict(row) for row in cursor.fetchall()]
    report_dict['scores'] = {s['category']: s['score'] for s in scores}
    
    # Get manufacturing scores
    cursor.execute('''
        SELECT partners_score, timeline_score, financial_score 
        FROM manufacturing_scores WHERE report_id = ?
    ''', (report_id,))
    mfg = cursor.fetchone()
    if mfg:
        report_dict['manufacturing_scores'] = {
            'partners': mfg['partners_score'],
            'timeline': mfg['timeline_score'],
            'financial': mfg['financial_score']
        }
    
    # Get campaign history
    cursor.execute('''
        SELECT campaign_name, status, delay_months, kickstarter_url
        FROM campaign_history WHERE report_id = ?
        ORDER BY id
    ''', (report_id,))
    history = [dict(row) for row in cursor.fetchall()]
    report_dict['campaign_history'] = history
    
    conn.close()
    return report_dict

def search_campaigns(query: str) -> List[Dict]:
    """Search campaigns by name or creator"""
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    search_term = f"%{query}%"
    cursor.execute('''
        SELECT * FROM campaigns 
        WHERE name LIKE ? OR creator LIKE ?
        ORDER BY verified DESC, name
    ''', (search_term, search_term))
    
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def export_to_json(output_path: str = None):
    """Export all data to JSON format"""
    campaigns = get_all_campaigns()
    
    data = {
        'campaigns': []
    }
    
    for campaign in campaigns:
        campaign_data = dict(campaign)
        report = get_report_by_campaign_id(campaign['id'])
        if report:
            campaign_data['report'] = report
        data['campaigns'].append(campaign_data)
    
    json_str = json.dumps(data, indent=2, default=str)
    
    if output_path:
        with open(output_path, 'w') as f:
            f.write(json_str)
        print(f"Data exported to {output_path}")
    else:
        print(json_str)
    
    return json_str

if __name__ == '__main__':
    # Example usage
    print("All campaigns:")
    for campaign in get_all_campaigns():
        print(f"  - {campaign['name']} by {campaign['creator']} ({'Verified' if campaign['verified'] else 'Unverified'})")
    
    print("\nSearch for 'Smart':")
    for campaign in search_campaigns('Smart'):
        print(f"  - {campaign['name']}")

