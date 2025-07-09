import environ

@environ.config(prefix="APP")
class AppConfig:
    MONGO_URI = environ.var("mongodb://root:123456@127.0.0.1:27017/neuralrec2_db")
    