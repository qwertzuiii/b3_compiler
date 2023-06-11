def _get_argument_index(arg_list, arg_name):
    try:
        index = arg_list.index(arg_name)
    except ValueError:
        return None

    if len(arg_list) - 1 < index + 1:
        return None
    else:
        return index + 1
    
def _check_argument_exists(arg_list, arg_name):
    try:
        index = arg_list.index(arg_name)
    except ValueError:
        return False

    return True


class console:
    def __init__(self, prefix=""):
        self.prefix = prefix

    def print(self, *args):
        print(self.prefix, *args)