import sys
import typing
from config.config import DevelopementConfig
from flask import Flask, jsonify, request
#from data.Dbclasses import *
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.debug = True
#app.config.from_object(DevelopementConfig)

app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql+psycopg2://postgres:pass@localhost/my_db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SQLALCHEMY_ECHO'] = True



db = SQLAlchemy(app)



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
        return self._repr(id=self.id, subtopicid=self.subtopicid, answerid=self.answerid, value=self.value)


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
    '''
    question = Question(2,7,'Какие документы нужны для поступления по общему конкурсу?')
    db.session.add(question)
    db.session.commit()

    question = Question(2,8,'Какие документы нужны для целевого приема?')
    db.session.add(question)
    db.session.commit()

    question = Question(2,9,'Какие документы нужны для приема без экзаменов?')
    db.session.add(question)
    db.session.commit()

    question = Question(2,10,'Какие документы нужны для приема вне конкурса (особая квота)?')
    db.session.add(question)
    db.session.commit()

    question = Question(2,11,'Какие документы нужны иностранным гражданам?')
    db.session.add(question)
    db.session.commit()

    question = Question(2,12,'Нужны ли оригиналы?')
    db.session.add(question)
    db.session.commit()

    question = Question(3,13,'Что такое обучение по контракту?')
    db.session.add(question)
    db.session.commit()

    question = Question(3,14,'Где можно взять шаблон договора?')
    db.session.add(question)
    db.session.commit()

    question = Question(3,15,'До какого числа нужно заключить договор?')
    db.session.add(question)
    db.session.commit()

    question = Question(3,16,'Кто и как заключает договор? ')
    db.session.add(question)
    db.session.commit()

    question = Question(3,17,'Как можно оплатить (мат. Капитал, оплата онлайн, образовательный кредит)?')
    db.session.add(question)
    db.session.commit()

    question = Question(4,18,'Где можно взять шаблон согласия?')
    db.session.add(question)
    db.session.commit()

    question = Question(4,19,'До какого числа нужно подать согласие?')
    db.session.add(question)
    db.session.commit()

    question = Question(4,20,'Сколько согласий одновременно можно подать?')
    db.session.add(question)
    db.session.commit()

    question = Question(4,21,'Можно ли менять поданное согласие?')
    db.session.add(question)
    db.session.commit()

    question = Question(4,22,'Как подать согласие?')
    db.session.add(question)
    db.session.commit()


    question = Question(5,23,'Когда начинается прием документов?')
    db.session.add(question)
    db.session.commit()

    question = Question(5,24,'Когда заканчивается прием документов?')
    db.session.add(question)
    db.session.commit()

    question = Question(5,25,'До какого числа можно вносить изменения в заявление?')
    db.session.add(question)
    db.session.commit()

    question = Question(5,26,'До какого числа необходимо подать согласие?')
    db.session.add(question)
    db.session.commit()

    question = Question(5,27,'До какого числа можно заключить договор на контрактное обучение?')
    db.session.add(question)
    db.session.commit()

    question = Question(5,28,'До какого числа необходимо предоставить оригиналы?')
    db.session.add(question)
    db.session.commit()

    question = Question(5,29,'Когда публикуются приказы о зачислении?')
    db.session.add(question)
    db.session.commit()

    question = Question(6,30,'Когда проводятся вступительные испытания по материалам ВУЗа?')
    db.session.add(question)
    db.session.commit()

    question = Question(6,31,'Когда станут известны результаты экзаменов?')
    db.session.add(question)
    db.session.commit()

    question = Question(6,32,'Как найти расписание вступительных испытаний?')
    db.session.add(question)
    db.session.commit()

    question = Question(6,33,'Когда проводится апелляция?')
    db.session.add(question)
    db.session.commit()

    question = Question(7,34,'Когда публикуются приказы о зачислении на бюджетные места?')
    db.session.add(question)
    db.session.commit()

    question = Question(7,35,'Когда публикуются приказы о зачислении на контрактные места?')
    db.session.add(question)
    db.session.commit()

    question = Question(7,36,'Когда публикуются приказы о зачислении на места в пределах особой квоты?')
    db.session.add(question)
    db.session.commit()

    question = Question(8,37,'Когда нужно подать документы на заселение?')
    db.session.add(question)
    db.session.commit()

    question = Question(8,38,'Когда будет заселение в общежитие?')
    db.session.add(question)
    db.session.commit()

    question = Question(8,39,'Могу ли я заселиться раньше/позже?')
    db.session.add(question)
    db.session.commit()

    question = Question(9,40,'Какие «льготы» установлены правилами приема?')
    db.session.add(question)
    db.session.commit()

    question = Question(9,41,'Какие документы подавать при поступлении по «льготе»?')
    db.session.add(question)
    db.session.commit()

    question = Question(9,42,'До какого числа необходимо подать документы «по льготе»?')
    db.session.add(question)
    db.session.commit()

    question = Question(9,43,'Можно ли сдавать вступительные испытания по материалам ВУЗа, если я поступаю по «льготе»?')
    db.session.add(question)
    db.session.commit()

    question = Question(9,44,'Какие минимальные баллы ЕГЭ нужны при поступлении «по льготе»?')
    db.session.add(question)
    db.session.commit()

    question = Question(9,45,'Когда издается приказ о зачислении «по льготе»?')
    db.session.add(question)
    db.session.commit()

    question = Question(9,46,'Есть ли инклюзивное сопровождение при поступлении в НГТУ?')
    db.session.add(question)
    db.session.commit()

    question = Question(9,47,'На какие направления действует «льготное право поступление»? (возможно, дублирует следующий вопрос)')
    db.session.add(question)
    db.session.commit()

    question = Question(9,48,'На сколько направлений действует «льготное право поступление»?')
    db.session.add(question)
    db.session.commit()

    question = Question(10,49,'Кто может поступать «без вступительных испытаний»?')
    db.session.add(question)
    db.session.commit()

    question = Question(10,50,'До какого числа необходимо подать документы при поступлении «БВИ»?')
    db.session.add(question)
    db.session.commit()

    question = Question(10,51,'Какие документы подавать при поступлении БВИ?')
    db.session.add(question)
    db.session.commit()

    question = Question(10,52,'Нужно ли иметь результаты ЕГЭ при поступлении БВИ?')
    db.session.add(question)
    db.session.commit()

    question = Question(10,53,'Можно ли воспользоваться правом поступления БВИ, если сдавать вступительные испытания по материалам ВУЗа?')
    db.session.add(question)
    db.session.commit()

    question = Question(10,54,'Когда издается приказ о зачислении «БВИ»?')
    db.session.add(question)
    db.session.commit()

    question = Question(10,55,'На сколько направлений действует право поступление «БВИ»?')
    db.session.add(question)
    db.session.commit()

    question = Question(11,56,'Что такое целевое обучение?')
    db.session.add(question)
    db.session.commit()

    question = Question(11,57,'Кто заключает договор на целевое обучение? (возможно, дублирует после следующий вопрос)')
    db.session.add(question)
    db.session.commit()

    question = Question(11,58,'Где взять шаблон договора на целевое обучение? (возможно, дублирует следующий вопрос)')
    db.session.add(question)
    db.session.commit()

    question = Question(11,59,'Как заключить договор на целевое обучение?')
    db.session.add(question)
    db.session.commit()

    question = Question(11,60,'Какие документы необходимо подавать при поступлении на целевое обучение?')
    db.session.add(question)
    db.session.commit()

    question = Question(11,61,'До какого числа необходимо подать документы при поступлении на целевое обучение?')
    db.session.add(question)
    db.session.commit()

    question = Question(11,62,'Когда издается приказ о зачислении на целевое обучение?')
    db.session.add(question)
    db.session.commit()

    question = Question(12,63,'Какие индивидуальные достижения засчитываются при поступлении?')
    db.session.add(question)
    db.session.commit()

    question = Question(12,64,'Сколько баллов можно получить за индивидуальные достижения?')
    db.session.add(question)
    db.session.commit()

    question = Question(12,65,'До какого числа необходимо предоставить документы, подтверждающие наличие индивидуальных достижений?')
    db.session.add(question)
    db.session.commit()

    question = Question(12,66,'Как предоставить документы, подтверждающие наличие индивидуальных достижений?')
    db.session.add(question)
    db.session.commit()

    question = Question(12,67,'За какие года действуют индивидуальные достижения?')
    db.session.add(question)
    db.session.commit()

    question = Question(13,68,'Какие направления есть в НГТУ?')
    db.session.add(question)
    db.session.commit()

    question = Question(13,69,'На сколько направлений можно подать документы?')
    db.session.add(question)
    db.session.commit()

    question = Question(13,70,'Как поменять направление?')
    db.session.add(question)
    db.session.commit()

    question = Question(13,71,'Смогу ли я поменять направление после поступления?')
    db.session.add(question)
    db.session.commit()

    question = Question(13,72,'Смогу ли перейти на бюджет, если поступлю на контракт? (не уверен, что этот вопрос сюда)')
    db.session.add(question)
    db.session.commit()

    question = Question(13,73,'До какого числа можно изменить направления в заявлении?')
    db.session.add(question)
    db.session.commit()

    question = Question(13,74,'Сколько бюджетных и контарктых мест на напрвлениях?')
    db.session.add(question)
    db.session.commit()

    question = Question(13,75,'Какая стоимость обучения по контаркту на разных направлениях?')
    db.session.add(question)
    db.session.commit()

    question = Question(13,76,'Какие экзамены нужно сдавать для поступления на различные направления НГТУ?')
    db.session.add(question)
    db.session.commit()

    question = Question(13,77,'*Подобрать направление, с учетом сданных экзаменов?')
    db.session.add(question)
    db.session.commit()

    question = Question(14,78,'Какие минимальные баллы ЕГЭ?')
    db.session.add(question)
    db.session.commit()

    question = Question(14,79,'Какие ЕГЭ нужно сдавать для разных направлений?')
    db.session.add(question)
    db.session.commit()

    question = Question(14,80,'ЕГЭ за какие года действуют?')
    db.session.add(question)
    db.session.commit()

    question = Question(14,81,'Где можно сдать ЕГЭ? (а точно нужен этот и следующий вопрос?)')
    db.session.add(question)
    db.session.commit()

    question = Question(14,82,'Кто имеет права сдавать ЕГЭ?')
    db.session.add(question)
    db.session.commit()

    question = Question(14,83,'Нужно ли предоставлять свидетельство с результатами ЕГЭ?')
    db.session.add(question)
    db.session.commit()

    question = Question(14,84,'Если я сдал(а) ЕГЭ, нужно ли мне сдавать ВИ? (возможно, дублирует следующей вопрос)')
    db.session.add(question)
    db.session.commit()

    question = Question(15,85,'Кто имеет право сдавит ВИ?')
    db.session.add(question)
    db.session.commit()

    question = Question(15,86,'Как записаться на сдачу ВИ?')
    db.session.add(question)
    db.session.commit()

    question = Question(15,87,'До какого числа необходимо подать документы при поступлении по ВИ?')
    db.session.add(question)
    db.session.commit()

    question = Question(15,88,'Где будет происходить сдача ВИ? (возможно, лишний)')
    db.session.add(question)
    db.session.commit()

    question = Question(15,89,'В каком формате проходят ВИ?')
    db.session.add(question)
    db.session.commit()

    question = Question(15,90,'В какие даты проходят ВИ (расписание)?')
    db.session.add(question)
    db.session.commit()

    question = Question(15,91,'Как проходит апелляция при ВИ?')
    db.session.add(question)
    db.session.commit()

    question = Question(15,92,'Что такое система «прокторинга»?')
    db.session.add(question)
    db.session.commit()

    question = Question(15,93,'Могу ли я сдать ВИ из дома?')
    db.session.add(question)
    db.session.commit()

    question = Question(15,94,'Когда станут известны результаты ВИ?')
    db.session.add(question)
    db.session.commit()

    question = Question(15,95,'Где можно найти демоверсии ВИ?')
    db.session.add(question)
    db.session.commit()

    question = Question(15,96,'Существует ли инклюзивное сопровождении при сдачи ВИ по материалам ВУЗа?')
    db.session.add(question)
    db.session.commit()

    question = Question(15,97,'Могу ли я получить комнату в общежитии на время сдачи ВИ?')
    db.session.add(question)
    db.session.commit()

    question = Question(16,98,'Какие минимальные баллы необходимо набрать для участия в конкурсе на поступление?')
    db.session.add(question)
    db.session.commit()

    question = Question(16,99,'Какие минимальные баллы для обучения по контракту?')
    db.session.add(question)
    db.session.commit()

    question = Question(16,100,'*Подобрать направление, с учетом сданных экзаменов?')
    db.session.add(question)
    db.session.commit()

    question = Question(17,101,'Как оценить свои шансы поступит на бюджет? (Если бы поступление было сегодня)')
    db.session.add(question)
    db.session.commit()

    question = Question(17,102,'Какие минимальные баллы для обучения по контракту?')
    db.session.add(question)
    db.session.commit()

    question = Question(17,103,'Где просмотреть рейтинговые списки?')
    db.session.add(question)
    db.session.commit()

    question = Question(17,104,'Какие проходные баллы прошлых лет?')
    db.session.add(question)
    db.session.commit()

    question = Question(17,105,'Сколько бюджетные мест на направлениях?')
    db.session.add(question)
    db.session.commit()

    question = Question(17,106,'Где просмотреть приказы на зачисление?')
    db.session.add(question)
    db.session.commit()

    question = Question(17,107,'Когда издаются приказы на зачисления?')
    db.session.add(question)
    db.session.commit()

    question = Question(17,108,'Можно ли пойти на контракт, если не поступил на бюджет?')
    db.session.add(question)
    db.session.commit()

    question = Question(18,109,'Кто имеет право получить комнату в общежитии?')
    db.session.add(question)
    db.session.commit()

    question = Question(18,110,'Какие условия проживания в общежитии (правила, права и обязанности)?')
    db.session.add(question)
    db.session.commit()

    question = Question(18,111,'Какие нужны документы для заселения?')
    db.session.add(question)
    db.session.commit()

    question = Question(18,112,'Когда я должен подать документы для заселения?')
    db.session.add(question)
    db.session.commit()

    question = Question(18,113,'Могу ли я получить комнату в общежитии после поступления?')
    db.session.add(question)
    db.session.commit()

    question = Question(18,114,'Могу ли я выселиться из комнаты до окончания обучения?')
    db.session.add(question)
    db.session.commit()

    question = Question(18,115,'Сколько стоит проживание?')
    db.session.add(question)
    db.session.commit()

    question = Question(18,116,'Что входит в стоимость проживания? | нужно ли оплачивать коммунальные услуги?')
    db.session.add(question)
    db.session.commit()

    question = Question(18,117,'Как получить комнату в общежитии повышенной комфортности?')
    db.session.add(question)
    db.session.commit()

    question = Question(18,118,'Когда происходит заселение в общежитие?')
    db.session.add(question)
    db.session.commit()

    question = Question(18,119,'Могу ли я заселиться раньше/позже?')
    db.session.add(question)
    db.session.commit()

    question = Question(18,120,'Могут ли меня выселить из общежития? (возможно, дублирует второй вопрос)')
    db.session.add(question)
    db.session.commit()

    question = Question(18,121,'Смогу ли я поменять комнату/общежитие, если меня что-то будет не устраивать? (возможно, дублирует второй вопрос)')
    db.session.add(question)
    db.session.commit()

    question = Question(18,122,'Могу ли я лично посмотреть на условия проживания? (возможно, дублирует второй вопрос)')
    db.session.add(question)
    db.session.commit()

    question = Question(18,123,'Можно ли приводить гостей? (возможно, дублирует второй вопрос)')
    db.session.add(question)
    db.session.commit()

    question = Question(18,124,'Можно ли держать домашних животных? (возможно, дублирует второй вопрос)')
    db.session.add(question)
    db.session.commit()

    question = Question(18,125,'Могу ли я получить комнату на время ВИ?')
    db.session.add(question)
    db.session.commit()
    '''
