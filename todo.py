from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
import datetime
from sqlalchemy.orm import sessionmaker
import random

Base = declarative_base()  # klasa Table, która opisuje tabele dziedziczy z klasy DeclarativeBase, która jest zwracana
# przez metodę declarative_base() i tą zwróconą klasę zapisujemy do zmiennej Base

class Table(Base):  # w tej klasie opisujemy naszą tabelę, zmienne w klasie to kolumny, wierszami naszej tabeli będą
    # kolejne instancje klasy Table
    iterator = 0
    __tablename__ = 'task'  # nazwa tabeli w bazie danych
    id = Column(Integer, primary_key=True)  # id to kolumna w tabeli typu int, primary key to unikalna wartość
    # identyfikująca jednoznacznie każdy rekord tabeli
    task = Column(String, default='default_value')  # kolumna typu string, default - domyślna wartość kolumny
    data = datetime.datetime.today().date()
    deadline = Column(Date, default=datetime.datetime.today())  # przechowuje date, SQLAlchemy automatycznie konwertuje
    # date z SQLa do Pythona (sposób w jaki ta data jest zapisywana)
    def __repr__ (self):
        return "{}".format(self.task)  # zwraca ciąg znaków reprezentujący obiekt klasy. # W koncepcji ORM każdy wiersz w tabeli jest obiektem klasy.

class Menu:
    def __init__(self):
        self.engine = create_engine('sqlite:///todo.db?check_same_thread=False')  # tworzymy tabelę w bazie danych
        # opisujemy tabelę w klasie Table
        Base.metadata.create_all(self.engine)  # po opisaniu tabeli w klasie Table tworzymy ją w bazie danych wywołując metodę
        # create_all i podając jako argument engine.create_all() generuje zapytania SQLa
        # według tego co wpisaliśmy w klasie Table
        # CREATE TABLE task (
        # id INTEGER,
        # task VARCHAR itd...

        Session = sessionmaker(bind=self.engine)  # teraz pozostaje nam tylko pracować z tabelą, musimy stworzyć w tym celu sesję
        self.session = Session()  # obiekt session to jedyne czego potrzebujemy aby zarządzać naszą bazą danych

    def menu(self):
        key = 1
        while key != 0:
            print("1) Today's tasks")
            print("2) Week's tasks")
            print("3) All tasks")
            print("4) Missed tasks")
            print("5) Add task")
            print("6) Delete task")
            print("0) Exit")
            key = int(input())
            print("")
            if key == 1:
                self.today_tasks()
            elif key == 2:
                self.weeks_tasks()
            elif key == 3:
                self.all_tasks()
            elif key == 4:
                self.missed_tasks()
            elif key == 5:
                self.add_task()
            elif key == 6:
                self.delete_task()
        print("Bye!")

    def print_task(self, tasks, date=False):
        if not tasks:
            print("Nothing to do!")
        else:
            i=1
            if date==False:
                for task in tasks:
                    print(f'{i}. {task}')
            else:
                for task in tasks:
                    print(f"{i}. {task}. {task.deadline.strftime('%d %b')}")
                    i += 1

    def missed_tasks (self):
        today = datetime.datetime.today()
        rows = self.session.query(Table).filter(Table.deadline < today.date()).order_by(Table.deadline).all()
        print("Missed tasks:")
        if not rows:
            print("Nothing is missed!")
        else:
            self.print_task(rows, True)
        print("")

    def delete_task (self):
        rows = self.session.query(Table).all()
        if not rows:
            print("Nothing to delete\n")
        else:
            print("Choose the number of the task you want to delete:")
            self.print_task(rows, True)
            task_to_delete = int(input())
            self.session.delete(rows[task_to_delete-1])
            self.session.commit()
            print("The task has been deleted!\n")

    def today_tasks(self):
        today = datetime.datetime.today()
        rows = self.session.query(Table).filter(Table.deadline == today.date()).all()
        if not rows:
            print(f"Today {datetime.datetime.today().strftime('%d %b')}:\nNothing to do!")
        else:
            print(f"Today {datetime.datetime.strptime(str(rows[0].data), '%Y-%m-%d').strftime('%d %b')}")
            self.print_task(rows)
        print("")

    def weeks_tasks(self):
        today = datetime.datetime.today()
        for x in range(7):
            rows = self.session.query(Table).filter(Table.deadline == today.date()+datetime.timedelta(days=x)).all()
            print(f"{(today.date() + datetime.timedelta(days=x)).strftime('%A %d %b')}:")
            self.print_task(rows)
            print("")

    def all_tasks (self):
        rows = self.session.query(Table).order_by(Table.deadline).all()
        print("All tasks:")
        self.print_task(rows, True)
        print("")

    def add_task (self):
        Table.iterator += 1
        task_name = " ".join(input("Enter task\n").split())
        deadline = datetime.datetime.strptime(input("Enter deadline\n"), '%Y-%m-%d')
        new_row = Table(task=task_name, data=datetime.datetime.today().date(),
                        deadline=deadline)
        self.session.add(new_row)
        self.session.commit()
        print("The task has been added!\n")

new_task = Menu()
new_task.menu()
