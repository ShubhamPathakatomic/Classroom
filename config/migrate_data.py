import sqlite3
from django.db import transaction
from django.conf import settings
from your_app_name.models import ( # Replace 'your_app_name' with your actual app name (e.g., api)
    Department,
    BuildingFloor,
    Teacher,
    Classroom,
    Subject,
    Student,
    Mark
)

# --- Configuration ---
# IMPORTANT: Adjust this path to your OLD database file.
# This should be the db.sqlite3 file from your MAIN branch, not the new one.
OLD_DATABASE_PATH = settings.BASE_DIR / 'db.sqlite3' # Assumes db.sqlite3 is in project root

print(f"Attempting to migrate data from OLD DB: {OLD_DATABASE_PATH}")

# Dictionaries to map old primary keys to new Django ORM objects
# This is crucial for correctly setting up Foreign Keys and Many-to-Many fields
old_to_new_department = {}
old_to_new_buildingfloor = {}
old_to_new_teacher = {}
old_to_new_classroom = {}
old_to_new_subject = {}
old_to_new_student = {} # Will be used for friends as well

try:
    # Connect to the old database
    conn = sqlite3.connect(OLD_DATABASE_PATH)
    cursor = conn.cursor()

    print("\n--- Starting Data Migration ---")
    with transaction.atomic(): # Use a transaction for atomicity

        # 1. Migrate Departments
        print("Migrating Departments...")
        cursor.execute("SELECT id, name FROM api_department")
        for old_id, name in cursor.fetchall():
            new_department, created = Department.objects.get_or_create(
                name=name,
                defaults={'id': old_id} # Try to preserve old ID, but Django might assign new one
            )
            old_to_new_department[old_id] = new_department
            # If get_or_create didn't use old_id, update map with actual new_department.id
            if new_department.id != old_id and not created:
                print(f"Warning: Department '{name}' (old ID: {old_id}) already exists with new ID: {new_department.id}. Skipping creation.")
            elif new_department.id != old_id and created:
                 print(f"Department '{name}' (old ID: {old_id}) created with new ID: {new_department.id}.")
            else:
                print(f"Department '{name}' (ID: {old_id}) migrated.")

        # 2. Migrate BuildingFloors
        print("\nMigrating BuildingFloors...")
        cursor.execute("SELECT id, name, level FROM api_buildingfloor") # Assuming BuildingFloor exists in old schema
        for old_id, name, level in cursor.fetchall():
            new_buildingfloor, created = BuildingFloor.objects.get_or_create(
                name=name,
                level=level,
                defaults={'id': old_id}
            )
            old_to_new_buildingfloor[old_id] = new_buildingfloor
            if new_buildingfloor.id != old_id and not created:
                 print(f"Warning: BuildingFloor '{name}-Level {level}' (old ID: {old_id}) already exists with new ID: {new_buildingfloor.id}. Skipping creation.")
            elif new_buildingfloor.id != old_id and created:
                 print(f"BuildingFloor '{name}-Level {level}' (old ID: {old_id}) created with new ID: {new_buildingfloor.id}.")
            else:
                print(f"BuildingFloor '{name}-Level {level}' (ID: {old_id}) migrated.")

        # 3. Migrate Teachers
        print("\nMigrating Teachers...")
        cursor.execute("SELECT id, name, department_id FROM api_teacher")
        for old_id, name, old_department_id in cursor.fetchall():
            department_obj = old_to_new_department.get(old_department_id)
            if not department_obj:
                print(f"Skipping Teacher '{name}': Department with old ID {old_department_id} not found.")
                continue
            
            new_teacher, created = Teacher.objects.get_or_create(
                name=name,
                defaults={'department': department_obj, 'id': old_id}
            )
            old_to_new_teacher[old_id] = new_teacher
            if new_teacher.id != old_id and not created:
                print(f"Warning: Teacher '{name}' (old ID: {old_id}) already exists with new ID: {new_teacher.id}. Skipping creation.")
            elif new_teacher.id != old_id and created:
                 print(f"Teacher '{name}' (old ID: {old_id}) created with new ID: {new_teacher.id}.")
            else:
                print(f"Teacher '{name}' (ID: {old_id}) migrated.")

        # 4. Migrate Classrooms
        print("\nMigrating Classrooms...")
        # Make sure the teacher_id column is nullable or handle cases where it was NULL in old DB
        cursor.execute("SELECT id, name, floor_id, teacher_id FROM api_classroom")
        for old_id, name, old_floor_id, old_teacher_id in cursor.fetchall():
            floor_obj = old_to_new_buildingfloor.get(old_floor_id)
            teacher_obj = old_to_new_teacher.get(old_teacher_id) if old_teacher_id else None # Handle NULL teacher_id

            if not floor_obj:
                print(f"Skipping Classroom '{name}': Floor with old ID {old_floor_id} not found.")
                continue

            new_classroom, created = Classroom.objects.get_or_create(
                name=name,
                defaults={'floor': floor_obj, 'teacher': teacher_obj, 'id': old_id}
            )
            old_to_new_classroom[old_id] = new_classroom
            if new_classroom.id != old_id and not created:
                print(f"Warning: Classroom '{name}' (old ID: {old_id}) already exists with new ID: {new_classroom.id}. Skipping creation.")
            elif new_classroom.id != old_id and created:
                print(f"Classroom '{name}' (old ID: {old_id}) created with new ID: {new_classroom.id}.")
            else:
                print(f"Classroom '{name}' (ID: {old_id}) migrated.")

        # 5. Migrate Subjects
        print("\nMigrating Subjects...")
        cursor.execute("SELECT id, name FROM api_subject")
        for old_id, name in cursor.fetchall():
            new_subject, created = Subject.objects.get_or_create(
                name=name,
                defaults={'id': old_id}
            )
            old_to_new_subject[old_id] = new_subject
            if new_subject.id != old_id and not created:
                print(f"Warning: Subject '{name}' (old ID: {old_id}) already exists with new ID: {new_subject.id}. Skipping creation.")
            elif new_subject.id != old_id and created:
                 print(f"Subject '{name}' (old ID: {old_id}) created with new ID: {new_subject.id}.")
            else:
                print(f"Subject '{name}' (ID: {old_id}) migrated.")

        # 6. Migrate Students (including primary_subject and initial friends)
        print("\nMigrating Students...")
        cursor.execute("SELECT id, name, classroom_id FROM api_student")
        for old_id, name, old_classroom_id in cursor.fetchall():
            classroom_obj = old_to_new_classroom.get(old_classroom_id)
            if not classroom_obj:
                print(f"Skipping Student '{name}': Classroom with old ID {old_classroom_id} not found.")
                continue
            
            # Create student without primary_subject initially
            new_student, created = Student.objects.get_or_create(
                name=name,
                defaults={'classroom': classroom_obj, 'id': old_id}
            )
            old_to_new_student[old_id] = new_student
            if new_student.id != old_id and not created:
                print(f"Warning: Student '{name}' (old ID: {old_id}) already exists with new ID: {new_student.id}. Skipping creation.")
            elif new_student.id != old_id and created:
                print(f"Student '{name}' (old ID: {old_id}) created with new ID: {new_student.id}.")
            else:
                print(f"Student '{name}' (ID: {old_id}) migrated.")

        # NOW handle primary_subject (from old Many-to-Many) for students
        print("\nAssigning primary_subject to Students...")
        cursor.execute("SELECT student_id, subject_id FROM api_student_subjects") # Old M2M table
        old_student_subjects_map = {}
        for student_id, subject_id in cursor.fetchall():
            if student_id not in old_student_subjects_map:
                old_student_subjects_map[student_id] = []
            old_student_subjects_map[student_id].append(subject_id)

        for old_student_id, old_subject_ids in old_student_subjects_map.items():
            student_obj = old_to_new_student.get(old_student_id)
            if not student_obj:
                print(f"Warning: Student with old ID {old_student_id} not found when assigning primary subject.")
                continue
            
            # --- Transformation Logic: Pick the first subject as primary_subject ---
            if old_subject_ids:
                first_old_subject_id = old_subject_ids[0]
                primary_subject_obj = old_to_new_subject.get(first_old_subject_id)
                if primary_subject_obj:
                    student_obj.primary_subject = primary_subject_obj
                    student_obj.save()
                    print(f"Assigned primary subject '{primary_subject_obj.name}' to student '{student_obj.name}'.")
                else:
                    print(f"Warning: Primary subject with old ID {first_old_subject_id} not found for student '{student_obj.name}'.")
            else:
                print(f"Student '{student_obj.name}' had no subjects in old DB. primary_subject remains null.")


        # 7. Migrate Friends (Many-to-Many - requires all students to be migrated first)
        print("\nMigrating Student Friendships...")
        cursor.execute("SELECT from_student_id, to_student_id FROM api_student_friends") # Old M2M table
        for old_from_id, old_to_id in cursor.fetchall():
            from_student = old_to_new_student.get(old_from_id)
            to_student = old_to_new_student.get(old_to_id)
            if from_student and to_student:
                from_student.friends.add(to_student)
                print(f"Friendship: {from_student.name} <-> {to_student.name}")
            else:
                print(f"Warning: Skipping friendship between old IDs {old_from_id} and {old_to_id} due to missing student(s).")

        # 8. Migrate Marks
        print("\nMigrating Marks...")
        cursor.execute("SELECT id, student_id, subject_id, score FROM api_mark")
        for old_id, old_student_id, old_subject_id, score in cursor.fetchall():
            student_obj = old_to_new_student.get(old_student_id)
            subject_obj = old_to_new_subject.get(old_subject_id)

            if not student_obj:
                print(f"Skipping Mark (ID: {old_id}): Student with old ID {old_student_id} not found.")
                continue
            if not subject_obj:
                print(f"Skipping Mark (ID: {old_id}): Subject with old ID {old_subject_id} not found.")
                continue

            try:
                # Use get_or_create to prevent duplicates if Mark unique_together constraint is hit
                new_mark, created = Mark.objects.get_or_create(
                    student=student_obj,
                    subject=subject_obj,
                    defaults={'score': score, 'id': old_id}
                )
                if new_mark.id != old_id and not created:
                    print(f"Warning: Mark for {student_obj.name} - {subject_obj.name} already exists with new ID: {new_mark.id}. Skipping creation.")
                elif new_mark.id != old_id and created:
                    print(f"Mark (old ID: {old_id}) for {student_obj.name} - {subject_obj.name} created with new ID: {new_mark.id}.")
                else:
                    print(f"Mark (ID: {old_id}) for {student_obj.name} - {subject_obj.name} migrated.")
            except Exception as e:
                print(f"Error migrating Mark (old ID: {old_id}) for {student_obj.name} - {subject_obj.name}: {e}")

    print("\n--- Data Migration Complete Successfully! ---")

except sqlite3.Error as e:
    print(f"\nSQLite Error: {e}")
    print("Please ensure the OLD_DATABASE_PATH is correct and the file is accessible.")
except Exception as e:
    print(f"\nAn unexpected error occurred: {e}")
    print("Ensure all models are correctly defined and migrations are applied to the new database.")
finally:
    if 'conn' in locals() and conn:
        conn.close()

