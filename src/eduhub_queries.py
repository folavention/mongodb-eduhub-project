#------IMPORTING REQUIREMENTS--------#

import random  # to pick random items from lists or fields
from pymongo import MongoClient  # to run MongoDB queries with Python
from faker import Faker  # could have used this for fake data, but we were asked to make it realistic, so we added names ourselves
from datetime import datetime, timedelta  # for handling dates and current time
import json  # to export or save results
from bson import ObjectId  # generates unique IDs for MongoDB documents
from mimesis import Person, Text, Internet  # similar to Faker, I used it for bio, avatar, and names
from pymongo.errors import DuplicateKeyError, WriteError  # to catch duplicate key errors in MongoDB
import time  # for timing operations
import pprint  # to print data in a readable format

#--------CONNECTION TO MONGODB----------#

client = MongoClient("mongodb://localhost:27017/")
db = client["eduhub_db"]   # To create a Database named eduhub_db

users =db["users"]     # To create collection named users
courses = db["courses"]    # To create collection named courses
enrollments = db["enrollments"]   #To create collection named enrollments
lessons = db["lessons"]     #To create collection named lessons
assignments = db["assignments"]    #To create collection named assignments
assignments_submissions = db["assignments_submissions"]    #To create collection named assignments_submissions


#-------- DATA PREPARATION/SCHEMA FOR USERS COLLECTION----------#


#------ Setup Mimesis ------

person = Person()   # generate person-related data
text = Text()       # generate random text
internet = Internet()  # generate emails, URLs, etc.


#----- Define User Data Lists-----

user_Id = [
    "EDU1001", "EDU1002", "EDU1003", "EDU1004", "EDU1005", "EDU1006", "EDU1007", "EDU1008", "EDU1009", "EDU1010",
    "EDU1011", "EDU1012", "EDU1013", "EDU1014", "EDU1015", "EDU1016", "EDU1017", "EDU1018", "EDU1019", "EDU1020"
]

First_Names = [
    "Kabiru", "Aisha", "Joan", "Michael", "Sarah", "Jerry", "Emily", "Daniel", "Sophia", "James",
    "Olivia", "John", "Pius", "Robert", "Olivia", "Joseph", "Isabella", "Charles", "Chidera", "Thomas"
]

Last_Names = [
    "Adekunle", "Mohammed", "Smith", "Johnson", "Brown", "Williams", "Jones", "Chidubem", "Abubakar", "David",
    "Frank", "Harry", "Adewale", "Usman", "Efe", "Wilson", "Anderson", "Thomas", "Stanley", "Okafor"
]

roles = ["student", "instructor"]  # possible roles for users

skills = [
    "Python", "JavaScript", "Data Analysis", "Machine Learning",
    "Web Development", "Database Management", "Public Speaking",
    "Cybersecurity", "Project Management", "Teaching"
]


#-------- Assign Instructors & Students ----

instructor_ids = random.sample(user_Id, k=4)  # randomly pick 4 instructors
student_ids = [uid for uid in user_Id if uid not in instructor_ids]  # rest are students


#------ Generate Student Users ------

users = []  # list to store all user documents

for i in range(16):
    first_names = random.choice(First_Names)
    last_names = random.choice(Last_Names)
    
    student = {
        "_id": ObjectId(),  # unique MongoDB ID
        "userId": random.sample(student_ids, k=1)[0],
        # Build an email: first name (lowercase) + one random character from last name + random number (10–100)
        # Example: "johns55@eduhub.com
        "email": f"{first_names.lower()}{random.choice(last_names).lower()}{random.randint(1, 100)}@eduhub.com",
        "first_name": first_names,
        "last_name": last_names,
        "roles": "student",
        "grades": [random.randint(50, 100) for _ in range(random.randint(4, 8))], #randomly select numbersfrom 50 -100 and for each the random should be between 4 to 8 e.g [58, 70,85,90]
        "dateJoined": datetime.now() + timedelta(weeks=28), # Set join date 28 weeks in the future from now
        "profile": {
            "bio": f"{first_names} is a dedicated student and {text.sentence()}",   # Generate a bio sentence with the first name and some random text
            "avatar": f"downloads/pictures/{internet.slug()}.png", # Create a fake file path for profile picture
            "skills": random.choice(skills),  # Randomly select one skill from the skills list
            "IsActive": random.choice([True, False])
        }
    }
    users.append(student)  # add to list


#------- Generate Instructor Users ------

