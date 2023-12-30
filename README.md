This is a project we did for our assembly course at Shiraz University.
I tried to create a simulator for x86 processors that can read assembly code and generate machine code.
I supported five general type of instructions:
1. REG → REG
2. REG → MEM
3. MEM → REG
4. IMM → REG
5. Simple JMP

Introduction to what we do
First let's take a look at what happens when an assembler assembles a code. We use 32-bit assembly and support only certain modes, so we're working to understand those modes better.
Usually in supported format we have two general byte to specify an instruction and its operand(s).
1) opCode 2) Mod-REG-R/M
opCode
Opcode has three parts:
1. Six MSB bits that specify the Instruction.
   <img width="320" alt="Screenshot 2023-12-31 at 12 02 54 AM" src="https://github.com/SinaHkz/x8086-Assembler/assets/118515310/0829df62-07cd-43ba-a172-3e83d397b75c">
   
2. The second bit, called ‘d’, shows whether the part in the second byte is for the destination or source.
If d = 0, REG is the source and R/M is the destination, otherwise, it’s the other way around.

4. The LSB bit, called ‘s’, shows whether the register in the operands is 8-bit or 16/32-bit. If s = 0, it means REG is an 8-bit register, otherwise, it’s a 16/32-bit register.
Question: how to understand whether a register is 16-bit or 32-bit ?
Answer: we add a prefix for 16-bit register to specify it from 32-bit.

Mod-REG-R/M
This byte also has three part:
1. The two most significant bits (MSBs) represent the mod part, specifying the type of
process we are performing. We use only 11 and 00 mods in this project.
<img width="443" alt="Screenshot 2023-12-31 at 12 04 37 AM" src="https://github.com/SinaHkz/x8086-Assembler/assets/118515310/f4bac2c3-0748-4ff8-8c1e-02fa54a2cec6">
2. Next three bits represent the REG part, show register code
3. The three least significant bits (LSBs) represent either the memory or the second register
used in the code.
<img width="436" alt="Screenshot 2023-12-31 at 12 05 05 AM" src="https://github.com/SinaHkz/x8086-Assembler/assets/118515310/8ca1b608-4866-422c-89ff-c1456c4c98ef">

One operand instructions
These instructions have their own opCode type and we discuss them separately.
inc
1. The opcode for 32-bit registers is represented as 40h + [REG value]. This value is in hexadecimal format, and the addition should be performed using hexadecimal numbers.
2. The opCode for 16-bit register is represented as 32-bit does but with an addition of 66 prefix.
3. The opCode of the 8-bit register is represented as “FE xx000xxx”. xx is mod and xxx is register value.

dec
1. The opcode for 32-bit registers is represented as 48h + [REG value]. This value is in hexadecimal format, and the addition should be performed using hexadecimal numbers.
2. The opCode for 16-bit register is represented as 32-bit does but with an addition of 66 prefix.
3. The opCode of the 8-bit register is represented as “FE xx001xxx”. xx is mod and xxx is register value.
Push
1. The opcode for 32-bit registers is represented as 50h + [REG value]. This value is in hexadecimal format, and the addition should be performed using hexadecimal numbers.
2. The opCode for 16-bit register is represented as 32-bit does but with an addition of 66 prefix.
Note: push instruction machine code when push an immediate value is “6a immValue”. If immValue is between -128 and 127 it will be written in 1 byte otherwise written in 4 byte and ofcourse in little endian.
Pop
1. The opcode for 32-bit registers is represented as 58h + [REG value]. This value is in hexadecimal format, and the addition should be performed using hexadecimal numbers.
2. The opCode for 16-bit register is represented as 32-bit does but with an addition of 66 prefix.
Assembler for x86 7
Jmp instruction
Jmp instruction opCode is “eb” and the second byte of its machine code is the space of label between jmp and label.



