-- Problem Name: Confirmation Rate
-- Submission ID: https://leetcode.com/submissions/detail/1455681880/
-- Write your PostgreSQL query statement below
WITH user_confitmations AS(
    SELECT user_id, COUNT(*) AS total, COALESCE(SUM(
    CASE WHEN action = 'confirmed' THEN 1.0 END 
    ), 0.0) AS confirmed_count,
    COALESCE(SUM(
    CASE WHEN action = 'timeout' THEN 1.0 END 
    ), 0.0) AS rejected_count
    
    FROM Signups
    LEFT JOIN Confirmations USING(user_id)
    GROUP BY user_id
)

SELECT user_id, 
    CASE 
         WHEN confirmed_count = 0 THEN 0.00
         ELSE ROUND(confirmed_count / total, 2)
    END confirmation_rate
FROM user_confitmations;

