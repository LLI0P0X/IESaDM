from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

# Создаем базу данных (в данном случае используется SQLite)
engine = create_engine('sqlite:///apkexport.db', echo=False)

# Базовый класс для моделей
Base = declarative_base()


# Таблица для фреймов
class Frame(Base):
    __tablename__ = 'frames'
    FrameID = Column(Integer, primary_key=True)
    FrameName = Column(String(100), nullable=False)
    ParentFrameID = Column(Integer, ForeignKey('frames.FrameID'))
    FrameType = Column(String(50), nullable=False)

    # Связь с родительским фреймом
    parent = relationship("Frame", remote_side=[FrameID], back_populates="children")
    children = relationship("Frame", back_populates="parent")

    # Связь со слотами
    slots = relationship("Slot", back_populates="frame")


# Таблица для слотов
class Slot(Base):
    __tablename__ = 'slots'
    SlotID = Column(Integer, primary_key=True)
    FrameID = Column(Integer, ForeignKey('frames.FrameID'), nullable=False)
    SlotName = Column(String(100), nullable=False)
    SlotValue = Column(Text)

    # Связь с фреймом
    frame = relationship("Frame", back_populates="slots")


# Создаем таблицы в базе данных
Base.metadata.create_all(engine)

# Создаем сессию для работы с базой данных
Session = sessionmaker(bind=engine)
session = Session()


# Заполняем фреймы и слоты данными
def populate_database():
    # Уровень 1: Продукция АПК
    product_frame = Frame(FrameID=1, FrameName="Продукция АПК", FrameType="Категория")
    session.add(product_frame)
    session.commit()

    # Слоты для фрейма "Продукция АПК"
    session.add_all([
        Slot(FrameID=1, SlotName="Тип продукции", SlotValue="Сельскохозяйственная продукция"),
        Slot(FrameID=1, SlotName="Примеры", SlotValue="Зерно, мясо, молоко")
    ])
    session.commit()

    # Уровень 2: Страны-импортеры
    country_frame = Frame(FrameID=2, FrameName="Страны-импортеры", ParentFrameID=1, FrameType="Страна")
    session.add(country_frame)
    session.commit()

    # Слоты для фрейма "Страны-импортеры"
    session.add_all([
        Slot(FrameID=2, SlotName="Название страны", SlotValue="Китай"),
        Slot(FrameID=2, SlotName="Объем импорта", SlotValue="10 млн тонн")
    ])
    session.commit()

    # Уровень 3: Цепочки поставок
    supply_chain_frame = Frame(FrameID=3, FrameName="Цепочки поставок", ParentFrameID=2, FrameType="Цепочка")
    session.add(supply_chain_frame)
    session.commit()

    # Слоты для фрейма "Цепочки поставок"
    session.add_all([
        Slot(FrameID=3, SlotName="Этапы", SlotValue="Производство, Транспортировка, Складирование"),
        Slot(FrameID=3, SlotName="Участники", SlotValue="Производители, Перевозчики, Склады")
    ])
    session.commit()

    # Уровень 3: Финансовые потоки
    financial_flow_frame = Frame(FrameID=4, FrameName="Финансовые потоки", ParentFrameID=1, FrameType="Финансы")
    session.add(financial_flow_frame)
    session.commit()

    # Слоты для фрейма "Финансовые потоки"
    session.add_all([
        Slot(FrameID=4, SlotName="Объем инвестиций", SlotValue="500 млн долларов"),
        Slot(FrameID=4, SlotName="Налоговые льготы", SlotValue="До 20% от стоимости экспорта")
    ])
    session.commit()

    # Уровень 3: Участники экспорта
    participants_frame = Frame(FrameID=5, FrameName="Участники экспорта", ParentFrameID=1, FrameType="Участник")
    session.add(participants_frame)
    session.commit()

    # Слоты для фрейма "Участники экспорта"
    session.add_all([
        Slot(FrameID=5, SlotName="Производители", SlotValue="Крупные агрохолдинги"),
        Slot(FrameID=5, SlotName="Перевозчики", SlotValue="Международные логистические компании")
    ])
    session.commit()


# Пример запроса для получения данных
def query_data():
    # Получаем все фреймы
    frames = session.query(Frame).all()
    for frame in frames:
        print(f"Фрейм: {frame.FrameName} (Тип: {frame.FrameType})")
        for slot in frame.slots:
            print(f"  Слот: {slot.SlotName} -> {slot.SlotValue}")

if __name__ == '__main__':

    # Заполняем базу данных
    populate_database()
    # Выполняем запрос
    query_data()
