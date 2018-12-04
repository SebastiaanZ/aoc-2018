from datetime import datetime
from collections import namedtuple, defaultdict
import numpy as np


def get_shift(log):
    ilog = iter(log)
    guard = int(next(ilog).action[7:].strip().split(" ")[0])
    shift_log = np.zeros(60, dtype="int")
    for entry in ilog:
        if entry.action.startswith("Guard"):
            yield guard, shift_log
            shift_log = np.zeros(60)
            guard = int(entry.action[7:].strip().split(" ")[0])
            continue
        if entry.action == "falls asleep":
            sleep = entry.dt.minute
        else:
            wakes = entry.dt.minute
            shift_log[sleep:wakes] = 1
    yield guard, shift_log


Log = namedtuple("Log", ["dt", "action"])
Total = namedtuple("Total", ["guard", "total", "minute_sum"])

timelog = []
with open("day4-input.txt") as f:
    for entry in f:
        time = datetime.strptime(entry[:18], "[%Y-%m-%d %H:%M]")
        action = entry.strip()[19:]
        timelog.append(Log(time, action))

timelog.sort(key=lambda x: x.dt)

guards = defaultdict(list)
for guard, shift_log in get_shift(timelog):
    guards[guard].append(shift_log)

totals = []
for guard, shifts in guards.items():
    all_shifts = np.concatenate(shifts).reshape((len(shifts), 60))
    total = all_shifts.sum()
    minute_sum = all_shifts.sum(axis=0)
    totals.append(Total(guard, total, minute_sum))

part1 = max(totals, key=lambda x: x.total)
print("Day 4, part 1:")
print(f"Guard #{part1.guard}, total: {part1.total}, minute: {part1.minute_sum.argmax()}")
print(f"Answer: {part1.guard*part1.minute_sum.argmax()}")

print("\nDay 4, part 2:")
part2 = max(totals, key=lambda x: x.minute_sum.max())
print(f"Guard #{part2.guard}, total: {part2.total}, minute: {part2.minute_sum.argmax()}")
print(f"Answer: {part2.guard*part2.minute_sum.argmax()}")
