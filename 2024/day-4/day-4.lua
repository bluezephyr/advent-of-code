#!/usr/bin/env lua

-- local filename = "test.txt"
local filename = "input1.txt"
local locations = io.open(filename, "r")

local input = {}
for line in locations:lines() do
    input[#input + 1] = line
end

local function iterator_len(iterator)
    local nof_matches = 0
    while true do
        local item = iterator()
        if item == nil then
            break
        end
        nof_matches = nof_matches + 1
    end
    return nof_matches
end

local function find_pattern(line, pattern)
    local reverse = string.reverse(line)
    local matches = string.gmatch(line, pattern)
    local reverse_matches = string.gmatch(reverse, pattern)
    return iterator_len(matches) + iterator_len(reverse_matches)
end

local function skew_table_right(t)
    local output = {}
    local line_len = #t[1]
    for i = 1, #t do
        output[i] = string.rep(".", i - 1) .. t[i] .. string.rep(".", line_len - i)
    end
    return output
end

local function skew_table_left(t)
    local output = {}
    local line_len = #t[1]
    for i = 1, #t do
        output[i] = string.rep(".", line_len - i) .. t[i] .. string.rep(".", i - 1)
    end
    return output
end

local function get_all_columns(t)
    local columns = {}
    for c = 1, #t[1] do
        local column = ""
        for r = 1, #t do
            -- Append the character at pos (c, r)
            column = column .. string.sub(t[r], c, c)
        end
        columns[#columns + 1] = column
    end
    return columns
end

local function print_table(t)
    print()
    for _, l in pairs(t) do
        print(l)
    end
end

local function add_rows(t, rows)
    for _, row in pairs(rows) do
        t[#t + 1] = row
    end
end

local function part_1(in_data)
    -- Add all columns to the input
    local all_rows = {}
    add_rows(all_rows, in_data)
    add_rows(all_rows, get_all_columns(in_data))
    add_rows(all_rows, get_all_columns(skew_table_right(in_data)))
    add_rows(all_rows, get_all_columns(skew_table_left(in_data)))
    -- print_table(all_rows)

    local nof_matches = 0
    for _, line in pairs(all_rows) do
        local line_matches = find_pattern(line, "XMAS")
        nof_matches = nof_matches + line_matches
        -- print("The line '" .. line .. "' contains " .. line_matches .. " matches.")
    end

    print("The total number of matches is " .. nof_matches)
end

local function is_within(c, r, cols, rows)
    if c - 1 > 0 and c + 1 <= cols and r - 1 > 0 and r + 1 <= rows then
        return true
    end
    return false
end

local function char_at(t, r, c)
    return string.sub(t[r], c, c)
end

local function is_m_or_s(t, r, c)
    if char_at(t, r, c) == "M" or char_at(t, r, c) == "S" then
        return true
    end
    return false
end

-- The diagonals in the x must be different
-- M M    M S
--  A      A
-- S S    M S
local function check_mas(t, r, c)
    -- Check that all chars are "M" or "S"
    if not (is_m_or_s(t, r - 1, c - 1) and is_m_or_s(t, r + 1, c + 1) and
            is_m_or_s(t, r - 1, c + 1) and is_m_or_s(t, r + 1, c - 1)) then
        return false
    end

    -- Check that the diagonals are different
    if (char_at(t, r - 1, c - 1) == char_at(t, r + 1, c + 1)) or
        (char_at(t, r - 1, c + 1) == char_at(t, r + 1, c - 1)) then
        return false
    end
    return true
end

local function is_mas_match(t, r, c)
    if is_within(c, r, #t[1], #t) then
        -- print(r .. ", " .. c .. " is within")
        if check_mas(t, r, c) then
            return true
        end
    end
    return false
end

local function part_2(t)
    -- Iterate over all rows and columns
    local nof_matches = 0
    for r = 1, #t do
        for c = 1, #t[1] do
            if char_at(t, r, c) == "A" and is_mas_match(t, r, c) then
                nof_matches = nof_matches + 1
            end
        end
    end
    print("The total number of matches is " .. nof_matches)
end

print("The input file '" .. filename .. "' contains " .. #input .. " lines")

-- print_table(input)
part_1(input)
part_2(input)
