from string import ascii_uppercase
from workforce import Manager, Tasklist


def work(fn: str, worker_ids: str, n_workers: int=1, base_effort: int=0) -> tuple:
    with open(fn) as f:
        instructions = f.readlines()
        tasklist = Tasklist(worker_ids,
                            instructions,
                            base_effort)

    manager = Manager(n_workers)

    time = 0
    while tasklist:
        while manager.has_free_workers:
            if tasklist.has_available_tasks:
                task = tasklist.available_task
                manager.employ_free_worker(task, time)
            else:
                time = manager.finish_task()
            if not tasklist:
                break
        else:
            time = manager.finish_task()
    else:
        while manager.assigned_workers:
            time = manager.finish_task()

    return "".join(tasklist.done_order), time


if __name__ == "__main__":
    answer1, time = work("day7-input.txt",
                         ascii_uppercase,
                         n_workers=1,
                         base_effort=0)

    order, answer2 = work("day7-input.txt",
                          ascii_uppercase,
                          n_workers=5,
                          base_effort=60)

    assert(answer1 == "GRTAHKLQVYWXMUBCZPIJFEDNSO")
    assert(answer2 == 1115)

    print(f"Part I  task order: {answer1}    time: {time}")
    print(f"Part II task order: {order}    time: {answer2}")
