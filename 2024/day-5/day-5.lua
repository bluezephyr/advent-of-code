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

    map.reset = function(the_lines)
        for y = 1, #the_lines do
            local line = the_lines[y]
            for x = 1, #line do
                data[x] = data[x] or {}
                data[x][y] = line:sub(x, x)
            end
        end
    end

    map.reset(lines)
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
    if pos.v == "v" then
        pos.v = "<"; return pos
    end
    if pos.v == "^" then
        pos.v = ">"; return pos
    end
    if pos.v == "<" then
        pos.v = "^"; return pos
    end
    if pos.v == ">" then
        pos.v = "v"; return pos
    end
end

local function get_direction(pos)
    if pos.v == "v" then return { x = 0, y = 1 } end
    if pos.v == "^" then return { x = 0, y = -1 } end
    if pos.v == "<" then return { x = -1, y = 0 } end
    if pos.v == ">" then return { x = 1, y = 0 } end
end

-- Move the guard one step and return the new position
local function step_guard(pos, map)
    local direction = get_direction(pos)
    local new_pos = { v = pos.v, x = pos.x + direction.x, y = pos.y + direction.y }
    if not map.on_map(new_pos.x, new_pos.y) then
        return nil
    end
    if map.get(new_pos.x, new_pos.y) == "#" then
        return rotate(pos)
    end
    return new_pos
end

local function guard_positions(map)
    local nof_positions = 0
    for pos in map.positions() do
        if pos.v == "^" or
            pos.v == ">" or
            pos.v == "<" or
            pos.v == "v" then
            nof_positions = nof_positions + 1
        end
    end
    return nof_positions
end

local function find_guard_start(map)
    for pos in map.positions() do
        if pos.v == "v" or pos.v == "^" or pos.v == "<" or pos.v == ">" then
            return pos
        end
    end
end

-- Return true if the guard is stuck in a loop
local function guard_is_stuck(start_pos, map)
    local guard_pos = start_pos
    local prev_pos = guard_pos
    while true do
        guard_pos = step_guard(guard_pos, map)
        if guard_pos == nil then
            map.set(prev_pos.x, prev_pos.y, prev_pos.v)
            return false
        end

        if map.get(guard_pos.x, guard_pos.y) == guard_pos.v then
            -- Been here before
            return true
        end

        if prev_pos.x ~= guard_pos.x or prev_pos.y ~= guard_pos.y then
            map.set(prev_pos.x, prev_pos.y, prev_pos.v)
            prev_pos.x = guard_pos.x
            prev_pos.y = guard_pos.y
            prev_pos.v = guard_pos.v
        end
    end
end

local function part_1(lines)
    local map = create_map(lines)
    local guard_pos = find_guard_start(map)
    print("Guard found at pos (" .. guard_pos.x .. ", " .. guard_pos.y .. ")")
    while true do
        map.set(guard_pos.x, guard_pos.y, "X")
        guard_pos = step_guard(guard_pos, map)
        if guard_pos == nil then break end
    end
    map.print()
    print("The guard visited " .. guard_positions(map) .. " positions")
end

local function part_2(lines)
    local map = create_map(lines)
    local stuck_positions = 0
    for pos in map.positions() do
        local guard_pos = find_guard_start(map)
        if map.get(pos.x, pos.y) == "." then
            map.set(pos.x, pos.y, "#")
            if guard_is_stuck(guard_pos, map) then
                -- print("The guard is stuck " .. stuck_positions)
                stuck_positions = stuck_positions + 1
            end
            map.reset(lines)
        end
    end
    print("There are " .. stuck_positions .. " positions for the guard to be stuck")
end

-- Program start
local filename = "test.txt"
-- local filename = "input1.txt"
local input = read_input(filename)
print("The input file '" .. filename .. "' contains " .. #input .. " lines")

part_1(input)
part_2(input)
