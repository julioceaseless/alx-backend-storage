-- Task 3: Ranks Bands by number of fans
-- Display country of origin and no. of fans
SELECT origin, SUM(fans) AS nb_fans
FROM metal_bands
GROUP BY origin
ORDER BY nb_fans DESC;
