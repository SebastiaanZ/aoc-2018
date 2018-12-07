from string import ascii_uppercase
from workforce import Workforce, Task


def work(fn: str, worker_ids: str, n_workers: int=1, base_effort: int=0):
    with open(fn) as f:
        instructions = f.readlines()
        to_do = Task.create_tasklist(worker_ids,
                                     instructions,
                                     base_effort)

    Workforce.recruite_workers(n_workers)
    time = 0

    while to_do:
        while Workforce.free_workers:
            to_do.sort()
            task = to_do[0]
            if not task.requirements:
                worker = Workforce.get_free_worker()
                worker.start_task(task, time)
                to_do.pop(0)
            else:
                time = Workforce.finish_task()
            if not to_do:
                break
        else:
            time = Workforce.finish_task()
    else:
        while Workforce.assigned_workers:
            time = Workforce.finish_task()

    return "".join(Task.done_order), time


if __name__ == "__main__":
    answer1 = work("day7-input.txt",
                   ascii_uppercase,
                   n_workers=1,
                   base_effort=0)[0]
    answer2 = work("day7-input.txt",
                   ascii_uppercase,
                   n_workers=5,
                   base_effort=60)[1]

    assert(answer1 == "GRTAHKLQVYWXMUBCZPIJFEDNSO")
    assert(answer2 == 1115)

    print(f"Part I Task order: {answer1}")
    print(f"Part II completion time: {answer2}")
