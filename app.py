import sys
import typing
from config.config import DevelopementConfig
from flask import Flask, jsonify, request
#from data.Dbclasses import *
from flask_sqlalchemy import SQLAlchemy
from data.req import getData
from config.logger import createLogger



app = Flask(__name__)
app.debug = True
#app.config.from_object(DevelopementConfig)

app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql+psycopg2://postgres:EGORletov2312@localhost/my_db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SQLALCHEMY_ECHO'] = True



db = SQLAlchemy(app)

logger = createLogger()

class Topic(db.Model):
    __tablename__ = 'topic'
    id = db.Column(db.Integer(), primary_key=True)
    value = db.Column(db.String(255), nullable=False)
    topic = db.relationship('Subtopic', backref='subtopic_topics',
                            primaryjoin="and_(Topic.id == foreign(Subtopic.topicid))",
                            )

    def __init__(self, value):
        self.value = value
    def _repr(self, **fields: typing.Dict[str, typing.Any]) -> str:
        '''
        Helper for __repr__
        '''
        field_strings = []
        at_least_one_attached_attribute = False
        for key, field in fields.items():
            try:
                field_strings.append(f'{key}={field!r}')
            except SQLAlchemy.orm.exc.DetachedInstanceError:
                field_strings.append(f'{key}=DetachedInstanceError')
            else:
                at_least_one_attached_attribute = True
        if at_least_one_attached_attribute:
            return f"<{self.__class__.__name__}({','.join(field_strings)})>"
        return f"<{self.__class__.__name__} {id(self)}>"
    #def __repr__(self):
        #return '"Topic": %r'   % self.value
    def __repr__(self):
        return self._repr(id=self.id, value=self.value)

class Subtopic(db.Model):
    __tablename__ = 'subtopic'
    id = db.Column(db.Integer(), primary_key=True)
    topicid = db.Column(db.Integer(), db.ForeignKey('topic.id'), nullable=False)
    value = db.Column(db.String(255), nullable=False)
    question = db.relationship('Question', backref='question_topics',
                            primaryjoin="and_(Subtopic.id == foreign(Question.subtopicid))",
                            )

    def __init__(self, topic, value):
        self.topicid = topic
        self.value = value
    def _repr(self, **fields: typing.Dict[str, typing.Any]) -> str:
        '''
        Helper for __repr__
        '''
        field_strings = []
        at_least_one_attached_attribute = False
        for key, field in fields.items():
            try:
                field_strings.append(f'{key}={field!r}')
            except SQLAlchemy.orm.exc.DetachedInstanceError:
                field_strings.append(f'{key}=DetachedInstanceError')
            else:
                at_least_one_attached_attribute = True
        if at_least_one_attached_attribute:
            return f"<{self.__class__.__name__}({','.join(field_strings)})>"
        return f"<{self.__class__.__name__} {id(self)}>"
    def __repr__(self):
        return self._repr(id=self.id, topicid=self.topicid, value=self.value)

class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer(), primary_key=True)
    subtopicid = db.Column(db.Integer(), db.ForeignKey('subtopic.id'), nullable=False)
    value = db.Column(db.String(255), nullable=False)
    Questionincr = db.relationship('Questionincr', backref='question_questionincr',
                            primaryjoin="and_(Question.id == foreign(Questionincr.questionid))"
                            )
    controller = db.relationship('ControllerAnswer', backref='Controller_question',
                            primaryjoin="and_(Question.id == foreign(ControllerAnswer.questionid))"
                            )

    def __init__(self,subtopicId,value):
        self.subtopicid = subtopicId
        self.value = value

    def _repr(self, **fields: typing.Dict[str, typing.Any]) -> str:
        '''
        Helper for __repr__
        '''
        field_strings = []
        at_least_one_attached_attribute = False
        for key, field in fields.items():
            try:
                field_strings.append(f'{key}={field!r}')
            except SQLAlchemy.orm.exc.DetachedInstanceError:
                field_strings.append(f'{key}=DetachedInstanceError')
            else:
                at_least_one_attached_attribute = True
        if at_least_one_attached_attribute:
            return f"<{self.__class__.__name__}({','.join(field_strings)})>"
        return f"<{self.__class__.__name__} {id(self)}>"

    def __repr__(self):
        return self._repr(id=self.id, subtopicid=self.subtopicid, value=self.value)


class Answer(db.Model):
    __tablename__ = 'answer'
    id = db.Column(db.Integer(), primary_key=True)
    value = db.Column(db.Text(), nullable=False)
    controller = db.relationship('ControllerAnswer', backref='Controller_answer',
                            primaryjoin="and_(Answer.id == foreign(ControllerAnswer.answerid))"
                            )
    def __init__(self,value):
        self.value = value

    def _repr(self, **fields: typing.Dict[str, typing.Any]) -> str:
        '''
        Helper for __repr__
        '''
        field_strings = []
        at_least_one_attached_attribute = False
        for key, field in fields.items():
            try:
                field_strings.append(f'{key}={field!r}')
            except SQLAlchemy.orm.exc.DetachedInstanceError:
                field_strings.append(f'{key}=DetachedInstanceError')
            else:
                at_least_one_attached_attribute = True
        if at_least_one_attached_attribute:
            return f"<{self.__class__.__name__}({','.join(field_strings)})>"
        return f"<{self.__class__.__name__} {id(self)}>"
    def __repr__(self):
        return self._repr(id=self.id, value=self.value)


class Questionincr(db.Model):
    __tablename__='questionincr'
    id = db.Column(db.Integer(), primary_key=True)
    value = db.Column(db.String(255), nullable=False)
    questionid = db.Column(db.Integer(), db.ForeignKey('question.id'), nullable=False)


    def __init__(self,value,questionId):
        self.value = value
        self.questionid = questionId

    def _repr(self, **fields: typing.Dict[str, typing.Any]) -> str:
        '''
        Helper for __repr__
        '''
        field_strings = []
        at_least_one_attached_attribute = False
        for key, field in fields.items():
            try:
                field_strings.append(f'{key}={field!r}')
            except SQLAlchemy.orm.exc.DetachedInstanceError:
                field_strings.append(f'{key}=DetachedInstanceError')
            else:
                at_least_one_attached_attribute = True
        if at_least_one_attached_attribute:
            return f"<{self.__class__.__name__}({','.join(field_strings)})>"
        return f"<{self.__class__.__name__} {id(self)}>"

    def __repr__(self):
        return self._repr(id=self.id, questionid=self.questionid, value=self.value)

class Nationality(db.Model):
    __tablename__="nationality"
    id = db.Column(db.Integer(), primary_key=True)
    value = db.Column(db.String(255), nullable=False)
    controller = db.relationship('ControllerAnswer', backref='Controller_Nationality',
                            primaryjoin="and_(Nationality.id == foreign(ControllerAnswer.nationality))"
                            )
    def _repr(self, **fields: typing.Dict[str, typing.Any]) -> str:
        '''
        Helper for __repr__
        '''
        field_strings = []
        at_least_one_attached_attribute = False
        for key, field in fields.items():
            try:
                field_strings.append(f'{key}={field!r}')
            except SQLAlchemy.orm.exc.DetachedInstanceError:
                field_strings.append(f'{key}=DetachedInstanceError')
            else:
                at_least_one_attached_attribute = True
        if at_least_one_attached_attribute:
            return f"<{self.__class__.__name__}({','.join(field_strings)})>"
        return f"<{self.__class__.__name__} {id(self)}>"

    def __repr__(self):
        return self._repr(id=self.id, value=self.value)

class OldEducation(db.Model):
    __tablename__="education"
    id = db.Column(db.Integer(), primary_key=True)
    value = db.Column(db.String(255), nullable=False)
    controller = db.relationship('ControllerAnswer', backref='Controller_oldeducation',
                            primaryjoin="and_(OldEducation.id == foreign(ControllerAnswer.oldeducation))"
                            )
    def _repr(self, **fields: typing.Dict[str, typing.Any]) -> str:
        '''
        Helper for __repr__
        '''
        field_strings = []
        at_least_one_attached_attribute = False
        for key, field in fields.items():
            try:
                field_strings.append(f'{key}={field!r}')
            except SQLAlchemy.orm.exc.DetachedInstanceError:
                field_strings.append(f'{key}=DetachedInstanceError')
            else:
                at_least_one_attached_attribute = True
        if at_least_one_attached_attribute:
            return f"<{self.__class__.__name__}({','.join(field_strings)})>"
        return f"<{self.__class__.__name__} {id(self)}>"

    def __repr__(self):
        return self._repr(id=self.id, value=self.value)

class Direction(db.Model):
    __tablename__="direction"
    id = db.Column(db.Integer(), primary_key=True)
    value = db.Column(db.String(255), nullable=False)
    controller = db.relationship('ControllerAnswer', backref='Controller_Direction',
                            primaryjoin="and_(Direction.id == foreign(ControllerAnswer.direction))"
                            )
    def _repr(self, **fields: typing.Dict[str, typing.Any]) -> str:
        '''
        Helper for __repr__
        '''
        field_strings = []
        at_least_one_attached_attribute = False
        for key, field in fields.items():
            try:
                field_strings.append(f'{key}={field!r}')
            except SQLAlchemy.orm.exc.DetachedInstanceError:
                field_strings.append(f'{key}=DetachedInstanceError')
            else:
                at_least_one_attached_attribute = True
        if at_least_one_attached_attribute:
            return f"<{self.__class__.__name__}({','.join(field_strings)})>"
        return f"<{self.__class__.__name__} {id(self)}>"

    def __repr__(self):
        return self._repr(id=self.id, value=self.value)

class Resthelth(db.Model):
    __tablename__="resthelth"
    id = db.Column(db.Integer(), primary_key=True)
    value = db.Column(db.String(255), nullable=False)
    controller = db.relationship('ControllerAnswer', backref='Controller_Resthelth',
                            primaryjoin="and_(Resthelth.id == foreign(ControllerAnswer.resthelth))"
                            )
    def _repr(self, **fields: typing.Dict[str, typing.Any]) -> str:
        '''
        Helper for __repr__
        '''
        field_strings = []
        at_least_one_attached_attribute = False
        for key, field in fields.items():
            try:
                field_strings.append(f'{key}={field!r}')
            except SQLAlchemy.orm.exc.DetachedInstanceError:
                field_strings.append(f'{key}=DetachedInstanceError')
            else:
                at_least_one_attached_attribute = True
        if at_least_one_attached_attribute:
            return f"<{self.__class__.__name__}({','.join(field_strings)})>"
        return f"<{self.__class__.__name__} {id(self)}>"

    def __repr__(self):
        return self._repr(id=self.id, value=self.value)


