import random
import string

PRIVATE_IPS_PREFIX = ('10.', '172.', '192.', )

def randomString(stringLength=10, mode='uppercase'):
    """Generate a random string of fixed length """
    if(mode == 'uppercase'):
        letters = string.ascii_uppercase + string.digits
    else:
        letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))
       

def get_client_ip(request):
    remote_address = request.META.get('HTTP_X_FORWARDED_FOR') or request.META.get('REMOTE_ADDR')
    ip = remote_address
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        proxies = x_forwarded_for.split(',')
        while (len(proxies) > 0 and proxies[0].startswith(PRIVATE_IPS_PREFIX)):
            proxies.pop(0)
            if len(proxies) > 0:
                ip = proxies[0]
                print("IP Address ",ip)
        return ip