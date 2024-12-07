#!/usr/bin/env lua

local function read_input(fname)
    local locations = io.open(fname, "r")

    local input = {}
    for line in locations:lines() do
        table.insert(input, line)
    end
    return input
end

local function string_to_list(str)
    local list = {}
    for c in str:gmatch(".") do
        table.insert(list, c)
    end
    return list
end

local function print_list(list)
    for _, item in pairs(list) do
        print(item)
    end
end


-- Take a list of lines and convert to a map (i.e., a table of all chars[x][y])
local function create_map(lines)
    local map = {}

    local data = {}
    for y = 1, #lines do
        local line = lines[y]
        for x = 1, #line do
            data[x] = data[x] or {}
            data[x][y] = line:sub(x, x)
        end
    end

    map.x_max = #lines[1]
    map.y_max = #lines

    map.get = function(x, y) return data[x][y] end
    map.set = function(x, y, value) data[x][y] = value end
    map.on_map = function(x, y)
        if x < 1 or x > map.x_max or y < 1 or y > map.y_max then
            return false
        else
            return true
        end
    end

    map.print = function()
        for y = 1, map.y_max do
            local line_out = ""
            for x = 1, map.x_max do
                line_out = line_out .. map.get(x, y)
            end
            print(line_out)
        end
    end

    -- Return an iterator for all the positions in the map
    map.positions = function()
        local x = 0
        local y = 1

        return function()
            x = x + 1
            if x > map.x_max then
                x = 1
                y = y + 1
            end
            if y > map.y_max then return nil end
            return { v = map.get(x, y), x = x, y = y }
        end
    end

    return map
end

local function rotate(pos)
    if pos.v == "v" then pos.v = "<"; return pos end
    if pos.v == "^" then pos.v = ">"; return pos end
    if pos.v == "<" then pos.v = "^"; return pos end
    if pos.v == ">" then pos.v = "v"; return pos end
end

local function get_direction(pos)
    if pos.v == "v" then return { x = 0, y = 1 } end
    if pos.v == "^" then return { x = 0, y = -1 } end
    if pos.v == "<" then return { x = -1, y = 0 } end
    if pos.v == ">" then return { x = 1, y = 0 } end
end

-- Move the guard one step and return the new position
local function move_guard(pos, map)
    local direction = get_direction(pos)
    local new_pos = { v = pos.v, x = pos.x + direction.x, y = pos.y + direction.y }
    if map.get(new_pos.x, new_pos.y) == "#" then
        return rotate(pos)
    end
    if map.on_map(new_pos.x, new_pos.y) then
        return new_pos
    end
    return nil
end

local function guard_positions(map)
    local nof_positions = 0
    for pos in map.positions() do
        if pos.v == "X" then
            nof_positions = nof_positions + 1
        end
    end
    return nof_positions
end

local function part_1(lines)
    local map = create_map(lines)
    local guard_pos
    for pos in map.positions() do
        if pos.v == "v" or pos.v == "^" or pos.v == "<" or pos.v == ">" then
            guard_pos = pos
            break
        end
    end
    print("Guard found at pos (" .. guard_pos.x .. ", " .. guard_pos.y .. ")")
    while true do
        map.set(guard_pos.x, guard_pos.y, "X")
        guard_pos = move_guard(guard_pos, map)
        if guard_pos == nil then break end
    end
    map.print()
    print("The guard visited " .. guard_positions(map) .. " positions")
end


-- Program start
-- local filename = "test.txt"
local filename = "input1.txt"
local input = read_input(filename)
print("The input file '" .. filename .. "' contains " .. #input .. " lines")

part_1(input)
