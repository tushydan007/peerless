Question 1 => What is GIL (Global Interpreter Lock) in Python?

GIL means Global Interpreter LOCK. Imagine you are in a kitchen with multiple chefs (threads) who want to cook at the same time. But there's only one gas cookwer with one burner (CPU execution in Python), and the kitchen rules (Python's GIL) say that only one chef can use the gas cooker at a time, even if there are multiple chefs waiting.

This means that even if you have a powerful multi-core processor, Python can only execute one thread at a time when using the default CPython interpreter. It affects multi-threading, especially for tasks that require a lot of CPU power.

Pros of GIL :

1. Simplifies memory management – Makes Python safer and easier to use by preventing multiple threads from accessing and modifying data at the same time.
2. Faster for single-threaded tasks – Python runs efficiently for tasks that don’t require multiple threads.
3. Works well with I/O operations – If your program spends time waiting (e.g., downloading files, reading databases), threading can still be useful because waiting tasks don't need the CPU.

Cons of GIL :

1. Slows down multi-threaded CPU tasks – If your task is CPU-intensive (e.g., heavy calculations, data processing), Python cannot use multiple cores efficiently.
2. Not ideal for parallel computing – Other languages like Java and C++ can fully use multiple cores for threading, but Python struggles due to GIL.
3. Developers need workarounds – To handle CPU-heavy tasks efficiently, you often need multiprocessing (which runs separate processes instead of threads) or switch to tools like Cython or JIT compilers.



Question 2 => If you see that a SQL SELECT query is slow - what would you do to improve it?

If a SQL SELECT query is slow, I would take the following steps to optimize it:

1. Use EXPLAIN (MySQL, PostgreSQL) or EXPLAIN ANALYZE to understand how the query is executed.
2. Use query caching (e.g., Redis, database query cache) for frequent queries.
3. Analyze slow query logs and identify frequently slow queries.
4. Use composite indexes if multiple columns are frequently queried together.
5. From the django query written to query the database, when querying a table that has a primary key related field, if its one to many relationship, I would use the prefetch_related method and for one to one relationship, I would use the select_related method to query tht table.
