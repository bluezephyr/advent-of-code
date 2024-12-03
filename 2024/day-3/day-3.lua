#!/usr/bin/env lua

-- local filename = "test.txt"
local filename = "input1.txt"
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
        program[program.len] = instr
        -- print("Instruction: " .. instr.op .. "(" .. instr.left .. "," .. instr.right .. ")")
    end
end

local function exec(instruction, env)
    if instruction.op == "mul" then
        local result = instruction.left * instruction.right
        env.product = env.product + result
    end
end

-- Parse program
local program = { len = 0, instructions = {} }
for _, line in pairs(input) do
    parse_instructions(line, program)
end
print("Instructions: " .. program.len)

-- Execute program
local env = { product = 0 }
for i = 1, program.len do
    exec(program[i], env)
end

print("The total product is " .. env.product)
