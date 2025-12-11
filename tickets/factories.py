import factory
from factory import SubFactory, faker
from tickets.models import Employee, ActionType, CategoryType, Office, Action, Attachment, Task
import random
import decimal

class ActionTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ActionType
    
    name = factory.Sequence(lambda n: f"action {n}")
    description = factory.Sequence(lambda n: f"Description for action {n}")

class CategoryTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CategoryType
    name = factory.Sequence(lambda n: f"category {n}")
    description = factory.Sequence(lambda n: f"Description for action {n}")

class EmployeeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Employee
    first_name = factory.faker.Faker('first_name', locale = 'it_IT')
    second_name = factory.faker.Faker('last_name', locale = 'it_IT')
    surname = "Alekseevich"
    email = factory.Sequence(lambda n: f'employee{n}@example.com')
    office = SubFactory('tickets.factories.OfficeFactory')
    role = factory.LazyFunction(lambda: random.choice(["role_1", "role_2", "role_3"]))
    parent = None

class OfficeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Office
    name = factory.Sequence(lambda n: f"Офис под номер {n}")
    parent = None
    address = factory.faker.Faker('address')
    type = random.choice(['Офис уровня 1', 'Офис уровня 2', 'Офис уровня 3'])
    work_time = random.choice(['9:00 - 20:00', '8:00 - 21:00', '00:00 - 24:00'])
    @factory.post_generation
    def main_worker(self, create, extracted, **kwargs):
        if create:
            self.main_worker = EmployeeFactory(office = self)


class TaskFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Task
    title = factory.Sequence(lambda n: f"title for task {n}")
    problem = factory.Sequence(lambda n: f"Problem for task {n}")
    author = SubFactory('tickets.factories.EmployeeFactory')
    worker = SubFactory('tickets.factories.EmployeeFactory')
    priority = factory.Sequence(lambda n: f"priority {n}")
    office = SubFactory('tickets.factories.OfficeFactory')
    status = random.choice(Task.STATUS_CHOICES)
    actual_cost = decimal.Decimal(random.randrange(10000))/100


