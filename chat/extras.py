from django.utils import timezone

def get_local_time():
    return timezone.localtime(timezone.now())

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1]
    else:
        ip = request.META.get('REMOTE_ADDR')
    request.session['client_ip'] = ip
    return ip
