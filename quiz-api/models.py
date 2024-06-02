import json

class Question:
    def __init__(self, id, title, text, image, position):
        self.id = id
        self.title = title
        self.text = text
        self.image = image
        self.position = position

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
            'position': self.position
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
            position=data['position']
        )
