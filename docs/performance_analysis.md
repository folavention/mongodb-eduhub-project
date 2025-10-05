Performance Analysis
1. Query Performance

Indexes:

Added indexes on frequently queried fields like userId, courseId, and enrollmentDate.

This reduced query times for user lookups, course filtering, and enrollment analytics.

Aggregation Pipelines:

Used $group and $project for analytics queries (e.g., total enrollments per course, average ratings).

With indexing in place, these pipelines ran efficiently even with growing data.

Projection Optimization:

Queries only return required fields (e.g., course title, category, price) instead of whole documents, which reduces I/O overhead.

2. Write Performance

Bulk Inserts:

For sample datasets, insert_many() was used instead of multiple insert_one() calls.

This reduced network round trips and improved seeding performance.

Validation Overhead:

JSON Schema validation slowed inserts when incorrect data types were provided (e.g., inserting an array into a string field).

Solution: Adjusted schema design and ensured proper field types in the insertion scripts.


3. Challenges & Solutions

Duplicate Key Errors:

Encountered when inserting sample data with the same _id.

Solution: Explicitly generate new ObjectId() values for each insert.

Schema Validation Errors:

Errors occurred when fields didn’t match schema types (e.g., array vs. string).

Solution: Updated the schema rules and ensured correct data formats in code.

Aggregation Projection Error:

$project initially caused an error by mixing exclusion and inclusion incorrectly.

Solution: Rewrote $project to properly map _id into courseId.

Inserting Courses:

For loop was creating x2 the number of range(), i didn't figure out why but.....

Solution: I used a while loop instead and it worked

4. Observations

Archiving significantly reduces load on active collections.

Indexing strategy and proper schema validation are key for both performance and data quality.

Aggregation pipelines are powerful but must be carefully designed to avoid performance bottlenecks.

Be careful with syntax when writing aggregation pipelines, because even small mistakes can break the entire query.