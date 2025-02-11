from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean, Float, Date
from sqlalchemy.dialects.postgresql import JSONB, UUID
from uuid import uuid4
from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

base = declarative_base()


class TypeUser(base):
    __tablename__ = "type_user"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(32), nullable=False, unique=True)
    description = Column(String(128), nullable=True)


class Profession(base):
    __tablename__ = "profession"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(String(128), nullable=True)


class User(base):
    __tablename__ = "user"
    id = Column(Integer, autoincrement=True, primary_key=True)
    uuid = Column(UUID(as_uuid=True), unique=True, default=uuid4())

    name = Column(String, nullable=True)
    surname = Column(String, nullable=True)
    patronymic = Column(String, nullable=True)

    email = Column(String, nullable=True, unique=True)
    password_hash = Column(String, nullable=True)
    id_type = Column(Integer, ForeignKey("type_user.id"))
    id_profession = Column(Integer, ForeignKey("profession.id"))
    type = relationship("TypeUser", lazy="joined")
    profession = relationship("Profession", lazy="joined")

    is_deleted = Column(Boolean, nullable=True, default=False)

    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, val: str):
        self.password_hash = generate_password_hash(val)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


class Document(base):
    __tablename__ = "document"
    id = Column(Integer, autoincrement=True, primary_key=True)
    uuid = Column(UUID(as_uuid=True), unique=True, default=uuid4)
    name = Column(String(32), unique=True, nullable=False)
    url_document = Column(String, nullable=False)
    data_create = Column(DateTime, nullable=False, default=datetime.now())
    description = Column(Text, nullable=True)

    users_document = relationship("UserToDocument", lazy="joined")


class UserToDocument(base):
    __tablename__ = "user_to_document"
    id_document = Column(ForeignKey("document.id"), primary_key=True)
    id_user = Column(ForeignKey("user.id"), primary_key=True)
    user = relationship("User", lazy="joined")
    datetime_view = Column(DateTime, default=datetime.now())


class StateObject(base):
    __tablename__ = "state_object"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(String(128), nullable=True)


class TypeEquipment(base):
    __tablename__ = "type_equipment"
    id = Column(Integer, autoincrement=True, primary_key=True)
    code = Column(String, unique=True, nullable=False)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(String(128), nullable=True)


class Object(base):
    __tablename__ = "object"
    id = Column(Integer, autoincrement=True, primary_key=True)
    uuid = Column(UUID(as_uuid=True), unique=True, default=uuid4)
    name = Column(String(256), nullable=False)
    address = Column(String(256), nullable=False)
    cx = Column(Float, nullable=True, default=0.0)
    cy = Column(Float, nullable=True, default=0.0)
    description = Column(Text, nullable=True)
    counterparty = Column(String(256), nullable=False)
    id_state = Column(ForeignKey("state_object.id"))
    state = relationship("StateObject", lazy="joined")
    equipment = relationship("Equipment", cascade="all, delete")
    staff = relationship(User, secondary="object_to_user")

    is_deleted = Column(Boolean, nullable=True, default=False)


class Equipment(base):
    __tablename__ = "equipment"
    id = Column(Integer, autoincrement=True, primary_key=True)
    uuid = Column(UUID(as_uuid=True), unique=True, default=uuid4)
    id_object = Column(ForeignKey("object.id"))
    name = Column(String(256), nullable=False)
    code = Column(String, nullable=True, unique=True)
    id_type = Column(ForeignKey("type_equipment.id"))
    type = relationship("TypeEquipment", lazy="joined")
    description = Column(Text, nullable=True)
    characteristics = Column(JSONB, nullable=True)


class ObjectToUser(base):
    __tablename__ = "object_to_user"
    id_object = Column(ForeignKey("object.id"), primary_key=True)
    id_user = Column(ForeignKey("user.id"), primary_key=True)


class ClassBrake(base):
    __tablename__ = "class_brake"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String, unique=True, nullable=False, default="1.1")
    description = Column(String, nullable=True)


class TypeBrake(base):
    __tablename__ = "type_brake"
    id = Column(Integer, autoincrement=True, primary_key=True)
    code = Column(String, unique=True, nullable=False, default="1.1")
    name = Column(String, nullable=False)
    id_type = Column(ForeignKey("class_brake.id"))
    type = relationship(ClassBrake, lazy="joined")


class StateEvent(base):
    __tablename__ = "state_event"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String, unique=True, nullable=False, default="")
    description = Column(String, nullable=True)


class TypeEvent(base):
    __tablename__ = "type_event"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String, unique=True, nullable=False, default="")
    description = Column(String, nullable=True)


class Event(base):
    __tablename__ = "event"
    id = Column(Integer, autoincrement=True, primary_key=True)
    uuid = Column(UUID(as_uuid=True), unique=True, default=uuid4)
    description = Column(Text, nullable=False)
    date_finish = Column(Date, nullable=False)

    id_accident = Column(ForeignKey("accident.id"))
    accident = relationship("Accident", lazy="joined")

    id_state_event = Column(ForeignKey("state_event.id"))
    state_event = relationship(StateEvent, lazy="joined")

    id_type_event = Column(ForeignKey("type_event.id"))
    type_event = relationship(TypeEvent, lazy="joined")


class Accident(base):
    __tablename__ = "accident"
    id = Column(Integer, autoincrement=True, primary_key=True)
    uuid = Column(UUID(as_uuid=True), unique=True, default=uuid4)

    id_object = Column(ForeignKey("object.id"))
    object = relationship(Object, lazy="joined")

    damaged_equipment = relationship(Equipment, secondary="equipment_to_accident", lazy="joined")

    datetime_start = Column(DateTime(timezone=True), nullable=False)
    datetime_end = Column(DateTime(timezone=True), nullable=True)

    type_brakes = relationship(TypeBrake, secondary="type_brake_to_accident", lazy="joined")

    time_line = Column(MutableDict.as_mutable(JSONB), nullable=False)

    causes_of_the_emergency = Column(Text, nullable=False)
    damaged_equipment_material = Column(Text, nullable=False)

    event = relationship(Event, back_populates="accident", lazy="joined")

    additional_material = Column(String, unique=True, nullable=True)


class TypeBrakeToAccident(base):
    __tablename__ = "type_brake_to_accident"
    id_accident = Column(ForeignKey("accident.id"), primary_key=True)
    id_type_brake = Column(ForeignKey("type_brake.id"), primary_key=True)


class EquipmentToAccident(base):
    __tablename__ = "equipment_to_accident"
    id_accident = Column(ForeignKey("accident.id"), primary_key=True)
    id_equipment = Column(ForeignKey("equipment.id"), primary_key=True)

