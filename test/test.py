import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, Timer, ClockCycles
from cocotb.handle import Force, Release
import random
import itertools
import os

async def check_cell_pin(dut, cell_pin, io_pairs, lenient=False):
    dut.clk.value = 0
    dut.rst_n.value = 1
    dut.ena.value = 1
    dut.page.value = cell_pin // 8
    for i, o in io_pairs:
        dut.cell_in.value = i
        await ClockCycles(dut.clk, 2)
        assert dut.uio_out.value == 0
        assert dut.uio_oe.value == 0
        r = dut.uo_out.value[~cell_pin%8]
        istr = bin(i)[2:].rjust(6, '0')
        ostr = 'any' if o is None else str(o)
        info = f"cell_pin {cell_pin} input {istr} output {r} expected {ostr}"
        if lenient and r.binstr == 'x' and o is not None:
            # workaround for incorrect rtl simulation of short-circuits involving x'es
            dut._log.info(info + " (ignored for sequential logic in rtl mode)")
        else:
            dut._log.info(info)
            assert o is None or r == o

def auto_iter(in_iter):
    try:
        return iter(in_iter)
    except TypeError:
        return iter((in_iter,))

def expand_dict(in_dict):
    return {p: v for k, v in in_dict.items() for p in auto_iter(k)}

def randomize_unused_pins(num_inputs, orig_tests, repeat=None, seed=None):
    if repeat is None:
        repeat = 5
    if seed is None:
        seed = 383
    rnd = random.Random(seed)
    mask = -(1 << num_inputs)
    tests = list(orig_tests)
    for rep in range(1, repeat):
        for i, o in orig_tests:
            tests.append((rnd.randrange(64) & mask | i & ~mask, o))
    return tuple(tests)

def comb(func, repeat=None, seed=None):
    # combinational logic
    num_inputs = func.__code__.co_argcount
    tests = []
    for inputs in itertools.product(range(2), repeat=num_inputs):
        inp_bin = sum(j << i for i, j in enumerate(inputs))
        out = func(*inputs)
        if out is not None:
            out &= 1
        tests.append((inp_bin, out))
    return randomize_unused_pins(num_inputs, tests, repeat, seed), False

def latch(invert_output, invert_data, has_reset, repeat=None, seed=None):
    if has_reset:
        num_inputs = 3
        pre_tests = [(0b110, 0), (0b111, 1), (0b110, 0), (0b100, 0), (0b101, 0), (0b111, 1), (0b101, 1), (0b100, 1), (0b000, 0), (0b100, 0), (0b110, 0), (0b111, 1), (0b101, 1), (0b100, 1)]
    else:
        num_inputs = 2
        pre_tests = [(0b10, 0), (0b11, 1), (0b10, 0), (0b00, 0), (0b01, 0), (0b11, 1), (0b01, 1), (0b00, 1)]
    tests = []
    for i, o in pre_tests:
        if invert_data:
            i ^= 0b10
        if invert_output:
            o ^= 1
        tests.append((i, o))
    return randomize_unused_pins(num_inputs, tests, repeat, seed), True

def clockgate(has_scanchain, repeat=None, seed=None):
    if has_scanchain:
        num_inputs = 3
        tests = [(0b000, 0), (0b001, 0), (0b011, 0), (0b010, 0), (0b011, 1), (0b010, 0), (0b011, 1), (0b001, 1), (0b000, 0), (0b001, 0),
                 (0b000, 0), (0b001, 0), (0b101, 0), (0b100, 0), (0b101, 1), (0b100, 0), (0b101, 1), (0b001, 1), (0b000, 0), (0b001, 0)]
    else:
        num_inputs = 2
        tests = [(0b00, 0), (0b01, 0), (0b11, 0), (0b10, 0), (0b11, 1), (0b10, 0), (0b11, 1), (0b01, 1), (0b00, 0), (0b01, 0)]
    return randomize_unused_pins(num_inputs, tests, repeat, seed), True

