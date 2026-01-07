"""
Management command to link a User account to an Employee record.
Usage: python manage.py link_user_to_employee <username> [--create-employee]
"""
from django.core.management.base import BaseCommand, CommandError
from tickets.models import User, Employee, Office


class Command(BaseCommand):
    help = 'Link a User account to an Employee record'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username to link')
        parser.add_argument(
            '--create-employee',
            action='store_true',
            help='Create a new Employee record if one does not exist',
        )
        parser.add_argument(
            '--employee-id',
            type=int,
            help='ID of existing Employee to link',
        )
        parser.add_argument(
            '--first-name',
            type=str,
            help='First name for new Employee (required if --create-employee)',
        )
        parser.add_argument(
            '--email',
            type=str,
            help='Email for new Employee (required if --create-employee)',
        )
        parser.add_argument(
            '--role',
            type=str,
            choices=['employee', 'worker', 'admin'],
            default='admin',
            help='Role for new Employee (default: admin)',
        )

    def handle(self, *args, **options):
        username = options['username']
        
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise CommandError(f'User "{username}" does not exist')

        # Check if user already has an employee
        if user.employee:
            self.stdout.write(
                self.style.WARNING(
                    f'User "{username}" is already linked to Employee: {user.employee}'
                )
            )
            return

        # Link to existing employee
        if options['employee_id']:
            try:
                employee = Employee.objects.get(id=options['employee_id'])
                user.employee = employee
                user.save()
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Successfully linked User "{username}" to Employee: {employee}'
                    )
                )
                return
            except Employee.DoesNotExist:
                raise CommandError(f'Employee with ID {options["employee_id"]} does not exist')

        # Create new employee
        if options['create_employee']:
            if not options['first_name']:
                raise CommandError('--first-name is required when using --create-employee')
            if not options['email']:
                raise CommandError('--email is required when using --create-employee')

            # Check if email already exists
            if Employee.objects.filter(email=options['email']).exists():
                raise CommandError(f'Employee with email "{options["email"]}" already exists')

            # Get first office if available
            office = Office.objects.first()

            employee = Employee.objects.create(
                first_name=options['first_name'],
                email=options['email'],
                role=options['role'],
                office=office,
            )

            user.employee = employee
            user.save()

            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully created Employee "{employee}" and linked to User "{username}"'
                )
            )
            return

        # No action specified
        self.stdout.write(
            self.style.ERROR(
                'No action specified. Use --create-employee to create a new Employee '
                'or --employee-id to link to an existing Employee.'
            )
        )
        self.stdout.write('\nAvailable Employees:')
        for emp in Employee.objects.all()[:10]:
            self.stdout.write(f'  ID: {emp.id}, Name: {emp.first_name} {emp.surname or ""}, Email: {emp.email}')
