from django.db import migrations
from django.conf import settings
from django.contrib.auth.hashers import make_password


def create_superadmin_with_profile(apps, schema_editor):
    app_label, model_name = settings.AUTH_USER_MODEL.split('.')
    User = apps.get_model(app_label, model_name)

    Role = apps.get_model('accounts', 'Role')
    Profile = apps.get_model('accounts', 'Profile')

    superadmin_role, _ = Role.objects.get_or_create(name='SuperAdmin')

    username = 'superadmin'
    email = 'superadmin@example.com'
    raw_password = 'test@me.com123'

    user, created = User.objects.get_or_create(
        username=username,
        defaults={
            'email': email,
            'is_staff': True,
            'is_superuser': True,
            'is_active': True,
            'password': make_password(raw_password),
        },
    )

    updated = False
    if not user.is_superuser:
        user.is_superuser = True
        updated = True
    if not user.is_staff:
        user.is_staff = True
        updated = True
    if not user.is_active:
        user.is_active = True
        updated = True
    if updated:
        user.save()

    profile, _ = Profile.objects.get_or_create(
        user=user,
        defaults={
            'phone': '0788223250',
            'department': None,
            'role': superadmin_role,
        },
    )

    if profile.role != superadmin_role:
        profile.role = superadmin_role
        profile.save()


def delete_superadmin_with_profile(apps, schema_editor):
    app_label, model_name = settings.AUTH_USER_MODEL.split('.')
    User = apps.get_model(app_label, model_name)
    Profile = apps.get_model('accounts', 'Profile')

    username = 'superadmin'

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return

    Profile.objects.filter(user=user).delete()
    user.delete()


class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0003_seed_roles'),
    ]

    operations = [
        migrations.RunPython(create_superadmin_with_profile, delete_superadmin_with_profile),
    ]