def flop(invert_output, invert_clock, has_reset, has_set, has_loopback, has_scanchain, repeat=None, seed=None):
    num_inputs = 2
    # bits of the most general flip-flop: sce scd de set_b reset_b data clock
    pre_tests = [(0b0011100, None), (0b0011101, 0), (0b0011110, 0), (0b0011111, 1), (0b0011100, 1), (0b0011101, 0)]
    if has_reset:
        num_inputs += 1
        pre_tests.extend([(0b0011110, 0), (0b0011111, 1), (0b0011010, 0), (0b0011011, 0)])
    if has_set:
        num_inputs += 1
        pre_tests.extend([(0b0010100, 1), (0b0010101, 1), (0b0011100, 1), (0b0011101, 0)])
    if has_loopback:
        num_inputs += 1
        pre_tests.extend([(0b0011110, 0), (0b0011111, 1), (0b0001100, 1), (0b0001101, 1),
                          (0b0011100, 1), (0b0011101, 0), (0b0001110, 0), (0b0001111, 0)])
    if has_scanchain:
        num_inputs += 2
        pre_tests.extend([(0b1111100, 0), (0b1111101, 1), (0b0111100, 1), (0b0111101, 0),
                          (0b0011110, 0), (0b0011111, 1), (0b1011110, 1), (0b1011111, 0)])
    tests = []
    for i, o in pre_tests:
        if not has_scanchain:
            i = i & 0b0011111
        if not has_loopback:
            i = (i & 0b1100000) >> 1 | i & 0b0001111
        if not has_set:
            i = (i & 0b1110000) >> 1 | i & 0b0000111
        if not has_reset:
            i = (i & 0b1111000) >> 1 | i & 0b0000011
        if invert_clock:
            i = (i & 0b1111110) | ~i & 0b0000001
        if invert_output and o is not None:
            o ^= 1
        tests.append((i, o))
    return randomize_unused_pins(num_inputs, tests, repeat, seed), True

