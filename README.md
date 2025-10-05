# EduHub Project

EduHub is a MongoDB-based learning management system simulation. It demonstrates database design, data modeling, and aggregation pipelines using **PyMongo** in Python. The project includes collections for users, courses, enrollments, lessons, assignments, and submissions.

---

## 📌 Features

* User management (students and instructors)
* Course creation and enrollment
* Lesson and assignment tracking
* Assignment submissions with feedback
* Analytics using MongoDB aggregation (enrollments, ratings, categories)
* Data validation and error handling
* Archiving strategy for old enrollments

---

## ⚙️ Project Setup Instructions

1. Clone this repository:

   ```bash
   git clone https://github.com/your-username/eduhub.git
   cd eduhub
   ```
2. Install dependencies:

   ```bash
   pip install pymongo faker
   ```
3. Make sure MongoDB is running locally or in a container (e.g., Docker).

   ```bash
   mongod --dbpath /your/db/path
   ```
4. Run the scripts to insert data and test queries:

   ```bash
   python insert_data.py
   python queries.py
   ```

---

## 🗄️ Database Schema Documentation

**Collections and Key Fields:**

* **users**: userId, email, roles, profile (bio, skills, etc.)
* **courses**: courseId, title, category, rating
* **enrollments**: enrollmentId, userId, courseId, enrollmentDate
* **lessons**: lessonId, courseId, title, content
* **assignments**: assignmentId, courseId, title, description
* **submissions**: submissionId, studentId, courseId, content, feedback

---

## 📊 Query Explanations

* **Total enrollment per course**: Groups enrollments by courseId and counts.
* **Average course rating**: Groups courses by courseId and computes average rating.
* **Group by category**: Groups courses by category and counts total courses.

---

## ⚡ Performance Analysis

* Indexes created on `userId`, `courseId`, and `category` improved query performance.
* Aggregation pipelines were optimized using `$group` + `$project`.
* Identified bottlenecks with `$lookup` on large collections and solved by pre-embedding references.

---

## 🛠️ Challenges Faced & Solutions

* **Schema validation errors** → Fixed by aligning inserted documents with MongoDB schema rules.
* **Duplicate key errors** → Used `ObjectId()` and careful `_id` handling.
* **Aggregation pipeline syntax issues** → Solved by step-by-step testing in MongoDB shell.

---

## 📂 Sample Data

Check the `sample_data.json` file for sample documents across collections.

---

## 📜 License

This project is licensed under the **MIT License** – feel free to use, learn, and adapt.
