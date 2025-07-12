from django.shortcuts import HttpResponse

def allowed_user(allowed_roles = []):
    def decorator(view_func):
        def wrapper_funct(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.values_list('name', flat = True)
                if any(g in allowed_roles for g in group) :
                    return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('أنت غير مؤهل لزيارة هذه الصفحة.')
        return wrapper_funct
    return decorator