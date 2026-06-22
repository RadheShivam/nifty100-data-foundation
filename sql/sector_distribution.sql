SELECT
    broad_sector,
    COUNT(*)
FROM sectors
GROUP BY broad_sector
ORDER BY COUNT(*) DESC;