class Privileges(db.Model):
    __tablename__="privileges"
    id = db.Column(db.Integer(), primary_key=True)
    value = db.Column(db.String(255), nullable=False)
    controller = db.relationship('ControllerAnswer', backref='Controller_priv',
                            primaryjoin="and_(Privileges.id == foreign(ControllerAnswer.privileges))"
                            )
    def _repr(self, **fields: typing.Dict[str, typing.Any]) -> str:
        '''
        Helper for __repr__
        '''
        field_strings = []
        at_least_one_attached_attribute = False
        for key, field in fields.items():
            try:
                field_strings.append(f'{key}={field!r}')
            except SQLAlchemy.orm.exc.DetachedInstanceError:
                field_strings.append(f'{key}=DetachedInstanceError')
            else:
                at_least_one_attached_attribute = True
        if at_least_one_attached_attribute:
            return f"<{self.__class__.__name__}({','.join(field_strings)})>"
        return f"<{self.__class__.__name__} {id(self)}>"

    def __repr__(self):
        return self._repr(id=self.id, value=self.value)

class Level(db.Model):
    __tablename__="level"
    id = db.Column(db.Integer(), primary_key=True)
    value = db.Column(db.String(255), nullable=False)
    controller = db.relationship('ControllerAnswer', backref='Controller_level',
                            primaryjoin="and_(Level.id == foreign(ControllerAnswer.level))"
                            )
    def _repr(self, **fields: typing.Dict[str, typing.Any]) -> str:
        '''
        Helper for __repr__
        '''
        field_strings = []
        at_least_one_attached_attribute = False
        for key, field in fields.items():
            try:
                field_strings.append(f'{key}={field!r}')
            except SQLAlchemy.orm.exc.DetachedInstanceError:
                field_strings.append(f'{key}=DetachedInstanceError')
            else:
                at_least_one_attached_attribute = True
        if at_least_one_attached_attribute:
            return f"<{self.__class__.__name__}({','.join(field_strings)})>"
        return f"<{self.__class__.__name__} {id(self)}>"

    def __repr__(self):
        return self._repr(id=self.id, value=self.value)

class ControllerAnswer(db.Model):
    __tablename__ = 'controller'
    id = db.Column(db.Integer(), primary_key=True)
    nationality = db.Column(db.Integer(), db.ForeignKey('nationality.id'), nullable=True)
    oldeducation = db.Column(db.Integer(),  db.ForeignKey('education.id'), nullable=True)
    direction = db.Column(db.Integer(),db.ForeignKey('direction.id'), nullable=True)
    resthelth = db.Column(db.Integer(),db.ForeignKey('resthelth.id'), nullable=True)
    privileges = db.Column(db.Integer(),db.ForeignKey('privileges.id'), nullable=True)
    level = db.Column(db.Integer(),db.ForeignKey('level.id'), nullable=True)
    answerid = db.Column(db.Integer(), db.ForeignKey('answer.id'), nullable=False)
    questionid = db.Column(db.Integer(), db.ForeignKey('question.id'), nullable=False)

    def _repr(self, **fields: typing.Dict[str, typing.Any]) -> str:
        '''
        Helper for __repr__
        '''
        field_strings = []
        at_least_one_attached_attribute = False
        for key, field in fields.items():
            try:
                field_strings.append(f'{key}={field!r}')
            except SQLAlchemy.orm.exc.DetachedInstanceError:
                field_strings.append(f'{key}=DetachedInstanceError')
            else:
                at_least_one_attached_attribute = True
        if at_least_one_attached_attribute:
            return f"<{self.__class__.__name__}({','.join(field_strings)})>"
        return f"<{self.__class__.__name__} {id(self)}>"

    def __repr__(self):
        return self._repr(id=self.id, nationality=self.nationality, oldeducation=self.oldeducation, direction=self.direction,
                          resthelth=self.resthelth, privileges=self.privileges, level=self.level, answerid=self.answerid,
                          questionid = self.questionid)

db.create_all()

def InitTopic():
    Topic1 = Topic("Подача документов")
    db.session.add(Topic1)
    db.session.commit()


    Topic1 = Topic("Календарь приема")
    db.session.add(Topic1)
    db.session.commit()

    Topic1 = Topic("Особые категории")
    db.session.add(Topic1)
    db.session.commit()

    Topic1 = Topic("Направления")
    db.session.add(Topic1)
    db.session.commit()

    Topic1 = Topic("Экзамены")
    db.session.add(Topic1)
    db.session.commit()

    Topic1= Topic("Оценить шансы")
    db.session.add(Topic1)
    db.session.commit()

    Topic1= Topic("Общежитие")
    db.session.add(Topic1)
    db.session.commit()


def InitSubtopic():
    subtopic1 = Subtopic(1, "Как подать документы")
    db.session.add(subtopic1)
    db.session.commit()

    subtopic1 = Subtopic(1, "Необходимый перечень документов")
    db.session.add(subtopic1)
    db.session.commit()

    subtopic1 = Subtopic(1, "Заключить договор на обучение по контракту")
    db.session.add(subtopic1)
    db.session.commit()

    subtopic1 = Subtopic(1, "Как подать согласие")
    db.session.add(subtopic1)
    db.session.commit()


    subtopic1 = Subtopic(2, "Основные даты")
    db.session.add(subtopic1)
    db.session.commit()

    subtopic1 = Subtopic(2, "Расписание вступительных испытаний")
    db.session.add(subtopic1)
    db.session.commit()

    subtopic1 = Subtopic(2, "Приказы о зачислении")
    db.session.add(subtopic1)
    db.session.commit()

    subtopic1 = Subtopic(2, "Заселение в общежитие")
    db.session.add(subtopic1)
    db.session.commit()

    subtopic1 = Subtopic(3, "Льготы")
    db.session.add(subtopic1)
    db.session.commit()

    subtopic1 = Subtopic(3, "Поступление БВИ")
    db.session.add(subtopic1)
    db.session.commit()

    subtopic1 = Subtopic(3, "Целевое обучение")
    db.session.add(subtopic1)
    db.session.commit()

    subtopic1 = Subtopic(3, "Индивидуальные достижения")
    db.session.add(subtopic1)
    db.session.commit()


    subtopic1 = Subtopic(4, "Направления")
    db.session.add(subtopic1)
    db.session.commit()

    subtopic1 = Subtopic(5, "ЕГЭ")
    db.session.add(subtopic1)
    db.session.commit()

    subtopic1 = Subtopic(5, "Вступительные испытания, проводимые ВУЗом")
    db.session.add(subtopic1)
    db.session.commit()

    subtopic1 = Subtopic(5, "Минимальные баллы")
    db.session.add(subtopic1)
    db.session.commit()

    subtopic1 = Subtopic(6, "Оценить шансы")
    db.session.add(subtopic1)
    db.session.commit()

    subtopic1 = Subtopic(7, "Общежитие")
    db.session.add(subtopic1)
    db.session.commit()


