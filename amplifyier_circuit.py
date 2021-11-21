from intcode_computer import intcode_computer
from itertools import permutations
from intcode_test_fixtures import day_7_input
from computer import IntcodeComputer, EndOfCodeError
from logging import getLogger

logger = getLogger()


def amplification_circuit_optimization(program, first_input: int, n_cycles: int):
    phase_space = [i for i in range(n_cycles)]
    thruster_signals = dict()
    for phases in permutations(phase_space):
        input_instruction = [first_input]
        for phase in phases:
            _, input_instruction = intcode_computer(
                program, [phase, input_instruction[0]]
            )
        thruster_signals[phases] = input_instruction[0]
    return thruster_signals


def test_amplification_circuit_optimization(day_7_input):
    thruster_signals = amplification_circuit_optimization(day_7_input, 0, 5)
    assert max(thruster_signals) == 359142


def fedback_amplification_circuit(
    program, phases=(9, 8, 7, 6, 5), first_input=0
):
    amplifiers = {
        stage: IntcodeComputer(program, inputs=[phases[stage]]) for stage in range(5)
    }
    amplifiers[0] = IntcodeComputer(program, inputs=[phases[0], first_input])
    final_out = None
    loop_count = 0
    while True:
        # loop over all amplifiers
        for idx, amplifier in amplifiers.items():
            out = None
            while out is None:
                if final_out == 139629729:
                    break_time = True
                try:
                    out = amplifier.do_next_instruction()
                    if out is not None:
                        final_out = out
                except EndOfCodeError:
                    logger.debug("Code has halted.")
                    return final_out
            # append the output to the next code's input
            amplifiers[(idx + 1) % len(amplifiers)].add_input(out)
            loop_count += 1


def fedback_amplification_circuit_optimizer(
    program, phase_space=(5, 6, 7, 8, 9), first_input=0
):
    max_out = 0
    for phases in permutations(phase_space):
        out = fedback_amplification_circuit(program, phases, first_input)
        max_out = max(out, max_out)
    return max_out


if __name__ == "__main__":
    program = [3,8,1001,8,10,8,105,1,0,0,21,30,55,76,97,114,195,276,357,438,99999,3,9,102,3,9,9,4,9,99,3,9,1002,9,3,9,1001,9,5,9,1002,9,2,9,1001,9,2,9,102,2,9,9,4,9,99,3,9,1002,9,5,9,1001,9,2,9,102,5,9,9,1001,9,4,9,4,9,99,3,9,1001,9,4,9,102,5,9,9,101,4,9,9,1002,9,4,9,4,9,99,3,9,101,2,9,9,102,4,9,9,1001,9,5,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,99,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,1,9,4,9,99,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,1,9,4,9,99,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,99]
    # answer = 359142
    # program = [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]
    thruster_signals = fedback_amplification_circuit_optimizer(program)
    print(thruster_signals)
