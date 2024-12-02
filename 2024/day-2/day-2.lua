#!/usr/bin/env lua

-- local filename = "test.txt"
local filename = "input1.txt"
local locations = io.open(filename, "r")

local list = {}
for line in locations:lines() do
    list[#list + 1] = line
end

print("The input file '" .. filename .. "' contains " .. #list .. " lines")

local function remove_index(line, index)
    if index == 0 then
        return line
    end

    local i = 0
    local new_line = ""
    for number in string.gmatch(line, "%d+") do
        i = i + 1
        if i ~= index then
            new_line = new_line .. " " .. number
        end
    end
    print("old: " .. line .. " new: " .. new_line .. "(" .. index .. ")")
    return new_line
end

local function is_line_safe(line)
    local previous
    local trend

    for number in string.gmatch(line, "%d+") do
        local num = tonumber(number)
        if previous then
            -- Check if strictly monotonic
            local delta
            if num > previous then
                delta = "increasing"
            elseif num < previous then
                delta = "decreasing"
            else
                -- No change
                return false
            end

            if trend and trend ~= delta then
                return false
            end
            trend = delta

            -- Check if adjacent levels within limits
            local diff = math.abs(num - previous)
            if diff < 1 or diff > 3 then
                -- Adjacent level difference too big
                return false
            end
        end

        previous = num
    end
    return true
end

local function is_report_safe(line)
    local nof_items = 0
    for _ in string.gmatch(line, "%d+") do
        nof_items = nof_items + 1
    end

    for index = 0, nof_items do
        local new_line = remove_index(line, index)
        if is_line_safe(new_line) then
            return true
        end
    end
    return false
end

local safe_reports = 0
for _, line in pairs(list) do
    if is_report_safe(line) then
        safe_reports = safe_reports + 1
    end
end

print("There are " .. safe_reports .. " safe reports")
