# Space Stoichiometry
from dataclasses import dataclass
from math import ceil
from typing import Dict, List, Tuple

# OUTLINE
# Parse input
# Start with Fuel reaction, determine components needed


@dataclass
class Chemical:
    amount: int
    name: str

    def to_tuple(self) -> Tuple[int, str]:
        return self.amount, self.name

    @classmethod
    def from_tuple(cls, t: Tuple[int, str]) -> "Chemical":
        return cls(*t)

    @classmethod
    def from_string(cls, s: str) -> "Chemical":
        args = s.strip().split(" ")
        return cls(int(args[0]), args[1].strip())


class Reaction:
    def __init__(self, reactants: List[Chemical], product: Chemical):
        self.reactants = reactants
        self.product_name = product.name
        self.product_amount = product.amount

    @classmethod
    def from_string(cls, s: str):
        # for example, "12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ"

        sides = s.strip().split("=>")
        reactants = [Chemical.from_string(c) for c in sides[0].split(",")]
        product = Chemical.from_string(sides[1])

        return cls(reactants=reactants, product=product)


def get_needed_ore(
    reaction_dict: Dict[str, Reaction],
    target: str,
    n_needed: int,
    reactants_needed: Dict[str, int],
    reactants_created: Dict[str, int],
):
    if target == "ORE":
        return reactants_needed

    reaction = reaction_dict[target]
    reps = ceil(n_needed / reaction.product_amount)

    for reactant in reaction.reactants:
        reactants_needed[reactant.name] = (
            reactants_needed.get(reactant.name, 0) + reactant.amount * reps
        )
        needed = reactants_needed.get(reactant.name, 0) - reactants_created.get(
            reactant.name, 0
        )
        if needed > 0:
            get_needed_ore(
                reaction_dict,
                target=reactant.name,
                n_needed=needed,
                reactants_needed=reactants_needed,
                reactants_created=reactants_created,
            )
    reactants_created[target] = (
        reactants_created.get(target, 0) + reps * reaction.product_amount
    )
    return reactants_needed
