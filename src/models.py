from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    to_do = db.Column(db.String(120), unique=False, nullable=False)
    done = db.Column(db.Boolean, unique=False, nullable=False)

    def repr(self):
        return f'Task is :{self.todo}, done:{self.done}, id:{self.id}'

    def to_dict(self):
        return {
            "id": self.id,
            "to_do": self.to_do,
            "done": self.done
        }

    @classmethod
    def get_by_id(cls,id_task):
        task= cls.query.filter_by(id=id_task).one_or_none()
        return task

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    @classmethod
    def get_all(cls):
        tasks= cls.query.all()
        return [task.to_dict() for task in tasks]

    def update(self, todo):
        self.to_do=to_do
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self