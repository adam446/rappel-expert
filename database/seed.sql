INSERT INTO recurring_tasks (
    title,
    description,
    amount,
    start_date,
    end_date,
    day_of_month,
    frequency,
    status
)
SELECT
    'Payer la facture mensuelle d''electricite',
    'Paiement mensuel de la facture d''electricite.',
    120.00,
    DATE '2026-06-15',
    DATE '2027-06-15',
    15,
    'monthly',
    'active'
WHERE NOT EXISTS (
    SELECT 1
    FROM recurring_tasks
    WHERE title = 'Payer la facture mensuelle d''electricite'
      AND start_date = DATE '2026-06-15'
);

WITH example_task AS (
    SELECT id, title, description, amount
    FROM recurring_tasks
    WHERE title = 'Payer la facture mensuelle d''electricite'
      AND start_date = DATE '2026-06-15'
    ORDER BY id
    LIMIT 1
),
dates AS (
    SELECT generate_series(
        DATE '2026-06-15',
        DATE '2027-06-15',
        INTERVAL '1 month'
    )::date AS due_date
)
INSERT INTO reminders (
    recurring_task_id,
    title,
    description,
    amount,
    due_date,
    status,
    expert_state,
    color
)
SELECT
    task.id,
    task.title,
    task.description,
    task.amount,
    dates.due_date,
    'pending',
    CASE
        WHEN dates.due_date < CURRENT_DATE THEN 'overdue'
        WHEN dates.due_date <= CURRENT_DATE + 7 THEN 'urgent'
        ELSE 'normal'
    END,
    CASE
        WHEN dates.due_date < CURRENT_DATE THEN 'red'
        WHEN dates.due_date <= CURRENT_DATE + 7 THEN 'orange'
        ELSE 'blue'
    END
FROM example_task AS task
CROSS JOIN dates
ON CONFLICT (recurring_task_id, due_date) DO NOTHING;
