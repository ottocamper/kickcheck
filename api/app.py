#!/usr/bin/env python3
"""
Flask API for KickCheck
Serves campaign and report data from the database
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import sys
import os

# Add database directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'database'))
from db_api import (
    get_all_campaigns,
    get_campaign_by_id,
    get_report_by_campaign_id,
    search_campaigns
)

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access

@app.route('/api/campaigns', methods=['GET'])
def get_campaigns():
    """Get all campaigns, optionally filtered by search query"""
    query = request.args.get('q', '')
    
    if query:
        campaigns = search_campaigns(query)
    else:
        campaigns = get_all_campaigns()
    
    # Format for frontend
    result = []
    for campaign in campaigns:
        report = get_report_by_campaign_id(campaign['id']) if campaign['verified'] else None
        
        campaign_data = {
            'name': campaign['name'],
            'creator': campaign['creator'],
            'grade': report['grade'] if report else None,
            'verified': bool(campaign['verified']),
            'kickstarterUrl': campaign['kickstarter_url'],
            'reportUrl': f"report.html?id={campaign['id']}" if report else None
        }
        result.append(campaign_data)
    
    return jsonify(result)

@app.route('/api/campaigns/<campaign_id>', methods=['GET'])
def get_campaign(campaign_id):
    """Get a single campaign by ID"""
    campaign = get_campaign_by_id(campaign_id)
    if not campaign:
        return jsonify({'error': 'Campaign not found'}), 404
    
    report = get_report_by_campaign_id(campaign_id) if campaign['verified'] else None
    
    return jsonify({
        'campaign': {
            'id': campaign['id'],
            'name': campaign['name'],
            'creator': campaign['creator'],
            'kickstarterUrl': campaign['kickstarter_url'],
            'verified': bool(campaign['verified'])
        },
        'report': report
    })

@app.route('/api/reports/<campaign_id>', methods=['GET'])
def get_report(campaign_id):
    """Get full report data for a campaign"""
    report = get_report_by_campaign_id(campaign_id)
    if not report:
        return jsonify({'error': 'Report not found'}), 404
    
    # Get campaign info
    campaign = get_campaign_by_id(campaign_id)
    
    # Format campaign history
    history = []
    for item in report.get('campaign_history', []):
        history.append({
            'campaign_name': item['campaign_name'],
            'status': item['status'],
            'delay_months': item.get('delay_months'),
            'kickstarter_url': item.get('kickstarter_url', '')
        })
    
    return jsonify({
        'title': campaign['name'],
        'creator': campaign['creator'],
        'grade': report['grade'],
        'overallScore': report['overall_score'],
        'scores': report.get('scores', {}),
        'manufacturingScores': report.get('manufacturing_scores', {}),
        'campaignHistory': history
    })

if __name__ == '__main__':
    app.run(debug=True, port=5001)

