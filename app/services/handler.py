import psutil
import GPUtil
import cpuinfo


class AppHandler:
    @staticmethod
    async def get_node_info():
        cpu_name = cpuinfo.get_cpu_info()['brand_raw']
        memory = AppHandler.get_size(psutil.virtual_memory().total)
        disk = AppHandler.get_size(psutil.disk_usage('/').free)
        gpu = GPUtil.getGPUs()[0].name

        return {
            "cpu": cpu_name,
            "memory": memory,
            "disk": disk,
            "gpu": gpu,
            "status": "online",
            "version": "0.0.1",
            "description": "CGP_worker",
        }

    @staticmethod
    def get_size(bytes, suffix="B"):
        factor = 1024
        for unit in ["", "K", "M", "G", "T", "P"]:
            if bytes < factor:
                return f"{bytes:.2f}{unit}{suffix}"
            bytes /= factor
