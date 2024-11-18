-- Problem Name: 1251. Average Selling Price
-- Submission ID: https://leetcode.com/submissions/detail/1456658328/
-- Write your PostgreSQL query statement below
SELECT
    P.product_id,
    ROUND(
    (
        CASE WHEN SUM(units) IS NULL THEN 0
        ELSE SUM(units * price * 1.0) / SUM(units) END
    ), 2) AS average_price
FROM Prices P
LEFT JOIN UnitsSold U ON U.product_id = P.product_id AND 
(P.start_date <= U.purchase_date AND U.purchase_date <= P.end_date)
GROUP BY P.product_id;