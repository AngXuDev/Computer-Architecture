"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
ADD = 0b10100000
PUSH = 0b01000101
POP = 0b01000110


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.SP = 7
        self.reg[self.SP] = 0xf4


    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            # 0b10000010,  # LDI R0,8
            # 0b00000000,
            # 0b00001000,
            # 0b01000111,  # PRN R0
            # 0b00000000,
            # 0b00000001,  # HLT

            # 0b10000010, # LDI R0,8
            # 0b00000000,
            # 0b00001000,
            # 0b10000010, # LDI R1,9
            # 0b00000001,
            # 0b00001001,
            # 0b10100010, # MUL R0,R1
            # 0b00000000,
            # 0b00000001,
            # 0b01000111, # PRN R0
            # 0b00000000,
            # 0b00000001, # HLT

            0b10000010, # LDI R0,1
            0b00000000,
            0b00000001,
            0b10000010, # LDI R1,2
            0b00000001,
            0b00000010,
            0b01000101, # PUSH R0
            0b00000000,
            0b01000101, # PUSH R1
            0b00000001,
            0b10000010, # LDI R0,3
            0b00000000,
            0b00000011,
            0b01000110, # POP R0
            0b00000000,
            0b01000111, # PRN R0
            0b00000000,
            0b10000010, # LDI R0,4
            0b00000000,
            0b00000100,
            0b01000101, # PUSH R0
            0b00000000,
            0b01000110, # POP R2
            0b00000010,
            0b01000110, # POP R1
            0b00000001,
            0b01000111, # PRN R2
            0b00000010,
            0b01000111, # PRN R1
            0b00000001,
            0b00000001 # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def ram_read(self, key):
        return self.ram[key]

    def ram_write(self, key, value):
        self.ram[key] = value

    def run(self):
        """Run the CPU."""
        halted = False

        while not halted:
            instruction = self.ram_read(self.pc)

            if instruction == PUSH:
                self.reg[self.SP] -= 1
                reg_num = self.ram_read(self.pc+1)
                reg_val = self.reg[reg_num]
                self.ram_write(self.reg[self.SP], reg_val)

                # operand_a = self.ram_read(self.pc+1)

                # self.ram_write(self.reg[self.SP], self.reg[operand_a])

                self.pc += 2

            elif instruction == POP:
                val = self.ram_read(self.reg[self.SP])
                reg_num = self.ram_read(self.pc + 1)
                self.reg[reg_num] = val
                # self.reg[operand_a] = self.ram_read(self.reg[self.SP])
                # operand_a = self.ram_read(self.pc+1)

                self.reg[self.SP] += 1

                self.pc += 2

            elif instruction == LDI:
                operand_a = self.ram_read(self.pc+1)
                operand_b = self.ram_read(self.pc+2)

                self.reg[operand_a] = operand_b

                self.pc += 3

            elif instruction == PRN:
                operand_a = self.ram_read(self.pc+1)
                print(self.reg[operand_a])

                self.pc += 2

            elif instruction == HLT:
                halted = True
                self.pc = 0
            
            elif instruction == MUL:
                operand_a = self.ram_read(self.pc+1)
                operand_b = self.ram_read(self.pc+2)

                self.alu("MUL", operand_a, operand_b)
                
                self.pc += 3

            elif instruction == ADD:
                operand_a = self.ram_read(self.pc+1)
                operand_b = self.ram_read(self.pc+2)

                self.alu("ADD", operand_a, operand_b)
                
                self.pc += 3

            else:
                print(f"Unknown instruction at index {self.pc}")
                sys.exit(1)
