
#!/usr/bin/python3
import argparse
import importlib.util
import sys
from codetypes import *
from wordasm import *

def eliminateLabels(code: list[LabeledAssemblyCode]) -> tuple[list[AssemblyCode], dict[str, int]]:
    """ Lowers away LabeledAssemblyCode instructions. Returns a tuple of AssemblyCode and
        a dictionary mapping label definitions to addresses."""
    labels: dict[str, int] = {}
    address = 0

    for line in code:
        if isinstance(line, Label):
            if line.label in labels:
                raise Exception("Duplicate label definition: {0}".format(line.label))
            labels[line.label] = address
        else:
            address += 4

    def labelAddress(ref: LabelRef) -> int:
        if ref.label not in labels:
            raise Exception("Undefined label: {0}".format(ref.label))
        return labels[ref.label]

    newCode: list[AssemblyCode] = []
    address = 0

    for line in code:
        if isinstance(line, Label):
            continue
        elif isinstance(line, LabelRef):
            newCode.append(Word(labelAddress(line)))
        elif isinstance(line, B) and isinstance(line.offset, LabelRef):
            target = labelAddress(line.offset)
            pc = address + 8
            delta = target - pc
            if delta % 4 != 0:
                raise Exception("Branch target is not word-aligned: {0}".format(line.offset.label))
            newCode.append(B(Word(delta // 4), line.cond))
        elif isinstance(line, Bl) and isinstance(line.offset, LabelRef):
            target = labelAddress(line.offset)
            pc = address + 8
            delta = target - pc
            if delta % 4 != 0:
                raise Exception("Branch target is not word-aligned: {0}".format(line.offset.label))
            newCode.append(Bl(Word(delta // 4), line.cond))
        elif isinstance(line, LdrRel):
            newCode.append(Ldr(line.rd, Reg(15), Word(labelAddress(line.l) - (address + 8)), line.cond))
        elif isinstance(line, LdrbRel):
            newCode.append(Ldrb(line.rd, Reg(15), Word(labelAddress(line.l) - (address + 8)), line.cond))
        elif isinstance(line, StrRel):
            newCode.append(Str(line.rd, Reg(15), Word(labelAddress(line.l) - (address + 8)), line.cond))
        elif isinstance(line, StrbRel):
            newCode.append(Strb(line.rd, Reg(15), Word(labelAddress(line.l) - (address + 8)), line.cond))
        else:
            newCode.append(line)

        address += 4

    return (newCode, labels)

def assembleCode(code: list[LabeledAssemblyCode | AssemblyCode], out = sys.stdout.buffer):
    """ Assembles a List of LabeledAssemblyCode objects to the target file. """
    newCode, labels = eliminateLabels(code)
    for label in labels:
        print("label {0} => {1}".format(label, labels[label]), file=sys.stderr)

    assembleWords(lowerAssemblyCode(newCode), out)

if __name__ == "__main__":
    if sys.platform == "win32":
        import os, msvcrt
        msvcrt.setmode(sys.stdout.fileno(  ), os.O_BINARY)

    parser = argparse.ArgumentParser(
                    prog="labelasm",
                    description="Assembles a sequence of LabeledAssemblyCode objects")
    parser.add_argument("filename")
    args = parser.parse_args()
    
    spec = importlib.util.spec_from_file_location("code", args.filename)
    code = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(code)
    assembleCode(code.CODE) 
