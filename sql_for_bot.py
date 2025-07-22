from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import sqlalchemy as sa


Base = declarative_base()

pg_engine = create_engine("postgresql://kyrs:Bobr16481@localhost/db")

Session = sessionmaker(bind=pg_engine)
class QuestionAndAnswer(Base):
    __tablename__ = "question_answer"

    id = sa.Column(sa.Integer, primary_key=True)
    question = sa.Column(sa.String)
    answer = sa.Column(sa.String)

Base.metadata.create_all(pg_engine)

class QuestionStatistics(Base):
    __tablename__ = "question_statistics"

    id = sa.Column(sa.Integer, primary_key=True)
    question = sa.Column(sa.String)
    times = sa.Column(sa.Integer)

Base.metadata.create_all(pg_engine)


def get_sql_questions():
    questions = []
    session = Session()
    obs = session.query(QuestionAndAnswer).all()
    for obsi in obs:
        questions.append(obsi.question)
    for i in range(len(questions)):
        ob = QuestionStatistics(question=questions[i], times=0)
        session.add(ob)
        session.commit()
        session.close()

def get_times():
    times = []
    session = Session()
    obs = session.query(QuestionStatistics).all()
    for obsi in obs:
        times.append(obsi.times)
    session.close()
    return times

def change_times(question):
    session = Session()
    session.query(QuestionStatistics).filter(QuestionStatistics.question == question).update({QuestionStatistics.times: QuestionStatistics.times+1})
    session.commit()
    session.close()
def get_sql_table():
    questions = []
    answer = []
    session = Session()
    obs = session.query(QuestionAndAnswer).all()
    for obsi in obs:
        questions.append(obsi.question)
        answer.append(obsi.answer)
    session.close()
    return questions, answer


def add_sql(question1, answer1):
    session = Session()
    bd_qa = QuestionAndAnswer(question=question1, answer=answer1)
    session.add(bd_qa)
    session.commit()
    session.close()

def get_statistics():
    session = Session()
    records = session.query(QuestionStatistics).order_by(QuestionStatistics.times.desc()).all()
    table_str = "ID | Question | Times\n"
    table_str += "-" * 30 + "\n"
    for record in records:
        table_str += f"{record.id} | {record.question} | {record.times}\n"
    session.close()
    return table_str


