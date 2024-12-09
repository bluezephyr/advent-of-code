#!/usr/bin/env lua

local function read_input(fname)
    local locations = io.open(fname, "r")

    local input = {}
    for line in locations:lines() do
        table.insert(input, line)
    end
    return input
end

-- Take a list of lines and convert to a map (i.e., a table of all chars[x][y])
local function create_map()
    local map = {}
    local data = {}
    map.x_max = 0
    map.y_max = 0

    map.add = function(lines)
        for y = 1, #lines do
            local line = lines[y]
            for x = 1, #line do
                data[x] = data[x] or {}
                data[x][y] = line:sub(x, x)
            end
        end
        map.x_max = #lines[1]
        map.y_max = #lines
    end

    map.clear = function(x_size, y_size)
        for y = 1, y_size do
            for x = 1, x_size do
                data[x] = data[x] or {}
                data[x][y] = "."
            end
        end
        map.x_max = y_size
        map.y_max = x_size
    end

    map.on_map = function(x, y)
        if x < 1 or x > map.x_max or y < 1 or y > map.y_max then
            return false
        else
            return true
        end
    end

    map.get = function(x, y) return data[x][y] end

    map.set = function(x, y, value)
        if map.on_map(x, y) then
            data[x][y] = value
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

    map.count = function(c)
        local n = 0
        for pos in map.positions() do
            if pos.v == c then
                n = n + 1
            end
        end
        return n
    end

    return map
end

local function append(list1, list2)
    for _, item in ipairs(list2) do
        list1[#list1 + 1] = item
    end
end

local function distance(pos1, pos2)
    return { x = pos2.x - pos1.x, y = pos2.y - pos1.y }
end

local function find_antennas(map)
    local antennas = {}
    for pos in map.positions() do
        if pos.v ~= "." then
            local antenna = antennas[pos.v] or {}
            antenna[#antenna + 1] = pos
            antennas[pos.v] = antenna
        end
    end
    return antennas
end

local function find_antinode_pairs(pos1, pos2)
    local d = distance(pos1, pos2)
    -- print(pos1.x, pos1.y, pos2.x, pos2.y)
    local node1 = { x = pos1.x - d.x, y = pos1.y - d.y }
    local node2 = { x = pos2.x + d.x, y = pos2.y + d.y }
    return { node1, node2 }
end

local function find_all_antinodes(antennas, finder)
    local antinodes = {}
    for _, antenna in pairs(antennas) do
        for i = 1, #antenna do
            for j = i + 1, #antenna do
                append(antinodes, finder(antenna[i], antenna[j]))
            end
        end
    end
    return antinodes
end

local function part_1(lines)
    local antenna_map = create_map()
    local node_map = create_map()
    antenna_map.add(lines)
    node_map.clear(antenna_map.x_max, antenna_map.y_max)

    antenna_map.print()
    local antennas = find_antennas(antenna_map)
    local nodes = find_all_antinodes(antennas, find_antinode_pairs)
    for _, node in pairs(nodes) do
        node_map.set(node.x, node.y, "#")
    end
    print()
    node_map.print()
    print("The map contains " .. node_map.count("#") .. " antinodes")
end

-- Program start
-- local filename = "test.txt"
local filename = "input1.txt"
local input = read_input(filename)
print("The input file '" .. filename .. "' contains " .. #input .. " lines")

part_1(input)
