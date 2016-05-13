__author__ = 'zinwnas'

from rolepermissions.permissions import register_object_checker
from project_mytif.roles import Doctor, Nurse

@register_object_checker()
def access_clinic(role, user, clinic):
    if role == Doctor:
        return True

    if user.clinic == clinic:
        return True

    return False