for i in range(4):
    first_names = random.choice(First_Names)
    last_names = random.choice(Last_Names)
    
    instructor = {
        "_id": ObjectId(),
        "userId": random.sample(instructor_ids, k=1)[0],
        "email": f"{first_names.lower()}{random.choice(last_names).lower()}{random.randint(10, 100)}@eduhub.com",
        "first_name": first_names,
        "last_name": last_names,
        "roles": "instructor",
        "dateJoined": datetime.now() + timedelta(weeks=28),
        "profile": {
            "bio": f"{first_names} is a dedicated instructor and {text.sentence()}",
            "avatar": f"downloads/pictures/{internet.slug()}.png",
            "skills": random.choice(skills),
            "IsActive": random.choice([True, False])
        }
    }
    users.append(instructor)


#------- Insert Users Into MongoDB -------

db.users.insert_many(users)
print(f"Inserted {len(users)} users into the database.")  # confirmation message


#------ Predefined Courses ------

courses = [
    {"title": "Machine Learning 101", "category": "Data Science", "tag": "AI"},
    {"title": "Web Development", "category": "Programming", "tag": "HTML"},
    {"title": "Python", "category": "Python", "tag": "Basics"},
    {"title": "Data Science", "category": "Data Science", "tag": "DS"},
    {"title": "Graphic Design", "category": "Design", "tag": "Illustrator"},
    {"title": "Cybersecurity", "category": "IT & Software", "tag": "Security"},
    {"title": "Project Management", "category": "Business", "tag": "Agile"},
    {"title": "Data Analysis with Excel", "category": "Data Science", "tag": "Excel"},
]


#------- Generate 8 Randomized Courses ------

for i in range(8):
    course_choice = random.choice(courses)  # pick a template course
    
    course = {
        # "_id": ObjectId(),  # MongoDB will auto-generate _id
        "courseId": random.randint(100, 400),  # random course ID
        "title": course_choice["title"],  # from template
        "description": f"{text.sentence()}",  # random description using mimesis text
        "instructorId": random.sample(instructor_ids, k=1)[0],  # random instructor
        "category": course_choice["category"],  # category from template
        "level": random.choice(['beginner', 'intermediate', 'advanced']),  # course level
        "price": f"${random.randint(3, 20) * 10}",  # random price in $30-$200, logic-3 x 10 = 30(prices will be all round figure)
        "tag": course_choice["tag"],  # tag from template
        "createdAt": datetime.now(),  # timestamp for creation
        "updatedAt": datetime.now(),  # timestamp for last update
        "isPublished": random.choice([True, False]),  # published or not
        "rating": random.randint(1, 5)  # random rating
    }
    
    courses.append(course)  # add to the main courses list


#------- Insert Courses Into MongoDB ------

db.courses.insert_many(courses)
print(f"Inserted {len(courses)} courses into the database.")  # confirmation message


#-------- Generate Enrollments ------

enrollments = []  # list to hold generated enrollments

for i in range(15):
    # Fetch all courses from DB (only courseId and duration needed)
    course_docs = list(db.courses.find({}, {"courseId": 1, "duration": 1}))
    
    # Fetch all student IDs from users collection
    student_ids = [user.get("userId") for user in db.users.find({"roles": "student"}, {"userId": 1})]

    # Pick a random course
    course_doc = random.choice(course_docs)
    course_id = course_doc.get("courseId")
    duration_weeks = course_doc.get("duration", 8)  # default 8 weeks if duration not set

    # Create an enrollment document
    enrollment = {
        "startDate": datetime.now(),
        "endDate": datetime.now() + timedelta(weeks=48),  # set course end date (can be dynamic)
        "courseId": course_id,
        "studentId": random.choice(student_ids),
        "status": random.choice(['In_Progress', 'Completed'])
    }
    
    enrollments.append(enrollment)  # add to list


#------ Insert Enrollments Into MongoDB ------

db.enrollments.insert_many(enrollments)
print(f"Inserted {len(enrollments)} enrollments into the database.")  # confirmation message


#------ Generate Lessons ------

lessons_titles = [
    "Basic Concepts of Machine Learning", "Advanced Machine Learning Techniques", "UI/UX Design",
    "Excel for Data Analysis", "Social Media Marketing Strategies", "Cybersecurity Fundamentals",
    "Project Management Essentials", "Python Programming Basics", "Web Development with HTML/CSS",
    "Digital Marketing Tools", "Graphic Design with Adobe Illustrator", "Data Science with Python",
    "Agile Project Management", "Network Security Basics", "Content Marketing Strategies"
]

lesson_doc = []  # list to hold all lesson documents

