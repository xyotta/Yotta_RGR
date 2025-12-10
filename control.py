from module import Model
from view import view
from ORM import ORM_Model


class Controller:
    def __init__(self):
        self.model = Model()  # Для SQL запитів (пошук, генерація)
        self.orm_model = ORM_Model()  # Для CRUD операцій (ORM)
        self.view = view()

    def run(self):
        while True:
            choice = self.show_menu()

            if choice == '1':
                self.view_table()
            elif choice == '2':
                self.Search()
            elif choice == '3':
                self.add_record()
            elif choice == '4':
                self.delete_record()
            elif choice == '5':
                self.search_students_by_grade_range()
            elif choice == '6':
                self.generate_N_new_elements()
            elif choice == '7':
                self.Update()
            elif choice == '8':
                self.search_teacher_like()
            elif choice == '9':
                self.search_workload()
            elif choice == '0':
                break
            else:
                self.view.show_message("Invalid choice.")

    def show_menu(self):
        self.view.show_message("\nMenu:")
        self.view.show_message("1. View table ")
        self.view.show_message("2. Search_by_id ")
        self.view.show_message("3. Add record ")
        self.view.show_message("4. Delete record ")
        self.view.show_message("5. Students filtered by grades [x,y] ")
        self.view.show_message("6. Generate N elements (SQL)")
        self.view.show_message("7. Update record ")
        self.view.show_message("8. Search teachers with TEXT in name ")
        self.view.show_message("9. Search teachers by count of subjects ")
        self.view.show_message("0. Quit")
        return input("Enter choice: ")


    def view_table(self):
        table = self.view.get_table()
        rows = self.orm_model.view_table(table)
        self.view.show_table(rows)

    def Search(self):
        id = self.view.get_id()
        # Використовуємо стару SQL модель
        result = self.model.Search_by_id(id)

        if not result:
            self.view.show_message("Record not found.")
            return

        rtype = result["type"]

        if rtype == "student":
            self.view.show_student(result)
        elif rtype == "teacher":
            self.view.show_teacher(result)
        elif rtype == "subject":
            self.view.show_subject(result)
        elif rtype == "record":
            self.view.show_record(result)

    def search_students_by_grade_range(self):
        self.view.show_message("enter min grade")
        g1 = self.view.input()
        self.view.show_message("enter max grade")
        g2 = self.view.input()
        rows, ms = self.model.search_by_grade_range(g1, g2)
        self.view.show_students_by_grade(rows, ms)

    def add_record(self):
        table = self.view.get_table()
        data = self.view.get_add_data(table)

        if table == "Student":
            if self.orm_model.add_student(*data):
                self.view.show_message("Student added (ORM).")
            else:
                self.view.show_message("cannot add student.")

        elif table == "Teacher":
            if self.orm_model.add_teacher(*data):
                self.view.show_message("Teacher added (ORM).")
            else:
                self.view.show_message("cannot add teacher.")

        elif table == "Subject":
            # Виклик ORM
            if self.orm_model.add_subject(*data):
                self.view.show_message("Subject added (ORM).")
            else:
                self.view.show_message("Error: teacher does not exist.")

        else:
            self.view.show_message("Unknown table.")

    def delete_record(self):
        table = self.view.get_table()
        record_id = self.view.get_id()
        if record_id is None:
            return

        if self.orm_model.delete_elem(table, record_id):
            self.view.show_message("Record deleted (ORM).")
        else:
            self.view.show_message("Error: Cannot delete (check FK or ID).")

    def generate_N_new_elements(self):
        self.view.show_message("Enter which table you want to generate elements for?:")
        table = self.view.get_table()
        self.view.show_message("Enter number of elements:")
        n = int(self.view.input())

        if table == "Student":
            ms = self.model.generate_students(n)
            self.view.show_message(f"Generated {n} students in {ms:.2f} ms")
        elif table == "Teacher":
            ms = self.model.generate_teachers(n)
            self.view.show_message(f"Generated {n} teachers in {ms:.2f} ms")
        elif table == "Subject":
            ms = self.model.generate_subjects(n)
            self.view.show_message(f"Generated {n} subjects in {ms:.2f} ms")

    def Update(self):
        table = self.view.get_table()
        id = self.view.get_id()

        if table == "Student":
            name, birth_date, stud_id = self.view.get_add_data(table)
            # Виклик ORM
            if self.orm_model.update_student(id, name, birth_date, stud_id):
                self.view.show_message("Student updated successfully (ORM).")
            else:
                self.view.show_message("Error: Update failed, check data or ID.")

        elif table == "Teacher":
            name, birth_date, tch_id = self.view.get_add_data(table)
            if self.orm_model.update_teacher(id, name, birth_date, tch_id):
                self.view.show_message("Teacher updated successfully (ORM).")
            else:
                self.view.show_message("Error: Update failed, check data or ID.")

        elif table == "Subject":
            name, hours_per_week, new_subject_id, tch_id = self.view.get_add_data(table)
            if self.orm_model.update_subject(id, name, hours_per_week, new_subject_id, tch_id):
                self.view.show_message("Subject updated successfully (ORM).")
            else:
                self.view.show_message("Error: Update failed, check data or ID.")

        else:
            self.view.show_message("Unknown, check id or table.")

    def search_teacher_like(self):
        self.view.show_message("Enter text to search in name:")
        text = input()
        result = self.model.Teachers_with_TEXT_in_their_name(text)
        if result:
            rows, ms = result
            self.view.show_teachers_search(rows, ms)
        else:
            self.view.show_message("Error or nothing found.")

    def search_workload(self):
        self.view.show_message("Enter minimum number of subjects:")
        try:
            n = int(self.view.input())
            result = self.model.search_teachers_by_work(n)

            if result:
                rows, ms = result
                self.view.show_workload_stats(rows, ms)
            else:
                self.view.show_message("Error or nothing found.")
        except ValueError:
            self.view.show_message("Invalid input")