# pip install wmi 필요
import wmi

def getCondition():

    computer = wmi.WMI()

    os_info = computer.Win32_OperatingSystem()[0]
    cpu_info = computer.Win32_Processor()[0]
    gpu_info = computer.Win32_VideoController()[0]

    system_ram = round(float(os_info.TotalVisibleMemorySize) / 1048576)  # KB to GB


    cpu_spec = 'CPU : {0}'.format(cpu_info.Name)
    gpu_spec = 'GPU : {0}'.format(gpu_info.Name)
    ram_spec = 'RAM : {0} GB'.format(system_ram)

    return cpu_spec + "\n" + gpu_spec + "\n" + ram_spec