-- 1. SELECT: выбрать всех клиентов
SELECT * FROM customers;

-- 2. WHERE: выбрать только оплаченные заказы дороже 1500
SELECT *
FROM orders
WHERE status = 'paid' AND amount > 1500;

-- 3. JOIN: объединить данные о клиентах и заказах
SELECT customers.name,
       customers.city,
       customers.segment,
       orders.order_date,
       orders.amount,
       orders.category,
       orders.status
FROM customers
JOIN orders ON customers.customer_id = orders.customer_id;

-- 4. GROUP BY: агрегировать данные по категориям
SELECT category,
       COUNT(*) AS total_orders,
       ROUND(AVG(amount), 2) AS avg_amount,
       ROUND(SUM(amount), 2) AS total_revenue
FROM orders
WHERE status = 'paid'
GROUP BY category;

-- 5. GROUP BY по клиентам: основа для признаков
SELECT customer_id,
       COUNT(*) AS orders_count,
       ROUND(SUM(amount), 2) AS total_spent,
       ROUND(AVG(amount), 2) AS avg_check
FROM orders
WHERE status = 'paid'
GROUP BY customer_id;
