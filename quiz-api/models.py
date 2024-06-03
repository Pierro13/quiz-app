import json

class Question:
    def __init__(self, id, title, text, image, position, answers=None):
        self.id = id
        self.title = title
        self.text = text
        self.image = image
        self.position = position
        self.answers = answers or []

    @classmethod
    def from_row(cls, row):
        return cls(
            id=row['id'],
            title=row['titre'],
            text=row['texte'],
            image=row['image'],
            position=row['position']
        )

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'text': self.text,
            'image': self.image,
            'position': self.position,
            'answers': [answer.to_dict() for answer in self.answers]
        }

    def to_json(self):
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str):
        data = json.loads(json_str)
        return cls(
            id=data['id'],
            title=data['title'],
            text=data['text'],
            image=data['image'],
            position=data['position'],
            answers=[Answer.from_json(answer) for answer in data['answers']]
        )

class Answer:
    def __init__(self, id, question_id, text, is_correct):
        self.id = id
        self.question_id = question_id
        self.text = text
        self.is_correct = is_correct

    @classmethod
    def from_row(cls, row):
        return cls(
            id=row['id'],
            question_id=row['question_id'],
            text=row['texte'],
            is_correct=row['is_correct']
        )

    def to_dict(self):
        return {
            'id': self.id,
            'question_id': self.question_id,
            'text': self.text,
            'is_correct': self.is_correct
        }

    def to_json(self):
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str):
        data = json.loads(json_str)
        return cls(
            id=data['id'],
            question_id=data['question_id'],
            text=data['text'],
            is_correct=data['is_correct']
        )



class User:
    def __init__(self, id, username, date, score=0):
        self.id = id
        self.username = username
        self.date = date
        self.score = score
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'date': self.date,
            'score': self.score
        }
    
    def to_json(self):
        return json.dumps(self.to_dict())


