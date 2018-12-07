class Manager:
    def __init__(self, n_workers: int=1) -> None:
        self.free_workers: set = set(range(n_workers))
        self.workers: dict = {i: Worker(i) for i in range(n_workers)}
        self.n_workers: int = n_workers
        self.assigned_workers: list = list()

    @property
    def has_free_workers(self) -> bool:
        return bool(self.free_workers)

    def employ_free_worker(self, task, time) -> None:
        worker_id = self.free_workers.pop()
        worker = self.workers[worker_id]
        worker.start_task(task, time)
        self.assigned_workers.append(worker)

    def finish_task(self) -> int:
        self.assigned_workers.sort(reverse=True)
        worker = self.assigned_workers.pop(-1)
        self.free_workers.add(worker.id)
        return worker.complete_task()


class Worker:
    def __init__(self, ident: int) -> None:
        self.id: int = ident
        self.task = None

        self._start: int
        self._finish: int

    @property
    def finished(self) -> int:
        return self._finished

    def __repr__(self) -> str:
        return "%s(%r)" % (self.__class__.__name__, self.id)

    def __lt__(self, other) -> bool:
        return self.finished < other.finished

    def start_task(self, task, time) -> None:
        self.task = task
        self._start = time
        self._finished = time + task.effort

    def complete_task(self) -> int:
        self.task.complete()
        self.task = None
        return self._finished


class Tasklist:
    def __init__(self,  idents: str, instructions: list, base_fee: int=0) -> None:
        self.done: set = set()
        self.done_order: list = list()

        self.base_fee: int = base_fee
        self.tasks = {ident: Task(ident, base_fee, self) for ident in idents}

        self.to_do = list(self.tasks.values())

        for instruction in instructions:
            task_id = instruction[-13]
            requirement = instruction[5]
            self.tasks[task_id].add_requirement(requirement)

    def __len__(self) -> int:
        return len(self.to_do)

    @property
    def has_available_tasks(self) -> bool:
        self.to_do.sort(reverse=True)
        return not self.to_do[-1].requirements

    @property
    def available_task(self):
        return self.to_do.pop()


class Task:
    def __init__(self, ident: str, base_fee: int, manager: Tasklist):
        self.id: str = ident
        self.ord = ord(ident) - 65
        self.effort: int = self.ord + base_fee + 1
        self._requirements: set = set()
        self.manager = manager

    def __len__(self) -> int:
        return len(self._requirements - self.manager.done)

    def __lt__(self, other) -> bool:
        return len(self) * 26 + self.ord < len(other) * 26 + other.ord

    def __repr__(self) -> str:
        requiremens_left = self._requirements - self.manager.done
        return "%s(%r, requirements=%r)" % (self.__class__.__name__,
                                            self.id,
                                            requiremens_left)

    @property
    def requirements(self) -> set:
        return self._requirements - self.manager.done

    def add_requirement(self, requirement: str) -> None:
        self._requirements.add(requirement)

    def complete(self) -> None:
        self.manager.done.add(self.id)
        self.manager.done_order.append(self.id)


if __name__ == "__main__":
    from string import ascii_uppercase
    from aoc_day7 import work

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