for i in range(25):
    # Fetch all courseIds from courses collection
    course_ids = [course.get("courseId") for course in db.courses.find({}, {"courseId": 1})]

    # Create lesson document
    lesson = {
        "lessonId": ObjectId(),
        "courseId": random.sample(course_ids, k=1)[0],  # randomly assign course
        "title": random.choice(lessons_titles),
        "content": f"{text.sentence()}",
        "videoUrl": f"downloads/videos/{internet.slug()}.mp4",
        "resources": [f"downloads/resources/{internet.slug()}.pdf"],
        "duration": f"{random.randint(10, 60)}minutes",
        "createdAt": datetime.now(),
        "updatedAt": datetime.now()
    }
    
    lesson_doc.append(lesson)  # add to list


#------ Insert Lessons Into MongoDB -------

db.lessons.insert_many(lesson_doc)
print(f"Inserted {len(lesson_doc)} lessons into the database.")  # confirmation message


#------ Generate Assignments --------

Assignments = []  # list to hold all assignment documents

# Pre-fetch IDs to avoid querying DB every loop iteration
lesson_ids = [lesson.get("lessonId") for lesson in db.lessons.find({}, {"lessonId": 1})]
course_ids = [course.get("courseId") for course in db.courses.find({}, {"courseId": 1})]
student_ids = [user.get("userId") for user in db.users.find({"roles": "student"}, {"userId": 1})]

for i in range(10):
    assignment = {
        "studentId": random.choice(student_ids),  # assign random student
        "courseId": random.choice(course_ids),    # assign random course
        "lessonId": random.choice(lesson_ids),    # assign random lesson
        "description": f"{text.sentence()}",
        "dueDate": datetime.now(),
        "assignment_grades": random.choice(["A", "B", "C", "D", "E", "F"])
    }
    Assignments.append(assignment)  # add to list


#------ Insert Assignments Into MongoDB --------

db.assignments.insert_many(Assignments)
print(f"Inserted {len(Assignments)} assignments into the database.")  # confirmation message


#----- Generate Assignment Submissions -----

Assignment_submissions = []  # list to hold all submission documents

# Pre-fetch IDs to reduce repeated DB queries
course_ids = [course.get("courseId") for course in db.courses.find({}, {"courseId": 1})]
student_ids = [user.get("userId") for user in db.users.find({"roles": "student"}, {"userId": 1})]

for i in range(12):
    submission = {
        "submissionId": ObjectId(),  # unique ID
        "studentId": random.choice(student_ids),  # assign random student
        "courseId": random.choice(course_ids),    # assign random course
        "content": f"{text.sentence()}",          # submission content
        "submissionDate": datetime.now(),         # timestamp
        "feedback": f"{text.sentence()}",         # instructor feedback
        "isSubmitted": random.choice([True, True, False])  # mostly submitted
    }
    Assignment_submissions.append(submission)


#------ Insert Submissions Into MongoDB -------

assignments_submissions.insert_many(Assignment_submissions)
print(f"Inserted {len(Assignment_submissions)} assignment submissions into the database.")  # confirmation


#----- Users (students and instructors) ------

# Single student user
student_user = {
    "userId": "EDU1022",
    "first_name": "Jessica",
    "last_name": "Martins",
    "email": "jessmar81@eduhub.com",
    "roles": "student", 
    "grades": [88, 92, 79],
    "dateJoined": datetime.now(),
    "profile": {
        "bio": "Hardworking student",
        "avatar": "path/to/avatar.jpg",
        "skills": "Python", 
        "isActive": True
    }
}

# Single instructor user
instructor_user = {
    "userId": "EDU1021",
    "first_name": "Jackson",
    "last_name": "Smith",
    "email": "john.smith@example.com",
    "roles": "instructor",
    "grades": [],  # instructors may not have grades
    "dateJoined": datetime.now(),
    "profile": {
        "bio": "Experienced instructor",
        "avatar": "path/to/avatar.jpg",
        "skills": "Machine Learning", 
        "isActive": True
    }
}


#------ Courses -------

course = {
    "courseId": "C001",
    "title": "Python for Beginners",
    "category": "Programming",
    "level": "Beginner",
    "price": 100,
    "tag": ["Python", "Programming"],
    "createdAt": datetime.now(),
    "updatedAt": datetime.now(),
    "isPublished": True,
    "instructorId": instructor_user["userId"]  # link course to instructor
}


#----- Enrollments -------

enrollment = {
    "enrollmentId": "E001",
    "userId": student_user["userId"],  # link to student
    "courseId": course["courseId"],    # link to course
    "status": "Enrolled",  # or "Completed"
    "enrolledAt": datetime.now()
}


#----- Lessons -------

