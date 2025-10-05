from datetime import datetime, timedelta
from pymongo import MongoClient

# Connect to your database
client = MongoClient("mongodb://localhost:27017/")
db = client["eduhub_db"]

def archive_old_enrollments():
    cutoff_date = datetime.now() - timedelta(days=365)

    # Get old enrollments
    old_enrollments = list(db.enrollments.find({"enrollmentDate": {"$lt": cutoff_date}}))

    if not old_enrollments:
        print("No old enrollments to archive.")
        return

    # Add timestamp for archiving
    for doc in old_enrollments:
        doc["archivedAt"] = datetime.now()

    # Insert into archive collection
    db.enrollments_archive.insert_many(old_enrollments)

    # Delete from main collection
    db.enrollments.delete_many({"enrollmentDate": {"$lt": cutoff_date}})

    print(f"Archived {len(old_enrollments)} enrollments.")

if __name__ == "__main__":
    archive_old_enrollments()
