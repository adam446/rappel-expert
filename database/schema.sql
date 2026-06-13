CREATE TABLE IF NOT EXISTS recurring_tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    amount NUMERIC(10, 2),
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    day_of_month INTEGER NOT NULL CHECK (day_of_month BETWEEN 1 AND 31),
    frequency VARCHAR(50) NOT NULL DEFAULT 'monthly',
    status VARCHAR(50) NOT NULL DEFAULT 'active',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS reminders (
    id SERIAL PRIMARY KEY,
    recurring_task_id INTEGER NOT NULL REFERENCES recurring_tasks(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    amount NUMERIC(10, 2),
    due_date DATE NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'pending',
    expert_state VARCHAR(50) NOT NULL DEFAULT 'normal',
    color VARCHAR(50) NOT NULL DEFAULT 'blue',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_reminders_recurring_task_due_date
        UNIQUE (recurring_task_id, due_date)
);

CREATE INDEX IF NOT EXISTS idx_reminders_recurring_task_id
    ON reminders(recurring_task_id);

CREATE INDEX IF NOT EXISTS idx_reminders_due_date
    ON reminders(due_date);

CREATE INDEX IF NOT EXISTS idx_reminders_expert_state
    ON reminders(expert_state);