def InitQuestion():
    question = Question(1,'Как подать документы через сайт?')
    db.session.add(question)
    db.session.commit()

    question = Question(1,'Как подать документы лично?')
    db.session.add(question)
    db.session.commit()

    question = Question(1,'Как подать документы по почте?')
    db.session.add(question)
    db.session.commit()

    question = Question(1,'Как подать документы через Госуслуги?')
    db.session.add(question)
    db.session.commit()

    question = Question(1,'Как изменить поданное заявление?')
    db.session.add(question)
    db.session.commit()

    question = Question(2,'Какие документы нужны для поступления по общему конкурсу?')
    db.session.add(question)
    db.session.commit()

    question = Question(2,'Какие документы нужны для целевого приема?')
    db.session.add(question)
    db.session.commit()

    question = Question(2,'Какие документы нужны для приема без экзаменов?')
    db.session.add(question)
    db.session.commit()

    question = Question(2,'Какие документы нужны для приема вне конкурса (особая квота)?')
    db.session.add(question)
    db.session.commit()

    question = Question(2,'Какие документы нужны иностранным гражданам?')
    db.session.add(question)
    db.session.commit()

    question = Question(2,'Нужны ли оригиналы?')
    db.session.add(question)
    db.session.commit()

    question = Question(3,'Что такое обучение по контракту?')
    db.session.add(question)
    db.session.commit()

    question = Question(3,'Где можно взять шаблон договора?')
    db.session.add(question)
    db.session.commit()

    question = Question(3,'До какого числа нужно заключить договор?')
    db.session.add(question)
    db.session.commit()

    question = Question(3,'Кто и как заключает договор? ')
    db.session.add(question)
    db.session.commit()

    question = Question(3,'Как можно оплатить (мат. Капитал, оплата онлайн, образовательный кредит)?')
    db.session.add(question)
    db.session.commit()

    question = Question(4,'Где можно взять шаблон согласия?')
    db.session.add(question)
    db.session.commit()

    question = Question(4,'До какого числа нужно подать согласие?')
    db.session.add(question)
    db.session.commit()

    question = Question(4,'Сколько согласий одновременно можно подать?')
    db.session.add(question)
    db.session.commit()

    question = Question(4,'Можно ли менять поданное согласие?')
    db.session.add(question)
    db.session.commit()

    question = Question(4,'Как подать согласие?')
    db.session.add(question)
    db.session.commit()


    question = Question(5,'Когда начинается прием документов?')
    db.session.add(question)
    db.session.commit()

    question = Question(5,'Когда заканчивается прием документов?')
    db.session.add(question)
    db.session.commit()

    question = Question(5,'До какого числа можно вносить изменения в заявление?')
    db.session.add(question)
    db.session.commit()

    question = Question(5,'До какого числа необходимо подать согласие?')
    db.session.add(question)
    db.session.commit()

    question = Question(5,'До какого числа можно заключить договор на контрактное обучение?')
    db.session.add(question)
    db.session.commit()

    question = Question(5,'До какого числа необходимо предоставить оригиналы?')
    db.session.add(question)
    db.session.commit()

    question = Question(5,'Когда публикуются приказы о зачислении?')
    db.session.add(question)
    db.session.commit()

    question = Question(6,'Когда проводятся вступительные испытания по материалам ВУЗа?')
    db.session.add(question)
    db.session.commit()

    question = Question(6,'Когда станут известны результаты экзаменов?')
    db.session.add(question)
    db.session.commit()

    question = Question(6,'Как найти расписание вступительных испытаний?')
    db.session.add(question)
    db.session.commit()

    question = Question(6,'Когда проводится апелляция?')
    db.session.add(question)
    db.session.commit()

    question = Question(7,'Когда публикуются приказы о зачислении на бюджетные места?')
    db.session.add(question)
    db.session.commit()

    question = Question(7,'Когда публикуются приказы о зачислении на контрактные места?')
    db.session.add(question)
    db.session.commit()

    question = Question(7,'Когда публикуются приказы о зачислении на места в пределах особой квоты?')
    db.session.add(question)
    db.session.commit()

    question = Question(8,'Когда нужно подать документы на заселение?')
    db.session.add(question)
    db.session.commit()

    question = Question(8,'Когда будет заселение в общежитие?')
    db.session.add(question)
    db.session.commit()

    question = Question(8,'Могу ли я заселиться раньше/позже?')
    db.session.add(question)
    db.session.commit()

    question = Question(9,'Какие «льготы» установлены правилами приема?')
    db.session.add(question)
    db.session.commit()

    question = Question(9,'Какие документы подавать при поступлении по «льготе»?')
    db.session.add(question)
    db.session.commit()

    question = Question(9,'До какого числа необходимо подать документы «по льготе»?')
    db.session.add(question)
    db.session.commit()

    question = Question(9,'Можно ли сдавать вступительные испытания по материалам ВУЗа, если я поступаю по «льготе»?')
    db.session.add(question)
    db.session.commit()

    question = Question(9,'Какие минимальные баллы ЕГЭ нужны при поступлении «по льготе»?')
    db.session.add(question)
    db.session.commit()

    question = Question(9,'Когда издается приказ о зачислении «по льготе»?')
    db.session.add(question)
    db.session.commit()

    question = Question(9,'Есть ли инклюзивное сопровождение при поступлении в НГТУ?')
    db.session.add(question)
    db.session.commit()

    question = Question(9,'На какие направления действует «льготное право поступление»? (возможно, дублирует следующий вопрос)')
    db.session.add(question)
    db.session.commit()

    question = Question(9,'На сколько направлений действует «льготное право поступление»?')
    db.session.add(question)
    db.session.commit()

    question = Question(10,'Кто может поступать «без вступительных испытаний»?')
    db.session.add(question)
    db.session.commit()

    question = Question(10,'До какого числа необходимо подать документы при поступлении «БВИ»?')
    db.session.add(question)
    db.session.commit()

    question = Question(10,'Какие документы подавать при поступлении БВИ?')
    db.session.add(question)
    db.session.commit()

    question = Question(10,'Нужно ли иметь результаты ЕГЭ при поступлении БВИ?')
    db.session.add(question)
    db.session.commit()

    question = Question(10,'Можно ли воспользоваться правом поступления БВИ, если сдавать вступительные испытания по материалам ВУЗа?')
    db.session.add(question)
    db.session.commit()

    question = Question(10,'Когда издается приказ о зачислении «БВИ»?')
    db.session.add(question)
    db.session.commit()

    question = Question(10,'На сколько направлений действует право поступление «БВИ»?')
    db.session.add(question)
    db.session.commit()

    question = Question(11,'Что такое целевое обучение?')
    db.session.add(question)
    db.session.commit()

    question = Question(11,'Кто заключает договор на целевое обучение? (возможно, дублирует после следующий вопрос)')
    db.session.add(question)
    db.session.commit()

    question = Question(11,'Где взять шаблон договора на целевое обучение? (возможно, дублирует следующий вопрос)')
    db.session.add(question)
    db.session.commit()

    question = Question(11,'Как заключить договор на целевое обучение?')
    db.session.add(question)
    db.session.commit()

    question = Question(11,'Какие документы необходимо подавать при поступлении на целевое обучение?')
    db.session.add(question)
    db.session.commit()

    question = Question(11,'До какого числа необходимо подать документы при поступлении на целевое обучение?')
    db.session.add(question)
    db.session.commit()

    question = Question(11,'Когда издается приказ о зачислении на целевое обучение?')
    db.session.add(question)
    db.session.commit()

    question = Question(12,'Какие индивидуальные достижения засчитываются при поступлении?')
    db.session.add(question)
    db.session.commit()

    question = Question(12,'Сколько баллов можно получить за индивидуальные достижения?')
    db.session.add(question)
    db.session.commit()

    question = Question(12,'До какого числа необходимо предоставить документы, подтверждающие наличие индивидуальных достижений?')
    db.session.add(question)
    db.session.commit()

    question = Question(12,'Как предоставить документы, подтверждающие наличие индивидуальных достижений?')
    db.session.add(question)
    db.session.commit()

    question = Question(12,'За какие года действуют индивидуальные достижения?')
    db.session.add(question)
    db.session.commit()

    question = Question(13,'Какие направления есть в НГТУ?')
    db.session.add(question)
    db.session.commit()

    question = Question(13,'На сколько направлений можно подать документы?')
    db.session.add(question)
    db.session.commit()

    question = Question(13,'Как поменять направление?')
    db.session.add(question)
    db.session.commit()

    question = Question(13,'Смогу ли я поменять направление после поступления?')
    db.session.add(question)
    db.session.commit()

    question = Question(13,'Смогу ли перейти на бюджет, если поступлю на контракт? (не уверен, что этот вопрос сюда)')
    db.session.add(question)
    db.session.commit()

    question = Question(13,'До какого числа можно изменить направления в заявлении?')
    db.session.add(question)
    db.session.commit()

    question = Question(13,'Сколько бюджетных и контарктых мест на напрвлениях?')
    db.session.add(question)
    db.session.commit()

    question = Question(13,'Какая стоимость обучения по контаркту на разных направлениях?')
    db.session.add(question)
    db.session.commit()

    question = Question(13,'Какие экзамены нужно сдавать для поступления на различные направления НГТУ?')
    db.session.add(question)
    db.session.commit()

    question = Question(13,'*Подобрать направление, с учетом сданных экзаменов?')
    db.session.add(question)
    db.session.commit()

    question = Question(14,'Какие минимальные баллы ЕГЭ?')
    db.session.add(question)
    db.session.commit()

    question = Question(14,'Какие ЕГЭ нужно сдавать для разных направлений?')
    db.session.add(question)
    db.session.commit()

    question = Question(14,'ЕГЭ за какие года действуют?')
    db.session.add(question)
    db.session.commit()

    question = Question(14,'Где можно сдать ЕГЭ? (а точно нужен этот и следующий вопрос?)')
    db.session.add(question)
    db.session.commit()

    question = Question(14,'Кто имеет права сдавать ЕГЭ?')
    db.session.add(question)
    db.session.commit()

    question = Question(14,'Нужно ли предоставлять свидетельство с результатами ЕГЭ?')
    db.session.add(question)
    db.session.commit()

    question = Question(14,'Если я сдал(а) ЕГЭ, нужно ли мне сдавать ВИ? (возможно, дублирует следующей вопрос)')
    db.session.add(question)
    db.session.commit()

    question = Question(15,'Кто имеет право сдавит ВИ?')
    db.session.add(question)
    db.session.commit()

    question = Question(15,'Как записаться на сдачу ВИ?')
    db.session.add(question)
    db.session.commit()

    question = Question(15,'До какого числа необходимо подать документы при поступлении по ВИ?')
    db.session.add(question)
    db.session.commit()

    question = Question(15,'Где будет происходить сдача ВИ? (возможно, лишний)')
    db.session.add(question)
    db.session.commit()

    question = Question(15,'В каком формате проходят ВИ?')
    db.session.add(question)
    db.session.commit()

    question = Question(15,'В какие даты проходят ВИ (расписание)?')
    db.session.add(question)
    db.session.commit()

    question = Question(15,'Как проходит апелляция при ВИ?')
    db.session.add(question)
    db.session.commit()

    question = Question(15,'Что такое система «прокторинга»?')
    db.session.add(question)
    db.session.commit()

    question = Question(15,'Могу ли я сдать ВИ из дома?')
    db.session.add(question)
    db.session.commit()

    question = Question(15,'Когда станут известны результаты ВИ?')
    db.session.add(question)
    db.session.commit()

    question = Question(15,'Где можно найти демоверсии ВИ?')
    db.session.add(question)
    db.session.commit()

    question = Question(15,'Существует ли инклюзивное сопровождении при сдачи ВИ по материалам ВУЗа?')
    db.session.add(question)
    db.session.commit()

    question = Question(15,'Могу ли я получить комнату в общежитии на время сдачи ВИ?')
    db.session.add(question)
    db.session.commit()

    question = Question(16,'Какие минимальные баллы необходимо набрать для участия в конкурсе на поступление?')
    db.session.add(question)
    db.session.commit()

    question = Question(16,'Какие минимальные баллы для обучения по контракту?')
    db.session.add(question)
    db.session.commit()

    question = Question(16,'*Подобрать направление, с учетом сданных экзаменов?')
    db.session.add(question)
    db.session.commit()

    question = Question(17,'Как оценить свои шансы поступит на бюджет? (Если бы поступление было сегодня)')
    db.session.add(question)
    db.session.commit()

    question = Question(17,'Какие минимальные баллы для обучения по контракту?')
    db.session.add(question)
    db.session.commit()

    question = Question(17,'Где просмотреть рейтинговые списки?')
    db.session.add(question)
    db.session.commit()

    question = Question(17,'Какие проходные баллы прошлых лет?')
    db.session.add(question)
    db.session.commit()

    question = Question(17,'Сколько бюджетные мест на направлениях?')
    db.session.add(question)
    db.session.commit()

    question = Question(17,'Где просмотреть приказы на зачисление?')
    db.session.add(question)
    db.session.commit()

    question = Question(17,'Когда издаются приказы на зачисления?')
    db.session.add(question)
    db.session.commit()

    question = Question(17,'Можно ли пойти на контракт, если не поступил на бюджет?')
    db.session.add(question)
    db.session.commit()

    question = Question(18,'Кто имеет право получить комнату в общежитии?')
    db.session.add(question)
    db.session.commit()

    question = Question(18,'Какие условия проживания в общежитии (правила, права и обязанности)?')
    db.session.add(question)
    db.session.commit()

    question = Question(18,'Какие нужны документы для заселения?')
    db.session.add(question)
    db.session.commit()

    question = Question(18,'Когда я должен подать документы для заселения?')
    db.session.add(question)
    db.session.commit()

    question = Question(18,'Могу ли я получить комнату в общежитии после поступления?')
    db.session.add(question)
    db.session.commit()

    question = Question(18,'Могу ли я выселиться из комнаты до окончания обучения?')
    db.session.add(question)
    db.session.commit()

    question = Question(18,'Сколько стоит проживание?')
    db.session.add(question)
    db.session.commit()

    question = Question(18,'Что входит в стоимость проживания? | нужно ли оплачивать коммунальные услуги?')
    db.session.add(question)
    db.session.commit()

    question = Question(18,'Как получить комнату в общежитии повышенной комфортности?')
    db.session.add(question)
    db.session.commit()

    question = Question(18,'Когда происходит заселение в общежитие?')
    db.session.add(question)
    db.session.commit()

    question = Question(18,'Могу ли я заселиться раньше/позже?')
    db.session.add(question)
    db.session.commit()

    question = Question(18,'Могут ли меня выселить из общежития? (возможно, дублирует второй вопрос)')
    db.session.add(question)
    db.session.commit()

    question = Question(18,'Смогу ли я поменять комнату/общежитие, если меня что-то будет не устраивать? (возможно, дублирует второй вопрос)')
    db.session.add(question)
    db.session.commit()


    question = Question(18,'Можно ли приводить гостей? (возможно, дублирует второй вопрос)')
    db.session.add(question)
    db.session.commit()

    question = Question(18,'Можно ли держать домашних животных? (возможно, дублирует второй вопрос)')
    db.session.add(question)
    db.session.commit()

    question = Question(18,'Могу ли я получить комнату на время ВИ?')
    db.session.add(question)
    db.session.commit()