lesson = {
    "lessonId": "L001",
    "courseId": course["courseId"],  # link to course
    "title": "Introduction to Python",
    "description": "Learn the basics of Python programming",
    "content": "Lesson content goes here...",
    "createdAt": datetime.now(),
    "updatedAt": datetime.now()
}


#------ Assignments ------

assignment = {
    "assignmentId": "A001",
    "studentId": student_user["userId"],  # link to student
    "courseId": course["courseId"],       # link to course
    "lessonId": lesson["lessonId"],       # link to lesson
    "description": "Complete the Python exercises",
    "dueDate": datetime.now(),
    "assignment_grades": random.choice(["A", "B", "C", "D", "E", "F"])
}


# ----- Summary dictionary for easy access -----

collections_dict = {
    "users": [student_user, instructor_user],
    "courses": [course],
    "enrollments": [enrollment],
    "lessons": [lesson],
    "assignments": [assignment]
}

print("All collection dictionaries ready.")

# --- Ensure single string for skills ---
student_user['profile']['skills'] = random.choice(skills)
instructor_user['profile']['skills'] = random.choice(skills)

# --- Remove duplicates before insertion ---
db.users.delete_many({"userId": {"$in": [student_user['userId'], instructor_user['userId']]}})
db.courses.delete_many({"courseId": course['courseId']})
db.enrollments.delete_many({"enrollmentId": enrollment['enrollmentId']})
db.lessons.delete_many({"lessonId": lesson['lessonId']})

# --- Insertion Functions ---
def insert_user(user):
    try:
        result = db.users.insert_one(user)
        print(f"User '{user['userId']}' inserted successfully.")
        return result.inserted_id
    except Exception as e:
        print(f"Error inserting user '{user.get('userId', 'N/A')}': {e}")
        return None

def create_course(course):
    try:
        result = db.courses.insert_one(course)
        print(f"Course '{course['courseId']}' inserted successfully.")
        return result.inserted_id
    except Exception as e:
        print(f"Error inserting course '{course.get('courseId', 'N/A')}': {e}")
        return None

def enrol_student(enrollment):
    try:
        result = db.enrollments.insert_one(enrollment)
        print(f"Enrollment '{enrollment['enrollmentId']}' inserted successfully.")
        return result.inserted_id
    except Exception as e:
        print(f"Error inserting enrollment '{enrollment.get('enrollmentId', 'N/A')}': {e}")
        return None

def add_lesson(lesson):
    try:
        result = db.lessons.insert_one(lesson)
        print(f"Lesson '{lesson['lessonId']}' inserted successfully.")
        return result.inserted_id
    except Exception as e:
        print(f"Error inserting lesson '{lesson.get('lessonId', 'N/A')}': {e}")
        return None

# --- Perform Insertions ---
new_user_id_1 = insert_user(student_user)
new_user_id_2 = insert_user(instructor_user)
new_course_id = create_course(course)
new_enrollment_id = enrol_student(enrollment)
new_lesson_id = add_lesson(lesson)

# --- Print All Inserted IDs ---
insert_results = {
    "student_user_id": new_user_id_1,
    "instructor_user_id": new_user_id_2,
    "course_id": new_course_id,
    "enrollment_id": new_enrollment_id,
    "lesson_id": new_lesson_id
}

print("\nAll insertions completed. Inserted IDs:")
print(insert_results)

#find all active students
def active_students(users):
    try:
        active_students = db.users.find({"roles": "student", "profile.IsActive": True})
        return list(active_students)
    except Exception as e:
        print(f"Error retrieving active students: {e}")
        return []
    

#retrieve course details with instructor details
def course_details(courses):
    try:
        course_details = db.courses.find({courses}, {"instructorId": 1})
        return list(course_details)
    except Exception as e:
        print(f"Error retrieving course details: {e}")
        return []
    

#get course by a specific category
def get_course_by_category(courses):
    try:
        courses = db.courses.find({"category": "programming"})
        return list(courses)
    except Exception as e:
        print(f"Error retrieving courses by category: {e}")
        return []
    
#get students enrolled in a specific course
def students_in_course(enrollments):
    try:
        enrollments = db.courses.find({"title": "Web Development", "role": "student"})
        return list(enrollments)
    except Exception as e:
        print(f"Error finding students in Web Development")
        return []
    

#course by title(case insensitive partial match)
def course_by_title(courses):
    try:
        search_title = "data"
        courses = db.courses.find({"title":{"$regex": search_title, "$options": "i"}})
        return list(courses)
    except Exception as e:
        print(f"Error retrieving courses by title: {e}")
        return []

acitve_students = active_students(users)
course_info = course_details(courses)
course_by_category = get_course_by_category(courses)
student_in_course = students_in_course(enrollments)
course_title = course_by_title(courses)
results = {"active user": acitve_students, 
           "found course": course_info, 
           "found course": course_by_category, 
           "found course": student_in_course,
           "found course": course_title
           }
