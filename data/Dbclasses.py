from app import db
import typing


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
    answerid = db.Column(db.Integer(), db.ForeignKey('answer.id'), nullable=False)
    value = db.Column(db.String(255), nullable=False)

    def __init__(self,subtopicId,AnswerId,value):
        self.subtopicid = subtopicId
        self.answerid = AnswerId
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
    question = db.relationship('Question', backref='question_answer',
                            primaryjoin="and_(Answer.id == foreign(Question.answerid))"
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

