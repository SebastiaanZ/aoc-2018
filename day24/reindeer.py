from dataclasses import dataclass
from itertools import count
from bisect import insort_left
from operator import methodcaller
import re


class Disease:
    def __init__(self, fn: str, boost: int=0) -> None:
        self.sides: dict = {"immune_system": set(), "infection": set()}
        self.selection_order = []
        self.process_status_file(fn, boost)
        self.targeted = set()

    def process_status_file(self, fn: str, boost: int=0) -> None:
        p_numbers = re.compile(r"\d+")
        p_immunity = re.compile(r"(?<=immune to ).*?(?=[;)])")
        p_weakness = re.compile(r"(?<=weak to ).*?(?=[;)])")
        p_attack_type = re.compile(r"(?<=[\d+] )(\w+)(?= dam)")
        ident = count()

        with open(fn) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                if ":" in line:
                    current_side = "immune_system" if line.startswith("Immune") else "infection"
                    enemy = "immune_system" if current_side == "infection" else "infection"
                    addition = boost if current_side == "immune_system" else 0
                    continue

                units, hp, damage, initiative = (int(n) for n in p_numbers.findall(line))
                damage += addition
                immunity = p_immunity.findall(line)
                immunity = set(immunity[0].split(', ')) if immunity else set()
                weakness = p_weakness.findall(line)
                weakness = set(weakness[0].split(', ')) if weakness else set()
                attack_type = p_attack_type.search(line)[0]

                army = Army(next(ident), current_side, enemy, units, hp, immunity, weakness,
                            damage, attack_type, initiative)
                self.sides[current_side].add(army)
                insort_left(self.selection_order, army)

    def selection_phase(self):
        self.attack_order = []
        self.targeted = set()
        for attacker in self.selection_order:
            candidates = [c for c in self.sides[attacker.enemy]
                          if c not in self.targeted and attacker.attack_type not in c.immunity]
            if candidates:
                candidate = max(candidates, key=methodcaller("damage_estimation",
                                                             attacker.attack_type,
                                                             attacker.effective_power))
                self.targeted.add(candidate)
                attacker.target = candidate
                insort_left(self.attack_order, (-attacker.initiative, attacker))

    def attack_phase(self):
        self.selection_order = []
        for _, attacker in self.attack_order:
            if attacker.alive:
                attacker.attack()
                if not attacker.target.alive:
                    self.sides[attacker.enemy].remove(attacker.target)
        for army in self.sides["immune_system"]:
            insort_left(self.selection_order, army)
        for army in self.sides["infection"]:
            insort_left(self.selection_order, army)

    def battle(self):
        old_units = sum(sum(army.units for army in side) for side in self.sides.values())
        while self.sides["immune_system"] and self.sides["infection"]:
            self.selection_phase()
            self.attack_phase()
            new_units = sum(sum(army.units for army in side) for side in self.sides.values())
            if old_units == new_units:
                return False, None
            old_units = new_units

        if self.sides["immune_system"]:
            return True, sum(army.units for army in self.sides["immune_system"])
        else:
            return False, sum(army.units for army in self.sides["infection"])


@dataclass
class Army:
    ident: int
    side: str
    enemy: str
    units: int
    hp: int
    immunity: set
    weakness: set
    damage: int
    attack_type: str
    initiative: int
    target: 'Army' = None

    @property
    def effective_power(self):
        return self.units * self.damage

    def __lt__(self, other):
        return (self.effective_power, self.initiative) > (other.effective_power, other.initiative)

    def __hash__(self):
        return hash(self.ident)

    def __repr__(self):
        return f"Army(ident={self.ident!r}, units={self.units!r} side={self.side!r})"

    @property
    def alive(self):
        return self.units > 0

    def damage_estimation(self, attack_type, effective_power):
        return (((attack_type in self.weakness) + 1) * effective_power,
                self.effective_power,
                self.initiative)

    def attack(self):
        self.target.take_damage(self.attack_type, self.effective_power)

    def take_damage(self, attack_type, effective_power):
        damage = self.damage_estimation(attack_type, effective_power)[0]
        killed = damage // self.hp
        self.units -= killed

