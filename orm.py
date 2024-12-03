from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import insert, CheckConstraint, update, select, delete
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase, Mapped, mapped_column

import asyncio
import datetime
import os
import sqlalchemy

a = [('Fish', 2018, 5054.0, 1117.0, 599.0, 3178.62, 2238.0, 0.8),
     ('Fish', 2019, 4983.0, 1086.0, 647.0, 3256.86, 2118.0, 0.8),
     ('Fish', 2020, 4975.0, 1143.0, 606.0, 3095.83, 2400.0, 0.85),
     ('Fish', 2021, 5053.0, 1148.0, 700.0, 3287.57, 2200.0, 0.85),
     ('Fish', 2022, 4920.0, 1161.0, 555.0, 2976.41, 2300.0, 0.85),
     ('Fish', 2023, 5369.0, 1176.0, 656.0, 3279.78, 2500.0, 0.85),
     ('Potato', 2018, 22395.0, 16838.3, 1257.3, 23494.6, 268.1, 0.95),
     ('Potato', 2019, 22074.9, 16727.9, 759.9, 23201.3, 463.6, 0.95),
     ('Potato', 2020, 19607.2, 15897.8, 748.8, 21981.0, 556.4, 0.95),
     ('Potato', 2021, 17958.9, 13716.4, 1016.1, 20257.6, 246.8, 0.95),
     ('Potato', 2022, 18800.0, 13716.4, 1016.1, 20257.6, 246.8, 0.95),
     ('Potato', 2023, 20200.0, 13716.4, 1016.1, 20257.6, 246.8, 0.95),
     ('Milk', 2018, 30611.1, 1638.9, 6493.0, 36486.6, 576.3, 0.9),
     ('Milk', 2019, 31360.4, 1680.1, 6727.8, 37358.4, 611.0, 0.9),
     ('Milk', 2020, 32225.1, 1798.9, 7044.4, 38348.5, 707.2, 0.9),
     ('Milk', 2021, 32339.6, 2012.7, 6889.5, 38351.9, 806.2, 0.9),
     ('Milk', 2022, 32983.78, 2012.7, 6889.5, 38351.9, 806.2, 0.9),
     ('Milk', 2023, 33810.64, 2012.7, 6889.5, 38351.9, 806.2, 0.9),
     ('Meat', 2018, 10629.7, 862.0, 879.7, 11105.0, 354.4, 0.85),
     ('Meat', 2019, 10866.5, 912.0, 771.8, 11157.4, 415.3, 0.85),
     ('Meat', 2020, 11222.0, 977.6, 648.0, 11206.4, 609.0, 0.85),
     ('Meat', 2021, 11346.0, 1032.2, 620.8, 11375.3, 633.6, 0.85),
     ('Meat', 2022, 11346.0, 1032.2, 620.8, 11375.3, 633.6, 0.85),
     ('Meat', 2023, 11346.0, 1032.2, 620.8, 11375.3, 633.6, 0.85),
     ('Grain', 2018, 113.3, 90.7, 0.4, 77.0, 54.83, 0.95),
     ('Grain', 2019, 121.2, 72.6, 0.3, 77.9, 39.3, 0.95),
     ('Grain', 2020, 133.4, 76.9, 0.4, 80.6, 48.5, 0.95),
     ('Grain', 2021, 121.4, 81.6, 0.2, 81.9, 42.8, 0.95),
     ('Grain', 2022, 157.6, 81.6, 0.2, 81.9, 50.5, 0.95),
     ('Grain', 2023, 145.0, 81.6, 0.2, 81.9, 79.9, 0.95),
     ('Сonfectionery', 2018, 3914.0, 110.0, 180.0, 3630.0, 510.0, 0.0),
     ('Сonfectionery', 2019, 4016.0, 140.0, 200.0, 3600.0, 590.0, 0.0),
     ('Сonfectionery', 2020, 3892.0, 120.0, 200.0, 3450.0, 660.0, 0.0),
     ('Сonfectionery', 2021, 4073.0, 110.0, 210.0, 3250.0, 820.0, 0.0),
     ('Сonfectionery', 2022, 3990.0, 120.0, 240.0, 2910.0, 720.0, 0.0),
     ('Сonfectionery', 2023, 3990.0, 120.0, 250.0, 2830.0, 850.0, 0.0),
     ('Sugar', 2018, 6273.0, 230.0, 320.0, 3320.0, 380.0, 0.8),
     ('Sugar', 2019, 7264.0, 790.0, 230.0, 3380.0, 640.0, 0.8),
     ('Sugar', 2020, 5796.0, 490.0, 170.0, 3280.0, 990.0, 0.9),
     ('Sugar', 2021, 5931.0, 540.0, 140.0, 3210.0, 470.0, 0.9),
     ('Sugar', 2022, 6037.0, 800.0, 50.0, 3110.0, 520.0, 0.9),
     ('Sugar', 2023, 6037.0, 840.0, 40.0, 3080.0, 640.0, 0.9),
     ('Seed oil', 2018, 5.94, 0.92, 1.33, 1.74, 2.11, 0.85),
     ('Seed oil', 2019, 6.77, 0.58, 1.4, 2.34, 3.1, 0.85),
     ('Seed oil', 2020, 7.45, 0.14, 1.36, 2.68, 3.2, 0.9),
     ('Seed oil', 2021, 6.74, 0.45, 1.08, 2.46, 3.41, 0.9),
     ('Seed oil', 2022, 8.14, 0.31, 0.95, 3.43, 3.18, 0.9),
     ('Seed oil', 2023, 8.14, 0.07, 0.91, 3.58, 3.74, 0.9)]
