# This is a script that will act as an assembler to translate the .asm file to
# hack language for any given asm program
# just load any asm file in the main function and it will ouput a test file and hack file

# Created a dictionary that holds all the translation of assembly language to binary
# which could then be accessed through key and value mapping
# the value of a condidition for CompTable values has been factored in

# To check if the results are correct, use the Assembler.bat to build a comparison
# Load the Assembly file to be translated in Assembler.bat, then click on the = sign and 
# then you can load your generated hack file, then click run to start the comparison.

CompTable = { # this combined with the a value
    "0": "0101010",
    "1": "0111111",
    "-1": "0111010",
    "D": "0001100",
    "A": "0110000",
    "!D": "0001101",
    "!A": "0110001",
    "-D": "0001111",
    "-A": "0110011",
    "D+1": "0011111",
    "A+1": "0110111",
    "D-1": "0001110",
    "A-1": "0110010",
    "D+A": "0000010",
    "D-A": "0010011",
    "A-D": "0000111",
    "D&A": "0000000",
    "D|A": "0010101",
    "M": "1110000",
    "!M": "1110001",
    "-M": "1110011",
    "M+1": "1110111",
    "M-1": "1110010",
    "D+M": "1000010",
    "D-M": "1010011",
    "M-D": "1000111",
    "D&M": "1000000",
    "D|M": "1010101"
    }

# for the DestinationTableination values as provided in the nandtetris table of the book
DestinationTable = {
    "null": "000",
    "M": "001",
    "D": "010",
    "A": "100",
    "MD": "011",
    "AM": "101",
    "AD": "110",
    "AMD": "111"
    }

# for the jump segment of the c instruction
JumpTable = {
    "null": "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111"
    }

# symbols for the RAM address for predefine variables and will also hold other
# variables which are not pref
Symboltable = {
    "SP": 0,
    "LCL": 1,
    "ARG": 2,
    "THIS": 3,
    "THAT": 4,
    "SCREEN": 16384,
    "KBD": 24576,
    }

# a loop for RO-R15: 0-15
for i in range (0,16):
    label = "R" + str(i)
    Symboltable[label] = i
# print(Symboltable) # works well

def cleanFile(file):
    # Remove commented lines and white spaces
    # forms a temporary test file that we give to aTranslation
    outfile = open("general.test", "w") # a temporary file to save file without comments.
    for line in file:
        line = line.strip()
        commentindex = line.find("/")
        if commentindex > 0:
            linelabel = line[0:commentindex]
            outfile.write(linelabel + "\n")
        elif commentindex == 0:
            pass
        elif line == "":
            pass
        else:
            outfile.write(line+"\n")
    outfile.close()

def Counters(file):
    # this function updates the Symboltable with program and variable lables
    # It also returns a list of a and c instructions which will be used
    # for translation
    programCounter = 0
    variableCounter = 16
    instructions = []
    for line in file: # for program lables
        line = line.strip()
        if line[0] == "(":
            programLable = line[1:-1]
            Symboltable[programLable] = programCounter
        else:
            programCounter += 1
            instructions.append(line)

    for line in instructions: # for valriable lables
        if line[0] == "@":
            if line[1].isalpha():
                variableLabel = line[1:] # prints the label ignoring @
                # print("the variable label is " + variableLabel)
                if variableLabel in Symboltable: # checks if the label already exists in Symboltable
                    pass
                else:
                    Symboltable[variableLabel] = variableCounter
                    variableCounter += 1
    return instructions # returns a list of a and c instruction


def aTranslate(line):
    # this is for conducting A translation on each line of the clean file
    if line[1].isalpha():
        variableLabel = line[1:] # gets the label
        variableValue = Symboltable.get(variableLabel) # gets the value of the key from the Symboltable
        binaryValue = bin(variableValue)[2:].zfill(16) # converts it to binary
    else:
        variableValue = int(line[1:]) # if it is integer to the last digit
        binaryValue = bin(variableValue)[2:].zfill(16) # converts it to binary
    return binaryValue

def cTranslate(line):
    if line.find("=") > 0:
        line_list = line.split("=") # returns a list of two parts
        jump = "000"
        dest_value = DestinationTable.get(line_list[0])
        comp_value = CompTable.get(line_list[1])
    else:
        line_list = line.split(";")
        jump = JumpTable.get(line_list[1]) # find a way of handling jump
        dest_value = "000"
        comp_value = CompTable.get(line_list[0])
    ctranslation = "111" + comp_value + dest_value + jump
    return ctranslation

def assemblerTranslator():
    rawfile = open("RectL.asm", "r")
    cleanfile = open("general.test", "r")
    outfile = open("general.hack", "w") # the final file that is loaded
    # in assembler bat for comparison
    cleanFile(rawfile)
    instructions = Counters(cleanfile)
    for line in instructions:
        print(line)
        char = line[0]
        if char == "@":
            tline = aTranslate(line)
        else:
            tline = cTranslate(line)
        outfile.write(tline + "\n")
    rawfile.close()
    cleanfile.close()
    outfile.close()

assemblerTranslator()
