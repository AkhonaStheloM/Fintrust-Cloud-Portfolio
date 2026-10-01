CREATE OR REPLACE VIEW v_migration_portfolio AS
SELECT
    a.asset_id,
    a.asset_name,
    a.asset_type,
    a.environment,
    m.migration_strategy,
    m.migration_wave,
    m.target_service,
    m.estimated_cutover_date,
    m.status
FROM   asset_register a
JOIN   migration_plan  m ON a.asset_id = m.asset_id
WHERE  a.decommission_flag = 0
ORDER BY m.migration_wave, a.asset_name;

CREATE OR REPLACE VIEW v_wave_progress AS
SELECT
    migration_wave,
    COUNT(*) AS total_assets,
    SUM(CASE WHEN status = 'C' THEN 1 ELSE 0 END) AS complete,
    SUM(CASE WHEN status = 'I' THEN 1 ELSE 0 END) AS in_progress,
    SUM(CASE WHEN status = 'F' THEN 1 ELSE 0 END) AS failed,
    ROUND(
        100.0 * SUM(CASE WHEN status = 'C' THEN 1 ELSE 0 END) / COUNT(*), 1
    ) AS completion_pct
FROM   migration_plan
GROUP BY migration_wave
ORDER BY migration_wave;

SELECT * FROM v_wave_progress WHERE completion_pct < 50;

-- Total portfolio completion
SELECT
    SUM(total_assets) AS portfolio_total,
    SUM(complete) AS total_complete,
    ROUND(100.0 * SUM(complete) / SUM(total_assets), 1) AS overall_pct
FROM v_wave_progress;