import platform
import psutil

def get_cpu_info():
    if platform.system() == 'Darwin' or platform.system() == 'Linux':
        try:
        	cpu_info = psutil.cpu_times_percent()
        	cpu_times_user = cpu_info[0]
        	cpu_times_system = cpu_info[2]
        	cpu_times_idle = cpu_info[3]
        except Exception as ex:
            return False
    else:
        return False
    return {'cpu_manufactory': platform.machine(),
            'cpu_model': platform.processor(),
            'cpu_time_user': cpu_times_user,
            'cpu_time_system': cpu_times_system,
            'cpu_time_idle': cpu_times_idle}

def get_mem_info():
	try:
		mem_info = psutil.virtual_memory()
		mem_total = mem_info[0]
		mem_available = mem_info[1]
		mem_percent = mem_info[2]
		mem_used = mem_info[3]
		mem_free = mem_info[4]
		mem_buffers = mem_info[7]
		mem_cached = mem_info[8]
		mem_shared = mem_info[9]
	except Exception as ex:
		return False;
	return {'mem_total': mem_total,
		'mem_available': mem_available,
		'mem_percent': mem_percent,
		'mem_used': mem_used,
		'mem_free': mem_free,
		'mem_buffers': mem_buffers,
		'mem_cached': mem_cached,
		'mem_shared': mem_shared}
def get_disk_info():
	try:
		disk_info = psutil.disk_usage('.')
		disk_total = disk_info[0]
		disk_used = disk_info[1]
		disk_free = disk_info[2]
		disk_percent = disk_info[3]
	except Exception as ex:
		return False;
	return {'disk_total': disk_total,
		'disk_used': disk_used,
		'disk_free': disk_free,
		'disk_percent': disk_percent}
def activate():
    return get_cpu_information()