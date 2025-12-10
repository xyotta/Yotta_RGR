from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.exc import SQLAlchemyError


DATABASE_URI = 'postgresql+psycopg2://postgres:1111@localhost:5432/postgres'
engine = create_engine(DATABASE_URI, echo=False)

Base = declarative_base()
Session = sessionmaker(bind=engine)




class Student(Base):
    __tablename__ = "Student"
    stud_id = Column(Integer, primary_key=True)
    Name = Column(String)
    birth = Column(Date)
    records = relationship("Record", back_populates="student", cascade="all, delete-orphan")


class Teacher(Base):
    __tablename__ = "Teacher"
    tch_id = Column(Integer, primary_key=True)
    Name = Column(String)
    birth = Column(Date)
    subjects = relationship("Subject", back_populates="teacher", cascade="all, delete-orphan")


class Subject(Base):
    __tablename__ = "Subject"
    subj_id = Column(Integer, primary_key=True)
    Name = Column(String)
    hour_per_week = Column(Integer)
    tch_id = Column(Integer, ForeignKey("Teacher.tch_id", ondelete="CASCADE"))

    teacher = relationship("Teacher", back_populates="subjects")
    records = relationship("Record", back_populates="subject", cascade="all, delete-orphan")


class Record(Base):
    __tablename__ = "Records"
    grade_id = Column(Integer, primary_key=True, autoincrement=True)
    stud_id = Column(Integer, ForeignKey("Student.stud_id", ondelete="CASCADE"))
    subj_id = Column(Integer, ForeignKey("Subject.subj_id", ondelete="CASCADE"))
    grade = Column(Integer)

    student = relationship("Student", back_populates="records")
    subject = relationship("Subject", back_populates="records")


Base.metadata.create_all(engine)




class ORM_Model:
    def __init__(self):
        self.session = Session()

    def view_table(self, table):
        mapping = {"Student": Student, "Teacher": Teacher, "Subject": Subject}
        cls = mapping.get(table)
        if not cls: return []

        # Конвертуємо об'єкти в кортежі для сумісності з view.py
        rows = self.session.query(cls).order_by(cls.__table__.primary_key.columns.values()[0]).all()
        result = []
        for row in rows:
            result.append(tuple(getattr(row, col.name) for col in row.__table__.columns))
        return result

    def add_student(self, name, birth, stud_id):
        try:
            st = Student(stud_id=stud_id, Name=name, birth=birth)
            self.session.add(st)
            self.session.commit()
            return True
        except SQLAlchemyError:
            self.session.rollback()
            return False

    def add_teacher(self, name, birth, tch_id):
        try:
            t = Teacher(tch_id=tch_id, Name=name, birth=birth)
            self.session.add(t)
            self.session.commit()
            return True
        except SQLAlchemyError:
            self.session.rollback()
            return False

    def add_subject(self, name, hours, subj_id, tch_id):
        try:
            if not self.session.get(Teacher, tch_id): return False
            s = Subject(subj_id=subj_id, Name=name, hour_per_week=hours, tch_id=tch_id)
            self.session.add(s)
            self.session.commit()
            return True
        except SQLAlchemyError:
            self.session.rollback()
            return False

    def update_student(self, value, valuenew1, valuenew2, valuenew3):
        try:
            st = self.session.get(Student, value)
            if not st: return False
            if valuenew1: st.Name = valuenew1
            if valuenew2: st.birth = valuenew2
            if valuenew3: st.stud_id = valuenew3
            self.session.commit()
            return True
        except SQLAlchemyError:
            self.session.rollback()
            return False

    def update_teacher(self, value, valuenew1, valuenew2, valuenew3):
        try:
            t = self.session.get(Teacher, value)
            if not t: return False
            if valuenew1: t.Name = valuenew1
            if valuenew2: t.birth = valuenew2
            if valuenew3: t.tch_id = valuenew3
            self.session.commit()
            return True
        except SQLAlchemyError:
            self.session.rollback()
            return False

    def update_subject(self, value, valuenew1, valuenew2, valuenew3, valuenew4):
        try:
            s = self.session.get(Subject, value)
            if not s: return False
            if valuenew1: s.Name = valuenew1
            if valuenew2: s.hour_per_week = valuenew2
            if valuenew3: s.subj_id = valuenew3
            if valuenew4:
                if not self.session.get(Teacher, valuenew4): return False
                s.tch_id = valuenew4
            self.session.commit()
            return True
        except SQLAlchemyError:
            self.session.rollback()
            return False

    def delete_elem(self, table, record_id):
        try:
            mapping = {"Student": Student, "Teacher": Teacher, "Subject": Subject}
            cls = mapping.get(table)
            if not cls: return False

            obj = self.session.get(cls, record_id)
            if not obj: return False

            self.session.delete(obj)
            self.session.commit()
            return True
        except SQLAlchemyError:
            self.session.rollback()
            return False