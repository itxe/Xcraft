import platform


def get_cpu_information():
    if platform.system() == 'Darwin':
        try:
            import psutil
            cpu_times_user = psutil.cpu_times_percent()['user']
            cpu_times_system = psutil.cpu_times_percent()['system']
            cpu_times_idle = psutil.cpu_times_percent()['idle']
        except Exception as ex:
            cpu_times_user = 0
            cpu_times_system = 0
            cpu_times_idle = 0
            return False
    elif platform.system() == 'Linux':
        try:
            import psutil
            cpu_times_user = psutil.cpu_times_percent()['user']
            cpu_times_system = psutil.cpu_times_percent()['system']
            cpu_times_idle = psutil.cpu_times_percent()['idle']
        except Exception as ex:
            cpu_times_user = 0
            cpu_times_system = 0
            cpu_times_idle = 0
            return False
    else:
        cpu_times_user = 0
        cpu_times_system = 0
        cpu_times_idle = 0
        return False

    return {'cpu_manufactory': platform.machine(),
            'cpu_model': platform.processor(),
            'cpu_time_user': cpu_times_user,
            'cpu_time_system': cpu_times_system,
            'cpu_time_idle': cpu_times_idle}


def activate():
    return get_cpu_information()
