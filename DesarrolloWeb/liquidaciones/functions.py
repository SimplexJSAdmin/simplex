def get_modules(request):
    if request.user.is_authenticated:
        modules_names = [*map(lambda x: x.name, request.user.groups.all())]
        return modules_names
    else:
        return []

def block_load_file(preprocesos):
    if len(preprocesos)>0:
        return True
    return False