def InitTmp():
    nat = Nationality(value ="РФ")
    db.session.add(nat)
    db.session.commit()
    nat = Nationality(value ="СНГ")
    db.session.add(nat)
    db.session.commit()
    nat = Nationality(value ="Другие")
    db.session.add(nat)
    db.session.commit()

    ed = OldEducation(value="Школа")
    db.session.add(ed)
    db.session.commit()
    ed = OldEducation(value="Колледж")
    db.session.add(ed)
    db.session.commit()
    ed = OldEducation(value="Вуз")
    db.session.add(ed)
    db.session.commit()

    lv = Direction(value = 'очная')
    db.session.add(lv)
    db.session.commit()
    lv = Direction(value = 'заочная')
    db.session.add(lv)
    db.session.commit()

    lv = Resthelth(value='Есть')
    db.session.add(lv)
    db.session.commit()
    lv = Resthelth(value='Нет')
    db.session.add(lv)
    db.session.commit()


    pr = Privileges(value='Есть')
    db.session.add(pr)
    db.session.commit()
    pr = Privileges(value='Нет')
    db.session.add(pr)
    db.session.commit()

    lv = Level(value='Бакалавриат')
    db.session.add(lv)
    db.session.commit()
    lv = Level(value='Магистртура')
    db.session.add(lv)
    db.session.commit()
    lv = Level(value='Аспирантура')
    db.session.add(lv)
    db.session.commit()
    lv = Level(value='Колледж')
    db.session.add(lv)
    db.session.commit()

def InitIncr():
    tmp = Questionincr("Последний срок подачи документов", 1)
    db.session.add(tmp)
    db.session.commit()
    tmp = Questionincr("Последний срок подачи заявления", 1)
    db.session.add(tmp)
    db.session.commit()
    tmp = Questionincr("Когда нужно подать документы", 1)
    db.session.add(tmp)
    db.session.commit()
    tmp = Questionincr("Когда подавать заявление", 1)
    db.session.add(tmp)
    db.session.commit()
    tmp = Questionincr("Когда подать документы", 1)
    db.session.add(tmp)
    db.session.commit()
    tmp = Questionincr("Когда подать заявление", 1)
    db.session.add(tmp)
    db.session.commit()


    tmp = Questionincr("Подать в электронном виде",2)
    db.session.add(tmp)
    db.session.commit()
    tmp = Questionincr("Подать в цифровом виде",2)
    db.session.add(tmp)
    db.session.commit()
    tmp = Questionincr("Подать документы в электронном виде",2)
    db.session.add(tmp)
    db.session.commit()
    tmp = Questionincr("Подать заявление в цифровом виде",2)
    db.session.add(tmp)
    db.session.commit()
    tmp = Questionincr("Подать заявление на сайте",2)
    db.session.add(tmp)
    db.session.commit()
    tmp = Questionincr("Можно подать заявление на сайте",2)
    db.session.add(tmp)
    db.session.commit()
    tmp = Questionincr("Можно подать документы на сайте",2)
    db.session.add(tmp)
    db.session.commit()

    tmp = Questionincr("Подать заявление лично",3)
    db.session.add(tmp)
    db.session.commit()
    tmp = Questionincr("Подать заявление в приемной комиссии",3)
    db.session.add(tmp)
    db.session.commit()
    tmp = Questionincr("Подать заявление в вузе",3)
    db.session.add(tmp)
    db.session.commit()
    tmp = Questionincr("Подать документы лично",3)
    db.session.add(tmp)
    db.session.commit()
    tmp = Questionincr("Подать документы в приемной комиссии",3)
    db.session.add(tmp)
    db.session.commit()
    tmp = Questionincr("Подать документы в вузе",3)
    db.session.add(tmp)
    db.session.commit()
    tmp = Questionincr("Приехать подать документы",3)
    db.session.add(tmp)
    db.session.commit()
    tmp = Questionincr("Приехать подать заявление",3)
    db.session.add(tmp)
    db.session.commit()
    tmp = Questionincr("Прийти подать документы",3)
    db.session.add(tmp)
    db.session.commit()
    tmp = Questionincr("Прийти подать заявление",3)
    db.session.add(tmp)
    db.session.commit()


    tmp = Questionincr("Подать документы по почте",4)
    db.session.add(tmp)
    db.session.commit()
    tmp = Questionincr("Подать заявление по почте",4)
    db.session.add(tmp)
    db.session.commit()
    tmp = Questionincr("Отправить документы по почте",4)
    db.session.add(tmp)
    db.session.commit()
    tmp = Questionincr("Отправить заявление по почте",4)
    db.session.add(tmp)
    db.session.commit()

    tmp = Questionincr("госуслуги",5)
    db.session.add(tmp)
    db.session.commit()
    tmp = Questionincr("gosuslugi",5)
    db.session.add(tmp)
    db.session.commit()
    tmp = Questionincr("ЕПГУ",5)
    db.session.add(tmp)
    db.session.commit()

    tmp = Questionincr("изменить направление",6)
    db.session.add(tmp)
    db.session.commit()

    tmp = Questionincr("переписать заявление",6)
    db.session.add(tmp)
    db.session.commit()

    tmp = Questionincr("внести изменения в заявление",6)
    db.session.add(tmp)
    db.session.commit()

    tmp = Questionincr("удалить направление",6)
    db.session.add(tmp)
    db.session.commit()

    tmp = Questionincr("что нужно отправить",7)
    db.session.add(tmp)
    db.session.commit()

    tmp = Questionincr("что нужно принести",7)
    db.session.add(tmp)
    db.session.commit()

    tmp = Questionincr("какие документы нужны",7)
    db.session.add(tmp)
    db.session.commit()

    tmp = Questionincr("подать заявление целевик",8)
    db.session.add(tmp)
    db.session.commit()

    tmp = Questionincr("документы целевик",8)
    db.session.add(tmp)
    db.session.commit()

    tmp = Questionincr("заявление целевик",8)
    db.session.add(tmp)
    db.session.commit()

    tmp = Questionincr("заявление олимпиада",9)
    db.session.add(tmp)
    db.session.commit()
    tmp = Questionincr("олимпиада школьников",9)
    db.session.add(tmp)
    db.session.commit()
    tmp = Questionincr("поступить без вступительных экзаменов",9)
    db.session.add(tmp)
    db.session.commit()
    tmp = Questionincr("подать документы без вступительных экзаменов",9)
    db.session.add(tmp)
    db.session.commit()
    tmp = Questionincr("заявление без вступительных испытаний",9)
    db.session.add(tmp)
    db.session.commit()

    tmp = Questionincr("заявление особая квота",10)
    db.session.add(tmp)
    db.session.commit()
    tmp = Questionincr("заявление инвалид",10)
    db.session.add(tmp)
    db.session.commit()
    tmp = Questionincr("заявление сирота",10)
    db.session.add(tmp)
    db.session.commit()
    tmp = Questionincr("документы льготник",10)
    db.session.add(tmp)
    db.session.commit()
    tmp = Questionincr("документы особая квота",10)
    db.session.add(tmp)
    db.session.commit()
    tmp = Questionincr("документы инвалид",10)
    db.session.add(tmp)
    db.session.commit()
    tmp = Questionincr("документы сирота",10)
    db.session.add(tmp)
    db.session.commit()

    tmp = Questionincr("документы иностранец",11)
    db.session.add(tmp)
    db.session.commit()

    tmp = Questionincr("заявление казахстан",11)
    db.session.add(tmp)
    db.session.commit()

    tmp = Questionincr("документы казахстан",11)
    db.session.add(tmp)
    db.session.commit()

    tmp = Questionincr("заявление гражданин иностранного государства",11)
    db.session.add(tmp)
    db.session.commit()

    tmp = Questionincr("документы гражданин иностранного государства",11)
    db.session.add(tmp)
    db.session.commit()

    tmp = Questionincr("обучение по контракту",12)
    db.session.add(tmp)
    db.session.commit()
    tmp = Questionincr("как учиться по контракту",12)
    db.session.add(tmp)
    db.session.commit()
    tmp = Questionincr("как учиться платно",12)
    db.session.add(tmp)
    db.session.commit()

    tmp = Questionincr("бланк контракта",13)
    db.session.add(tmp)
    db.session.commit()
    tmp = Questionincr("скачать договор",13)
    db.session.add(tmp)
    db.session.commit()
    tmp = Questionincr("скачать контракт",13)
    db.session.add(tmp)
    db.session.commit()

    tmp = Questionincr("до какого числа заключить договор",14)
    db.session.add(tmp)
    db.session.commit()
    tmp = Questionincr("до какого числа заключить и оплатить договор",14)
    db.session.add(tmp)
    db.session.commit()
    tmp = Questionincr("когда заключить контракт",14)
    db.session.add(tmp)
    db.session.commit()
    tmp = Questionincr("до какого числа заключить контракт",14)
    db.session.add(tmp)
    db.session.commit()
    tmp = Questionincr("до какого числа заключить и оплатить контракт",14)
    db.session.add(tmp)
    db.session.commit()

    tmp = Questionincr("как заключить договор",15)
    db.session.add(tmp)
    db.session.commit()
    tmp = Questionincr("кто заключает контракт",15)
    db.session.add(tmp)
    db.session.commit()
    tmp = Questionincr("как заключить контракт",15)
    db.session.add(tmp)
    db.session.commit()

    tmp = Questionincr("оплата договора",16)
    db.session.add(tmp)
    db.session.commit()
    tmp = Questionincr("оплата онлайн",16)
    db.session.add(tmp)
    db.session.commit()
    tmp = Questionincr("опата картой",16)
    db.session.add(tmp)
    db.session.commit()
    tmp = Questionincr("материнский капитал",16)
    db.session.add(tmp)
    db.session.commit()
    tmp = Questionincr("образовательный кредит",16)
    db.session.add(tmp)
    db.session.commit()

    tmp = Questionincr("заполнения согласия",17)
    db.session.add(tmp)
    db.session.commit()
    tmp = Questionincr("согласие личный кабинет",17)
    db.session.add(tmp)
    db.session.commit()

    tmp = Questionincr("число подачи согласия",18)
    db.session.add(tmp)
    db.session.commit()
    tmp = Questionincr("последний срок подачи согласия",18)
    db.session.add(tmp)
    db.session.commit()

    tmp = Questionincr("сколько согласий можно подать",19)
    db.session.add(tmp)
    db.session.commit()
    tmp = Questionincr("несколько согласий",19)
    db.session.add(tmp)
    db.session.commit()
    tmp = Questionincr("два согласия",19)
    db.session.add(tmp)
    db.session.commit()

    tmp = Questionincr("поменять согласие",20)
    db.session.add(tmp)
    db.session.commit()
    tmp = Questionincr("ошибся в согласии",20)
    db.session.add(tmp)
    db.session.commit()
    tmp = Questionincr("новое согласие",20)
    db.session.add(tmp)
    db.session.commit()

    tmp = Questionincr("подача согласия",21)
    db.session.add(tmp)
    db.session.commit()
    tmp = Questionincr("согласие госуслуги",21)
    db.session.add(tmp)
    db.session.commit()
    tmp = Questionincr("согласие личный кабинет",21)
    db.session.add(tmp)
    db.session.commit()
    tmp = Questionincr("прислать согласие",21)
    db.session.add(tmp)
    db.session.commit()



