#!/usr/bin/env lua

-- local filename = "test.txt"
-- local filename = "test2.txt"
local filename = "input1.txt"
local locations = io.open(filename, "r")

local input = {}
for line in locations:lines() do
    input[#input + 1] = line
end

print("The input file '" .. filename .. "' contains " .. #input .. " lines")

local function first_pos(list)
    local positions = {}
    for _, item in pairs(list) do
        if item then
            positions[#positions + 1] = item
        end
    end
    if #positions > 0 then
        table.sort(positions)
        return positions[1]
    end
    return 0
end

-- Return the next instruction in the stream and the location where to start the search
-- for the next instruction
local function next_instruction(stream, pos)
    local mul_start, mul_end, mul_op, mul_left, mul_right = string.find(stream, "(%mul)%((%d+),(%d+)%)", pos)
    local dont_start, dont_end, dont_op = string.find(stream, "(don't)%(%)", pos)
    local do_start, do_end, do_op = string.find(stream, "(do)%(%)", pos)
    local first_instr = first_pos({ mul_start, dont_start, do_start })
    -- print("NEXT: " .. pos .. ", first_instr: " .. first_instr)
    if first_instr == mul_start then
        local instr = { op = mul_op, left = mul_left, right = mul_right }
        -- print(instr.op .. "(" .. instr.left .. "," .. instr.right .. ") @" .. first_instr .. "-" .. mul_end)
        return instr, mul_end
    end
    if first_instr == dont_start then
        local instr = { op = dont_op }
        -- print(instr.op .. " @" .. first_instr .. "-" .. dont_end)
        return instr, dont_end
    end
    if first_instr == do_start then
        local instr = { op = do_op }
        -- print(instr.op .. " @" .. first_instr .. "-" .. do_end)
        return instr, do_end
    end
end

local function parse_instructions(stream, program)
    local pos = 1
    while pos <= #stream do
        local instr
        instr, pos = next_instruction(stream, pos)
        if not instr then
            return
        end
        program.len = program.len + 1
        program[program.len] = instr
    end
end

local function exec(instruction, env)
    if instruction.op == "mul" and env.enabled then
        local result = instruction.left * instruction.right
        env.product = env.product + result
    end
    if instruction.op == "don't" then
        env.enabled = false
    end
    if instruction.op == "do" then
        env.enabled = true
    end
end

-- Concat the input
local stream = ""
for _, line in pairs(input) do
    stream = stream .. line
end

-- Parse program
local program = { len = 0, instructions = {} }
parse_instructions(stream, program)
print("Instructions: " .. program.len)

-- Execute program
print("Running program")
local env = { product = 0, enabled = true }
for i = 1, program.len do
    exec(program[i], env)
end

print("The total product is " .. env.product)
