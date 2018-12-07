class Workforce(object):

    free_workers: set = set()
    assigned_workers: list = list()
    total_workers: int = 0
    workers: dict = dict()

    def __init__(self, ident: int) -> None:
        self.id: int = ident
        self.task: Task = None
        self.free_workers.add(self.id)

        self._start: int
        self._finished: int

    @property
    def finished(self):
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
        self.free_workers.add(self.id)
        self.task.complete()
        self.task = None
        return self._finished

    @classmethod
    def recruite_workers(cls, workers) -> list:
        cls.free_workers: set = set()
        cls.assigned_workers: list = list()
        cls.total_workers: int = 0
        cls.workers: dict = dict()
        cls.workers = {i: Workforce(i) for i in range(workers)}
        cls.total_workers = workers
        cls.free_workers = set(range(workers))
        return list(cls.workers.values())

    @classmethod
    def get_free_worker(cls):
        workerid = cls.free_workers.pop()
        worker = cls.workers[workerid]
        cls.assigned_workers.append(worker)
        return worker

    @classmethod
    def finish_task(cls) -> int:
        cls.assigned_workers.sort()
        return cls.assigned_workers.pop(0).complete_task()


class Task(object):
    done: set = set()
    done_order: list = list()
    base_fee: int

    def __init__(self, ident: str) -> None:
        self.id: str = ident
        self.ord = ord(ident) - 65
        self.effort = ord(ident) - 64 + self.base_fee
        self._requirements: set = set()

    def __len__(self):
        return len(self._requirements - self.done)

    def __lt__(self, other):
        return len(self) * 26 + self.ord < len(other) * 26 + other.ord

    def __repr__(self):
        return "%s(%r, requirements=%r)" % (self.__class__.__name__,
                                            self.id,
                                            self._requirements - self.done)

    @property
    def requirements(self) -> set:
        return self._requirements - self.done

    def add_requirement(self, requirement: str) -> None:
        self._requirements.add(requirement)

    def complete(self) -> None:
        self.done.add(self.id)
        self.done_order.append(self.id)

    @classmethod
    def create_tasklist(cls, idents: str, instructions: list, base_fee: int=0) -> dict:
        cls.done: set = set()
        cls.done_order: list = list()
        cls.base_fee: int
        cls.base_fee = base_fee
        task_mapping = {ident: Task(ident) for ident in idents}
        for instruction in instructions:
            task_id = instruction[-13]
            requirement = instruction[5]
            task_mapping[task_id].add_requirement(requirement)
        return list(task_mapping.values())


if __name__ == "__main__":
    from string import ascii_uppercase

    with open("day7-input.txt") as f:
        instructions = f.readlines()
        to_do = Task.create_tasklist(ascii_uppercase, instructions, 60)

    workers = Workforce.recruite_workers(5)
    time = 0
    while to_do:
        while Workforce.free_workers:
            to_do.sort()
            task = to_do[0]
            print(task)
            print(Workforce.assigned_workers)
            if not task.requirements:
                worker = Workforce.get_free_worker()
                worker.start_task(task, time)
                to_do.pop(0)
                print(Workforce.assigned_workers)
            else:
                print(Workforce.assigned_workers)
                time = Workforce.finish_task()
                print(time)
            if not to_do:
                break
        else:
            while Workforce.assigned_workers:
                time = Workforce.finish_task()
    else:
        while Workforce.assigned_workers:
            time = Workforce.finish_task()

        print("".join(Task.done_order))
        print("GRTAHKLQVYWXMUBCZPIJFEDNSO")
        print(time)