@cocotb.test()
async def test_cells(dut):
    dut._log.info("start")
    gatelevel = os.environ.get('GATES') == 'yes'

    clock = Clock(dut.clk, 20, units='us')
    cocotb.start_soon(clock.start())

    pin_mapping = expand_dict({
        (0,): 'conb.LO',
        (1,): 'conb.HI',
        (2, 3, 4, 5, 6): 'buf',
        (7, 8, 9, 10, 11): 'inv',
        (12, 13): 'and2',
        (14, 15): 'and3',
        (16, 17): 'and4',
        (18, 19): 'nand2',
        (20, 21): 'nand2b',
        (22,): 'nand3',
        (23,): 'nand3b',
        (24,): 'nand4',
        (25, 26): 'or2',
        (27, 28): 'or3',
        (29, 30): 'or4',
        (31, 32): 'nor2',
        (33, 34): 'nor2b',
        (35, 36): 'nor3',
        (37, 38): 'nor4',
        (39,): 'xor2',
        (40,): 'xnor2',
        (41, 42): 'a21o',
        (43, 44): 'a21oi',
        (45,): 'a22oi',
        (46,): 'a221oi',
        (47,): 'o21ai',
        (48, 49): 'mux2',
        (50,): 'mux4',
        (51,): 'dlxtp',
        (52,): 'dlrtp',
        (53,): 'dlrbp.Q',
        (54,): 'dlrbp.Q_N',
        (55,): 'dlrtn',
        (56,): 'dlrbn.Q',
        (57,): 'dlrbn.Q_N',
        (58, 60): 'dfrbp.Q',
        (59, 61): 'dfrbp.Q_N',
        (62,): 'sdfbbp.Q',
        (63,): 'sdfbbp.Q_N',
        (64,): 'ebufn*3',
        (65,): 'einvn*3',
        (66,): 'ebufn*3+sh',
        (67,): 'einvn*3+sh',
        (68, 69, 70): 'dlygate',
        (71,): 'dlclkp',
        (72,): 'sdlclkp',
    })

    cell_mapping = {
        'conb.HI': 'pwr#',
        'conb.LO': 'gnd#',
        'ha.COUT': 'and2',
        'ha.SUM': 'xor2',
        'fa.COUT': 'maj3',
        'fa.SUM': 'xor3',
        'fah.COUT': 'maj3',
        'fah.SUM': 'xor3',
        'fahcin.COUT': 'maj3#b',
        'fahcin.SUM': 'xnor3',
        'fahcon.COUT_N': 'maj3#i',
        'fahcon.SUM': 'xor3',
        'ebufn*3+sh': 'ebufn*3',
        'einvn*3+sh': 'einvn*3',
        'dlxbp.Q': 'dlxtp',
        'dlxbp.Q_N': 'dlxtp#i',
        'dlxbn.Q': 'dlxtn',
        'dlxbn.Q_N': 'dlxtn#i',
        'dlrbp.Q': 'dlrtp',
        'dlrbp.Q_N': 'dlrtp#i',
        'dlrbn.Q': 'dlrtn',
        'dlrbn.Q_N': 'dlrtn#i',
        'dfxbp.Q': 'dfxtp',
        'dfxbp.Q_N': 'dfxtp#i',
        'dfrbp.Q': 'dfrtp',
        'dfrbp.Q_N': 'dfrtp#i',
        'dfsbp.Q': 'dfstp',
        'dfsbp.Q_N': 'dfstp#i',
        'dfbbp.Q': 'dfbtp#',
        'dfbbp.Q_N': 'dfbtp#i',
        'dfbbn.Q': 'dfbtn#',
        'dfbbn.Q_N': 'dfbtn#i',
        'edfxbp.Q': 'edfxtp',
        'edfxbp.Q_N': 'edfxtp#i',
        'sdfxbp.Q': 'sdfxtp',
        'sdfxbp.Q_N': 'sdfxtp#i',
        'sdfrbp.Q': 'sdfrtp',
        'sdfrbp.Q_N': 'sdfrtp#i',
        'sdfsbp.Q': 'sdfstp',
        'sdfsbp.Q_N': 'sdfstp#i',
        'sdfbbp.Q': 'sdfbtp#',
        'sdfbbp.Q_N': 'sdfbtp#i',
        'sdfbbn.Q': 'sdfbtn#',
        'sdfbbn.Q_N': 'sdfbtn#i',
        'sedfxbp.Q': 'sedfxtp',
        'sedfxbp.Q_N': 'sedfxtp#i',
        'ebufn+ebufp': 'mux2',
        'einvn+einvp': 'mux2i',
        'dlygate': 'buf',
        'dlymetal': 'buf',
        'clkbuf': 'buf',
        'clkinv': 'inv',
        'clkinvlp': 'inv',
        'clkdlybuf': 'buf',
        'lpflow_inputiso0p': 'and2b#r',
        'lpflow_inputiso0n': 'and2',
        'lpflow_inputiso1p': 'or2',
        'lpflow_inputiso1n': 'or2b',
        'lpflow_inputisolatch': 'dlxtp',
        'lpflow_isobufsrc': 'and2b#r',
    }

    pin_tests = {
        'gnd#':      comb(lambda: 0),
        'pwr#':      comb(lambda: 1),
        'buf':       comb(lambda a: a),
        'inv':       comb(lambda a: ~a),
        'and2':      comb(lambda a,b: a & b),
        'and2b':     comb(lambda a,b: ~a & b),
        'and2b#r':   comb(lambda a,b: a & ~b),
        'and3':      comb(lambda a,b,c: a & b & c),
        'and3b':     comb(lambda a,b,c: ~a & b & c),
        'and4':      comb(lambda a,b,c,d: a & b & c & d),
        'and4b':     comb(lambda a,b,c,d: ~a & b & c & d),
        'and4bb':    comb(lambda a,b,c,d: ~a & ~b & c & d),
        'nand2':     comb(lambda a,b: ~(a & b)),
        'nand2b':    comb(lambda a,b: ~(~a & b)),
        'nand3':     comb(lambda a,b,c: ~(a & b & c)),
        'nand3b':    comb(lambda a,b,c: ~(~a & b & c)),
        'nand4':     comb(lambda a,b,c,d: ~(a & b & c & d)),
        'nand4b':    comb(lambda a,b,c,d: ~(~a & b & c & d)),
        'nand4bb':   comb(lambda a,b,c,d: ~(~a & ~b & c & d)),
        'or2':       comb(lambda a,b: a | b),
        'or2b':      comb(lambda a,b: a | ~b),
        'or3':       comb(lambda a,b,c: a | b | c),
        'or3b':      comb(lambda a,b,c: a | b | ~c),
        'or4':       comb(lambda a,b,c,d: a | b | c | d),
        'or4b':      comb(lambda a,b,c,d: a | b | c | ~d),
        'or4bb':     comb(lambda a,b,c,d: a | b | ~c | ~d),
        'nor2':      comb(lambda a,b: ~(a | b)),
        'nor2b':     comb(lambda a,b: ~(a | ~b)),
        'nor3':      comb(lambda a,b,c: ~(a | b | c)),
        'nor3b':     comb(lambda a,b,c: ~(a | b | ~c)),
        'nor4':      comb(lambda a,b,c,d: ~(a | b | c | d)),
        'nor4b':     comb(lambda a,b,c,d: ~(a | b | c | ~d)),
        'nor4bb':    comb(lambda a,b,c,d: ~(a | b | ~c | ~d)),
        'xor2':      comb(lambda a,b: a ^ b),
        'xor3':      comb(lambda a,b,c: a ^ b ^ c),
        'xnor2':     comb(lambda a,b: ~(a ^ b)),
        'xnor3':     comb(lambda a,b,c: ~(a ^ b ^ c)),
        'a2111o':    comb(lambda a,b,c,d,e: (a & b) | c | d | e),
        'a2111oi':   comb(lambda a,b,c,d,e: ~((a & b) | c | d | e)),
        'a211o':     comb(lambda a,b,c,d: (a & b) | c | d),
        'a211oi':    comb(lambda a,b,c,d: ~((a & b) | c | d)),
        'a21bo':     comb(lambda a,b,c: (a & b) | ~c),
        'a21boi':    comb(lambda a,b,c: ~((a & b) | ~c)),
        'a21o':      comb(lambda a,b,c: (a & b) | c),
        'a21oi':     comb(lambda a,b,c: ~((a & b) | c)),
        'a221o':     comb(lambda a,b,c,d,e: (a & b) | (c & d) | e),
        'a221oi':    comb(lambda a,b,c,d,e: ~((a & b) | (c & d) | e)),
        'a222oi':    comb(lambda a,b,c,d,e,f: ~((a & b) | (c & d) | (e & f))),
        'a22o':      comb(lambda a,b,c,d: (a & b) | (c & d)),
        'a22oi':     comb(lambda a,b,c,d: ~((a & b) | (c & d))),
        'a2bb2o':    comb(lambda a,b,c,d: (~a & ~b) | (c & d)),
        'a2bb2oi':   comb(lambda a,b,c,d: ~((~a & ~b) | (c & d))),
        'a311o':     comb(lambda a,b,c,d,e: (a & b & c) | d | e),
        'a311oi':    comb(lambda a,b,c,d,e: ~((a & b & c) | d | e)),
        'a31o':      comb(lambda a,b,c,d: (a & b & c) | d),
        'a31oi':     comb(lambda a,b,c,d: ~((a & b & c) | d)),
        'a32o':      comb(lambda a,b,c,d,e: (a & b & c) | (d & e)),
        'a32oi':     comb(lambda a,b,c,d,e: ~((a & b & c) | (d & e))),
        'a41o':      comb(lambda a,b,c,d,e: (a & b & c & d) | e),
        'a41oi':     comb(lambda a,b,c,d,e: ~((a & b & c & d) | e)),
        'o2111a':    comb(lambda a,b,c,d,e: (a | b) & c & d & e),
        'o2111ai':   comb(lambda a,b,c,d,e: ~((a | b) & c & d & e)),
        'o211a':     comb(lambda a,b,c,d: (a | b) & c & d),
        'o211ai':    comb(lambda a,b,c,d: ~((a | b) & c & d)),
        'o21ba':     comb(lambda a,b,c: (a | b) & ~c),
        'o21bai':    comb(lambda a,b,c: ~((a | b) & ~c)),
        'o21a':      comb(lambda a,b,c: (a | b) & c),
        'o21ai':     comb(lambda a,b,c: ~((a | b) & c)),
        'o221a':     comb(lambda a,b,c,d,e: (a | b) & (c | d) & e),
        'o221ai':    comb(lambda a,b,c,d,e: ~((a | b) & (c | d) & e)),
        'o222ai':    comb(lambda a,b,c,d,e,f: ~((a | b) & (c | d) & (e | f))),
        'o22a':      comb(lambda a,b,c,d: (a | b) & (c | d)),
        'o22ai':     comb(lambda a,b,c,d: ~((a | b) & (c | d))),
        'o2bb2a':    comb(lambda a,b,c,d: (~a | ~b) & (c | d)),
        'o2bb2ai':   comb(lambda a,b,c,d: ~((~a | ~b) & (c | d))),
        'o311a':     comb(lambda a,b,c,d,e: (a | b | c) & d & e),
        'o311ai':    comb(lambda a,b,c,d,e: ~((a | b | c) & d & e)),
        'o31a':      comb(lambda a,b,c,d: (a | b | c) & d),
        'o31ai':     comb(lambda a,b,c,d: ~((a | b | c) & d)),
        'o32a':      comb(lambda a,b,c,d,e: (a | b | c) & (d | e)),
        'o32ai':     comb(lambda a,b,c,d,e: ~((a | b | c) & (d | e))),
        'o41a':      comb(lambda a,b,c,d,e: (a | b | c | d) & e),
        'o41ai':     comb(lambda a,b,c,d,e: ~((a | b | c | d) & e)),
        'maj3':      comb(lambda a,b,c: a + b + c >= 2),
        'maj3#b':    comb(lambda a,b,c: a + b + 1-c >= 2),
        'maj3#i':    comb(lambda a,b,c: ~(a + b + c >= 2)),
        'mux2':      comb(lambda a,b,c: (a, b)[c]),
        'mux2i':     comb(lambda a,b,c: (~a, ~b)[c]),
        'mux4':      comb(lambda a,b,c,d,e,f: (a, b, c, d)[e + 2*f]),
        'ebufn*3':   comb(lambda a,b,c,d,e: (a, b, c, None)[d + 2*e]),
        'einvn*3':   comb(lambda a,b,c,d,e: (~a, ~b, ~c, None)[d + 2*e]),
        'dlxtp':     latch(invert_output=False, invert_data=False, has_reset=False),
        'dlxtp#i':   latch(invert_output=True,  invert_data=False, has_reset=False),
        'dlxtn':     latch(invert_output=False, invert_data=True,  has_reset=False),
        'dlxtn#i':   latch(invert_output=True,  invert_data=True,  has_reset=False),
        'dlrtp':     latch(invert_output=False, invert_data=False, has_reset=True),
        'dlrtp#i':   latch(invert_output=True,  invert_data=False, has_reset=True),
        'dlrtn':     latch(invert_output=False, invert_data=True,  has_reset=True),
        'dlrtn#i':   latch(invert_output=True,  invert_data=True,  has_reset=True),
        'dlclkp':    clockgate(has_scanchain=False),
        'sdlclkp':   clockgate(has_scanchain=True),
        'dfxtp':     flop(invert_output=False, invert_clock=False, has_reset=False, has_set=False, has_loopback=False, has_scanchain=False),
        'dfxtp#i':   flop(invert_output=True , invert_clock=False, has_reset=False, has_set=False, has_loopback=False, has_scanchain=False),
        'dfrtp':     flop(invert_output=False, invert_clock=False, has_reset=True,  has_set=False, has_loopback=False, has_scanchain=False),
        'dfrtp#i':   flop(invert_output=True , invert_clock=False, has_reset=True,  has_set=False, has_loopback=False, has_scanchain=False),
        'dfrtn':     flop(invert_output=False, invert_clock=True,  has_reset=True,  has_set=False, has_loopback=False, has_scanchain=False),
        'dfrtn#i':   flop(invert_output=True , invert_clock=True,  has_reset=True,  has_set=False, has_loopback=False, has_scanchain=False),
        'dfstp':     flop(invert_output=False, invert_clock=False, has_reset=False, has_set=True,  has_loopback=False, has_scanchain=False),
        'dfstp#i':   flop(invert_output=True , invert_clock=False, has_reset=False, has_set=True,  has_loopback=False, has_scanchain=False),
        'dfbtp#':    flop(invert_output=False, invert_clock=False, has_reset=True,  has_set=True,  has_loopback=False, has_scanchain=False),
        'dfbtp#i':   flop(invert_output=True , invert_clock=False, has_reset=True,  has_set=True,  has_loopback=False, has_scanchain=False),
        'dfbtn#':    flop(invert_output=False, invert_clock=True,  has_reset=True,  has_set=True,  has_loopback=False, has_scanchain=False),
        'dfbtn#i':   flop(invert_output=True , invert_clock=True,  has_reset=True,  has_set=True,  has_loopback=False, has_scanchain=False),
        'edfxtp':    flop(invert_output=False, invert_clock=False, has_reset=False, has_set=False, has_loopback=True,  has_scanchain=False),
        'edfxtp#i':  flop(invert_output=True , invert_clock=False, has_reset=False, has_set=False, has_loopback=True,  has_scanchain=False),
        'sdfxtp':    flop(invert_output=False, invert_clock=False, has_reset=False, has_set=False, has_loopback=False, has_scanchain=True),
        'sdfxtp#i':  flop(invert_output=True , invert_clock=False, has_reset=False, has_set=False, has_loopback=False, has_scanchain=True),
        'sdfrtp':    flop(invert_output=False, invert_clock=False, has_reset=True,  has_set=False, has_loopback=False, has_scanchain=True),
        'sdfrtp#i':  flop(invert_output=True , invert_clock=False, has_reset=True,  has_set=False, has_loopback=False, has_scanchain=True),
        'sdfrtn':    flop(invert_output=False, invert_clock=True,  has_reset=True,  has_set=False, has_loopback=False, has_scanchain=True),
        'sdfrtn#i':  flop(invert_output=True , invert_clock=True,  has_reset=True,  has_set=False, has_loopback=False, has_scanchain=True),
        'sdfstp':    flop(invert_output=False, invert_clock=False, has_reset=False, has_set=True,  has_loopback=False, has_scanchain=True),
        'sdfstp#i':  flop(invert_output=True , invert_clock=False, has_reset=False, has_set=True,  has_loopback=False, has_scanchain=True),
        'sdfbtp#':   flop(invert_output=False, invert_clock=False, has_reset=True,  has_set=True,  has_loopback=False, has_scanchain=True),
        'sdfbtp#i':  flop(invert_output=True , invert_clock=False, has_reset=True,  has_set=True,  has_loopback=False, has_scanchain=True),
        'sdfbtn#':   flop(invert_output=False, invert_clock=True,  has_reset=True,  has_set=True,  has_loopback=False, has_scanchain=True),
        'sdfbtn#i':  flop(invert_output=True , invert_clock=True,  has_reset=True,  has_set=True,  has_loopback=False, has_scanchain=True),
        'sedfxtp':   flop(invert_output=False, invert_clock=False, has_reset=False, has_set=False, has_loopback=True,  has_scanchain=True),
        'sedfxtp#i': flop(invert_output=True , invert_clock=False, has_reset=False, has_set=False, has_loopback=True,  has_scanchain=True),
    }

    for i in range(73):
        cell = pin_mapping[i]
        if cell in cell_mapping:
            cell = cell_mapping[cell]
        io_pairs, sequential = pin_tests[cell]
        lenient = sequential and not gatelevel
        await check_cell_pin(dut, i, io_pairs, lenient)

