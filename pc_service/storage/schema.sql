-- Real-time Sales Assistant (v2.1, in-person sales mode)
-- 3 tables: calls, call_replays, realtime_suggestions
-- contacts removed: not used in v2.1.

CREATE TABLE IF NOT EXISTS calls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    start_time DATETIME NOT NULL,
    end_time DATETIME,
    duration_sec INTEGER,
    phone_number TEXT,
    contact_name TEXT,
    scenario TEXT,
    transcript TEXT,
    audio_path TEXT,
    mode TEXT DEFAULT 'in_person',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS call_replays (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    call_id INTEGER NOT NULL,
    summary TEXT,
    customer_concerns TEXT,
    objections TEXT,
    emotion_curve TEXT,
    highlights TEXT,
    improvements TEXT,
    next_actions TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (call_id) REFERENCES calls(id)
);

CREATE TABLE IF NOT EXISTS realtime_suggestions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    call_id INTEGER NOT NULL,
    timestamp DATETIME NOT NULL,
    customer_text TEXT,
    scenario TEXT,
    intent TEXT,
    emotion TEXT,
    recommended_script TEXT,
    next_step TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (call_id) REFERENCES calls(id)
);

CREATE INDEX IF NOT EXISTS idx_calls_start_time ON calls(start_time);
CREATE INDEX IF NOT EXISTS idx_calls_mode ON calls(mode);
CREATE INDEX IF NOT EXISTS idx_suggestions_call_id ON realtime_suggestions(call_id);