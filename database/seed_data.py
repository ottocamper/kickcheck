#!/usr/bin/env python3
"""
Seed the database with initial sample data
"""

import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), 'kickcheck.db')

# Sample data
CAMPAIGNS = [
    {
        'id': 'nexus-hub',
        'name': 'The Ultimate Smart Home Hub',
        'creator': 'Nexus Technologies',
        'kickstarter_url': 'https://www.kickstarter.com/projects/nexus/smart-home-hub',
        'verified': True
    },
    {
        'id': 'ecoflow',
        'name': 'EcoFlow: Sustainable Water Bottle System',
        'creator': 'GreenLife Innovations',
        'kickstarter_url': 'https://www.kickstarter.com/projects/greenlife/ecoflow-bottle',
        'verified': True
    },
    {
        'id': 'fittrack',
        'name': 'FitTrack AI - Next-Gen Fitness Tracker',
        'creator': 'FitAI Technologies',
        'kickstarter_url': 'https://www.kickstarter.com/projects/fitai/fittrack',
        'verified': True
    },
    {
        'id': 'audiotech',
        'name': 'AirPods Pro Alternative - Premium Wireless Earbuds',
        'creator': 'AudioTech Industries',
        'kickstarter_url': 'https://www.kickstarter.com/projects/audiotech/wireless-earbuds',
        'verified': True
    },
    {
        'id': 'solarcharge',
        'name': 'SolarCharge Pro - Portable Power Station',
        'creator': 'SolarTech Solutions',
        'kickstarter_url': 'https://www.kickstarter.com/projects/solartech/solarcharge',
        'verified': False
    },
    {
        'id': 'ecopack',
        'name': 'EcoPack - Sustainable Travel Backpack',
        'creator': 'EcoWear Collective',
        'kickstarter_url': 'https://www.kickstarter.com/projects/ecowear/ecopack',
        'verified': False
    }
]

REPORTS = {
    'nexus-hub': {
        'grade': 'A',
        'overall_score': 92,
        'scores': {
            'businessLegitimacy': 25,
            'trackRecord': 23,
            'manufacturing': 20,
            'financial': 18,
            'communication': 22
        },
        'manufacturing_scores': {
            'partners': 22,
            'timeline': 20,
            'financial': 18
        },
        'campaign_history': [
            {'name': 'Smart Thermostat Pro', 'status': 'on-time', 'delay': None, 'url': 'https://www.kickstarter.com/projects/nexus/thermostat'},
            {'name': 'Home Security Camera System', 'status': 'on-time', 'delay': None, 'url': 'https://www.kickstarter.com/projects/nexus/camera'},
            {'name': 'IoT Light Switch', 'status': 'delayed', 'delay': 8, 'url': 'https://www.kickstarter.com/projects/nexus/lightswitch'}
        ]
    },
    'ecoflow': {
        'grade': 'B+',
        'overall_score': 85,
        'scores': {
            'businessLegitimacy': 24,
            'trackRecord': 21,
            'manufacturing': 18,
            'financial': 16,
            'communication': 20
        },
        'manufacturing_scores': {
            'partners': 20,
            'timeline': 18,
            'financial': 16
        },
        'campaign_history': [
            {'name': 'EcoBottle Original', 'status': 'on-time', 'delay': None, 'url': 'https://www.kickstarter.com/projects/greenlife/ecobottle'},
            {'name': 'Reusable Coffee Cup', 'status': 'on-time', 'delay': None, 'url': 'https://www.kickstarter.com/projects/greenlife/cup'},
            {'name': 'Travel Water Filter', 'status': 'delayed', 'delay': 6, 'url': 'https://www.kickstarter.com/projects/greenlife/filter'}
        ]
    },
    'fittrack': {
        'grade': 'B',
        'overall_score': 78,
        'scores': {
            'businessLegitimacy': 22,
            'trackRecord': 19,
            'manufacturing': 16,
            'financial': 15,
            'communication': 18
        },
        'manufacturing_scores': {
            'partners': 18,
            'timeline': 16,
            'financial': 15
        },
        'campaign_history': [
            {'name': 'FitBand Basic', 'status': 'on-time', 'delay': None, 'url': 'https://www.kickstarter.com/projects/fitai/fitband'},
            {'name': 'Smart Scale Pro', 'status': 'delayed', 'delay': 10, 'url': 'https://www.kickstarter.com/projects/fitai/scale'}
        ]
    },
    'audiotech': {
        'grade': 'A-',
        'overall_score': 88,
        'scores': {
            'businessLegitimacy': 25,
            'trackRecord': 22,
            'manufacturing': 19,
            'financial': 17,
            'communication': 21
        },
        'manufacturing_scores': {
            'partners': 21,
            'timeline': 19,
            'financial': 17
        },
        'campaign_history': [
            {'name': 'Wireless Headphones V1', 'status': 'on-time', 'delay': None, 'url': 'https://www.kickstarter.com/projects/audiotech/headphones1'},
            {'name': 'Bluetooth Speaker', 'status': 'on-time', 'delay': None, 'url': 'https://www.kickstarter.com/projects/audiotech/speaker'},
            {'name': 'Studio Monitor Headphones', 'status': 'delayed', 'delay': 7, 'url': 'https://www.kickstarter.com/projects/audiotech/monitor'}
        ]
    }
}

def seed_database():
    """Seed the database with sample data"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Insert campaigns
    for campaign in CAMPAIGNS:
        cursor.execute('''
            INSERT OR REPLACE INTO campaigns (id, name, creator, kickstarter_url, verified)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            campaign['id'],
            campaign['name'],
            campaign['creator'],
            campaign['kickstarter_url'],
            1 if campaign['verified'] else 0
        ))
    
    # Insert reports and related data
    for campaign_id, report_data in REPORTS.items():
        # Insert report
        cursor.execute('''
            INSERT OR REPLACE INTO reports (id, campaign_id, grade, overall_score)
            VALUES (?, ?, ?, ?)
        ''', (
            f"report-{campaign_id}",
            campaign_id,
            report_data['grade'],
            report_data['overall_score']
        ))
        
        report_id = f"report-{campaign_id}"
        
        # Insert score breakdown
        score_categories = {
            'businessLegitimacy': 'Business Legitimacy',
            'trackRecord': 'Track Record',
            'manufacturing': 'Manufacturing Readiness',
            'financial': 'Financial Planning',
            'communication': 'Communication & Transparency'
        }
        
        for key, label in score_categories.items():
            cursor.execute('''
                INSERT OR REPLACE INTO score_breakdown (report_id, category, score, max_score)
                VALUES (?, ?, ?, ?)
            ''', (
                report_id,
                label,
                report_data['scores'][key],
                25
            ))
        
        # Insert manufacturing scores
        mfg = report_data['manufacturing_scores']
        cursor.execute('''
            INSERT OR REPLACE INTO manufacturing_scores (report_id, partners_score, timeline_score, financial_score)
            VALUES (?, ?, ?, ?)
        ''', (
            report_id,
            mfg['partners'],
            mfg['timeline'],
            mfg['financial']
        ))
        
        # Insert campaign history
        for history_item in report_data['campaign_history']:
            cursor.execute('''
                INSERT OR REPLACE INTO campaign_history (report_id, campaign_name, status, delay_months, kickstarter_url)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                report_id,
                history_item['name'],
                history_item['status'],
                history_item.get('delay'),
                history_item['url']
            ))
    
    conn.commit()
    conn.close()
    print("Database seeded with sample data")

if __name__ == '__main__':
    seed_database()

