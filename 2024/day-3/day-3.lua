#!/usr/bin/env lua

-- local filename = "test.txt"
local filename = "test2.txt"
-- local filename = "input1.txt"
local locations = io.open(filename, "r")

local input = {}
for line in locations:lines() do
    input[#input + 1] = line
end

print("The input file '" .. filename .. "' contains " .. #input .. " lines")

local function parse_instructions(line, program)
    for instruction in string.gmatch(line, "%mul%(%d+,%d+%)") do
        program.len = program.len + 1
        local instr = {
            op = string.gmatch(instruction, "%mul")(),
            left = tonumber(string.gmatch(instruction, "%((%d+)")()),
            right = tonumber(string.gmatch(instruction, "(%d+)%)")())
        }
        print("Instruction: " .. instr.op .. "(" .. instr.left .. "," .. instr.right .. ")")
        program[program.len] = instr
    end
end

local function exec(instruction, env)
    if instruction.op == "mul" then
        local result = instruction.left * instruction.right
        env.product = env.product + result
    end
end

-- Concat the input
local input_stream = ""
for _, line in pairs(input) do
    input_stream = input_stream .. line
end

-- Parse program
local program = { len = 0, instructions = {} }
parse_instructions(input_stream, program)
print("Instructions: " .. program.len)

-- Execute program
local env = { product = 0 }
for i = 1, program.len do
    exec(program[i], env)
end

print("The total product is " .. env.product)