print (results)


#update a user's profile
def update_user_profile(users):
    try:
        result = db.users.update_one({"userId": "EDU1005"}, {"$set": {"profile.skills": ["Good Communication", "Critical Thinking","Team Work"]}})
        return result.modified_count
    except Exception as e:
        print(f"Error updating user profile: {e}")
        return 0
    
#mark a course as published
def mark_a_course_as_published(courses):
    try:
        result = db.courses.update_one({"courseId": 101}, {"$set": {"isPublished": True}})
        return result.modified_count
    except Exception as e:
        print(f"Error marking course as published: {e}")
        return 0
    

#update assignment grades
def update_assignment_grades(assignments):
    try: 
        result = db.assignments.update_one({"studentId": "EDU1007", "courseId": 101}, {"$set": {"assignment_grades": "A"}})
        return result.modified_count
    except Exception as e:
        print(f"Error updating assignment grades: {e}")
        return 0


#add tags to an existing course
def add_tags_to_course(courses):
    try:
        result = db.courses.update_one({"courseId": 102}, {"$set": {"tag": "Full Stack"}})
        return result.modified_count
    except Exception as e:
        print(f"Error adding tags to course: {e}")
        return 0
    
update_profile = update_user_profile(users)
mark_course = mark_a_course_as_published(courses)
update_grades = update_assignment_grades(assignments)
new_course_tag = add_tags_to_course(courses)

results = {"profile updated": update_profile, 
           "course marked": mark_course, 
           "grades updated": update_grades, 
           "tags added": new_course_tag
           }
print (results)


# --- Soft delete a student ---
def soft_delete_user(users_collection, student_id=None):
    try:
        filter_query = {"role": "student"}
        if student_id:
            filter_query["userId"] = student_id
        result = users_collection.update_one(filter_query, {"$set": {"is_active": False}})
        print(f"Soft deleted {result.modified_count} student(s).")
        return result.modified_count
    except Exception as e:
        print(f"Error soft deleting user: {e}")
        return 0

# --- Delete an enrollment ---
def delete_enrollment(enrollments_collection, student_id, course_id):
    try:
        result = enrollments_collection.delete_one({"studentId": student_id, "courseId": course_id})
        print(f"Deleted {result.deleted_count} enrollment(s).")
        return result.deleted_count
    except Exception as e:
        print(f"Error deleting enrollment: {e}")
        return 0

# --- Remove a lesson ---
def remove_lesson(lessons_collection, course_id, title):
    try:
        result = lessons_collection.delete_one({"courseId": course_id, "title": title})
        print(f"Removed {result.deleted_count} lesson(s).")
        return result.deleted_count
    except Exception as e:
        print(f"Error removing lesson: {e}")
        return 0

# --- Example usage ---
deleted_students = soft_delete_user(db.users, student_id="EDU1010")
deleted_enrollments = delete_enrollment(db.enrollments, "EDU1010", 103)
removed_lessons = remove_lesson(db.lessons, 104, "Python")

# Print summary of operations
print({
    "deleted_students": deleted_students,
    "deleted_enrollments": deleted_enrollments,
    "removed_lessons": removed_lessons
})

# --- Query / Filter Functions ---


def course_by_price(courses_collection):
    """Find courses priced between $50 and $200"""
    try:
        query = {"price": {"$gte": 50, "$lte": 200}}
        projection = {
            "courseId": 1,
            "title": 1,
            "category": 1,
            "level": 1,
            "price": 1,
            "tag": 1,
            "createdAt": 1,
            "updatedAt": 1,
            "isPublished": 1
        }
        result = list(courses_collection.find(query, projection))
        print(f"Found {len(result)} courses in price range $50-$200")
        return result
    except Exception as e:
        print(f"Error listing course price range ($50 to $200): {e}")
        return []

def joined_last_6months(users_collection):
    """Get users who joined in the last 6 months"""
    try:
        six_months_ago = datetime.now() - timedelta(weeks=24)
        query = {"dateJoined": {"$gte": six_months_ago}}
        projection = {
            "userId": 1,
            "first_name": 1,
            "last_name": 1,
            "roles": 1,
            "email": 1,
            "dateJoined": 1
        }
        result = list(users_collection.find(query, projection))
        print(f"Found {len(result)} users who joined in last 6 months")
        return result
    except Exception as e:
        print(f"Error getting users joined last six months: {e}")
        return []