def InitAnswer():
    answer = Answer('Если у вас есть результаты ЕГЭ, то с 20-го июня до 29 июля, если вы будете сдавать экзамены - до 17-го июля')
    db.session.add(answer)
    db.session.commit()

    answer = Answer('Вам нужно зарегистрироваться на https://ciu.nstu.ru/enrollee_account/registration , перейти по ссылке полученной на адрес электронной почты, заполнить анкету, распечатать ее и приложить сканы анкеты и всех необходимых документов')
    db.session.add(answer)
    db.session.commit()

    answer = Answer('Прийти по адресу пр. Карла Маркса 20, корпус 2 (холл 1 этажа). Режим работы пн-пт с 10:00 до 17:00. С собой нужно иметь иметь все необходимые документы и их копии.')
    db.session.add(answer)
    db.session.commit()

    answer = Answer('Скачать бланк заявления с сайта университета и отправить его почтой по адресу 630073, г. Новосибирск, пр. К. Маркса, 20.Однако, напоминаем Вам, что приоритетный способ подачи документов - онлайн через личный кабинет поступающего на nstu.ru либо через портал Госуслуг')
    db.session.add(answer)
    db.session.commit()

    answer = Answer('Зарегистрироваться на портале gosuslugi.ru выбрать услугу …, и следовать инструкциям на портале. После того как ваше заявление будет рассмотрено вам придет уведомление и с портала Госуслуг и от НГТУ')
    db.session.add(answer)
    db.session.commit()

    answer = Answer('Для того, чтобы внести какие-либо измнения в заявление Вам необходимо зайти в личный кабинет поступающего и указать, что именно нужно изменить в личных сообщения приемной комиссии. Напоминаем, что если Вы подавали документы очно, то логин и пароль от вашего личного кабинета указан в расписке.')
    db.session.add(answer)
    db.session.commit()

    answer = Answer('Для поступления по общему конкурсу необходимо предосавтить: - документ удостверяющий личность; - документ об образовании государственного образца (аттестат, диплом СПО или ВО), СНИЛС (при наличии); - нотариально заверенные переводы иностаранного документа об образовании (если вы заканчивали иностранное учебное заведение); - документы, подтверждающие индивидуальные достижения (при наличии); - заявление, заполенное в личном кабинете (в случае, если Вы подаете документы очно, заявление заполнят сотрудники приемной комиссии)')
    db.session.add(answer)
    db.session.commit()

    answer = Answer('Для поступления в рамках особой квоты по целевому приему Вам необходимо предоставить следующие докеументы: - документ удостверяющий личность; - документ об образовании государственного образца (аттестат, диплом СПО или ВО), СНИЛС (при наличии); - нотариально заверенные переводы иностаранного документа об образовании (если вы заканчивали иностранное учебное заведение); - документы, подтверждающие индивидуальные достижения (при наличии); - заявление, заполенное в личном кабинете (в случае, если Вы подаете документы очно, заявление заполнят сотрудники приемной комиссии); -договор о целевом обучении')
    db.session.add(answer)
    db.session.commit()

    answer = Answer('Для поступления в пределах особой квоты без вступительных испытаний Вас необходимо предосавтить: - документ удостверяющий личность; - документ об образовании государственного образца (аттестат, диплом СПО или ВО), СНИЛС (при наличии); - нотариально заверенные переводы иностаранного документа об образовании (если вы заканчивали иностранное учебное заведение); - документы, подтверждающие индивидуальные достижения (при наличии); - заявление, заполенное в личном кабинете (в случае, если Вы подаете документы очно, заявление заполнят сотрудники приемной комиссии); -диплом победителя или призера олимпиады из перечня. Проверить, входит ли олимпиада в установленный перечень можно на сайте https://rsr-olymp.ru/')
    db.session.add(answer)
    db.session.commit()

    answer = Answer('Для поступления в пределах особой квоты Вам необходимо предосавтить: - документ удостверяющий личность; - документ об образовании государственного образца (аттестат, диплом СПО или ВО), СНИЛС (при наличии); - нотариально заверенные переводы иностаранного документа об образовании (если вы заканчивали иностранное учебное заведение); - документы, подтверждающие индивидуальные достижения (при наличии); - заявление, заполенное в личном кабинете (в случае, если Вы подаете документы очно, заявление заполнят сотрудники приемной комиссии); - документы, подтверждающие Ваше права поступать в пределах особой квоты')
    db.session.add(answer)
    db.session.commit()

    answer = Answer('Для поступления по общему конкурсу необходимо предосавтить: - документ удостверяющий личность; - документ об образовании государственного образца (аттестат, диплом СПО или ВО), - нотариально заверенные переводы иностаранного документа об образовании  - заявление, заполенное в личном кабинете (в случае, если Вы подаете документы очно, заявление заполнят сотрудники приемной комиссии);')
    db.session.add(answer)
    db.session.commit()

    answer = Answer('Для подачи заявления оригиналы документов не требуются. При поступлении нужно представить подлинник документа об образовании в течении учебного года')
    db.session.add(answer)
    db.session.commit()

    answer = Answer('Обучение по контракту предусматривает ежесеметровую оплату обучения (https://www.nstu.ru/studies/cost_education/edu_cost), обучающийся платно имеет право по итогам сесии перевестисб на вакантные бюджетные места')
    db.session.add(answer)
    db.session.commit()

    answer = Answer('шаблон договора - https://ciu.nstu.ru/documents_pub/download?id=42304, https://ciu.nstu.ru/documents_pub/download?id=42305, https://ciu.nstu.ru/documents_pub/download?id=42306 рекомендуем скачать заполненный договор в личном кабинете')
    db.session.add(answer)
    db.session.commit()

    answer = Answer('заключить и оплатить договор нужно не позднее 10-го сентября, но вы можете сделать это сразу, подав согласие на платное обучение, еще до зачисления')
    db.session.add(answer)
    db.session.commit()

    answer = Answer('Если вам нет 18-ти лет, то договор заключается с одним из родителей, кроме того после оплаты можно получить налоговый вычет. Если вам есть 18 лет, то договор можете заключить вы непосредственно. Также может быть заключен трехсторонний договор с предприятием. Договор можно заключить из личного кабинета. ')
    db.session.add(answer)
    db.session.commit()

    answer = Answer('Оплатить можно - из личного кабинета картой, банковским переводом, в отделении банка Левобережный в  1-м корпусе НГТУ. Также есть программы образовательных кредитов и оплата материнским капиталом')
    db.session.add(answer)
    db.session.commit()

    answer = Answer('согласие подается из личного кабинета в разделе "согласие"')
    db.session.add(answer)
    db.session.commit()

    answer = Answer('согласие на целевые места, без вступительных испытаний, особую квоту нужно подать не позднее 18-00 4 августа. По общему конкурсу - не позднее 18-00 11 августа (время новосибирское). Согласие подается через личный кабинет')
    db.session.add(answer)
    db.session.commit()

    answer = Answer('одновременно можно подать одно согласие (на одну конкурсную группу) на бюджетные места и одно на платные места ( возможно не на другую конкурсную группу)')
    db.session.add(answer)
    db.session.commit()

    answer = Answer('Да можно подавать новое согласие. которое заменит текущее. Сделать это можно из личного кабинета. ')
    db.session.add(answer)
    db.session.commit()

    answer = Answer('Если заявление подано в НГТУ (лично или в личном кабинете), то согласие можно подать в личном кабинете, выбрав конкурсную группу и прикрепив скан. Если заявление подано на портале госуслуг, то согласие можно подать только на госуслугах. Согласие на платные места можно подать только через личный кабинет НГТУ')
    db.session.add(answer)
    db.session.commit()

    answer = Answer('20 июня 2021г.')
    db.session.add(answer)
    db.session.commit()

    answer = Answer('17 июля — завершение приема документов, необходимых для поступления, от лиц, поступающих на обучение по результатам вступительных испытаний, проводимых университетом самостоятельно; 29 июля — завершение приема документов, необходимых для поступления, от лиц, поступающих на обучение по результатам единого государственного экзамена (ЕГЭ), а также без прохождения вступительных испытаний.')
    db.session.add(answer)
    db.session.commit()

    answer = Answer('До 17 июля лицам, поступающим на обучения по результатам ВИ, проводимых ВУЗом; до 29 июля поступающим по материалам ЕГЭ или поступающим БВИ')
    db.session.add(answer)
    db.session.commit()

    answer = Answer('4 августа — завершение приема заявлений о согласии на зачисление от поступающих в пределах особой квоты, целевой квоты и БВИ; 11 августа — завершение приема заявлений о согласии на зачисление на основные конкурсные места; 21 августа — завершение приема заявлений о согласии на зачисление на основные конкурсные места, оставшиеся после зачисления 17 августа')
    db.session.add(answer)
    db.session.commit()

    answer = Answer('? до 21 августа')
    db.session.add(answer)
    db.session.commit()

    answer = Answer('Оригиналы документов об образовании, а также заявлений и согласий на зачисление необходимо предоставить в течении учебного года')
    db.session.add(answer)
    db.session.commit()

    answer = Answer('6 августа — издание приказов о зачислении лиц, поступающих без вступительных испытаний, поступающих на места в пределах квот;17 августа — издание приказов о зачислении лиц, подавших заявление о согласии на зачисление на основные конкурсные места до заполнения 100% основных конкурсных мест. 23 августа — издание приказов о зачислении лиц, подавших заявление о согласии на зачисление на основные конкурсные места, оставшиеся после зачисления 17 августа.23 августа — издание приказов о зачислении на обучение на места по договорам об оказании платных образовательных услуг.')
    db.session.add(answer)
    db.session.commit()

    answer = Answer('Основной этап: 19—29 июля; 9—18 августа (заочное и контарктное обучение)')
    db.session.add(answer)
    db.session.commit()

    answer = Answer('Результаты экзаменов становятся известны сразу, после прохождения тестирования.')
    db.session.add(answer)
    db.session.commit()

    answer = Answer('Запись на вступительные экзамены проводится через личный кабинет потсупающего на сайте университета. Сдающий выбирает удобное для себя время и дату сдачи.')
    db.session.add(answer)
    db.session.commit()

    answer = Answer('Заявление на аппеляцию отправляется в течении одного часа с момента завершения тестирования')
    db.session.add(answer)
    db.session.commit()

    answer = Answer('6 августа — издание приказов о зачислении лиц, поступающих без вступительных испытаний, поступающих на места в пределах квот;17 августа — издание приказов о зачислении лиц, подавших заявление о согласии на зачисление на основные конкурсные места до заполнения 100% основных конкурсных мест. 23 августа — издание приказов о зачислении лиц, подавших заявление о согласии на зачисление на основные конкурсные места, оставшиеся после зачисления 17 августа.')
    db.session.add(answer)
    db.session.commit()

    answer = Answer('23 August')
    db.session.add(answer)
    db.session.commit()

    answer = Answer('6 August')
    db.session.add(answer)
    db.session.commit()

    answer = Answer('В момент подачи документов в личном кабинете поступающего необходимо оставить отметку о том, что Вы нуждаетесь в общежитии. Далее, в случае вашего потсупления, Вам придет уведовление о дате и порядке заселения.')
    db.session.add(answer)
    db.session.commit()

    answer = Answer('Заселение в общежитие производится в конце августа. На электронную почту, указанную Вами при регистрации придет оповещение с рекомендуемой датой заезда.')
    db.session.add(answer)
    db.session.commit()

    answer = Answer('Вы можете заселиться не в дату заезда, однако, лучше заранее предупредить об этом дирекцию студ.городка')
    db.session.add(answer)
    db.session.commit()


    answer = Answer('Право на прием на обучение в пределах особой квоты имеют дети-инвалиды, инвалиды I и II групп, инвалиды с детства, инвалиды вследствие военной травмы или заболевания, полученных в период прохождения военной службы, дети-сироты и дети, оставшиеся без попечения родителей, а также лица из числа детей-сирот и детей, оставшихся без попечения родителей и ветераны боевых действий из числа лиц, указанных в подпунктах 1-4 пункта 1 статьи 3 Федерального закона от 12 января 1995 г. № 5-ФЗ «О ветеранах». Право поступления БВИ имеют победители и призеры заключительного этапа всероссийской олимпиады школьников, члены сборных команд Российской Федерации, участвовавшие в международных олимпиадах по общеобразовательным предметам')
    db.session.add(answer)
    db.session.commit()

    answer = Answer('Для поступления в пределах "особых квот" необходимо дополнительно к общему списку документов прикрепить докумнеты, подтверждающие наличии у абитуриента право на поступления в рамках данной категории.')
    db.session.add(answer)
    db.session.commit()

    answer = Answer('до 29 июля')
    db.session.add(answer)
    db.session.commit()

    answer = Answer('Да, если вы относитесь к категории "инвалиды, в том числе дети-инвалиды"')
    db.session.add(answer)
    db.session.commit()

    answer = Answer('Для поступления по льготе Вам необходимо набрать баллы минимальные баллы, устанволенные университетом самостоятельно. ПРи этом в пределах особой квоты установленно ограниченное число мест, и набор минимальных баллов не может гарантировать Вам поступление на бюджет, если число таких абитуриентов будет превышать размер квоты. В этом случае поступление происходить на конкрусной (рейтинговой) основе в пределах квоты.')
    db.session.add(answer)
    db.session.commit()

    answer = Answer('6 August')
    db.session.add(answer)
    db.session.commit()

    answer = Answer('При поступлении в НГТУ реализуется инклюизивное сопровождение. Заявку на сопровждение вы можете оставить в личном кабинете поступающего, либо обратиться по телефону....')
    db.session.add(answer)
    db.session.commit()

    answer = Answer('Поступление в пределах особой квоты действует на все направления, где есть бюджетные места.')
    db.session.add(answer)
    db.session.commit()

    answer = Answer('Вы можете принять участие в конкурсе сразу на несколько направлений в пределах особой квоты, однако, восопользоваться своим правом сможете только на одно из них, написав соответвующее согласие.')
    db.session.add(answer)
    db.session.commit()

    answer = Answer('Победители и призеры заключительного этапа всероссийской олимпиады школьников (далее – всероссийская олимпиада), членам сборных команд Российской Федерации, участвовавших в международных олимпиадах по общеобразовательным предметам и сформированных в порядке, установленном федеральным органом исполнительной власти, осуществляющим функции по выработке и реализации государственной политики и нормативно-правовому регулированию в сфере общего образования (далее – члены сборных команд, участвовавших в международных олимпиадах) предоставляется право на прием без вступительных испытаний в соответствии с частью 4 статьи 71 Федерального закона № 273-ФЗ. Победители и призеры олимпиад школьников, проводимых в порядке, устанавливаемом федеральным органом исполнительной власти, осуществляющим функции по выработке государственной политики и нормативно-правовому регулированию в сфере высшего образования, по согласованию с федеральным органом исполнительной власти, осуществляющим функции по выработке и реализации государственной политики и нормативно-правовому регулированию в сфере общего образования, предоставляются особые права в соответствии с частью 12 статьи 71 Федерального закона № 273-ФЗ – право на прием без вступительных испытаний по результатам олимпиад школьников.')
    db.session.add(answer)
    db.session.commit()

    answer = Answer('до 29 июля')
    db.session.add(answer)
    db.session.commit()

    answer = Answer('Необходимо дополнтельно к оснвоным документам предоставить скан диплома олимпиады.')
    db.session.add(answer)
    db.session.commit()

    answer = Answer('Да, необходимо иметь результаты ЕГЭ, либо результаты ВИ, проводимых ВУЗом самостоятельно. Они должны быть больше минимального балла,установленного университетом, кроме тогопПри поступлении БВИ по результатам олимпиады школьников необходимо иметь не менее 75 баллов по соответвующему предмету.')
    db.session.add(answer)
    db.session.commit()

    answer = Answer('Да.')
    db.session.add(answer)
    db.session.commit()

    answer = Answer('6 August')
    db.session.add(answer)
    db.session.commit()

    answer = Answer('Вы можете принять участие в конкурсе сразу на несколько направлений, однако, восопользоваться своим правом сможете только на одно из них, написав соответвующее согласие.')
    db.session.add(answer)
    db.session.commit()

    answer = Answer('Целевое обучение — система подготовки специалистов для  предприятий и организаций, когда на основании имеющегося у абитуриента договора о целевом обучении с государственной организацией он может быть зачислен на бюджетное место в пределах квоты целевого приема, не участвуя в общем конкурсе. При этом после окончания обучения этот студент должен будет отработать на заключившем с ним договор предприятии не менее 3-х лет.')
    db.session.add(answer)
    db.session.commit()

    answer = Answer('Договор на целевое обучение может быть заключен с одним из следующих предприятий (организаций): •	Федеральные государственные органы, органы государственной власти субъектов Российской Федерации, органы местного самоуправления  •	Государственные и муниципальные учреждения, унитарные предприятия  •	Государственные корпорации  •	Государственные компании  •	Организации, включенные в сводный реестр организаций оборонно-промышленного комплекса, формируемый в соответствии с частью 2 статьи 21 Федерального закона от 31 декабря 2014 года № 488-ФЗ «О промышленной политике в Российской Федерации»  •	Хозяйственные общества, в уставном капитале которых присутствует доля Российской Федерации, субъекта Российской Федерации или муниципального образования  •	Акционерные общества, акции которых находятся в собственности или в доверительном управлении государственной корпорации  •	Дочерние хозяйственные общества организаций, указанных в пунктах 4, 6 и 7  •	Организации, которые созданы государственными корпорациями или переданы государственным корпорациям в соответствии с положениями федеральных законов об указанных корпорациях ')
    db.session.add(answer)
    db.session.commit()

    answer = Answer('Шаблон договора на целевое обучение можно взять по адресу https://nstu.ru/entrance/committee/targeted_training  «Типовая форма договора о целевом обучении по образовательной программе среднего профессионального и высшего образования»')
    db.session.add(answer)
    db.session.commit()

    answer = Answer('Алгоритм заключения договора на целевое обучение находится по адресу https://nstu.ru/entrance/committee/targeted_training в разделе «Памятка абитуриенту».')
    db.session.add(answer)
    db.session.commit()

    answer = Answer('Для поступления в рамках особой квоты по целевому приему Вам необходимо предоставить следующие докеументы: - документ удостверяющий личность; - документ об образовании государственного образца (аттестат, диплом СПО или ВО), СНИЛС (при наличии); - нотариально заверенные переводы иностаранного документа об образовании (если вы заканчивали иностранное учебное заведение); - документы, подтверждающие индивидуальные достижения (при наличии); - заявление, заполенное в личном кабинете (в случае, если Вы подаете документы очно, заявление заполнят сотрудники приемной комиссии); -договор о целевом обучении')
    db.session.add(answer)
    db.session.commit()

    answer = Answer('Документы для поступления на целевое обучение необходимо подать в следующие сроки:- при поступлении на бакалавриат или специалитет – до 29 июля 2021 г.- при поступлении в магистратуру – до 20 июля 2021 г.')
    db.session.add(answer)
    db.session.commit()

    answer = Answer('Зачисление абитуриентов, поступающих в рамках квоты целевого приема, состоится 6 августа 2021 г.')
    db.session.add(answer)
    db.session.commit()

    answer = Answer('1) наличие статуса чемпиона, призера Олимпийских игр, Паралимпийских игр, Сурдлимпийских игр, чемпиона мира, чемпиона Европы, лица, занявшего первое место на первенстве мира, первенстве Европы по видам спорта, включенным в программы Олимпийских игр, Паралимпийских игр, Сурдлимпийских игр – 10 баллов;2) наличие статуса чемпиона мира, чемпиона Европы, победителя первенства мира, первенства Европы по видам спорта, не включенным в программы Олимпийских игр, Паралимпийских игр, Сурдлимпийских игр – 9 баллов;3) наличие золотого знака отличия Всероссийского физкультурно-спортивного комплекса «Готов к труду и обороне» (ГТО) (далее – Комплекс ГТО) и удостоверения к нему, полученных поступающим в соответствии с Порядком награждения лиц, выполнивших нормативы испытаний (тестов) Всероссийского физкультурно-спортивного комплекса «Готов к труду и обороне» (ГТО), соответствующими знаками отличия Всероссийского физкультурно-спортивного комплекса «Готов к труду и обороне» (ГТО), утвержденным приказом Министерства спорта Российской Федерации от 14 января 2016 г. № 16, если поступающий награжден указанным золотым знаком за выполнение нормативов Комплекса ГТО, установленных для возрастной группы населения Российской Федерации, к которой поступающий относится (относился) в текущем году и (или) в предшествующем году – 3 балла;4) наличие полученных в образовательных организациях Российской Федерации документов об образовании или об образовании и о квалификации с отличием (аттестата о среднем общем образовании с отличием, аттестата о среднем (полном) общем образовании с отличием, аттестата о среднем (полном) общем образовании для награжденных золотой (серебряной) медалью, диплома о среднем профессиональном образовании с отличием, диплома о начальном профессиональном образовании с отличием, диплома о начальном профессиональном образовании для награжденных золотой (серебряной) медалью) – 5 баллов;5) участие и (или) результаты участия в олимпиадах школьников (не используемые для получения особых прав и (или) особого преимущества при поступлении на обучение по конкретным условиям поступления). Профиль олимпиады и конкретное количество баллов за данный вид индивидуальных достижений, начисляется в соответствиис Приложением № 1;6) участие и (или) результаты участия в мероприятиях, включенных в перечень, утвержденный Министерством просвещения Российской Федерации в соответствии с пунктом 4 Правил выявления детей, проявивших выдающиеся способности и сопровождения их дальнейшего развития, утвержденных постановлением Правительства Российской Федерации от 17 ноября 2015 г. № 1239 – 5 баллов;7) наличие статуса победителя (призера) национального и (или) международного чемпионата по профессиональному мастерству среди инвалидов и лиц с ограниченными возможностями здоровья «Абилимпикс» – 5 баллов;8) осуществление волонтерской (добровольческой) деятельности (если с даты завершения периода осуществления указанной деятельности до дня завершения приема документов и вступительных испытаний прошло не более четырех лет), при наличии оформленной и зарегистрированной «Личной книжки волонтера» или подтвержденной печатью регионального ресурсного центра электронной Личной книжки волонтера:- до 50 часов – 1 балл;- 50-100 часов – 2 балла;- 100-150 часов – 3 балла;- 150 и более часов – 4 балла;9) наличие удостоверения Волонтер года:- в регионе – 1 балл;- России – 2 балла.')
    db.session.add(answer)
    db.session.commit()

    answer = Answer('максимальное количесвто баллов - 10')
    db.session.add(answer)
    db.session.commit()

    answer = Answer('до 29 июля')
    db.session.add(answer)
    db.session.commit()

    answer = Answer('Сканы данных документов, необходимо прикреить в личном кабинете поступающего')
    db.session.add(answer)
    db.session.commit()

    answer = Answer('Без ограничения, однако если поступающий награжден указанным золотым знаком за выполнение нормативов Комплекса ГТО, установленных для возрастной группы населения Российской Федерации, к которой поступающий относится (относился) в текущем году и (или) в предшествующем году – 3 балла;')
    db.session.add(answer)
    db.session.commit()

    answer = Answer('С полным перченем направлений НГТУ вы можете ознакомиться по ссылке https://xn--c1atqe.xn--p1ai/entrance/entrance_all/bachelor')
    db.session.add(answer)
    db.session.commit()

    answer = Answer('На 4 направления')
    db.session.add(answer)
    db.session.commit()

    answer = Answer('Необходимо написать соответвующую просьба в сообщения для приемной комиссии через личный кабинет поступающего, либо обратиться в приемную комиссию лично')
    db.session.add(answer)
    db.session.commit()

    answer = Answer('В процессе обучения возможен перевод на другую специальность или фаукльтет при наличии свободных бюджетных или контрактных мест, успешной сдачи сессии и закрытия акеадемичской разницы между дисциплинами,е сли такая есть')
    db.session.add(answer)
    db.session.commit()

    answer = Answer('Перевод с контрактного обучения на бюджетное возможен при наличии свободных бюджетных мест, а также упешной сдачи двух сессий подряд')
    db.session.add(answer)
    db.session.commit()

    answer = Answer('До 17 июля, если вы поступаете по ВИ, проводимыми университетом самостоятельно, и до 29 июля, если вы поступаете по результатам ЕГЭ')
    db.session.add(answer)
    db.session.commit()

    answer = Answer('План набора достепн по ссылке https://xn--c1atqe.xn--p1ai/entrance/entrance_all/bachelor')
    db.session.add(answer)
    db.session.commit()

    answer = Answer('Актуальная стоимость обучения доступна по ссылке https://www.nstu.ru/studies/cost_education/edu_cost')
    db.session.add(answer)
    db.session.commit()

    answer = Answer('Перчень необходимых экзаменов для поступления на различные направления НГТУ доступен по ссылке https://xn--c1atqe.xn--p1ai/entrance/entrance_all/bachelor')
    db.session.add(answer)
    db.session.commit()

    answer = Answer('https://xn--c1atqe.xn--p1ai/entrance/committee/search_direction')
    db.session.add(answer)
    db.session.commit()

    answer = Answer('Для лиц, поступающих на базе среднего общего образования приняты слебующие минимальные баллы ЕГЭ и ВИ: Русский язык 40 Математика (профильный уровень) 39 Информатика и ИКТ 44 Физика 39 Химия 39 Биология 39 География 40 Обществознание 45 Литература 40 История 35 Иностранный язык 30 ')
    db.session.add(answer)
    db.session.commit()

    answer = Answer('Перчень необходимых экзаменов для поступления на различные направления НГТУ доступен по ссылке https://xn--c1atqe.xn--p1ai/entrance/entrance_all/bachelor')
    db.session.add(answer)
    db.session.commit()

    answer = Answer('С 2017 (включительно) по 2021')
    db.session.add(answer)
    db.session.commit()

    answer = Answer(' ')
    db.session.add(answer)
    db.session.commit()

    answer = Answer(' ')
    db.session.add(answer)
    db.session.commit()

    answer = Answer('Нет, данные подгружаются из федеральной базы автоматически')
    db.session.add(answer)
    db.session.commit()

    answer = Answer('Нет, однако если вы входите в категорию лиц, имеющих право сдавать ВИ по материалам ВУЗа, то вы можете сдать и их, после чего выбрать наилучший результат')
    db.session.add(answer)
    db.session.commit()

    answer = Answer('- инвалиды (в том числе, дети-инвалиды); - иностранные граждане; - лица, получившие документ о среднем общем образовании в иностранной организации;- лица поступающие на обучение на базе среднего профессионального или высшего образования')
    db.session.add(answer)
    db.session.commit()

    answer = Answer('В личном кабиенте поступающего, либо при личном образении в приемную комиссию')
    db.session.add(answer)
    db.session.commit()

    answer = Answer(' ')
    db.session.add(answer)
    db.session.commit()


    answer = Answer('Сдача ВИ првоодится преимущесвенно в дистанционном формате, однако, возможна и очная сдача ВИ в помещениях университета')
    db.session.add(answer)
    db.session.commit()


    answer = Answer('Сдача ВИ првоодится преимущесвенно в дистанционном формате с использованием системы прокторинга. Это онлайн тестирвоание при наблюдении порктором процесса написания экзамена сдающими с использованием веб-камеры и микрофона. Возможна и очная сдача ВИ в помещениях университета')
    db.session.add(answer)
    db.session.commit()


    answer = Answer('С 12 июля по 29 июля - осоновной поток; с 9 августа по 18 августа - второй поток. Расписание доступно по ссылке https://www.nstu.ru/entrance/entrance_all/schedule')
    db.session.add(answer)
    db.session.commit()


    answer = Answer('Аппеляция подается в течении часа после завершения ВИ. Абитуриентом заполняется бланк с указанием спорных номеров вопросов и комментариями. Скан такого заявления отправляется на почту exams2021@corp.nstu.ru . В теме письма указывается Фамилия И.О. Предмет Дата экзамена. Далее аппеляция рассматривается аппеляционной комисией. Начисление дополнительных баллов, присуждаемых по итогу аппеляции происодит автоматически, без  отправкиответных писем абитуриенту.')
    db.session.add(answer)
    db.session.commit()


    answer = Answer('Сиситема прокторинга подразумевает собой написание онлайн тестирования, на протяжении которого за сдающим наблюдает специалист "проктор" посредством веб-камеры и микрофона.  Он следит за тем, чтобы сдающий не пользовался посторонними материалами, и находился один в помещении.')
    db.session.add(answer)
    db.session.commit()


    answer = Answer('Да, при наличии подключения к интернету, веб-камеры и микрофона.')
    db.session.add(answer)
    db.session.commit()


    answer = Answer('Результаты ВИ известны сразу после окончания тестирования.')
    db.session.add(answer)
    db.session.commit()


    answer = Answer('Пробные ВИ доступны по ссылке https://dispace.edu.nstu.ru/didesk/course/show/8140/tests')
    db.session.add(answer)
    db.session.commit()


    answer = Answer('В НГТУ-НЭТИ создан специальный центр инклюзивного сопровождения с информацией о работе которого вы можете ознакомиться по ссылке https://www.nstu.ru/studies/study/ZIS')
    db.session.add(answer)
    db.session.commit()


    answer = Answer('В связи с эпидемиалогической ситуацией свободное предоставление комнат общежития на время сдачи ВИ ограничено. За дополнительной иформацией необходимо обратиться лично к проректору по учебной работе.')
    db.session.add(answer)
    db.session.commit()


    answer = Answer('Для лиц, поступающих на базе среднего общего образования приняты слебующие минимальные баллы ЕГЭ и ВИ: Русский язык 40 Математика (профильный уровень) 39 Информатика и ИКТ 44 Физика 39 Химия 39 Биология 39 География 40 Обществознание 45 Литература 40 История 35 Иностранный язык 30')
    db.session.add(answer)
    db.session.commit()


    answer = Answer('Минимальные баллы для поступленияна контракт определяется отдельно каждым факультетом. Обратитесь в деканат интереующего вас факультета.')
    db.session.add(answer)
    db.session.commit()


    answer = Answer('https://www.nstu.ru/entrance/committee/search_direction')
    db.session.add(answer)
    db.session.commit()


    answer = Answer('Для оценки своих шансов поступления на бюджет Вам стоит посмотреть рейтинговый список интересующего Вас направления. Выбрать "Просмотреть рейтинговый список только по поданным согласиям на текущий момент".  Если ваш номер в этом рейтинге меньше либор авен общему количеству бюджетных мест на данное направления, то на данный момент вы проходите. Обратите внимание, что ситуация может постоянно меняться вплоть до 18:00 11 августа.')
    db.session.add(answer)
    db.session.commit()


    answer = Answer('Минимальные баллы для поступленияна контракт определяется отдельно каждым факультетом. Обратитесь в деканат интереующего вас факультета.')
    db.session.add(answer)
    db.session.commit()



    answer = Answer('Рейтинговые списки доступны по ссылке https://www.nstu.ru/entrance/admission_campaign/entrance')
    db.session.add(answer)
    db.session.commit()



    answer = Answer('Проходные баллы 2020 года доступны по ссылке https://www.nstu.ru/entrance/committee/completition2020')
    db.session.add(answer)
    db.session.commit()

    answer = Answer('Общее количество бюджетных мест на направлении вы можете найти в таблице по ссылке (предваритеьно выбрав интересующий вас факультет) https://xn--c1atqe.xn--p1ai/entrance/entrance_all/bachelor')
    db.session.add(answer)
    db.session.commit()

    answer = Answer('Приказы на зачисления публикуются на официальном сайте университета nstu.ru')
    db.session.add(answer)
    db.session.commit()

    answer = Answer('6 августа — издание приказов о зачислении лиц, поступающих без вступительных испытаний, поступающих на места в пределах квот;17 августа — издание приказов о зачислении лиц, подавших заявление о согласии на зачисление на основные конкурсные места до заполнения 100% основных конкурсных мест. 23 августа — издание приказов о зачислении лиц, подавших заявление о согласии на зачисление на основные конкурсные места, оставшиеся после зачисления 17 августа.23 августа — издание приказов о зачислении на обучение на места по договорам об оказании платных образовательных услуг.')
    db.session.add(answer)
    db.session.commit()

    answer = Answer('Если вы не проходите на бюджет, вы можете оформить в личном кабинете абитуриента согласие на контракт и заключить договор на обучение.')
    db.session.add(answer)
    db.session.commit()

    answer = Answer('Места в общежитии распределяют деканаты в рамках установленных квот.')
    db.session.add(answer)
    db.session.commit()

    answer = Answer('С правилами, правами  и обязанностями проживающих в общежитии можно ознакомиться по ссылке https://www.nstu.ru/campus/hostel')
    db.session.add(answer)
    db.session.commit()

    answer = Answer('Для заселения в общежитие нужен паспорт,2 фото 3х4,папка-файл ')
    db.session.add(answer)
    db.session.commit()

    answer = Answer('Документы на заселение нужно  «подать» в момент заселения. А отметку о необходимости получения места в общежитии ставят в приемной комиссии в момент подачи документов.')
    db.session.add(answer)
    db.session.commit()

    answer = Answer('Получить  место в общежитии можно и после поступления, но только с разрешения деканата')
    db.session.add(answer)
    db.session.commit()

    answer = Answer('Из общежития можно выселиться до конца обучения  написав заявление о выселении   заведующему общежитием')
    db.session.add(answer)
    db.session.commit()

    answer = Answer('С 1.07.2021 стоимость проживания для контрактных студентов составляет - 853 руб. в месяц, для бюджетных - 547 руб. в месяц. Коммунальные услуги оплачивать отдельно не нужно.')
    db.session.add(answer)
    db.session.commit()

    answer = Answer(' ')
    db.session.add(answer)
    db.session.commit()

    answer = Answer('.Место в общежитии повышенной комфортности можно получить, обратившись к сотруднику Международной службы Короткову Владимиру Владимировичу vladimir.korotkov@inter.nstu.ru .')
    db.session.add(answer)
    db.session.commit()

    answer = Answer('Заселение в общежитие в 2021 году будет проходить с23 по 31 августа')
    db.session.add(answer)
    db.session.commit()

    answer = Answer('Раньше 23.08.2021 заселиться нельзя, позже – можно.')
    db.session.add(answer)
    db.session.commit()

    answer = Answer('Да, могут, за нарушение правил проживания')
    db.session.add(answer)
    db.session.commit()

    answer = Answer('Комнату поменять можно, если  по новому месту проживания будут свободные места.')
    db.session.add(answer)
    db.session.commit()

    answer = Answer(' ')
    db.session.add(answer)
    db.session.commit()

    answer = Answer('Приводить гостей можно после того, как будут сняты антиковидные ограничения.')
    db.session.add(answer)
    db.session.commit()

    answer = Answer('Категорически запрещено содержание домашних животных')
    db.session.add(answer)
    db.session.commit()

    answer = Answer('')
    db.session.add(answer)
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
        params = json['data']
        #params = {'nationality':1,'oldeducation':3,'direction':1, 'level':2}
        #print(params, file=sys.stderr)


        question = db.session.query(Question).filter(Question.value == que).all()
        print(question[0].id, file=sys.stderr)
        print(question[0].value, file=sys.stderr)

        """"
        if len(question) == 0:
             question = db.session.query(Questionincr).filter(Questionincr.value == que).all()
        
        """
        questionId = question[0].id



        query = db.session.query(ControllerAnswer, Answer)


        for attr,value in params.items():
            print("adasdasd", file=sys.stderr)
            query = query.filter(getattr(ControllerAnswer,attr)==value)
        """
        data = query.filter(Nationality.id == ControllerAnswer.nationality).filter(ControllerAnswer.questionid==questionId)\
            .filter(ControllerAnswer.answerid == Answer.id).all()
        print(data, file=sys.stderr)
        """
        data = query.filter(ControllerAnswer.answerid == Answer.id).filter(ControllerAnswer.questionid==questionId).all()
        res = []
        print(data, file=sys.stderr)
        for el in data:
            tmp = {"id": el.ControllerAnswer.id,  "answer": el.Answer.value}
            res.append(tmp)

        return jsonify(res)
    except:
        return jsonify(error=401)

if __name__ == '__main__':
   app.run()
