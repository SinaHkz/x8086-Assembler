reg32Bit = {
    "eax": "000",
    "ecx": "001",
    "edx": "010",
    "ebx": "011",
    "esp": "100",
    "esi": "110",
    "edi": "111",
    "ebp": "101"
}
reg16Bit = {
    "ax": "000",
    "cx": "001",
    "dx": "010",
    "bx": "011",
    "sp": "100",
    "si": "110",
    "di": "111",
    "bp": "101"
}
reg8Bit = {
    "al": "000",
    "cl": "001",
    "dl": "010",
    "bl": "011",
    "ah": "100",
    "ch": "101",
    "dh": "110",
    "bh": "111"
}
opCodesInstructions = {
    "add": "000000",
    "or": "000010",
    "and": "001000",
    "sub": "001010",
    "xor": "001100",
    "push": "110010",
    "pop": "110110"
}
opCodesInstructionsForAx = {
    "add": "05",
    "or": "0d",
    "and": "25",
    "sub": "2d",
    "xor": "35",
}


def zeroExtend(string):
    return "0x" + "0" * (20 - len(string)) + string[2:] + " "


def complement16(num):
    if -129 < num:
        num += 256
    else:
        num += 2 ** 32
    num = hex(num)[2:]
    if len(num) < 2:  # only neg num come here and should get extended by f.
        num = "f" * (2 - len(num)) + num
    return num


def generateModString(regMem1, regMem2, num, mod):
    str = mod
    if num == 32:
        str += reg32Bit.get(regMem1)
    elif num == 16:
        str += reg16Bit.get(regMem1)
    else:
        str += reg8Bit.get(regMem1)
    if mod == "00":  # if we have indirect addressing we have reg in regMem2 that is 32 bit
        str += reg32Bit.get(regMem2)
    elif num == 32:
        str += reg32Bit.get(regMem2)
    elif num == 16:
        str += reg16Bit.get(regMem2)
    else:
        str += reg8Bit.get(regMem2)
    return str


def binaryToHex(string):
    str1 = string[:4]
    str2 = string[4:]
    str1 = hex(int(str1, 2))[2:]
    str2 = hex(int(str2, 2))[2:]
    return str1 + str2