categoryList = ['Fish', 'Potato', 'Milk', 'Meat', 'Grain', 'Сonfectionery', 'Sugar', 'Seed oil']

database_url = f"sqlite+aiosqlite:///village.db"


class Base(DeclarativeBase):
    pass


engine = create_async_engine(
    url=database_url,
    echo=False,
)


class Village(Base):
    __tablename__ = 'village'

    _id: Mapped[int] = mapped_column(primary_key=True)
    category: Mapped[str]
    year: Mapped[int | None]
    production: Mapped[float | None]
    reserve: Mapped[float | None]
    importsmth: Mapped[float | None]
    dom_consumption: Mapped[float | None]
    export: Mapped[float | None]
    doctrine: Mapped[float | None]

    __table_args__ = (
        CheckConstraint('year >= 2015 AND year <= 2025', name='check_year_range'),
        CheckConstraint('production >= 0', name='check_production_positive'),
        CheckConstraint('reserve >= 0', name='check_reserve_positive'),
        CheckConstraint('importsmth >= 0', name='check_importsmth_positive'),
        CheckConstraint('dom_consumption >= 0', name='check_dom_consumption_positive'),
        CheckConstraint('export >= 0', name='check_export_positive'),
        CheckConstraint('doctrine >= 0', name='check_doctrine_positive'),
    )


async def remove_duplicate_names():
    async with engine.begin() as conn:
        res = await conn.execute(
            select(Village._id).group_by(Village.category, Village.year).having(sqlalchemy.func.count() > 1)
        )
        dup = res.fetchall()
        for i in dup:
            await conn.execute(delete(Village).where(Village._id == i[0]))
        return len(dup)


async def remove_all_duplicate_names():
    _l = 1
    while _l:
        _l = await remove_duplicate_names()


async def check_nones():
    async with engine.begin() as conn:
        result = await conn.execute(select(Village).where(
            Village.year is None | Village.production is None | Village.reserve is None | Village.importsmth is None |
            Village.doctrine is None | Village.dom_consumption is None | Village.export is None))
        for row in result:
            print(row)


async def check_names():
    async with engine.begin() as conn:
        result = await conn.execute(select(Village).where(not (Village.category in categoryList)))
        for row in result:
            print(row)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def remove_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def insert_village(village):
    async with engine.begin() as conn:
        await conn.execute(insert(Village).values(category=village[0], year=village[1], production=village[2],
                                                  reserve=village[3], importsmth=village[4], dom_consumption=village[5],
                                                  export=village[6], doctrine=village[7]))


async def select_villages():
    async with engine.begin() as conn:
        result = await conn.execute(select(Village))
        for row in result:
            print(row)


async def main():
    await remove_tables()
    await create_tables()
    for i in range(len(a)):
        await insert_village(a[i])
    await remove_all_duplicate_names()
    await select_villages()


if __name__ == "__main__":
    asyncio.run(main())
