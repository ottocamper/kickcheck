-- KickCheck Database Schema

-- Campaigns table - stores all Kickstarter campaigns
CREATE TABLE IF NOT EXISTS campaigns (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    creator TEXT NOT NULL,
    kickstarter_url TEXT NOT NULL,
    verified BOOLEAN DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Reports table - stores verification reports
CREATE TABLE IF NOT EXISTS reports (
    id TEXT PRIMARY KEY,
    campaign_id TEXT NOT NULL,
    grade TEXT,
    overall_score INTEGER,
    report_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (campaign_id) REFERENCES campaigns(id)
);

-- Score breakdown table - stores detailed scores
CREATE TABLE IF NOT EXISTS score_breakdown (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    report_id TEXT NOT NULL,
    category TEXT NOT NULL,
    score INTEGER NOT NULL,
    max_score INTEGER DEFAULT 25,
    FOREIGN KEY (report_id) REFERENCES reports(id)
);

-- Campaign history table - stores previous campaigns by creators
CREATE TABLE IF NOT EXISTS campaign_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    report_id TEXT NOT NULL,
    campaign_name TEXT NOT NULL,
    status TEXT NOT NULL, -- 'on-time' or 'delayed'
    delay_months INTEGER,
    kickstarter_url TEXT,
    FOREIGN KEY (report_id) REFERENCES reports(id)
);

-- Manufacturing scores table - stores manufacturing sub-scores
CREATE TABLE IF NOT EXISTS manufacturing_scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    report_id TEXT NOT NULL,
    partners_score INTEGER,
    timeline_score INTEGER,
    financial_score INTEGER,
    FOREIGN KEY (report_id) REFERENCES reports(id)
);

-- Indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_campaigns_verified ON campaigns(verified);
CREATE INDEX IF NOT EXISTS idx_reports_campaign_id ON reports(campaign_id);
CREATE INDEX IF NOT EXISTS idx_score_breakdown_report_id ON score_breakdown(report_id);

