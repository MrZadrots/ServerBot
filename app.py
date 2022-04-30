import _json
import logging
import sys
from config.config import DevelopementConfig
from flask import Flask, jsonify, json, Response, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


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
    subtopics = db.relationship('Subtopic', backref='subtopic')

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return '"Topic": %r' % self.value


class Subtopic(db.Model):
    __tablename__ = 'subtopic'
    id = db.Column(db.Integer(), primary_key=True)
    topicid = db.Column(db.Integer(), db.ForeignKey('topic.id'), nullable=False)
    value = db.Column(db.String(255), nullable=False)

    def __init__(self, TopicId, value):
        self.topicid = TopicId
        self.value = value

    def __repr__(self):
        return '"Subtopic": %r' % self.value

class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer(), primary_key=True)
    SubtopicId = db.Column(db.Integer(), db.ForeignKey('subtopic.id'), nullable=False)
    AnswerId = db.Column(db.Integer(), db.ForeignKey('answer.id'), nullable=False)
    value = db.Column(db.String(255), nullable=False)
    def __repr__(self):
        return "<Question:{}>".format(self.id, self.title[:10])


class Answer(db.Model):
    __tablename__ = 'answer'
    id = db.Column(db.Integer(), primary_key=True)
    value = db.Column(db.String(255), nullable=False)


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

    subtopic1 = Subtopic(1, "Заключить договор на обучение по контракту (или просто заключить договор)")
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

    subtopic1 = Subtopic(2, "Заселение в общежитие (а сюда ли эту подгруппу?)")
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

    subtopic1 = Subtopic(3, "Индивидуальные достижения")
    db.session.add(subtopic1)
    db.session.commit()

    subtopic1 = Subtopic(4, "Направления")
    db.session.add(subtopic1)
    db.session.commit()

    subtopic1 = Subtopic(5, "ЕГЭ")
    db.session.add(subtopic1)
    db.session.commit()


@app.route('/')
def index():
    #InitTopic()
    #InitSubtopic()
    return ("Hello world!")

@app.route('/getTopics')
def getTopics():
    data = Topic.query.all()
    #topics = []
    key = 0
    # = [{"a": 1, "b":2},{"a": 4, "b":2}]
    rad =[]
    for el in data:
        tmp = {"id": el.id, "value": el.value}
        rad.append(tmp)
    return jsonify(rad)

@app.route('/getTopic/<int:id>')
def getTopic(id):
    data = Topic.query.get(id)

    return jsonify(
        id = data.id,
        value = data.value,
    )

@app.route('/setTopic')
def setTopic():
    json = request.json
    print(json, file=sys.stderr)
    topic = Topic(json['value'])
    db.session.add(topic)
    db.session.commit()
    return jsonify(ok=200)

@app.route('/getSubtopic/<int:id>')
def getSubtopic(id):
    try:
        data = Subtopic.query.get(id)
        return jsonify(
            id = data.id,
            topicid = data.topicid,
            value = data.value
        )
    except:
        return jsonify(error='401')


@app.route('/setSubtopic')
def setSubtopic():
    json = request.json
    value = json['topic']
    topicid = Topic.query.get(value=value)
    print(json, file=sys.stderr)
    print(topicid, file=sys.stderr)

    return jsonify(ok=200)

@app.route('/getSubtopics')
def getSubtopics():
    data = Subtopic.query.all()
    rad =[]
    for el in data:
        tmp = {"id": el.id, "topic":el.topicid, "value": el.value}
        rad.append(tmp)
    return jsonify(rad)


if __name__ == '__main__':
   app.run()
