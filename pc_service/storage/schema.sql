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

CREATE TABLE IF NOT EXISTS contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    phone_number TEXT UNIQUE,
    name TEXT,
    company TEXT,
    notes TEXT,
    last_call_at DATETIME,
    call_count INTEGER DEFAULT 0
);

CREATE INDEX idx_calls_start_time ON calls(start_time);
CREATE INDEX idx_suggestions_call_id ON realtime_suggestions(call_id);
CREATE INDEX idx_contacts_phone ON contacts(phone_number);
