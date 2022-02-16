import argparse
import json
import os
import signal
import sys
from functools import partial

from pynput import keyboard

from settings import PIDFILE, CONFIG_FILE, CONFIG_DIR

toggle = False


def macro_listener():
    global toggle
    if toggle:
        toggle = False
        os.system('')
        os.system('')
    else:
        toggle = True
        os.system('pulsemeeter connect vi 1 a 1')
        os.system('pulsemeeter disconnect vi 1 a 3')


def set_running_config():
    try:
        with open(PIDFILE) as f:
            pid = int(next(f))
        # Does not work if simplified.
        if os.kill(pid, signal.SIGKILL) != False:
            print('Another copy is already running')
            sys.exit(0)
        else:
            pass
    except OSError:
        pass
    finally:
        with open(PIDFILE, 'w') as f:
            f.write(f'{os.getpid()}')


def stop_program():
    try:
        with open(PIDFILE) as f:
            pid = int(next(f))
        if os.kill(pid, signal.SIGKILL) != False:
            print('Instance stopped.')
    except OSError as e:
        print('No instance running found.')
    finally:
        sys.exit(0)


def arg_intepreter():
    parser = argparse.ArgumentParser()
    parser.add_argument('stop', action='store', const='NoValue', nargs='?')
    parser.add_argument('--here', action='store', const='NoValue', nargs='?')
    args = parser.parse_args()
    if args.stop is not None:
        stop_program()
    elif args.here is not None:
        set_running_config()
    else:
        try:
            with open(PIDFILE) as f:
                pid = int(next(f))
            # Does not work if simplified.
            if os.kill(pid, 0) != False:
                print('Another copy is already running')
                sys.exit(0)
            else:
                pass
        except OSError:
            pass
        config = get_config()
        config_len = len(config)
        if config_len <= 0:
            print("No macros in config.json, quiting...")
            sys.exit(0)
        elif config_len == 1:
            print(f"Running with 1 hotkey")
        else:
            print(f"Running with {config_len} hotkeys")
        os.system('macromachine --here &')
        sys.exit(0)



def get_config():
    if os.path.isfile(CONFIG_FILE):
        try:
            config: json = json.load(open(CONFIG_FILE))
        except Exception as e:
            print('Error reading config file')
            print(e)
            sys.exit(1)
    else:
        config = json.loads('[]')
        save_config(config)
    return config


def save_config(config):
    if not os.path.isdir(CONFIG_DIR):
        os.mkdir(CONFIG_DIR)
    with open(CONFIG_FILE, 'w') as outfile:
        json.dump(config, outfile, indent='\t', separators=(',', ': '))


toggleMem = {}


def toggleFunction(hotkey: str, on_commands: str, off_commands: str):
    global toggleMem
    if toggleMem[hotkey]:
        os.system(on_commands)
    else:
        os.system(off_commands)
    toggleMem[hotkey] ^= 1


def parse_config(config):
    result = {}
    for c in config.items():
        type = c[1]['type']
        if type == 'button':
            result[c[0]] = lambda: os.system(';'.join(c[1]['commands']))
        elif type == 'toggle':
            global toggleMem
            toggleMem[c[0]] = False
            result[c[0]] = partial(toggleFunction, c[0], ';'.join(c[1]['on_commands']), ';'.join(c[1]['off_commands']))

    return result


def main():
    arg_intepreter()
    config = get_config()
    settings = parse_config(config)
    listener = keyboard.GlobalHotKeys(settings)
    listener.start()
    while True:
        pass


if __name__ == '__main__':
    main()
    sys.exit(0)