def littleEdnian(imm, bit):
    try:  # handle push imm.
        isNeg = False
        if int(imm) < 0:
            temp = complement16(
                int(imm))  # convert -100dec to 100 in hex  | only neg num get passed to 16 compliment
            isNeg = True
        else:
            temp = hex(int(imm))[2:]
        if -128 > int(imm) or int(imm) > 127:
            if isNeg:
                temp = "f" * (bit // 4 - len(temp)) + temp  # bit is for little endian in 16 bit and 32 bit
            else:
                temp = "0" * (bit // 4 - len(temp)) + temp
            string = ""
            for i in range(len(temp) - 2, -1, -2):
                string += temp[i:i + 2] + " "
            return string
        elif len(temp) > 8:
            raise Exception
        elif len(temp) < 2:
            temp = "0" + temp
            return temp
        else:
            return temp
    except:
        res.append("invalid")
        return 0


def twoOperand(instruction, regMem1, regMem2, count, res):
    if regMem1 in reg32Bit.keys() and regMem2 in reg32Bit.keys():  # 32 bit register in mod 11
        second = generateModString(regMem2, regMem1, 32, "11")
        second = binaryToHex(second)
        first = binaryToHex(opCodesInstructions.get(instruction) + "01")
        res.append(zeroExtend(hex(count)) + first + " " + second + " ")
        return 2
    elif regMem1 in reg16Bit.keys() and regMem2 in reg16Bit.keys():  # 16 bit register in mod 11
        second = generateModString(regMem2, regMem1, 16, "11")
        second = binaryToHex(second)
        first = binaryToHex(opCodesInstructions.get(instruction) + "01")
        res.append(zeroExtend(hex(count)) + "66 " + first + " " + second + " ")
        return 3
    elif regMem1 in reg8Bit.keys() and regMem2 in reg8Bit.keys():  # 8 bit register in mod 11
        second = generateModString(regMem2, regMem1, 8, "11")
        second = binaryToHex(second)
        first = binaryToHex(opCodesInstructions.get(instruction) + "00")
        res.append(zeroExtend(hex(count)) + first + " " + second + " ")
        return 2


    elif regMem1[0] == '[' and regMem1[-1] == ']' and regMem1[
                                                      1:-1] in reg32Bit.keys() and regMem2 in reg32Bit.keys():  # this part is for (instruction [REG],REG).
        second = generateModString(regMem2, regMem1[1:-1], 32, "00")
        second = binaryToHex(second)
        first = binaryToHex(opCodesInstructions.get(instruction) + "01")
        res.append(zeroExtend(hex(count)) + first + ' ' + second)
        return 2
    elif regMem1[0] == '[' and regMem1[-1] == ']' and regMem1[1:-1] in reg32Bit.keys() and regMem2 in reg16Bit.keys():
        second = generateModString(regMem2, regMem1[1:-1], 16, "00")
        second = binaryToHex(second)
        first = binaryToHex(opCodesInstructions.get(instruction) + "01")
        res.append(zeroExtend(hex(count)) + "66 " + first + ' ' + second)
        return 3
    elif regMem1[0] == '[' and regMem1[-1] == ']' and regMem1[1:-1] in reg32Bit.keys() and regMem2 in reg8Bit:
        second = generateModString(regMem2, regMem1[1:-1], 8, "00")
        second = binaryToHex(second)
        first = binaryToHex(opCodesInstructions.get(instruction) + "00")
        res.append(zeroExtend(hex(count)) + first + ' ' + second)
        return 2


    elif regMem2[0] == '[' and regMem2[-1] == ']' and regMem2[
                                                      1:-1] in reg32Bit.keys() and regMem1 in reg32Bit.keys():  # this part is for (instruction REG,[REG]).
        second = generateModString(regMem1, regMem2[1:-1], 32, "00")
        second = binaryToHex(second)
        first = binaryToHex(opCodesInstructions.get(instruction) + "11")
        res.append(zeroExtend(hex(count)) + first + ' ' + second)
        return 2
    elif regMem2[0] == '[' and regMem2[-1] == ']' and regMem2[1:-1] in reg32Bit.keys() and regMem1 in reg16Bit.keys():
        second = generateModString(regMem1, regMem2[1:-1], 16, "00")
        second = binaryToHex(second)
        first = binaryToHex(opCodesInstructions.get(instruction) + "11")
        res.append(zeroExtend(hex(count)) + "66 " + first + ' ' + second)
        return 3
    elif regMem2[0] == '[' and regMem2[-1] == ']' and regMem2[1:-1] in reg32Bit.keys() and regMem1 in reg8Bit:
        second = generateModString(regMem1, regMem2[1:-1], 8, "00")
        second = binaryToHex(second)
        first = binaryToHex(opCodesInstructions.get(instruction) + "10")
        res.append(zeroExtend(hex(count)) + first + ' ' + second)
        return 2


def oneOperand(instruction, regMem1, count, res):
    if regMem1[0] == '[':
        res.append("invalid")
        return 0
    if instruction == "inc" and regMem1[0] != "[":
        if regMem1 in reg32Bit.keys():
            res.append(zeroExtend(hex(count)) + "4" + hex(int(reg32Bit.get(regMem1), 2))[2:])
            return 1
        elif regMem1 in reg16Bit.keys():
            res.append(zeroExtend(hex(count)) + "66 4" + hex(int(reg16Bit.get(regMem1), 2))[2:])
            return 2
        elif regMem1 in reg8Bit.keys():
            res.append(zeroExtend(hex(count)) + "fe" + " " + hex(int("11000" + reg8Bit.get(regMem1), 2))[2:])
            return 2
        else:
            res.append("invalid")
    elif instruction == "push" and regMem1[0] != "[":
        if regMem1[-1] == "h":
            regMem1 = int(regMem1[:-1], 16)
        elif regMem1[-1] == 'b':
            regMem1 = int(regMem1[:-1], 8)
        if regMem1 in reg32Bit.keys():
            res.append(zeroExtend(hex(count)) + "5" + hex(int(reg32Bit.get(regMem1), 2))[2:])
            return 1
        elif regMem1 in reg16Bit.keys():
            res.append(zeroExtend(hex(count)) + "66 5" + hex(int(reg16Bit.get(regMem1)))[2:])
            return 2
        string = littleEdnian(regMem1, 32)  # 32 bit immediate
        if -128 > int(regMem1) or int(regMem1) > 127:
            res.append(zeroExtend(hex(count)) + "68 " + string)
            return len(string) // 3 + 1
        res.append(zeroExtend(hex(count)) + "6a " + string)
        return len(string) // 3 + 1

    elif instruction == "dec" and regMem1[0] != "[":
        if regMem1 in reg32Bit.keys():
            x = int(reg32Bit.get(regMem1), 2)
            x += 48
            if x < 50:
                res.append(zeroExtend(hex(count)) + str(x))
                return 1
            else:
                res.append(zeroExtend(hex(count)) + "4" + hex(x % 40)[2:])
                return 1
        elif regMem1 in reg16Bit.keys():
            x = int(reg16Bit.get(regMem1), 2)
            x += 48
            if x < 50:
                res.append(zeroExtend(hex(count)) + "66 " + str(x))
                return 2
            else:
                res.append(zeroExtend(hex(count)) + "66 4" + hex(x % 40)[2:])
                return 2
        elif regMem1 in reg8Bit.keys():
            res.append(zeroExtend(hex(count)) + "fe" + " " + hex(int("11001" + reg8Bit.get(regMem1), 2))[2:])
            return 2
        else:
            res.append("invalid")
            return 0
    elif instruction == "pop" and regMem1[0] != "[":
        if regMem1 in reg32Bit.keys():
            x = int(reg32Bit.get(regMem1), 2)
            x += 58
            if x < 60:
                res.append(zeroExtend(hex(count)) + str(x))
                return 1
            else:
                res.append(zeroExtend(hex(count)) + "5" + hex(x % 50)[2:])
                return 1
        elif regMem1 in reg16Bit.keys():
            x = int(reg16Bit.get(regMem1), 2)
            x += 58
            if x < 60:
                res.append(zeroExtend(hex(count)) + "66 " + str(x))
                return 2
            else:
                res.append(zeroExtend(hex(count)) + "66 5" + hex(x % 50)[2:])
                return 2
        elif regMem1 in reg8Bit.keys():
            res.append(zeroExtend(hex(count)) + "fe" + " " + hex(int("11001" + reg8Bit.get(regMem1), 2))[2:])
            return 2
        else:
            res.append("invalid")
            return 0


def immOprand(instruction, regMem, imm, count, res):
    if regMem in reg32Bit.keys() or regMem in reg16Bit.keys():  # 32-16 bit register with imm
        if -128 < imm < 127:
            if imm < 0:
                second = complement16(imm)
            else:
                second = hex(imm)[2:]
                if len(second) < 2:
                    second = "0" + second
            is16bit = False
            first = "11" + opCodesInstructions.get(instruction)[2:5] + reg32Bit.get(regMem1)
            first = binaryToHex(first)
            machineCode = "83 " + first + " " + second + " "
            if regMem in reg16Bit.keys():
                machineCode = "66 " + machineCode
                is16bit = True
            res.append(zeroExtend(hex(count)) + machineCode)
            if is16bit:
                return 4
            return 3
        else:
            is16bit = False
            if regMem1 in reg32Bit:
                immHex = littleEdnian(imm, 32)
            else:
                immHex = littleEdnian(imm, 16)
            if instruction == "ax" or instruction == "eax":
                machineCode = opCodesInstructionsForAx.get(instruction) + " " + immHex
            else:
                if regMem1 in reg32Bit:
                    machineCode = "81 " + binaryToHex("11" + opCodesInstructions.get(instruction)[2:5] + reg32Bit.get(regMem1)) + " " + immHex
                else:
                    machineCode = "81 " + binaryToHex("11" + opCodesInstructions.get(instruction)[2:5] + reg16Bit.get(regMem1)) + " " + immHex
            if regMem in reg16Bit.keys():
                machineCode = "66 " + machineCode
                is16bit = True
            res.append(zeroExtend(hex(count)) + machineCode)
            if is16bit:
                return len(immHex) // 3 + 3
            return len(immHex) // 3 + 2
    elif regMem in reg8Bit.keys():  # 8 bit register with imm
        second = hex(imm)[2:]
        if regMem1 == "al":
            opCodeForAl = hex(int(opCodesInstructionsForAx.get(instruction), 16) - 1)[2:]
            res.append(zeroExtend(hex(count)) + opCodeForAl + " " + second)
            return 2
        first = "11" + opCodesInstructions.get(instruction)[2:5] + reg8Bit.get(regMem1)
        first = binaryToHex(first)
        res.append(zeroExtend(hex(count)) + "80 " + first + " " + second + " ")
        return 3
    else:
        res.append("invalid")
        return 0


with open('input.txt') as file:
    inp = file.read()
    inpList = inp.splitlines()
    label = {}
    jmpLoc = []
    count = 0
    res = []
    for i in range(len(inpList)):
        checkLabel = inpList[i].split(":")
        if len(checkLabel) == 2 and checkLabel[1] != "":  # label in a non-empty line
            L = checkLabel[0].lower()
            label[L] = count
            instructionLine = checkLabel[1][1:].split(" ")
        else:
            instructionLine = inpList[i].split(" ")
        instruction = instructionLine[0].lower()
        if instruction[-1] == ":":  # label in an empty line
            L = instruction[:-1]
            label[L] = count
            continue
        if instruction == "jmp":  # check the jmp instruction
            jmpLoc.append([instructionLine[1].lower(), len(res), count + 2])
            res.append(zeroExtend(hex(count)) + "eb ")
            count += 2
            continue
        regMem = instructionLine[1].split(",")  # separate registers
        regMem1 = regMem[0].lower()
        if len(regMem) > 1:  # two operands instructions
            regMem2 = regMem[1].lower()
            if regMem2 in reg32Bit.keys() or regMem2 in reg8Bit.keys() or regMem2 in reg16Bit.keys():
                count += twoOperand(instruction, regMem1, regMem2, count, res)
            else:
                count += immOprand(instruction, regMem1, int(regMem2), count, res)
        else:  # handle the one operand instruction
            count += oneOperand(instruction, regMem1, count, res)

    for i in range(len(jmpLoc)):  # fill the jmp string with addresses
        if jmpLoc[i][0] in label.keys():
            if label[jmpLoc[i][0]] - jmpLoc[i][2] > 0:
                res[jmpLoc[i][1]] += str(hex(label[jmpLoc[i][0]] - jmpLoc[i][2]))[2:]
            else:
                num = label[jmpLoc[i][0]] - jmpLoc[i][2]
                num += 256
                res[jmpLoc[i][1]] += str(hex(num))[2:]
for i in res:
    print(i)
