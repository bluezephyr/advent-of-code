#!/usr/bin/env lua

-- local filename = "test.txt"
local filename = "input1.txt"
local locations = io.open(filename, "r")

local input = {}
for line in locations:lines() do
    input[#input + 1] = line
end

print("The input file '" .. filename .. "' contains " .. #input .. " lines")

local function parse_instructions(line)
    local nof_instructions = 0
    local instructions = {}
    for instruction in string.gmatch(line, "%mul%(%d+,%d+%)") do
        nof_instructions = nof_instructions + 1
        local op = string.gmatch(instruction, "%mul")()
        local left = string.gmatch(instruction, "%((%d+)")()
        local right = tonumber(string.gmatch(instruction, "(%d+)%)")())
        local instr = {}
        instr.op = op
        instr.left = left
        instr.right = right
        instructions[nof_instructions] = instr
        print("Instruction: " .. instr.op .. "(" .. instr.left .. "," .. instr.right .. ")")
    end
    return instructions
end

local product = 0
local instructions = {}
for _, line in pairs(input) do
    instructions = parse_instructions(line)
    for _, instruction in pairs(instructions) do
        local result = instruction.left * instruction.right
        product = product + result
    end
end

print("Instructions: " .. #instructions)

-- local product = 0
-- for _, instruction in pairs(instructions) do
--     local result = instruction.left * instruction.right
--     product = product + result
-- end

print("The total product is " .. product)