def InitNewAnswer():

    ans = Answer("Вам нужно зарегистрироваться на https://ciu.nstu.ru/enrollee_account/registration , перейти по ссылке полученной на адрес электронной почты, заполнить анкету, распечатать ее и приложить сканы анкеты (заявления) и всех необходимых документов")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("Прийти по адресу пр. Карла Маркса 20, корпус 2 (холл 1 этажа). Режим работы пн-пт с 10:00 до 17:00. С собой нужно иметь иметь все необходимые документы и их копии.")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("Скачать бланк заявления с сайта университета и отправить его почтой по адресу 630073, г. Новосибирск, пр. К. Маркса, 20.Однако, напоминаем Вам, что приоритетный способ подачи документов - онлайн через личный кабинет поступающего на nstu.ru либо через портал Госуслуг")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("Зарегистрироваться на портале gosuslugi.ru выбрать услугу …, и следовать инструкциям на портале. После того как ваше заявление будет рассмотрено вам придет уведомление и с портала Госуслуг и от НГТУ")
    db.session.add(ans)
    db.session.commit()


    ans = Answer("Для того, чтобы внести какие-либо измнения в заявление Вам необходимо зайти в личный кабинет поступающего и указать, что именно нужно изменить в личных сообщения приемной комиссии. Напоминаем, что если Вы подавали документы очно, то логин и пароль от вашего личного кабинета указан в расписке. ")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("Для поступления по общему конкурсу необходимо предосавтить: - документ удостверяющий личность; - документ об образовании государственного образца (аттестат, диплом СПО или ВО), СНИЛС (при наличии); - нотариально заверенные переводы иностранного документа об образовании (если вы заканчивали иностранное учебное заведение); - документы, подтверждающие индивидуальные достижения (при наличии); - заявление, заполенное в личном кабинете (в случае, если Вы подаете документы очно, заявление заполнят сотрудники приемной комиссии)")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("Для поступления в рамках целевой квоты Вам необходимо предоставить следующие докеументы: - документ удостверяющий личность; - документ об образовании государственного образца (аттестат, диплом СПО или ВО), СНИЛС (при наличии);  - документы, подтверждающие индивидуальные достижения (при наличии); - заявление, заполенное в личном кабинете (в случае, если Вы подаете документы очно, заявление заполнят сотрудники приемной комиссии); - оригинал договора о целевом обучении, либо заверенная копия договора, либо копия договора с предъявлением оригинала")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("Для поступления в пределах особой квоты Вам необходимо предосавтить: - документ удостверяющий личность; - документ об образовании государственного образца (аттестат, диплом СПО или ВО), СНИЛС (при наличии); - нотариально заверенные переводы иностаранного документа об образовании (если вы заканчивали иностранное учебное заведение); - документы, подтверждающие индивидуальные достижения (при наличии); - заявление, заполенное в личном кабинете (в случае, если Вы подаете документы очно, заявление заполнят сотрудники приемной комиссии); - документы, подтверждающие Ваше право поступать в пределах особой квоты")
    db.session.add(ans)
    db.session.commit()
    ans = Answer("Для поступления в пределах особой квоты Вам необходимо предосавтить: - документ удостверяющий личность; - документ об образовании государственного образца (аттестат, диплом СПО или ВО), СНИЛС (при наличии); - нотариально заверенные переводы иностаранного документа об образовании (если вы заканчивали иностранное учебное заведение); - документы, подтверждающие индивидуальные достижения (при наличии); - заявление, заполенное в личном кабинете (в случае, если Вы подаете документы очно, заявление заполнят сотрудники приемной комиссии); - документы, подтверждающие Ваше право поступать в пределах особой квоты")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("Для поступления по общему конкурсу необходимо предосавтить: - документ удостверяющий личность; - документ об образовании государственного образца (аттестат, диплом СПО или ВО), - нотариально заверенные переводы иностаранного документа об образовании  - заявление, заполенное в личном кабинете (в случае, если Вы подаете документы очно, заявление заполнят сотрудники приемной комиссии);")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("Для того, чтобы быть зачисленным Вам необходимо предостваить оригинал документа об образовании в приемную комиссию университета в установленные порядком приема сроки.")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("Обучение по контракту предусматривает ежесеметровую оплату обучения (https://www.nstu.ru/studies/cost_education/edu_cost). При успешном закрытии трёх сессий подряд и наличии вакантного бюджетного места, возможен перевод студента, обучающегося по контракту, на бюджет.")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("шаблон договора - https://ciu.nstu.ru/documents_pub/download?id=42304, https://ciu.nstu.ru/documents_pub/download?id=42305, https://ciu.nstu.ru/documents_pub/download?id=42306 рекомендуем скачать заполненный договор в личном кабинете")
    db.session.add(ans)
    db.session.commit()
    ans = Answer("заключить и оплатить договор нужно не позднее 10-го сентября, но вы можете сделать это сразу, подав согласие на платное обучение, еще до зачисления")
    db.session.add(ans)
    db.session.commit()
    ans = Answer("Если вам нет 18-ти лет, то договор заключается с одним из родителей, кроме того после оплаты можно получить налоговый вычет. Если вам есть 18 лет, то договор можете заключить непосредственно Вы. Также может быть заключен трехсторонний договор с предприятием. Договор можно заключить из личного кабинета. ")
    db.session.add(ans)
    db.session.commit()
    ans = Answer("Оплатить можно - из личного кабинета картой, банковским переводом, в отделении банка Левобережный в  1-м корпусе НГТУ. Также есть программы образовательных кредитов и оплата материнским капиталом")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("согласие подается из личного кабинета в разделе согласие")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("согласие на целевые места, без вступительных испытаний, особую квоту нужно подать не позднее 18-00 28 июля. По общему конкурсу - не позднее 18-00 3 августа (время новосибирское). Согласие подается через личный кабинет. Обращаем Ваше внимание, что для того, чтобы быть зачисленным необходимо в те же сроки предоставить в приемную комиссию оригинал докумнета об образовании.")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("одновременно можно подать одно согласие (на одну конкурсную группу) на бюджетные места и одно на платные места ( возможно на ту же самую конкурсную группу)")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("Да можно подавать новое согласие. которое заменит текущее. Сделать это можно из личного кабинета. ")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("Если заявление подано в НГТУ (лично или в личном кабинете), то согласие можно подать в личном кабинете, выбрав конкурсную группу и прикрепив скан. Если заявление подано на портале госуслуг, то согласие можно подать только на госуслугах. Согласие на платные места можно подать только через личный кабинет НГТУ")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("20 июня 2021г.")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("11 июля — завершение приема документов, необходимых для поступления, от лиц, поступающих на обучение по результатам вступительных испытаний, проводимых университетом самостоятельно; 28 июля — завершение приема документов, необходимых для поступления, от лиц, поступающих на обучение по результатам единого государственного экзамена (ЕГЭ), а также без прохождения вступительных испытаний.")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("До 11 июля лицам, поступающим на обучения по результатам ВИ, проводимых ВУЗом; до 28 июля поступающим по материалам ЕГЭ или поступающим БВИ")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("28 июля — завершение приема заявлений о согласии и оригиналов документа об образовании на зачисление от поступающих в пределах особой квоты, целевой квоты и БВИ; 3 августа — завершение приема заявлений о согласии на зачисление и оригиналов документа об образовании на основные конкурсные места;")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("до 21 августа")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("28 июля — завершение приема заявлений о согласии и оригиналов документа об образовании на зачисление от поступающих в пределах особой квоты, целевой квоты и БВИ; 3 августа — завершение приема заявлений о согласии на зачисление и оригиналов документа об образовании на основные конкурсные места;")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("30 июля — издание приказов о зачислении лиц, поступающих без вступительных испытаний, поступающих на места в пределах квот; 9 августа — издание приказов о зачислении лиц, подавших заявление о согласии на зачисление на основные конкурсные места до заполнения 100% основных конкурсных мест; ")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("Основной этап: 1—25 июля; 9—19 августа (заочное и контарктное обучение)")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("Результаты экзаменов становятся известны сразу, после прохождения тестирования.")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("Запись на вступительные экзамены проводится через личный кабинет потсупающего на сайте университета. Сдающий выбирает удобное для себя время и дату сдачи.")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("Заявление на аппеляцию отправляется в течении одного часа с момента завершения тестирования")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("30 июля — издание приказов о зачислении лиц, поступающих без вступительных испытаний, поступающих на места в пределах квот; 9 августа — издание приказов о зачислении лиц, подавших заявление о согласии на зачисление на основные конкурсные места до заполнения 100% основных конкурсных мест")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("30 июля - Издание приказа о зачислении лиц, поступающих на контрактные места на направления, где ОТСУТСВУЮТ бюджетные места; 9 августа - Издание приказа о зачислении лиц, поступающих на контрактные места и подавших документы до 25 июля 2022г.; ")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("30 июля")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("В момент подачи документов в личном кабинете поступающего необходимо оставить отметку о том, что Вы нуждаетесь в общежитии. Далее, в случае вашего поступления, Вам придет уведовление о дате и порядке заселения.")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("Заселение в общежитие производится в конце августа. На электронную почту, указанную Вами при регистрации, придет оповещение с рекомендуемой датой заезда.")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("Вы можете заселиться не в дату заезда, однако, лучше заранее предупредить об этом дирекцию студ.городка")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("Право на прием на обучение в пределах особой квоты имеют дети-инвалиды, инвалиды I и II групп, инвалиды с детства, инвалиды вследствие военной травмы или заболевания, полученных в период прохождения военной службы, дети-сироты и дети, оставшиеся без попечения родителей, а также лица из числа детей-сирот и детей, оставшихся без попечения родителей и ветераны боевых действий из числа лиц, указанных в подпунктах 1-4 пункта 1 статьи 3 Федерального закона от 12 января 1995 г. № 5-ФЗ «О ветеранах». Право поступления БВИ имеют победители и призеры заключительного этапа всероссийской олимпиады школьников, члены сборных команд Российской Федерации, участвовавшие в международных олимпиадах по общеобразовательным предметам")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("Для поступления в пределах особых квот необходимо дополнительно к общему списку документов прикрепить докумнеты, подтверждающие наличии у абитуриента право на поступления в рамках данной категории.")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("до 28 июля")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("Да, если вы относитесь к категории инвалиды, в том числе дети-инвалиды")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("Для поступления по льготе Вам необходимо набрать минимальные баллы, устанволенные университетом самостоятельно. При этом в пределах особой квоты установленно ограниченное число мест, и набор минимальных баллов не может гарантировать Вам поступление на бюджет, если число таких абитуриентов будет превышать размер квоты. В этом случае поступление происходить на конкрусной (рейтинговой) основе в пределах квоты.")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("30 июля")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("При поступлении в НГТУ реализуется инклюизивное сопровождение. Заявку на сопровждение вы можете оставить в личном кабинете поступающего, либо обратиться по телефону 8-383-315-38-30")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("Поступление в пределах особой квоты действует на все направления, где есть бюджетные места.")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("Вы можете принять участие в конкурсе сразу на несколько направлений в пределах особой квоты, однако, восопользоваться своим правом сможете только на одно из них, написав соответвующее согласие.")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("Победители и призеры заключительного этапа всероссийской олимпиады школьников (далее – всероссийская олимпиада), членам сборных команд Российской Федерации, участвовавших в международных олимпиадах по общеобразовательным предметам и сформированных в порядке, установленном федеральным органом исполнительной власти, осуществляющим функции по выработке и реализации государственной политики и нормативно-правовому регулированию в сфере общего образования (далее – члены сборных команд, участвовавших в международных олимпиадах) предоставляется право на прием без вступительных испытаний в соответствии с частью 4 статьи 71 Федерального закона № 273-ФЗ.Победители и призеры олимпиад школьников, проводимых в порядке, устанавливаемом федеральным органом исполнительной власти, осуществляющим функции по выработке государственной политики и нормативно-правовому регулированию в сфере высшего образования, по согласованию с федеральным органом исполнительной власти, осуществляющим функции по выработке и реализации государственной политики и нормативно-правовому регулированию в сфере общего образования, предоставляются особые права в соответствии с частью 12 статьи 71 Федерального закона № 273-ФЗ – право на прием без вступительных испытаний по результатам олимпиад школьников.")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("до 28 июля")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("Необходимо дополнтельно к основным документам предоставить скан диплома олимпиады.")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("Да, необходимо иметь результаты ЕГЭ, либо результаты ВИ, проводимых ВУЗом самостоятельно. Они должны быть больше минимального балла,установленного университетом, кроме того при поступлении БВИ по результатам олимпиады школьников необходимо иметь не менее 75 баллов по соответвующему предмету.")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("Да.")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("30 июля")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("Данное право действует только в одну организацию высшего образования только на одну образовательную программу по выбору поступающего (вне зависимости от количества оснований, обусловливающих указанное право).")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("Целевое обучение — система подготовки специалистов для  предприятий и организаций, когда на основании имеющегося у абитуриента договора о целевом обучении с государственной организацией он может быть зачислен на бюджетное место в пределах квоты целевого приема, не участвуя в общем конкурсе. При этом после окончания обучения этот студент должен будет отработать на заключившем с ним договор предприятии не менее 3-х лет.")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("Договор на целевое обучение может быть заключен с одним из следующих предприятий (организаций):•	Федеральные государственные органы, органы государственной власти субъектов Российской Федерации, органы местного самоуправления •	Государственные и муниципальные учреждения, унитарные предприятия •	Государственные корпорации •	Государственные компании •	Организации, включенные в сводный реестр организаций оборонно-промышленного комплекса, формируемый в соответствии с частью 2 статьи 21 Федерального закона от 31 декабря 2014 года № 488-ФЗ «О промышленной политике в Российской Федерации» •	Хозяйственные общества, в уставном капитале которых присутствует доля Российской Федерации, субъекта Российской Федерации или муниципального образования •	Акционерные общества, акции которых находятся в собственности или в доверительном управлении государственной корпорации •	Дочерние хозяйственные общества организаций, указанных в пунктах 4, 6 и 7 •	Организации, которые созданы государственными корпорациями или переданы государственным корпорациям в соответствии с положениями федеральных законов об указанных корпорациях")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("Шаблон договора на целевое обучение можно взять по адресу https://nstu.ru/entrance/committee/targeted_training  «Типовая форма договора о целевом обучении по образовательной программе среднего профессионального и высшего образования»")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("Алгоритм заключения договора на целевое обучение находится по адресу https://nstu.ru/entrance/committee/targeted_training в разделе «Памятка абитуриенту».")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("Для поступления в рамках особой квоты по целевому приему Вам необходимо предоставить следующие докеументы: - документ удостверяющий личность; - документ об образовании государственного образца (аттестат, диплом СПО или ВО), СНИЛС (при наличии);  - документы, подтверждающие индивидуальные достижения (при наличии); - заявление, заполенное в личном кабинете (в случае, если Вы подаете документы очно, заявление заполнят сотрудники приемной комиссии); - оригинал договора о целевом обучении, либо заверенная копия договора, либо копия договора с предъявлением оригинала")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("Документы для поступления на целевое обучение необходимо подать в следующие сроки:- при поступлении на бакалавриат или специалитет – до 28июля 2021 г.")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("Зачисление абитуриентов, поступающих в рамках квоты целевого приема, состоится 30 июля")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("Полный перечень индивидуальных достижений доступен по ссылке https://nstu.ru/entrance/committee/prilogenie5  ")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("максимальное количесвто баллов - 10")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("до 28 июля")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("Сканы данных документов, необходимо прикреить в личном кабинете поступающего")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("Баллы начисляются за индивидуальные достижения,полученные абитуриентом в период обучения 10-11 классах (результаты, полученные в качестве индивидуальных достижений действительны в течении четырех лет с момента их получения). Баллы за знак ГТО: если поступающий награжден знаком ГТО за выполнение нормативов Комплекса ГТО, установленных для возрастной группы населения Российской Федерации, к которой поступающий относится (относился) в текущем году и (или) в предшествующем году")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("С полным перченем направлений НГТУ вы можете ознакомиться по ссылке https://xn--c1atqe.xn--p1ai/entrance/entrance_all/bachelor")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("На 4 направления")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("Необходимо написать соответвующую просьба в сообщения для приемной комиссии через личный кабинет поступающего, либо обратиться в приемную комиссию лично")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("В процессе обучения возможен перевод на другую специальность или фаукльтет при наличии свободных бюджетных или контрактных мест, успешной сдачи сессии и закрытия акеадемичской разницы между дисциплинами,е сли такая есть")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("Перевод с контрактного обучения на бюджетное возможен при наличии свободных бюджетных мест, а также упешной сдачи двух сессий подряд")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("До 11 июля, если вы поступаете по ВИ, проводимыми университетом самостоятельно, и до 28 июля, если вы поступаете по результатам ЕГЭ")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("План набора достепн по ссылке https://xn--c1atqe.xn--p1ai/entrance/entrance_all/bachelor")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("Актуальная стоимость обучения доступна по ссылке https://www.nstu.ru/studies/cost_education/edu_cost")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("Перчень необходимых экзаменов для поступления на различные направления НГТУ доступен по ссылке https://xn--c1atqe.xn--p1ai/entrance/entrance_all/bachelor")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("https://xn--c1atqe.xn--p1ai/entrance/committee/search_direction")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("Для лиц, поступающих на базе среднего общего образования приняты слебующие минимальные баллы ЕГЭ и ВИ:Русский язык 40Математика (профильный уровень) 39Информатика и ИКТ 44Физика 39Химия 39Биология 39География 40Обществознание 45Литература 40История 35Иностранный язык 30")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("Перчень необходимых экзаменов для поступления на различные направления НГТУ доступен по ссылке https://xn--c1atqe.xn--p1ai/entrance/entrance_all/bachelor")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("С 2018 (включительно) по 2021")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("По всем вопросам сдачи ЕГЭ Вы можете обратиться в Новосибирский институт мониторинга и развития образования по тел. 8-383-347-45-72")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("Школьники")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("Нет, данные подгружаются из федеральной базы автоматически")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("Нет, однако если вы входите в категорию лиц, имеющих право сдавать ВИ по материалам ВУЗа, то вы можете сдать и их, после чего выбрать наилучший результат")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("- инвалиды (в том числе, дети-инвалиды);- иностранные граждане;- лица, получившие документ об образовании в иностранной организации;- лица поступающие на обучение на базе среднего профессионального или высшего образования")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("В личном кабиенте поступающего, либо при личном образении в приемную комиссию")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("До 11 июля 2022г.")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("Сдача ВИ проводится преимущесвенно в дистанционном формате, однако, возможна и очная сдача ВИ в помещениях университета")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("Сдача ВИ првоодится преимущесвенно в дистанционном формате с использованием системы прокторинга. Это онлайн тестирование при наблюдении порктором процесса написания экзамена сдающими с использованием веб-камеры и микрофона. Возможна и очная сдача ВИ в помещениях университета")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("С 11 июля по 28 июля. Расписание доступно по ссылке https://www.nstu.ru/entrance/entrance_all/schedule")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("Аппеляция подается в течении часа после завершения ВИ. Абитуриентом заполняется бланк с указанием спорных номеров вопросов и комментариями. Скан такого заявления отправляется на почту exams2021@corp.nstu.ru . В теме письма указывается Фамилия И.О. Предмет Дата экзамена. Далее аппеляция рассматривается аппеляционной комисией. Начисление дополнительных баллов, присуждаемых по итогу аппеляции происодит автоматически, без  отправкиответных писем абитуриенту.")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("Сиситема прокторинга подразумевает собой написание онлайн тестирования, на протяжении которого за сдающим наблюдает специалист проктор посредством веб-камеры и микрофона.  Он следит за тем, чтобы сдающий не пользовался посторонними материалами, и находился один в помещении")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("Да, при наличии подключения к интернету, веб-камеры и микрофона.")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("Результаты ВИ известны сразу после окончания тестирования.")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("Пробные ВИ доступны по ссылке https://dispace.edu.nstu.ru/didesk/course/show/8140/tests")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("В НГТУ-НЭТИ создан специальный центр инклюзивного сопровождения с информацией о работе которого вы можете ознакомиться по ссылке https://www.nstu.ru/studies/study/ZIS")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("В связи с эпидемиалогической ситуацией свободное предоставление комнат общежития на время сдачи ВИ ограничено. За дополнительной иформацией необходимо обратиться лично к проректору по учебной работе.")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("Для лиц, поступающих на базе среднего общего образования приняты слебующие минимальные баллы ЕГЭ и ВИ:Русский язык 40Математика (профильный уровень) 39Информатика и ИКТ 44Физика 39Химия 39Биология 39География 40Обществознание 45Литература 40История 35Иностранный язык 30")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("Минимальные баллы для поступленияна контракт определяется отдельно каждым факультетом. Обратитесь в деканат интереующего вас факультета.")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("https://www.nstu.ru/entrance/committee/search_direction")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("Для оценки своих шансов поступления на бюджет Вам стоит посмотреть рейтинговый список интересующего Вас направления. Выбрать Просмотреть рейтинговый список только по поданным согласиям на текущий момент.  Если ваш номер в этом рейтинге меньше либор авен общему количеству бюджетных мест на данное направления, то на данный момент вы проходите. Обратите внимание, что ситуация может постоянно меняться вплоть до 18:00 3 августа.")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("Минимальные баллы для поступленияна контракт определяется отдельно каждым факультетом. Обратитесь в деканат интереующего вас факультета.")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("Рейтинговые списки доступны по ссылке https://www.nstu.ru/entrance/admission_campaign/entrance")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("Проходные баллы 2021 года доступны по ссылке https://www.nstu.ru/entrance/committee/completition2020")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("Общее количество бюджетных мест на направлении вы можете найти в таблице по ссылке (предварительно выбрав интересующий вас факультет) https://xn--c1atqe.xn--p1ai/entrance/entrance_all/bachelor")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("Приказы на зачисления публикуются на официальном сайте университета nstu.ru")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("30 июля — издание приказов о зачислении лиц, поступающих без вступительных испытаний, поступающих на места в пределах квот; 9 августа — издание приказов о зачислении лиц, подавших заявление о согласии на зачисление на основные конкурсные места до заполнения 100% основных конкурсных мест; ")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("Если вы не проходите на бюджет, вы можете оформить в личном кабинете абитуриента согласие на контракт и заключить договор на обучение.")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("Места в общежитии распределяют деканаты в рамках установленных квот.")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("С правилами, правами  и обязанностями проживающих в общежитии можно ознакомиться по ссылке https://www.nstu.ru/campus/hostel")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("Для заселения в общежитие нужен паспорт,2 фото 3х4,папка-файл ")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("Документы на заселение нужно  «подать» в момент заселения. А отметку о необходимости получения места в общежитии ставят в приемной комиссии в момент подачи документов.")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("Получить  место в общежитии можно и после поступления, но только с разрешения деканата")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("Из общежития можно выселиться до конца обучения  написав заявление о выселении   заведующему общежитием")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("С 1.07.2021 стоимость проживания для контрактных студентов составляет - 853 руб. в месяц, для бюджетных - 547 руб. в месяц. Коммунальные услуги оплачивать отдельно не нужно.")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("нет ответа")
    db.session.add(ans)
    db.session.commit()

    ans = Answer(".Место в общежитии повышенной комфортности можно получить, обратившись к сотруднику Международной службы Короткову Владимиру Владимировичу vladimir.korotkov@inter.nstu.ru .")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("Заселение в общежитие в 2021 году будет проходить с23 по 31 августа")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("Раньше 23.08.2021 заселиться нельзя, позже – 3можно.")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("Да, могут, за нарушение правил проживания")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("Комнату поменять можно, если  по новому месту проживания будут свободные места.")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("Приводить гостей можно после того, как будут сняты антиковидные ограничения.")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("Категорически запрещено содержание домашних животных")
    db.session.add(ans)
    db.session.commit()

    ans = Answer("В связи с эпидемиалогической ситуацией свободное предоставление комнат общежития на время сдачи ВИ ограничено. За дополнительной иформацией необходимо обратиться лично к проректору по учебной работе.")
    db.session.add(ans)
    db.session.commit()




    cntr = ControllerAnswer(questionid=1,answerid=1)
    db.session.add(cntr)
    db.session.commit()
    cntr = ControllerAnswer(questionid=2,answerid=2)
    db.session.add(cntr)
    db.session.commit()
    cntr = ControllerAnswer(questionid=3,answerid=3)
    db.session.add(cntr)
    db.session.commit()
    cntr = ControllerAnswer(questionid=4,answerid=4)
    db.session.add(cntr)
    db.session.commit()
    cntr = ControllerAnswer(questionid=5,answerid=5)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=6,answerid=6)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=7,answerid=7)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=8,answerid=8)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=9,answerid=9)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=10,answerid=10)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=11,answerid=11)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=12,answerid=12)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=13,answerid=13)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=14,answerid=14)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=15,answerid=15)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=16,answerid=16)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=17,answerid=17)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=18,answerid=18)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=19,answerid=19)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=20,answerid=20)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=21,answerid=21)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=22,answerid=22)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=23,answerid=23)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=24,answerid=24)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=25,answerid=25)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=26,answerid=26)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=27,answerid=27)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=28,answerid=28)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=29,answerid=29)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=30,answerid=30)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=31,answerid=31)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=32,answerid=32)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=33,answerid=33)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=34,answerid=34)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=35,answerid=35)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=36,answerid=36)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=37,answerid=37)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=38,answerid=38)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=39,answerid=39)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=40,answerid=40)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=41,answerid=41)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=42,answerid=42)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=43,answerid=43)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=44,answerid=44)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=45,answerid=45)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=46,answerid=46)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=47,answerid=47)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=48,answerid=48)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=49,answerid=49)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=50,answerid=50)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=51,answerid=51)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=52,answerid=52)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=53,answerid=53)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=54,answerid=54)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=55,answerid=55)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=56,answerid=56)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=57,answerid=57)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=58,answerid=58)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=59,answerid=59)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=60,answerid=60)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=61,answerid=61)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=62,answerid=62)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=63,answerid=63)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=64,answerid=64)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=65,answerid=65)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=66,answerid=66)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=67,answerid=67)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=68,answerid=68)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=69,answerid=69)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=70,answerid=70)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=71,answerid=71)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=72,answerid=72)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=73,answerid=73)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=74,answerid=74)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=75,answerid=75)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=76,answerid=76)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=77,answerid=77)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=78,answerid=78)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=79,answerid=79)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=80,answerid=80)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=81,answerid=81)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=82,answerid=82)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=83,answerid=83)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=84,answerid=84)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=85,answerid=85)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=86,answerid=86)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=87,answerid=87)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=88,answerid=88)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=89,answerid=89)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=90,answerid=90)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=91,answerid=91)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=92,answerid=92)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=93,answerid=93)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=94,answerid=94)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=95,answerid=95)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=96,answerid=96)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=97,answerid=97)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=98,answerid=98)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=99,answerid=99)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=100,answerid=100)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=101,answerid=101)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=102,answerid=102)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=103,answerid=103)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=104,answerid=104)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=105,answerid=105)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=95,answerid=95)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=106,answerid=106)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=107,answerid=107)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=108,answerid=108)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=109,answerid=109)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=110,answerid=110)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=111,answerid=111)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=112,answerid=112)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=113,answerid=113)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=114,answerid=114)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=115,answerid=115)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=116,answerid=116)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=117,answerid=117)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=118,answerid=118)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=119,answerid=119)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=120,answerid=120)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=121,answerid=121)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=122,answerid=122)
    db.session.add(cntr)
    db.session.commit()

    cntr = ControllerAnswer(questionid=123,answerid=123)
    db.session.add(cntr)
    db.session.commit()


