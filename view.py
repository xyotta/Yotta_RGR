class view:

    # ---------------- INPUT ----------------
    def input(self):
        return float(input())



    def get_table(self):
        return input("Enter table name (Student / Teacher / Subject): ").strip().capitalize()

    def get_char(self):
        return input("Enter value:")

    def get_id(self):
        try:
            return int(input("Enter record ID: "))
        except ValueError:
            return None

    def get_add_data(self, table):
        if table == "Student":
            name = input("Enter student name: ")
            birth = input("Enter birth date (YYYY-MM-DD): ")
            stud_id = self.get_id()
            return name, birth, stud_id

        elif table == "Teacher":
            name = input("Enter teacher name: ")
            birth = input("Enter birth date (YYYY-MM-DD): ")
            tch_id = self.get_id()
            return name, birth, tch_id

        elif table == "Subject":
            name = input("Enter subject name: ")
            self.show_message("enter subject hours")
            hours = self.input()
            self.show_message("enter subject id")
            subj_id = self.get_id()
            self.show_message("enter subject`s teacher id ")
            tch_id = self.get_id()
            return name, hours, subj_id, tch_id
        else:
            print("Unknown table.")
            return ()


    def show_table(self, rows):
        if not rows:
            print("Table is empty.")
        else:
            print("\n--- Table content ---")
            for row in rows:
                print(row)

    def show_column(self, rows):
        for r in rows:
            print(r)

    def show_message(self, msg):
        print(msg)

    def show_student(self, data):
        stud = data["data"][0]
        stud_id, name, birth = stud

        print(f"\nStudent: {name}, born {birth}, id: {stud_id}")

        subjects = data["subjects"]
        if subjects:
            print("Subjects:")
            for subj_id, subj_name, grade in subjects:
                print(f" - {subj_name} (ID {subj_id}), grade {grade}")
        else:
            print("No subjects.")

        count, avg = data["stats"]
        print(f"Grades: {count}, average: {avg}")

    def show_teacher(self, data):
        tch = data["data"][0]
        tid, name, birth = tch

        print(f"\nTeacher: {name}, born {birth}, id: {tid}")

        subjects = data["subjects"]
        if subjects:
            print("Subjects taught:")
            for subj_id, name, hours in subjects:
                print(f" - {name} ({hours}h/week)")
        else:
            print("No subjects.")

        count, avg = data["stats"]
        print(f"Grades given: {count}, average: {avg}")

    def show_subject(self, data):
        subj = data["data"][0]
        subj_id, name, hours, tch_id = subj

        print(f"\nSubject: {name} (ID {subj_id}), {hours} hours/week")

        teacher = data["teacher"]
        if teacher:
            t = teacher[0]
            print(f"Teacher: {t[1]}, born {t[2]}")
        else:
            print("Teacher not assigned.")

        count, avg = data["stats"]
        print(f"Grades: {count}, average: {avg}")

    def show_record(self, data):
        record = data["data"][0]
        grade_id, subj_id, stud_id, grade, date = record

        print(f"\nRecord ID: {grade_id}")
        print(f"Grade: {grade}")
        print(f"Date: {date}")

        student = data["student"][0]
        print(f"Student: {student[1]} (ID {student[0]})")

        subject = data["subject"][0]
        print(f"Subject: {subject[1]} (ID {subject[0]})")

        teacher = data["teacher"][0]
        print(f"Teacher: {teacher[1]} (ID {teacher[0]})")

    def show_students_by_grade(self, rows, time_ms):
        if not rows:
            print("\nNo students found in this grade range.")
            return

        print("\nStudents by average grade:")
        for stud_id, name, birth, avg_grade, count in rows:
            print(f" - {name} (ID {stud_id}), born {birth}, "
                  f"avg grade: {avg_grade:.2f}, grades: {count}")

        print(f"\nExecution time: {time_ms:.3f} ms\n")

    def show_teachers_search(self, rows, time_ms):
        if not rows:
            print("\nNo teachers found.")
        else:
            print(f"\nFound {len(rows)} teachers:")
            print(f"{'ID':<10} {'Name':<20} {'Birth Date':<15}")
            print("-" * 45)
            for row in rows:
                print(f"{row[0]:<10} {row[1]:<20} {row[2]}")

            print(f"\nExecution time: {time_ms:.3f} ms\n")

    def show_workload_stats(self, rows, time_ms):
        if not rows:
            print("\nNo teachers found.")
        else:
            print(f"\nTeachers workload statistics:")
            # Тут правильні заголовки для цього запиту
            print(f"{'ID':<5} {'Name':<20} {'Subjects':<10} {'Hours':<10}")
            print("-" * 50)
            for row in rows:
                print(f"{row[0]:<5} {row[1]:<20} {row[2]:<10} {row[3]:<10}")

            print(f"\nExecution time: {time_ms:.3f} ms\n")