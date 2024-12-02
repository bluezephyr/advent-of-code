#!/usr/bin/env lua

-- local filename = "test.txt"
local filename = "input1.txt"
local locations = io.open(filename, "r")

local list = {}
for line in locations:lines() do
    list[#list + 1] = line
end

print("The input file '" .. filename .. "' contains " .. #list .. " lines")

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

local safe_reports = {}

for _, line in pairs(list) do
    if is_line_safe(line) then
        safe_reports[#safe_reports + 1] = line
    end
end

print("There are " .. #safe_reports .. " safe reports")