@app.route('/')
def index():
    InitTopic()
    InitSubtopic()
    InitQuestion()
    InitTmp()
    InitIncr()
    InitNewAnswer()
    return ("Hello world!")

@app.route('/setIncr')
def setIncr():
    try:
        json = request.json
        print(json['value'], file = sys.stderr)
        print(json['questionId'], file=sys.stderr)
        incr = Questionincr(json['value'], json['questionId'])
        db.session.add(incr)
        db.session.commit()
        return jsonify(ok=200)
    except:
        return jsonify(error=400)

@app.route('/getTopics')
def getTopics():
    try:
        data = Topic.query.all()
        #topics = []
        key = 0
        # = [{"a": 1, "b":2},{"a": 4, "b":2}]
        rad =[]
        for el in data:
            tmp = {"id": el.id, "value": el.value}
            rad.append(tmp)
        return jsonify(rad)
    except:
        return jsonify(error=401)

@app.route('/getTopic/<int:id>')
def getTopic(id):
    try:
        data = Topic.query.get(id)

        return jsonify(
            id = data.id,
            value = data.value,
        )
    except:
        return jsonify(error=401)


@app.route('/setTopic')
def setTopic():
    try:
        json = request.json
        print(json, file=sys.stderr)
        topic = Topic(json['value'])
        db.session.add(topic)
        db.session.commit()
        return jsonify(ok=200)
    except:
        return jsonify(error=401)


