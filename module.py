from codecs import replace_errors

import psycopg2
from psycopg2 import errors

class Model:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname='postgres',
            user='postgres',
            password='1111',
            host='localhost',
            port=5432
        )

    def view_table(self, table):
        c = self.conn.cursor()
        c.execute(f'SELECT * FROM "{table}"')
        return c.fetchall()





    def update_student(self, value, valuenew1, valuenew2, valuenew3):
        c = self.conn.cursor()
        try:
            if valuenew1:
                c.execute('UPDATE "Student" SET "Name" = %s WHERE stud_id = %s', (valuenew1, value))
            if valuenew2:
                c.execute('UPDATE "Student" SET birth = %s WHERE stud_id = %s', (valuenew2, value))
            if valuenew3:
                c.execute('UPDATE "Student" SET stud_id = %s WHERE stud_id = %s', (valuenew3, value))

            self.conn.commit()
            return True

        except:
            self.conn.rollback()
            return False

    def update_teacher(self, value, valuenew1, valuenew2, valuenew3):
        c = self.conn.cursor()
        try:
            if valuenew1:
                c.execute('UPDATE "Teacher" SET "Name" = %s WHERE tch_id = %s', (valuenew1, value))
            if valuenew2:
                c.execute('UPDATE "Teacher" SET birth = %s WHERE tch_id = %s', (valuenew2, value))
            if valuenew3:
                c.execute('UPDATE "Teacher" SET tch_id = %s WHERE tch_id = %s', (valuenew3, value))

            self.conn.commit()
            return True

        except:
            self.conn.rollback()
            return False

    def update_subject(self, value, valuenew1, valuenew2, valuenew3,valuenew4):
        c = self.conn.cursor()
        try:
            if valuenew1:
                c.execute('UPDATE "Subject" SET "Name" = %s WHERE subj_id = %s', (valuenew1, value))
            if valuenew2:
                c.execute('UPDATE "Subject" SET "hour_per_week" = %s WHERE subj_id = %s', (valuenew2, value))
            if valuenew3:
                c.execute('UPDATE "Subject" SET subj_id = %s WHERE subj_id = %s', (valuenew3, value))
            if valuenew4:
                c.execute('UPDATE "Subject" SET tch_id = %s WHERE subj_id = %s', (valuenew4, value))
            self.conn.commit()
            return True
        except:
            self.conn.rollback()
            return False






    def add_student(self, name, birth, stud_id):
        c = self.conn.cursor()
        try:
            c.execute(
                'INSERT INTO "Student" ("Name","birth", stud_id) VALUES (%s, %s, %s)',
                (name, birth, stud_id)
            )
            self.conn.commit()
            return True
        except:
            self.conn.rollback()
            return False

    def add_teacher(self, name, birth, tch_id):
        c = self.conn.cursor()
        try:
            c.execute(
                'INSERT INTO "Teacher" ("Name", "birth", tch_id) VALUES (%s, %s, %s)',
                (name, birth, tch_id)
            )
            self.conn.commit()
            return True
        except:
            self.conn.rollback()
            return False

    def add_subject(self, name, hours, subj_id, tch_id):
        c = self.conn.cursor()
        try:
            c.execute(
                'INSERT INTO "Subject" ("Name", hour_per_week, subj_id, tch_id) VALUES (%s, %s, %s, %s)',
                (name, hours, subj_id, tch_id)
            )
            self.conn.commit()
            return True
        except:
            self.conn.rollback()
            return False

    def generate_students(self, count):
        c = self.conn.cursor()
        import time
        start = time.time()

        c.execute(f"""
            INSERT INTO "Student" ("Name", "birth", "stud_id")
            SELECT
                chr(trunc(65 + random() * 25)::int) ||
                chr(trunc(65 + random() * 25)::int) ||
                chr(trunc(65 + random() * 25)::int),
                date '1990-01-01' + (random() * 12000)::int,
                (SELECT COALESCE(MAX(stud_id), 0) FROM "Student") + i
            FROM generate_series(1, {count}) AS t(i);
        """)

        self.conn.commit()
        return (time.time() - start) * 1000

    def generate_teachers(self, count):
        c = self.conn.cursor()
        import time
        start = time.time()

        c.execute(f"""
            INSERT INTO "Teacher" ("Name", "birth", "tch_id")
            SELECT
                chr(trunc(65 + random() * 25)::int) ||
                chr(trunc(65 + random() * 25)::int),
                date '1990-01-01' + (random() * 12000)::int,
                (SELECT COALESCE(MAX(tch_id), 0) FROM "Teacher") + i
            FROM generate_series(1, {count}) AS t(i);
        """)

        self.conn.commit()
        return (time.time() - start) * 1000

    def generate_subjects(self, count):
        c = self.conn.cursor()
        import time
        start = time.time()

        c.execute(f"""
            INSERT INTO "Subject" ("Name", hour_per_week, subj_id, tch_id)
            SELECT
                chr(trunc(65 + random() * 25)::int) ||
                chr(trunc(65 + random() * 25)::int) ||
                chr(trunc(65 + random() * 25)::int) ||
                chr(trunc(65 + random() * 25)::int),
                trunc(1 + random() * 6),
                (SELECT COALESCE(MAX(subj_id), 0) FROM "Subject") + gs.i,
                tr.tch_id
            FROM generate_series(1, {count}) AS gs(i)
            CROSS JOIN LATERAL (
                SELECT tch_id FROM "Teacher"
                WHERE gs.i IS NOT NULL
                ORDER BY random() LIMIT 1
            ) AS tr;
        """)

        self.conn.commit()
        return (time.time() - start) * 1000

    def delete_elem(self, table, record_id):
        c = self.conn.cursor()
        try:
            if table == 'Student':
                c.execute('DELETE FROM "Student" WHERE stud_id = %s', (record_id,))
            elif table == 'Teacher':
                c.execute('DELETE FROM "Teacher" WHERE tch_id = %s', (record_id,))
            elif table == 'Subject':
                c.execute('DELETE FROM "Subject" WHERE subj_id = %s', (record_id,))

            self.conn.commit()
            return True

        except:
            self.conn.rollback()
            return False

    def search_by_grade_range(self, min_grade, max_grade):
        import time
        start = time.time()

        c = self.conn.cursor()
        c.execute("""
            SELECT st.stud_id,
                   st."Name",
                   st.birth,
                   COALESCE(AVG(r.grade), 0) AS avg_grade,
                   COUNT(r.grade) AS grade_count
            FROM "Student" st
            LEFT JOIN "Records" r ON r.stud_id = st.stud_id
            GROUP BY st.stud_id, st."Name", st.birth
            HAVING COALESCE(AVG(r.grade), 0) BETWEEN %s AND %s
            ORDER BY avg_grade DESC
        """, (min_grade, max_grade))

        rows = c.fetchall()
        ms = (time.time() - start) * 1000

        return rows, ms

    def Search_by_id(self, id):
        c = self.conn.cursor()

        # ---------- STUDENT ----------
        try:
            c.execute('SELECT * FROM "Student" WHERE stud_id = %s', (id,))
            student = c.fetchall()

            if student:  # знайдено
                c.execute('''
                    SELECT s.subj_id, s."Name", r.grade
                    FROM "Records" r
                    JOIN "Subject" s ON s.subj_id = r.subj_id
                    WHERE r.stud_id = %s
                ''', (id,))
                subjects = c.fetchall()

                c.execute('SELECT COUNT(grade), AVG(grade) FROM "Records" WHERE stud_id = %s', (id,))
                stats = c.fetchone()

                return {
                    "type": "student",
                    "data": student,
                    "subjects": subjects,
                    "stats": stats
                }
        except:

            try:
                c.execute('SELECT * FROM "Teacher" WHERE tch_id = %s', (id,))
                teacher = c.fetchall()

                if teacher:
                    c.execute('SELECT subj_id, "Name", hour_per_week FROM "Subject" WHERE tch_id = %s', (id,))
                    subjects = c.fetchall()

                    c.execute('''
                        SELECT COUNT(r.grade), AVG(r.grade)
                        FROM "Records" r
                        JOIN "Subject" s ON s.subj_id = r.subj_id
                        WHERE s.tch_id = %s
                    ''', (id,))
                    stats = c.fetchone()

                    return {
                        "type": "teacher",
                        "data": teacher,
                        "subjects": subjects,
                        "stats": stats
                    }
            except:
                try:
                    c.execute('SELECT * FROM "Subject" WHERE subj_id = %s', (id,))
                    subject = c.fetchall()

                    if subject:
                        c.execute('''
                            SELECT tch_id, "Name", birth
                            FROM "Teacher"
                            WHERE tch_id = (SELECT tch_id FROM "Subject" WHERE subj_id = %s)
                        ''', (id,))
                        teacher = c.fetchall()

                        c.execute('SELECT COUNT(grade), AVG(grade) FROM "Records" WHERE subj_id = %s', (id,))
                        stats = c.fetchone()

                        return {
                            "type": "subject",
                            "data": subject,
                            "teacher": teacher,
                            "stats": stats
                        }
                except:
                    # ---------- RECORD ----------
                    try:
                        c.execute('SELECT * FROM "Records" WHERE grade_id = %s', (id,))
                        record = c.fetchall()

                        grade_id, subj_id, stud_id, grade, date = record[0]

                        c.execute('SELECT tch_id, "Name", birth FROM "Teacher" '
                                  'WHERE tch_id = (SELECT tch_id FROM "Subject" WHERE subj_id = %s)',
                                  (subj_id,))
                        teacher = c.fetchall()

                        c.execute('SELECT stud_id, "Name", birth FROM "Student" WHERE stud_id = %s',
                                  (stud_id,))
                        student = c.fetchall()

                        c.execute('SELECT subj_id, "Name", hour_per_week FROM "Subject" WHERE subj_id = %s',
                                  (subj_id,))
                        subject = c.fetchall()

                        return {
                            "type": "record",
                            "data": record,
                            "teacher": teacher,
                            "student": student,
                            "subject": subject
                        }

                    except:
                        return False

    def Teachers_with_TEXT_in_their_name(self, text):
        import time
        start = time.time()
        c = self.conn.cursor()
        try:
            pattern = f"%{text}%"
            c.execute('''
                SELECT tch_id, "Name", birth 
                FROM "Teacher" 
                WHERE "Name" LIKE %s 
                ORDER BY birth ASC
            ''', (pattern,))
            rows = c.fetchall()
            ms = (time.time() - start) * 1000
            return rows, ms
        except:
            self.conn.rollback()
            return False

    def search_teachers_by_work(self, min_subjects):
        import time
        start = time.time()
        c = self.conn.cursor()
        try:
            c.execute('''
                SELECT t.tch_id, t."Name", COUNT(s.subj_id) as subj_count, SUM(s.hour_per_week) as total_hours
                FROM "Teacher" t
                JOIN "Subject" s ON t.tch_id = s.tch_id
                GROUP BY t.tch_id, t."Name"
                HAVING COUNT(s.subj_id) >= %s
                ORDER BY subj_count DESC
            ''', (min_subjects,))
            rows = c.fetchall()
            ms = (time.time() - start) * 1000
            return rows, ms
        except :
            self.conn.rollback()
            return False







