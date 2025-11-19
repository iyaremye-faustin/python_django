from django.db import migrations

def create_default_roles(apps, schema_editor):
    Role = apps.get_model('accounts', 'Role')

    roles = [
        'SuperAdmin',
        'Manager',
        'Staff',
        'Agent',
    ]

    for role in roles:
        Role.objects.get_or_create(name=role)


def delete_default_roles(apps, schema_editor):
    Role = apps.get_model('accounts', 'Role')
    Role.objects.filter(name__in=[
        'SuperAdmin',
        'Manager',
        'Staff',
        'Agent',
    ]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_department_created_at_department_updated_at_and_more'),
    ]

    operations = [
        migrations.RunPython(create_default_roles, delete_default_roles),
    ]
