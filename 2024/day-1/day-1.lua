#!/usr/bin/env lua

-- Read the input data into two tables
local nof_lines = 0
-- local locations = io.open("test.txt", "r")
local locations = io.open("input1.txt", "r")

local left_table = {}
local right_table = {}

for line in locations:lines() do
    nof_lines = nof_lines + 1
    local left, right = string.match(line, "(%g+)%s*(%g+)")
    left_table[#left_table + 1] = left
    right_table[#right_table + 1] = right
end

print("The input file contains " .. nof_lines .. " lines")

-- Sort the tables
table.sort(left_table)
table.sort(right_table)

-- Calculate the distances and store in a table
local distances = {}
for i = 1, #left_table do
    distances[i] = math.abs(left_table[i] - right_table[i])
end

local distance_sum = 0
for i = 1, #distances do
    distance_sum = distance_sum + distances[i]
end

print("The total distance is " .. distance_sum)
