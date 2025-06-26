# polybar-pomodorro
simple way to use pomodorro in your polybar

Timer has 3 modes:
- manual [M] - 5/15/25 min
- short session [1/2] - 25-5-25-15 min
- standart session [1/4] 25-5-25-5-25-5-25-15 min

How to setup:
- clone script
- add to polybar config.ini
- replace ${path_to_polybar-pomodorro} with project path
- restart polybar

config.ini example
```
[module/pomodorro]
type = custom/script
exec = ${path_to_polybar-pomodorro}/pomo.py
interval = 1
click-left = ${path_to_polybar-pomodorro}/pomo.py toggle
click-right =  ${path_to_polybar-pomodorro}/pomo.py chmod


