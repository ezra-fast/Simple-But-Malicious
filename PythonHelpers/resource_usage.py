# This program will print resource usage statistics of the local machine to the console; if a single process is specified by name, it will list the results for each instance of that process.

# print(f'CPU Utilization Over 5 Seconds: {psutil.cpu_percent(interval=5, percpu=False)}')

import argparse
import psutil

def command_parser():
    parser = argparse.ArgumentParser(
        prog='resource_usage_per_process',
        description='Per Process (PID and Name), list CPU and Memory Usage',
        epilog='No options: list all processes; -name option: list that processes resource utilization.')

    parser.add_argument('-n', '--name')      # option that takes a value

    prelim_args = parser.parse_args()
    args = []
    args.append(prelim_args.name)
    return args

def resource_usage_per_process():
    iterator = psutil.process_iter(['pid', 'name'])
    for process in iterator:
        try:
            print(f"PID: {process.pid} Name: {process.info['name']}", end='')
            current_process = psutil.Process(process.pid)
            memory_tuple = current_process.memory_info()
            if (current_process.cpu_percent(interval=0.5) > 100.0):
                print(f" CPU Usage: [psutil calculation error] Memory Usage: {memory_tuple.rss / 1048576} MB")
            else:
                print(f" CPU Usage: {current_process.cpu_percent(interval=0.5)} Memory Usage: {memory_tuple.rss / 1048576} MB")
        except KeyboardInterrupt:
            exit(0)
    
def resources_by_name(name):
    iterator = psutil.process_iter(['name'])
    named_processes = []
    for process in iterator:
        try:
            if (process.info['name'] == name):
                print(f"PID: {process.pid} Name: {process.info['name']}", end='')
                current_process = psutil.Process(process.pid)
                memory_tuple = current_process.memory_info()
                print(f" CPU Usage: {current_process.cpu_percent(interval=0.5)} Memory Usage: {memory_tuple.rss / 1048576} MB")
                named_processes.append(process)
        except KeyboardInterrupt:
            exit(0)
    if len(named_processes) < 1:
        print(f'\nThere are no instances of {name}\n')
def main():
    args = command_parser()
    if len(args) > 1:
        resources_by_name(args[0])
    else:
        resource_usage_per_process()
    
main()