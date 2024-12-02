#!/usr/bin/env lua

-- Finds start and end index of an item in a sorted list. Start at the designated position.
-- Returns nil if no match
local function find_match_interval(list, item)
    local first_index
    local last_index
    for i = 1, #list do
        if list[i] == item then
            first_index = i
            break
        end
    end

    if first_index ~= nil then
        for i = first_index, #list do
            if list[i] ~= item then
                last_index = i - 1
                break
            end
        end
    end

    return first_index, last_index
end

-- Read the input data into two lists
local nof_lines = 0
-- local locations = io.open("test.txt", "r")
local locations = io.open("input1.txt", "r")

local left_list = {}
local right_list = {}

for line in locations:lines() do
    nof_lines = nof_lines + 1
    local left, right = string.match(line, "(%g+)%s*(%g+)")
    left_list[#left_list + 1] = left
    right_list[#right_list + 1] = right
end

print("The input file contains " .. nof_lines .. " lines")

-- Sort the lists
table.sort(left_list)
table.sort(right_list)

-- Calculate the distances and store in a list
local distances = {}
for i = 1, nof_lines do
    distances[i] = math.abs(left_list[i] - right_list[i])
end

local total_distance = 0
for i = 1, nof_lines do
    total_distance = total_distance + distances[i]
end

print("The total distance is " .. total_distance)

-- Create a similarity table
local similarities = {}

for i = 1, nof_lines do
    -- Take the item in the left list and find the position of the first match in the
    -- right list
    local item = left_list[i]
    local first_index, last_index = find_match_interval(right_list, item)

    if first_index ~= nil then
        similarities[i] = item * (last_index - first_index + 1)
    end
end

local similarity_score = 0
for _, v in pairs(similarities) do
    similarity_score = similarity_score + v
end

print("The similarity score is " .. similarity_score)