def excel_tag_courses(courses_collection):
    """Find courses with tags Excel, AI, or Security"""
    try:
        query = {"tag": {"$in": ["Excel", "AI", "Security"]}}
        projection = {
            "courseId": 1,
            "title": 1,
            "category": 1,
            "tag": 1,
            "level": 1,
            "price": 1,
        }
        result = list(courses_collection.find(query, projection))
        print(f"Found {len(result)} courses with tags Excel, AI, or Security")
        return result
    except Exception as e:
        print(f"Error finding excel tagged courses: {e}")
        return []

def assignments_next_week_due(assignments_collection):
    """Retrieve assignments due in the next 7 days"""
    try:
        next_week = datetime.now() + timedelta(days=7)
        query = {"dueDate": {"$lte": next_week}}
        projection = {
            "courseId": 1,
            "lessonId": 1,
            "description": 1,
            "dueDate": 1,
            "assignment_grades": 1
        }
        result = list(assignments_collection.find(query, projection))
        print(f"Found {len(result)} assignments due in the next week")
        return result
    except Exception as e:
        print(f"Failure to retrieve assignments: {e}")
        return []


# --- Collect all query/filter results ---

query_filter_results = {
    "course_by_price": course_by_price(db.courses),
    "joined_last_6months": joined_last_6months(db.users),
    "excel_tag_courses": excel_tag_courses(db.courses),
    "assignments_next_week_due": assignments_next_week_due(db.assignments)
}


# --- Print result summary ---

print("\nSummary of Query Results:")
for key, value in query_filter_results.items():
    print(f"{key}: {len(value)} records found")

#count total enrollment per course
def total_enrollment_per_course():
    pipeline = [
        {
            "$group": {
                "_id": "$courseId",
                "totalEnrollments": {"$sum": 1} 
            
            }
        },
        {
            "$project": {
                "_Id": 0,
                "courseId": "$_id",
                "totalEnrollments": 1
            }
        }
    ]
    result = list(db.enrollments.aggregate(pipeline))
    return result


#calculate average course rating
def average_course_rating():
    pipeline = [
        {
            "$group": {
                "_id": "$courseId",
                "title": {"$first": "$title"},
                "averageRating": {"$avg": "$rating"},
                "totalRating": {"$sum": 1}
            }
        },
        {
            "$project": {
                "_id": 0,
                "courseId": "$_id",
                "title": 1,
                "averageRating": 1,
                "totalRating": 1
            }
        }
    ]
    result = list(db.courses.aggregate(pipeline))
    return result


# Group by course category
def group_by_category():
    pipeline = [
        {
            "$group": {
                "_id": "$category",             
                "totalCourses": {"$sum": 1}      
            }
        },
        {
            "$project": {
                "_id": 0,                        
                "category": "$_id",              
                "totalCourses": 1
            }
        }
    ]
    result = list(db.courses.aggregate(pipeline))
    return result


 #---- Collect all course analytics results ---- #
course_analytics_results = {
    "total_enrollment_per_course": total_enrollment_per_course(),
    "average_course_rating": average_course_rating(),
    "group_by_category": group_by_category()
}

print(course_analytics_results)

#Average grade per student
def average_grade_per_student():
    pipeline = [
        {"$unwind": "$grades"},
        {"$group": {
            "_id": "$userId",
            "first_name": {"$first": "$first_name"},
            "last_name": {"$first": "$last_name"},
            "averageGrade": {"$avg": "$grades"},
            "totalGrades": {"$sum": 1}
        }},
        {"$project": {
            "_id": 0,
            "userId": "$_id",
            "first_name": 1,
            "last_name": 1,
            "averageGrade": 1,
            "totalGrades": 1
        }}
    ]

    result = list(db.users.aggregate(pipeline))
    return result


#completion rate by course
def completion_rate():
    pipeline = [
        {"$group": {
            "_id": "$courseId",
            "totalEnrolled": {"$sum": 1},
            "completed": {"$sum": {"$cond": [{"$eq": ["$status", "Completed"]}, 1, 0]}}
        }},
        {"$project": {
            "courseId": "$_id",
            "_id": 0,
            "totalEnrolled": 1,
            "completed": 1,
            "completionRate": {
                "$cond": [
                    {"$eq": ["$totalEnrolled", 0]},
                    0,
                    {"$multiply": [
                        {"$divide": ["$completed", "$totalEnrolled"]},
                        100
                    ]}
                ]
            }
        }}
    ]

    result = list(db.enrollments.aggregate(pipeline))
    return result 



