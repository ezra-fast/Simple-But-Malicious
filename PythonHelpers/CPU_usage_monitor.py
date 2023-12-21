# This script goes though running processes on the system and prints process name, pid, and CPU usage to the console if the latter is greater than 0.0.
# This script ignores the System Idle Process because psutil.cpu_percent() cannot handle it

import psutil

# def command_parser():
#     parser = argparse.ArgumentParser(
#         prog='CPU Percent Over Time (for PID)',
#         description='For Process (PID), list average CPU percent usage over X amount of time.',
#         epilog='python prog_name.py -p PID -t TIME IN SECONDS.')

#     parser.add_argument('-t', '--time')
#     parser.add_argument('-p', '--pid')      # option that takes a value

#     prelim_args = parser.parse_args()
#     args = []
#     args.append(prelim_args.time)
#     args.append(int(prelim_args.pid))
#     return args
    
def more_than_nothing():
    for process in psutil.process_iter(['name', 'pid']):            # without the argument process_iter() throws a fit :(
        try:
            usage = process.cpu_percent(interval=0.2)
            if (usage > 0 and process.info['name'] != 'System Idle Process'):           # ignore System Idle Process bc it's always over 100
                print(f"CPU Usage: {usage},", end=' ')
                print(f"Name: {process.info['name']}, PID: {process.pid}")
        except KeyboardInterrupt:
            exit(0)

def main():
    more_than_nothing()

main()