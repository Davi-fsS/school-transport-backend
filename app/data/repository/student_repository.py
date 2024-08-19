from typing import List
from sqlalchemy.orm import Session
from data.model.student_model import StudentModel
from presentation.dto.UpdateStudent import UpdateStudent
from data.infrastructure.database import get_db

class StudentRepository():
    db: Session

    def __init__(self):
        self.db = next(get_db())

    def get_student(self, student_id: int):
        try:
            student = self.db.query(StudentModel).filter(StudentModel.id == student_id, StudentModel.disabled == False).first()

            if student is None:
                raise ValueError("Aluno não encontrado")

            return student
        except:
            self.db.rollback()
            raise ValueError("Erro ao fazer a leitura no sistema")
        finally:
            self.db.close()
        
    def get_student_by_code(self, student_code: str):
        try:
            student = self.db.query(StudentModel).filter(StudentModel.code == student_code, StudentModel.disabled == False).first()

            return student
        except:
            self.db.rollback()
            raise ValueError("Erro ao fazer a leitura no sistema")
        finally:
            self.db.close()
        
    def get_students_by_student_list(self, student_id_list: List[int]):
        try:
            students = self.db.query(StudentModel).filter(StudentModel.id.in_(student_id_list), StudentModel.disabled == False).all()
            return students
        except:
            self.db.rollback()
            raise ValueError("Erro ao fazer a leitura no sistema")
        finally:
            self.db.close()

    def create_student(self, student: StudentModel):
        try:
            self.db.add(student)
            self.db.commit()
            
            return student.id
        except:
            self.db.rollback()
            raise ValueError("Erro ao salvar no sistema")
        finally:
            self.db.close()

    def create_student_list(self, db_student_list: List[StudentModel]):
        created_ids = []
        try:
            for db_student in db_student_list:
                self.db.add(db_student)
                self.db.commit()
                created_ids.append(db_student.id)

            return created_ids
        except:
            self.db.rollback()
            raise ValueError("Erro ao salvar no sistema")
        finally:
            self.db.close()
        
    def update_student(self, student_update: UpdateStudent):
        with next(get_db()) as session:
            try:
                student = self.get_student(student_update.id)
                student.name = student_update.name
                student.year = student_update.year
                session.commit()
            except:
                session.rollback()
                raise ValueError("Erro ao salvar no sistema")
        
    def delete_student(self, student_id: int):
        with next(get_db()) as session:
            try:
                student = self.get_student(student_id)
                student.disabled = True
                session.commit()
            except:
                session.rollback()
                raise ValueError("Erro ao salvar no sistema")        