#Top performing Student
def top_student():
    pipeline = [
        {"$match": {"status": "Completed"}},
        {"$group": {
            "_id": "$studentId",
            "completedCourses": {"$sum": 1}
        }},
        {"$sort": {"completedCourses": -1}},
        {"$project": {
            "_id": 0,
            "studentId": "$_id",
            "completedCourses": 1
        }}
    ]
    result = list(db.enrollments.aggregate(pipeline))
    return result

# Collecting results in one dictionary
performance_results = {
    "average_grade_per_student": average_grade_per_student(),
    "completion_rate": completion_rate(),
    "top_students": top_student()
}

print(list(performance_results))

"""
INSTRUCTOR ANALYSIS
"""
#Total student taught by each Instructor
def students_per_instructor():
    pipeline = [
        {
            "$lookup": {
                "from": "courses",
                "localField": "courseId",
                "foreignField": "courseId",
                "as": "courseInfo"
            }
        },
        {"$unwind": "$courseInfo"},
        {
            "$group": {
                "_id": "$courseInfo.instructorId",
                "totalStudents": {"$addToSet": "$studentId"}
            }
        },
        {
            "$project": {
                "_id": 0,
                "instructorId": "$_id",
                "totalStudents": {"$size": "$totalStudents"}
            }
        }
    ]
    result = list(db.enrollments.aggregate(pipeline))
    return result


#Average course rating per instructor
def average_course_rating_per_instructor():
    pipeline = [
        {"$unwind": "$ratings"},   
        {
            "$group": {
                "_id": "$instructorId",  
                "averageRating": {"$avg": "$ratings.score"},
                "totalRatings": {"$sum": 1},
                "coursesTaught": {"$addToSet": "$title"}  
            }
        },
        {
            "$project": {
                "_id": 0,
                "instructorId": "$_id",
                "averageRating": 1,
                "totalRatings": 1,
                "coursesTaught": 1
            }
        }
    ]
    return list(db.courses.aggregate(pipeline))


#Revenue generated per instructor
def revenue_per_instructor():
    pipeline = [
        {
            "$lookup": {
                "from": "courses",
                "localField": "courseId",
                "foreignField": "courseId",
                "as": "courseInfo"
            }
        },
        {"$unwind": "$courseInfo"},  
        
        {
            "$group": {
                "_id": "$courseInfo.instructorId",
                "totalRevenue": {"$sum": "$courseInfo.price"},
                "courses": {"$addToSet": "$courseInfo.title"}
            }
        },
        
        {
            "$project": {
                "_id": 0,
                "instructorId": "$_id",
                "totalRevenue": 1,
                "courses": 1
            }
        }
    ]
    return list(db.enrollments.aggregate(pipeline))


#  Collect and print all results at once  #
instructor_analysis_results = {
    "Students per Instructor": students_per_instructor(),
    "Average Course Rating per Instructor": average_course_rating_per_instructor(),
    "Revenue per Instructor": revenue_per_instructor()
}

print(instructor_analysis_results)
"""
ADVANCED ANALYTICS
"""
def monthly_enrollment_trends():
    pipeline = [
        {
            "$group": {
                "_id": {
                    "year": {"$year": "$enrolledAt"},
                    "month": {"$month": "$enrolledAt"}
                },
                "totalEnrollments": {"$sum": 1}
            }
        },
        
        {
            "$sort": {"_id.year": 1, "_id.month": 1}
        },
        
        {
            "$project": {
                "_id": 0,
                "year": "$_id.year",
                "month": "$_id.month",
                "totalEnrollments": 1
            }
        }
    ]
    return list(db.enrollments.aggregate(pipeline))



#Most popular categories
def most_popular_categories():
    pipeline = [
        {
            "$lookup": {
                "from": "courses",
                "localField": "courseId",
                "foreignField": "courseId",
                "as": "courseInfo"
            }
        },
        {"$unwind": "$courseInfo"},  

        {
            "$group": {
                "_id": "$courseInfo.category",
                "totalEnrollments": {"$sum": 1}
            }
        },

        {"$sort": {"totalEnrollments": -1}},

        {
            "$project": {
                "_id": 0,
                "category": "$_id",
                "totalEnrollments": 1
            }
        }
    ]
    return list(db.enrollments.aggregate(pipeline))


#Student Engagement Metrics
def student_engagement_metrics():
    pipeline = [
        {
            "$group": {
                "_id": "$profile.isActive",   
                "count": {"$sum": 1}          
            }
        },
        {
            "$project": {
                "_id": 0,
                "status": {
                    "$cond": [
                        {"$eq": ["$_id", True]}, 
                        "Active", 
                        "Inactive"
                    ]
                },
                "count": 1
            }
        }
    ]
    result = list(db.users.aggregate(pipeline))
    return result

