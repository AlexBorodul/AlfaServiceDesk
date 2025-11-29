import factory
from factory import SubFactory
from tickets.models import Employee, ActionType, CategoryType, Office, Action, Attachment, Task
from faker import Faker
import random
import decimal

fake = Faker()

class ActionTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ActionType
    
    name = factory.Sequence(lambda n: "action {}".format(n))
    description = factory.Sequence(lambda n: "Description for action {}".format(n))

class CategoryTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CategoryType
    name = factory.Sequence(lambda n: "category {}".format(n))
    description = factory.Sequence(lambda n: "Description for action {}".format(n))

class EmployeeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Employee
    first_name, second_name = fake.name().split(' ')
    surname = "Alekseevich"
    email = factory.Sequence(lambda n: f'employee{n}@example.com')
    office = SubFactory('tickets.factories.OfficeFactory')
    role = random.choice(["role_1", "role_2", "role_3"])
    parent = None

class OfficeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Office
    name = factory.Sequence(lambda n: "Офис под номер {}".format(n))
    parent = None
    address = fake.address()
    type = random.choice(['Офис уровня 1', 'Офис уровня 2', 'Офис уровня 3'])
    work_time = random.choice(['9:00 - 20:00', '8:00 - 21:00', '00:00 - 24:00'])
    @factory.post_generation
    def main_worker(self, create, extracted, **kwargs):
        if create and extracted:
            self.main_worker = EmployeeFactory(office = self)



class TaskFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Task
    title = factory.Sequence(lambda n: "title for task {}".format(n))
    problem = factory.Sequence(lambda n: "Problem for task {}".format(n))
    author = SubFactory('tickets.factories.EmployeeFactory')
    worker = SubFactory('tickets.factories.EmployeeFactory')
    priority = factory.Sequence(lambda n: "priority {}".format(n))
    office = SubFactory('tickets.factories.OfficeFactory')
    status = random.choice(Task.STATUS_CHOICES)
    actual_cost = decimal.Decimal(random.randrange(10000))/100


