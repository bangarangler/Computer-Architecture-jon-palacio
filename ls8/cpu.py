"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.register = [0] * 8
        self.ram = [0] * 256
        self.pc = 0
        self.branchtable = {}
        self.branchtable[0b10100000] = self.handle_ADD
        self.branchtable[0b10100011] = self.handle_SUB
        self.branchtable[0b10100010] = self.handle_MUL
        self.branchtable[0b10100011] = self.handle_DIV
        # self.branchtable[0b01001000] = self.handle_PRA
        self.branchtable[0b01000111] = self.handle_PRN
        self.branchtable[130] = self.handle_LDI
        # self.branchtable[0b00000001] = self.handle_HLT
        self.branchtable["operand_a"] = 0
        self.branchtable["operand_b"] = 0

    def handle_ADD(self, operand_a, operand_b):
        self.alu("ADD", operand_a, operand_b)

    def handle_SUB(self, operand_a, operand_b):
        self.alu("SUB", operand_a, operand_b)

    def handle_MUL(self, operand_a, operand_b):
        self.alu("MUL", operand_a, operand_b)

    def handle_DIV(self, operand_a, operand_b):
        self.alu("DIV", operand_a, operand_b)

    def handle_PRN(self, operand_a, operand_b):
        self.alu("PRN", operand_a, operand_b)

    # def handle_PRA(self, operand_a, operand_b):
        # self.alu("PRA", operand_a, operand_b)

    def handle_LDI(self, operand_a, operand_b):
        self.alu("LDI", operand_a, operand_b)

    def handle_HLT(self, operand_a, operand_b):
        self.alu("HLT", operand_a, operand_b)

    def dispatch(self, IR, opA, opB):
        # Example calls into the branch table
        print(f"IR: {IR}")
        IR = int(IR, 2)
        print(f"{IR}")
        self.branchtable[IR](opA, opB)

    def load(self):
        """Load a program into memory."""


        # For now, we've just hardcoded a program:
        if len(sys.argv) is not 2:
            print(f"Sorry, no program found.")
            sys.exit("Must pass in a program.")
        try:
            address = 0
            program_name = sys.argv[1]
            with open(program_name) as file:
                for line in file:
                    # - line = #AABBBCCCC -> #[#,AABBCCCC] -> #
                    number = line.split("#", 1)[0]
                    if number.strip() == "":
                        continue
                    num =  int(number, 2)
                    print(num)
                    self.ram[address] = num
                    address += 1
            print(self.ram)
        except FileNotFoundError:
            print(f"{sys.argv[1]}")
            sys.exit("Exiting!")

        # program = [
            # # From print8.ls8
            # 0b10000010, # LDI R0,8
            # 0b00000000,
            # 0b00001000,
            # 0b01000111, # PRN R0
            # 0b00000000,
            # 0b00000001, # HLT
        # ]

        # for instruction in program:
            # self.ram[address] = instruction
            # address += 1

        print(f"{self.ram}")
    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value


    def alu(self, op, operand_a, operand_b):
        """ALU operations."""

        if op == "ADD":
            self.register[operand_a] += self.register[operand_b]
        #elif op == "SUB": etc
        elif op == "SUB":
            slef.register[operand_a] -= self.register[operand_b]
        elif op == "MUL":
            self.register[operand_a] *= self.register[operand_b]
        elif op == "DIV":
            self.register[operand_a] /= self.register[operand_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        running = True
        while running:
            IR = self.pc
            operand_a = self.ram_read(IR + 1)
            operand_b = self.ram_read(IR + 2)
            print(f"ram @ IR: {type(self.ram[IR])}")
            if self.ram[IR] == 0b00000001:
              running = False
            else:
              self.dispatch(bin(int(self.ram[IR])), operand_a, operand_b)
            # elif self.ram[IR] == 0b10000010:
                # self.register[operand_a] = operand_b
                # self.pc += 3
            # elif self.ram[IR] == 0b01000111:
                # print(self.register[operand_a])
                # self.pc += 2
            # elif self.ram[IR] == 0b10100010:
                # self.alu("MUL", operand_a, operand_b)
                # self.pc += 3




        # command = {
            # "HLT": 0b00000001,
            # "ADD": 0b10100000,
            # "SUB": 0b10100011,
            # "MUL": 0b10100010,
            # "DIV": 0b10100011,
            # "PRA": 0b01001000,
            # "PRN": 0b01000111,
            # "LDI": 0b10000010
        # }




cpu = CPU()
# cpu.ram_write(8,8)
# # print(f"{cpu.ram}")
# # print(f"{cpu.ram_read(64)}")
# # print(f"{cpu.ram}")
cpu.load()
cpu.run()
# dispatch(0B10100000, 1, 2)
# handle_ADD(1,2)
# cpu.dispatch(0b10100000,1,2)