@app.route('/getSubtopics')
def getSubtopics():
    #data = Subtopic.query \
            #.join(Topic, Topic.id == Subtopic.topicid, ) \
            #.all()
    try:
        result = db.session.query(Topic, Subtopic).filter(Topic.id == Subtopic.id).all()
        print(result[0].Topic.value, file=sys.stderr)
        rad =[]
        for el in result:
            tmp = {"id": el.Subtopic.id, "topic":el.Topic.value, "value": el.Subtopic.value}
            rad.append(tmp)
        return jsonify(rad)
    except:
        return jsonify(error=401)


@app.route('/getSubtopicOnTopic/<int:id>')
def getSubtopicOnTopic(id):
    try:
        #data = Subtopic.query(Subtopic).filter(Topic.id == Subtopic.id).get(id)
        result = db.session.query(Topic, Subtopic).filter((Subtopic.topicid == id) & (Topic.id == Subtopic.topicid)).all()
        print(result, file=sys.stderr)

        rad =[]
        for el in result:
            tmp = {"id": el.Subtopic.id, "topic":el.Topic.value, "value": el.Subtopic.value}
            rad.append(tmp)
        return jsonify(rad)

    except:
        return jsonify(error='401')


@app.route('/getQuestionOnSubtopic/<int:id>')
def getQuestionOnSubtopic(id):
    try:
        #rez = db.session.query(Subtopic, Question).filter((Subtopic.id == id) & (Subtopic.id == Question.subtopicid)).all()
        rez = db.session.query(Question,Subtopic).filter((Subtopic.id== id) & (Question.subtopicid == Subtopic.id))
        print(rez, file=sys.stderr)
        result = []
        for el in rez:
            tmp = {"id": el.Question.id, "subtopic": el.Subtopic.value, "question": el.Question.value}
            result.append(tmp)


        return jsonify(result)

    except:
        return jsonify(error='401')


