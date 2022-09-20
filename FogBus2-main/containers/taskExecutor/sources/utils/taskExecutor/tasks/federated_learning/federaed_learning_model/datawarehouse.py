"""
Data-warehouse is an interface between actual model storage and federated learning logic.

A simple model maybe just store on RAM while a larger model may be store on file etc.

The '''get''' function should provide all necessary retrieval information and '''set''' function should create
a model in data-warehouse. Overload get/set to fit your own model.

'''update''' should connect with model load function: base_model::def load(self, data), overload load to achieve
different update method

"""

import uuid
import pickle
import inspect
import os

from mysql import connector


class model_warehouse:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "instance"):
            setattr(cls, "instance", super(model_warehouse, cls).__new__(cls))
        return getattr(cls, "instance")

    def _generate_id(cls):
        return uuid.uuid1()

    def set(self, model, model_id=None):
        if not model_id:
            model_id = str(self._generate_id())
            while hasattr(self, model_id):
                model_id = str(self._generate_id())
        elif hasattr(self, model_id):
            return None

        setattr(self, str(model_id), model)
        return str(model_id)

    def get(self, model_id):
        if hasattr(self, str(model_id)):
            return getattr(self, model_id)
        return None


class data_warehouse:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "instance"):
            cls.instance = super(data_warehouse, cls).__new__(cls)
        return cls.instance

    @classmethod
    def _generate_id(cls):
        return uuid.uuid1()

    @classmethod
    def get(cls, model_id):
        if hasattr(cls, str(model_id)):
            return getattr(cls, model_id)
        return None

    @classmethod
    def set(cls, model, model_id=None):
        if not model_id:
            model_id = str(cls._generate_id())
            while hasattr(cls, model_id):
                model_id = str(cls._generate_id())
        elif hasattr(cls, model_id):
            return None
        setattr(cls, str(model_id), model)
        return str(model_id)

    @classmethod
    def update(cls, data, model_id):
        model = cls.get(model_id)
        if model: model.load(data)

    @classmethod
    def set_default_data(cls, scalar: int, length: int):
        if length >= 0:
            setattr(cls, "default_data_x", [i for i in range(length)])
            setattr(cls, "default_data_y", [i * scalar for i in range(length)])

    @classmethod
    def get_default_data(cls):
        if not hasattr(cls, "default_data_x") or not hasattr(cls, "default_data_y"):
            cls.set_default_data(0, 0)
        return getattr(cls, "default_data_x"), getattr(cls, "default_data_y")

    @classmethod
    def read_from_database(cls, db_name):

        sql = 'SELECT * FROM ' + db_name
        conn, cursor = cls.get_cursor()
        cursor.execute(sql)
        res = cursor.fetchall()
        conn.close()
        return res

    @classmethod
    def insert_xy(cls, x, y):
        sql = 'INSERT INTO xy (x, y) VALUES ' + (x, y).__str__()
        conn, cursor = cls.get_cursor()
        cursor.execute(sql)

        conn.commit()
        conn.close()

    @classmethod
    def get_cursor(cls):
        dbTasks = connector.connect(
            host="127.0.0.1",
            port=3306,
            user="root",
            password="passwordForRoot",
            database="FogBus2_Federated_Learning")
        cursor = dbTasks.cursor()

        return dbTasks, cursor

    @classmethod
    def clear(cls):
        conn, cursor = cls.get_cursor()
        sql = 'DELETE from xy'
        cursor.execute(sql)
        conn.commit()
        conn.close()

    @classmethod
    def get_cv1_data(cls, file_idx=0, role="train"):

        dir_path = os.path.dirname(inspect.getsourcefile(data_warehouse))+"/cv_data/"
        file_name = None
        if role == "train":
            file_name = "cv1_train_"+str(file_idx)+".txt"
        if role == "test":
            file_name = "cv1_test.txt"
        f = open(dir_path+file_name, "rb")
        d = pickle.loads(f.read())
        f.close()
        return d