# ---- Collect and print all results at once ---- #
analytics_results = {
    "Monthly Enrollment Trends": monthly_enrollment_trends(),
    "Most Popular Categories": most_popular_categories(),
    "Student Engagement Metrics": student_engagement_metrics()
}

print(analytics_results)


#User email lookup
# Remove duplicate emails before creating unique index

pipeline = [
    {"$group": {
        "_id": "$email",
        "ids": {"$push": "$_id"},
        "count": {"$sum": 1}
    }},
    {"$match": {"count": {"$gt": 1}}}
]

duplicates = list(db.users.aggregate(pipeline))
for dup in duplicates:
    # Keep the first occurrence, remove others
    ids_to_remove = dup["ids"][1:]
    db.users.delete_many({"_id": {"$in": ids_to_remove}})
    print(f"Removed {len(ids_to_remove)} duplicate(s) for email: {dup['_id']}")

# Now create a unique index on email field
db.users.create_index(
    [("email", 1)],   # 1 means ascending order
    unique=True,
    name="idx_user_email"
)

#course search by title and category
db.courses.create_index([("title", 1), ("category", 1)], name="idx_course_title_category")


#assignment queries by due date
db.assignments.find().sort("dueDate", 1)


#Enrollment queries by student and course
db.enrollments.create_index([("studentId", 1), ("courseId", 1)], name="idx_student_course")

import pprint
import time

def analyze_query_performance(collection, query, index_field, index_name):
    try:
        # Create index
        collection.create_index([(index_field, 1)], name=index_name)
        print(f"Index '{index_name}' created on field '{index_field}'")

        # Explain before timing
        plan_before = collection.find(query).explain("executionStats")
        print("\nExecution plan (before timing):")
        pprint.pprint(plan_before)

        # Execute query and measure time
        start = time.time()
        result = list(collection.find(query))
        end = time.time()
        print(f"\nQuery returned {len(result)} documents in {end - start:.6f} seconds")

        # Print query results 
        print("\nQuery Results:")
        for i, doc in enumerate(result, start=1):
            print(f"Document {i}:")
            pprint.pprint(doc)
            print("-" * 50)

        # Explain after timing
        plan_after = collection.find(query).explain("executionStats")
        print("\nExecution plan (after timing):")
        pprint.pprint(plan_after["executionStats"])

        return result

    except Exception as e:
        print(f"Error analyzing query: {e}")
        return []


# Define the validator (your existing student_validator)
student_validator = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": [
            "userId", "email", "first_name", "last_name",
            "roles", "grades", "dateJoined", "profile"
        ],
        "properties": {
            "userId": {"bsonType": "string", "description": "Must be a string and required"},
            "email": {"bsonType": "string", "pattern": "^.+@.+\\..+$", "description": "Must be a valid email address"},
            "first_name": {"bsonType": "string", "description": "First name must be a string"},
            "last_name": {"bsonType": "string", "description": "Last name must be a string"},
            "roles": {"enum": ["student"], "description": "Only 'student' role allowed in this collection"},
            "grades": {"bsonType": "array", "items": {"bsonType": "int"}, "minItems": 1, "description": "Grades must be an array of integers"},
            "dateJoined": {"bsonType": "date", "description": "Must be a valid date"},
            "profile": {
                "bsonType": "object",
                "required": ["bio", "avatar", "skills", "isActive"],
                "properties": {
                    "bio": {"bsonType": "string", "description": "Bio must be a string"},
                    "avatar": {"bsonType": "string", "description": "Avatar must be a string (path/url)"},
                    "skills": {"bsonType": "array", "description": "Skills must be an array of strings"},
                    "isActive": {"bsonType": "bool", "description": "Must be true or false"}
                }
            }
        }
    }
}

# Apply the validator to the collection
try:
    db.command({
        "collMod": "users",       # Modify existing collection
        "validator": student_validator,
        "validationLevel": "moderate"  # Or "strict"
    })
    print("Validator applied successfully to 'users' collection.")
except Exception as e:
    print(f"Failed to apply validator: {e}")

#Duplicate key error handling
def insert_user(user):
    try:
        db.users.insert_one(user)
        print("User inserted successfully.")
    except DuplicateKeyError:
        print("Error: Duplicate key detected. A user with this _id already exists.")

#Invalid data type insertions error handling
def insert_student(student):
    try:
        db.students.insert_one(student)
        print("Student inserted successfully.")
    except WriteError as e:
        print(f"Error: Invalid data type. {e}")
#Missing required field error handling
def insert_course(course):
    try:
        db.courses.insert_one(course)
        print("Course inserted successfully.")
    except WriteError as e:
        print(f"Error: Missing required field. {e}")