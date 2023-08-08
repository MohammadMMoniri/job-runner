from mongoengine import connect, Document, StringField, DictField, signals, BooleanField

connect(host="mongodb://root:example@localhost:27017")


class Job(Document):
    code = StringField(required=True)
    scheduling = StringField()
    base_image = StringField(required=True)
    environments = DictField()
    language = StringField(required=True)
    validated = BooleanField(required=True, default=False)

    @classmethod
    def retrieve_job_by_id(cls, code_id: str):
        return cls.objects.get(id=code_id)