@app.route('/getAnswerOnQuestion/<int:id>')
def getAnswerOnQuestion(id):
    try:
        rezQ = db.session.query(Question).filter(Question.id == id).all()
        print(rezQ, file=sys.stderr)
        rez = db.session.query(ControllerAnswer, Answer, Question).filter((ControllerAnswer.questionid == id)& \
                            (Answer.id == ControllerAnswer.answerid) &\
                            (Question.id == ControllerAnswer.questionid)).all()



        rad = []
        for el in rez:
            tmp = {"id": el.Answer.id, "question": el.Question.value, "answer":el.Answer.value}
            rad.append(tmp)
        return jsonify(rad)
    except:
        return jsonify(error='401')


@app.route('/getSubtopic/<int:id>')
def getSubtopic(id):
    try:
        #data = Subtopic.query(Subtopic).filter(Topic.id == Subtopic.id).get(id)
        result = db.session.query(Topic, Subtopic).filter((Topic.id == Subtopic.id) & (Topic.id == id)).all()
        print(result, file=sys.stderr)

        rad =[]
        for el in result:
            tmp = {"id": el.Subtopic.id, "topic":el.Topic.value, "value": el.Subtopic.value}
            rad.append(tmp)
        return jsonify(rad)
        #return jsonify(
            #id = data.id,
            #topicid = data.topicid,
            #value = data.value
        #)
    except:
        return jsonify(error='401')


@app.route('/setSubtopic')
def setSubtopic():
    try:
        json = request.json
        print(json, file=sys.stderr)
        value = json['topic']
        topicid = Topic.query.filter(Topic.value == value).all()
        newSub = Subtopic(topicid[0].id, json['value'])
        print(topicid[0].id, file=sys.stderr)
        print(newSub, file=sys.stderr)
        db.session.add(newSub)
        db.session.commit()
        return jsonify(ok=200)
    except:
        return jsonify(eroor=401)


@app.route('/getQuestionsOnSubtopic')
def getQuestionsOnSubtopic():
    try:
        json = request.json
        value = json['Subtopic']
        rez = db.session.query(Subtopic, Question).filter((Subtopic.value == value) & (Subtopic.id == Question.subtopicid)).all()
        print(rez, file=sys.stderr)
        result = []
        for el in rez:
            tmp = {"id": el.Question.id, "subtopic": el.Subtopic.value, "question": el.Question.value}
            result.append(tmp)


        return jsonify(result)
    except:
        return jsonify(eroor=401)

@app.route('/setQuestion')
def setQuestion():
    try:
        #Получение данных из запроса
        json = request.json
        subtopicV = json['subtopic']
        subtopicA = json['answer']
        subtopicQ = json['question']

        #Добавление ответа в БД
        answer = Answer(subtopicA)
        db.session.add(answer)
        db.session.commit()

        #Добавление ответа в БД
        sub = Subtopic.query.filter(Subtopic.value == subtopicV).all()
        anws = Answer.query.filter(Answer.value == subtopicA).all()
        print(sub, file=sys.stderr)
        print(anws, file=sys.stderr)
        que = Question(sub[0].id, anws[0].id, subtopicQ)
        db.session.add(que)
        db.session.commit()


        return jsonify(ok=200)
    except:
        return jsonify(error=401)


@app.route('/getAnswer')
def getAnswer():
    try:
        json = request.json
        que = json['question']
        params = getData(json['token'])
        #params = {'nationality':1,'oldeducation':3,'direction':1, 'level':2}
        print(params, file=sys.stderr)


        question = db.session.query(Question).filter(Question.value == que).all()
        print("DJIKB", file=sys.stderr)
        print(len(question), file=sys.stderr)

        if len(question)==0:
            print("Вошли", file=sys.stderr)
            question = db.session.query(Questionincr).filter(Questionincr.value == que).all()
            if len(question)==0:
                print("Вошли2", file=sys.stderr)
                return jsonify(msg='Такого вопроса нет')

            questionId = question[0].questionid
        else:
            questionId = question[0].id
        print("asdasda", file=sys.stderr)

        #print(question, file=sys.stderr)


        #print(questionId, file=sys.stderr)
        query = db.session.query(ControllerAnswer, Answer, Nationality, Direction, OldEducation, Level, Privileges, Resthelth)

        query = db.session.query(ControllerAnswer, Answer   )

        for attr,value in params.items():
            print(attr, file=sys.stderr)

            query = query.filter(((getattr(ControllerAnswer,attr)==value) & (getattr(ControllerAnswer,attr)!=None))|(getattr(ControllerAnswer,attr)==None))
            print(query)
        print("Добавили аттрибуты", file = sys.stderr)
        '''
        data = query.filter((Nationality.id == ControllerAnswer.Nationality | ControllerAnswer.Nationality == None))\
            .filter((Direction.id == ControllerAnswer.Direction | ControllerAnswer.Direction == None))\
            .filter((OldEducation.id == ControllerAnswer.OldEducation | ControllerAnswer.OldEducation == None))\
            .filter((Level.id == ControllerAnswer.Level | ControllerAnswer.Level == None))\
            .filter((Privileges.id == ControllerAnswer.Privileges | ControllerAnswer.Privileges == None))\
            .filter((Resthelth.id == ControllerAnswer.Resthelth | ControllerAnswer.Resthelth == None))\
            .filter(ControllerAnswer.questionid==questionId)\
            .filter(ControllerAnswer.answerid == Answer.id).all()
            
        '''
        data = query.filter(ControllerAnswer.questionid==questionId)\
            .filter(ControllerAnswer.answerid == Answer.id).all()

        print("Выполнили запрос", file = sys.stderr)
        print(data, file=sys.stderr)

        #data = query.filter(ControllerAnswer.answerid == Answer.id).filter(ControllerAnswer.questionid==questionId).all()
        res = []
        print("DATA", file=sys.stderr)
        print(data, file=sys.stderr)
        for el in data:
            tmp = {"id": el.ControllerAnswer.id,  "answer": el.Answer.value}
            res.append(tmp)

        return jsonify(res)
        #else:
           # return jsonify(msg = 'Ответа нет')
    except:
        return jsonify(error=401)

if __name__ == '__main__':
   app.run()
