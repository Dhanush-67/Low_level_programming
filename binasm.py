#!/usr/bin/python3
import argparse
import importlib.util
import sys

from codetypes import *
from wordasm import *
from binasm import *


def _rol32(value: int, amount: int) -> int:
    amount %= 32
    value &= 0xFFFFFFFF
    return ((value << amount) | (value >> (32 - amount))) & 0xFFFFFFFF


def _encode_operand2(op2: Reg | Word) -> tuple[int, int]:
    if isinstance(op2, Reg):
        return (0, op2.reg)

    value = op2.value & 0xFFFFFFFF
    for rotate_imm in range(16):
        imm8 = _rol32(value, 2 * rotate_imm)
        if imm8 <= 0xFF:
            return (1, (rotate_imm << 8) | imm8)

    raise Exception(f"Immediate value cannot be encoded in ARM operand2: {op2.value}")


def _encode_data_processing(
    cond: Cond,
    opcode: int,
    set_flags: int,
    rn: int,
    rd: int,
    op2: Reg | Word,
) -> Word:
    immediate_bit, operand2 = _encode_operand2(op2)
    return Word(
        (int(cond) << 28)
        | (immediate_bit << 25)
        | (opcode << 21)
        | (set_flags << 20)
        | (rn << 16)
        | (rd << 12)
        | operand2
    )


def _encode_single_transfer(cond: Cond, load: bool, byte: bool, rd: int, rn: int, off: Word) -> Word:
    offset = off.value
    up_bit = 1
    if offset < 0:
        up_bit = 0
        offset = -offset

    if offset > 0xFFF:
        raise Exception(f"Offset out of range for load/store instruction: {off.value}")

    return Word(
        (int(cond) << 28)
        | (0b01 << 26)
        | (1 << 24)
        | (up_bit << 23)
        | (int(byte) << 22)
        | (int(load) << 20)
        | (rn << 16)
        | (rd << 12)
        | offset
    )


def _encode_branch(cond: Cond, link: bool, offset: Word | LabelRef) -> Word:
    if not isinstance(offset, Word):
        raise Exception(f"Expected label references to be eliminated before assembly: {offset}")

    return Word(
        (int(cond) << 28)
        | ((0b1010 | int(link)) << 24)
        | (offset.value & 0x00FFFFFF)
    )


def lowerAssemblyCode(code: list[AssemblyCode]) -> list[Word]:
    output: list[Word] = []

    for line in code:
        if isinstance(line, Word):
            output.append(line)
        elif isinstance(line, Add):
            output.append(_encode_data_processing(line.cond, 0b0100, 0, line.r1.reg, line.rd.reg, line.op2))
        elif isinstance(line, Sub):
            output.append(_encode_data_processing(line.cond, 0b0010, 0, line.r1.reg, line.rd.reg, line.op2))
        elif isinstance(line, Cmp):
            output.append(_encode_data_processing(line.cond, 0b1010, 1, line.r1.reg, 0, line.op2))
        elif isinstance(line, Mov):
            output.append(_encode_data_processing(line.cond, 0b1101, 0, 0, line.r1.reg, line.op2))
        elif isinstance(line, Mul):
            output.append(
                Word(
                    (int(line.cond) << 28)
                    | (line.rd.reg << 16)
                    | (line.r1.reg << 8)
                    | (0b1001 << 4)
                    | line.r2.reg
                )
            )
        elif isinstance(line, SDiv):
            output.append(
                Word(
                    (int(line.cond) << 28)
                    | (0b01110001 << 20)
                    | (line.rd.reg << 16)
                    | (0b1111 << 12)
                    | (line.r2.reg << 8)
                    | (0b0001 << 4)
                    | line.r1.reg
                )
            )
        elif isinstance(line, UDiv):
            output.append(
                Word(
                    (int(line.cond) << 28)
                    | (0b01110011 << 20)
                    | (line.rd.reg << 16)
                    | (0b1111 << 12)
                    | (line.r2.reg << 8)
                    | (0b0001 << 4)
                    | line.r1.reg
                )
            )
        elif isinstance(line, B):
            output.append(_encode_branch(line.cond, False, line.offset))
        elif isinstance(line, Bl):
            output.append(_encode_branch(line.cond, True, line.offset))
        elif isinstance(line, Bx):
            output.append(Word((int(line.cond) << 28) | (0x12FFF1 << 4) | line.r.reg))
        elif isinstance(line, Blx):
            output.append(Word((int(line.cond) << 28) | (0x12FFF3 << 4) | line.r.reg))
        elif isinstance(line, Ldr):
            output.append(_encode_single_transfer(line.cond, True, False, line.rd.reg, line.r1.reg, line.off))
        elif isinstance(line, Ldrb):
            output.append(_encode_single_transfer(line.cond, True, True, line.rd.reg, line.r1.reg, line.off))
        elif isinstance(line, Str):
            output.append(_encode_single_transfer(line.cond, False, False, line.rd.reg, line.r1.reg, line.off))
        elif isinstance(line, Strb):
            output.append(_encode_single_transfer(line.cond, False, True, line.rd.reg, line.r1.reg, line.off))
        else:
            raise Exception(f"Invalid instruction: {line}")

    return output


def assembleCode(code: list[AssemblyCode], out=sys.stdout.buffer):
    """ Assembles a List of AssemblyCode objects to the target file. """
    assembleWords(lowerAssemblyCode(code), out)


if __name__ == "__main__":
    if sys.platform == "win32":
        import os
        import msvcrt

        msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)

    parser = argparse.ArgumentParser(
        prog="binasm",
        description="Assembles a sequence of AssemblyCode objects",
    )
    parser.add_argument("filename")
    args = parser.parse_args()

    spec = importlib.util.spec_from_file_location("code", args.filename)
    code = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(code)
    assembleCode(code.CODE)
