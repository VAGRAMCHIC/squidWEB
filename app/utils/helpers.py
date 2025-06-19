from flask_login import current_user
from flask_login.mixins import AnonymousUserMixin
from flask import redirect



def split_list(input_list, chunk_size):
    """
    Разбивает список на части указанного размера.
    
    :param input_list: Исходный список
    :param chunk_size: Размер каждой части
    :return: Список списков (частей исходного списка)
    """
    return [input_list[i:i + chunk_size] for i in range(0, len(input_list), chunk_size)]


def get_username():
    if isinstance(current_user, AnonymousUserMixin):
        return ""
        return redirect("account.login")
    else:
        return current_user.username
