#!/usr/bin/env python3

import sys, json
from datetime import datetime
from subprocess import call
from time import strftime, gmtime

STATE_FILE = '/tmp/polybar-pomodorro.json'
NAME = "%{F#f0c674}PMDR%{F-}"

def save_data(file_name,is_paused,mode,iteration,action,timestamp,remain):
    # mode 
    # 1 - manual  (25 | 5 | 15)
    # 2 - half sprint (25/5/25/15)
    # 3 - full sprint (25/5/25/5/25/5/25/15)
    # 
    # iteration - (1,2) (1,4)
    #
    # action
    # 1 - work 25min
    # 2 - short break 5min
    # 3 - long break 15 min
    data = {
            "is_paused": is_paused,
            "mode": mode,
            "iteration": iteration,
            "action": action,
            "timestamp": timestamp,
            "time_remain": remain
    }

    with open(file_name, "w") as file:
        json.dump(data, file)


def load_data(file_name):
    try:
        with open(file_name, "r") as file:
            return json.load(file)

    except FileNotFoundError:
        now = datetime.now()
        save_data(file_name, True, 1, [0,0], 1, now.timestamp(), 25*60)
        return load_data(file_name)

def set_next_mode(current_mode,current_action):
    if current_mode == 1:
        if current_action == 3:
            return 2,1
        else:
            return 1, current_action + 1
    elif current_mode == 2:
        return 3, 1
    elif current_mode == 3:
        return 1,1

def get_iteration_by_mode(mode):
    if mode == 2:
        return [1,2]
    elif mode == 3:
        return [1,4]

def get_timer_by_action(action):
    if action == 1:
        return 25*60
    elif action == 2:
        return 5*60
    elif action == 3:
        return 15*60


def print_pomo(mode,iteration,remain):
    print_mode = "M"
    if mode != 1:
        print_mode = f"{iteration[0]}/{iteration[1]}"
    
    print(f"{NAME} [{print_mode}] {strftime('%M:%S', gmtime(remain))}")

def main():
    data = load_data(STATE_FILE)
    is_paused = data["is_paused"]
    mode = data["mode"]
    iteration = data["iteration"]
    action = data["action"]
    timestamp = data["timestamp"]
    remain = data["time_remain"]
    c_timestamp = datetime.now().timestamp()

    if len(sys.argv) == 2:
        if sys.argv[1] == "toggle":
            is_paused = not is_paused
        elif sys.argv[1] == "chmod":
            mode, action = set_next_mode(mode,action)
            remain = get_timer_by_action(action)
            iteration = get_iteration_by_mode(mode)
            is_paused = True
    else:
        if not data["is_paused"]:
            remain = data["time_remain"] - (int(c_timestamp - int(data["timestamp"])))

    if remain <= 0:
        if mode == 1:
            is_paused = True
            iteration = [0,0]
        if action == 1:
            msg = 'Time to break'
            if mode != 1 and iteration[0]==iteration[1]:
                action += 2
            else:
                action += 1
        elif action == 2:
            msg = 'Break is over. Lets working'
            action -= 1
            if mode != 1:
                iteration[0] += 1
        elif action == 3:
            msg = 'Break is over. Lets working'
            action -= 2
            is_paused = True
            if mode != 1 and iteration[0]==iteration[1]:
                iteration[0] = 1


        remain = get_timer_by_action(action)
        call(['notify-send', 'Pomodoro', msg, '-t', '5000'])

    save_data(STATE_FILE,is_paused,mode,iteration,action,c_timestamp,remain) 

    print_pomo(mode,iteration,remain)



if __name__ == "__main__":
    main()
