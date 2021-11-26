#!/usr/local/bin/python3
# route.py : Find routes through maps
#
# Code by: Himanshu Hansaria hhansar Shubham Bipin Kumar sbipink Arunima Shukla arushuk
#
# Based on skeleton code by V. Mathur and D. Crandall, January 2021
#
import math
from math import cos, asin, sqrt, pi, tanh
import sys
import copy

#Basic graph structure inspired from "https://www.bogotobogo.com/python/python_graph_data_structures.php"
class Vertex:
    def __init__(self, node, lat=0, lon=0):
        self.id = node
        # self.state = state
        self.lat = lat
        self.lon = lon
        self.g = 0
        self.h = 0
        self.f = 0
        self.adjacent = {}

    def __str__(self):
        return str(self.id) + ' adjacent: ' + str([x.id for x in self.adjacent])

    def add_neighbor(self, neighbor, weight):
        self.adjacent[neighbor] = weight

    def get_connections(self):
        return self.adjacent.keys()

    def get_id(self):
        return self.id

    def get_weight(self, neighbor):
        return self.adjacent[neighbor]

class Graph:
    def __init__(self):
        self.vert_dict = {}
        self.num_vertices = 0

    def __iter__(self):
        return iter(self.vert_dict.values())

    def add_vertex(self, node, lat=0, lon=0):
        self.num_vertices = self.num_vertices + 1
        new_vertex = Vertex(node, lat, lon)
        self.vert_dict[node] = new_vertex
        return new_vertex

    def get_vertex(self, n):
        if n in self.vert_dict:
            return self.vert_dict[n]
        else:
            return None

    def add_edge(self, frm, to, cost = 0):
        if frm not in self.vert_dict:
            self.add_vertex(frm)
        if to not in self.vert_dict:
            self.add_vertex(to)

        self.vert_dict[frm].add_neighbor(self.vert_dict[to], cost)
        self.vert_dict[to].add_neighbor(self.vert_dict[frm], cost)

    def get_vertices(self):
        return self.vert_dict.keys()


# Find the possible moves from position (row, col)
# def moves(map, row, col):
#     moves = ((row + 1, col, "D"), (row - 1, col, "U"), (row, col - 1, "L"), (row, col + 1, "R"))
#
#     # Return only moves that are within the house_map and legal (i.e. go through open space ".")
#     return [move for move in moves if valid_index(move[:-1], len(map), len(map[0])) and (map[move[0]][move[1]] in ".@")]

#Haversine formula inspired from here "https://stackoverflow.com/questions/27928/calculate-distance-between-two-latitude-longitude-points-haversine-formula"
def getHaversineDistanceInMiles(lat1,lon1,lat2,lon2):
    if (lat1==0 and lon1==0) or (lat2==0 and lon2==0):
        return 0
    R = 6371; # Radius of the earth in km
    dLat = deg2rad(lat2-lat1);
    dLon = deg2rad(lon2-lon1);
    a = math.sin(dLat/2) * math.sin(dLat/2) + math.cos(deg2rad(lat1)) * math.cos(deg2rad(lat2)) * math.sin(dLon/2) * math.sin(dLon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a));
    d = R * c; # Distance in km
    return d*0.62137

def distance(lat1, lon1, lat2, lon2):
    if (lat1==0 and lon1==0) or (lat2==0 and lon2==0):
        return 0
    p = pi/180
    a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p) * cos(lat2*p) * (1-cos((lon2-lon1)*p))/2
    return 12742 * asin(sqrt(a)) #2*R*asin...
def deg2rad(deg):
    return deg * math.pi/180
def build_vertices(filename,g):
    with open(filename, "r") as f:
        lines = f.readlines()

    for line in lines:
        city, latitude, longitude = line.split(" ")
        g.add_vertex(city.strip(), float(latitude), float(longitude))


def build_edges(filename,g):
    with open(filename, "r") as f:
        lines = f.readlines()

    for line in lines:
        frm, to, length, speed_limit, highway_name = line.split(" ")
        g.add_edge(frm.strip(), to.strip(), [int(length), int(speed_limit), highway_name])


def get_heuristic(curr_node, end_node):
    # h = getHaversineDistanceInMiles(curr_node.lat, curr_node.lon, end_node.lat, end_node.lon)
    h = distance(curr_node.lat, curr_node.lon, end_node.lat, end_node.lon)
    return h*0.62137*0.01


def print_route_taken(route_taken):
    formatted_route_taken = []
    cities = route_taken[0].split(":")[1:]
    distance = route_taken[1].split(":")[1:]
    # print("cities:")
    # print(cities)
    # print("distance:")
    # print(distance)
    for i in range(len(cities)):
        route = (cities[i], distance[i])
        formatted_route_taken.append(route)
    # print("FORMATTED ROUTE TAKEN")
    # print(formatted_route_taken)
    return formatted_route_taken

def get_min_f(li):
    arr = [e[0] for e in li]
    return arr.index(min(arr))
def get_route(start, end, cost):

    g = Graph()
    build_vertices("city-gps.txt",g)
    build_edges("road-segments.txt",g)

    i_v = g.get_vertex(start)
    f_v = g.get_vertex(end)

    #Doing for distance initially


    """
    Find shortest driving route between start city and end city
    based on a cost function.

    1. Your function should return a dictionary having the following keys:
        -"route-taken" : a list of pairs of the form (next-stop, segment-info), where
           next-stop is a string giving the next stop in the route, and segment-info is a free-form
           string containing information about the segment that will be displayed to the user.
           (segment-info is not inspected by the automatic testing program).
        -"total-segments": an integer indicating number of segments in the route-taken
        -"total-miles": a float indicating total number of miles in the route-taken
        -"total-hours": a float indicating total amount of time in the route-taken
        -"total-delivery-hours": a float indicating the expected (average) time 
                                   it will take a delivery driver who may need to return to get a new package
    2. Do not add any extra parameters to the get_route() function, or it will break our grading and testing code.
    3. Please do not use any global variables, as it may cause the testing code to fail.
    4. You can assume that all test cases will be solvable.
    5. The current code just returns a dummy solution.
    """

    #start here
    if (start==end):
        return {"total-segments" : 0,
                "total-miles" : 0,
                "total-hours": 0,
                "total-delivery-hours": 0,
                "route-taken" : ""}
    # i_v.h = get_heuristic(i_v, f_v)
    # i_v.f = i_v.g + i_v.h
    route_taken = ("", "")
    route = []
    fringe = [(0, i_v, route_taken, (0, 0, 0, 0))] #d, seg, time, del_time
    # print(i_v.f)
    # heapq.heappush(fringe, (i_v.f, i_v))
    visited = set()

    while fringe:
        idx = get_min_f(fringe)
        (curr_f, curr_v, route_taken, search_mat) = fringe.pop(idx)

        # print("ROUTE ::::")
        # print(route, end="\n\n")
        # print(curr_v.get_id())
        visited.add(curr_v.get_id())
        printable_route_taken = print_route_taken(route_taken)
        if curr_v.get_id() == end:
            # print(route_taken)
            return {"total-segments": search_mat[1],
                "total-miles": float(search_mat[0]),
                "total-hours": float(search_mat[2]),
                "total-delivery-hours": float(search_mat[3]),
                "route-taken": printable_route_taken}
        for s_v in curr_v.get_connections():

            if s_v.get_id() in visited:
                continue
            # print(s_v)
            h = get_heuristic(s_v, f_v)
            curr_cost_segments = search_mat[1] + 1
            curr_cost_distance = search_mat[0] + curr_v.get_weight(s_v)[0]
            curr_cost_time = search_mat[2] + curr_v.get_weight(s_v)[0] / curr_v.get_weight(s_v)[1]
            t_road = curr_v.get_weight(s_v)[0] / curr_v.get_weight(s_v)[1]
            p = 0
            if curr_v.get_weight(s_v)[1] >= 50:
                p = tanh(curr_v.get_weight(s_v)[0]/1000)
            delivery_cost = t_road + 2 * p * (t_road + search_mat[3])
            curr_cost_del = search_mat[3] + delivery_cost


            if cost =="segments":
                flag = False
                for v in fringe:
                    if s_v.get_id() == v[1].get_id() and v[3][1] < curr_cost_segments:
                        flag = True
                if flag:
                    continue
                # if s_v in [v[1] for v in fringe]:
                #     if curr_cost_segments > s_v.g:
                #
                #         continue
                f = h + curr_cost_segments
                new_s_v = copy.copy(s_v)
                # new_s_v.g = curr_cost_segments
                new_s_v.f = f
                new_s_v.h = h
            elif cost == "distance":
                flag = False
                for v in fringe:
                    if s_v.get_id() == v[1].get_id() and v[3][0] < curr_cost_distance:
                        flag = True
                if flag:
                    continue
                # if s_v in [v[1] for v in fringe]:
                #     if curr_cost_distance > s_v.g:
                #         continue
                f = h + curr_cost_distance
                new_s_v = copy.copy(s_v)
                # new_s_v.g = curr_cost_distance
                new_s_v.f = f
                new_s_v.h = h
            elif cost == "time":
                flag = False
                # if s_v in [v[1] for v in fringe]:
                #     if curr_cost_time > s_v.g:
                #         continue
                for v in fringe:
                    if s_v.get_id() == v[1].get_id() and v[3][2] < curr_cost_time:
                        flag = True
                if flag:
                    continue
                f = h + curr_cost_time
                new_s_v = copy.copy(s_v)
                # new_s_v.g = curr_cost_time
                new_s_v.f = f
                new_s_v.h = h
            elif cost == "delivery":
                flag = False
                for v in fringe:
                    if s_v.get_id() == v[1].get_id() and v[3][3] < curr_cost_del:
                        flag = True
                if flag:
                    continue
                # if s_v in [v[1] for v in fringe]:
                #     if curr_cost_del > s_v.g:
                #         continue
                f = h + curr_cost_del
                new_s_v = copy.copy(s_v)
                # new_s_v.g = curr_cost_del
                new_s_v.f = f
                new_s_v.h = h

            highway_dist = f"{curr_v.get_weight(s_v)[2]} for {curr_v.get_weight(s_v)[0]} miles"




            # print("DEBUG OUTPUT")
            # print(new_s_v.get_id())
            # print(highway_dist)
            updated_route_taken = route_taken[0] + ":" + new_s_v.get_id()
            updated_routed_highway_distance = route_taken[1] + ":" + highway_dist
            fringe.append((new_s_v.f, new_s_v, (updated_route_taken, updated_routed_highway_distance), (curr_cost_distance, curr_cost_segments, curr_cost_time, curr_cost_del)))


    return -1
    # route_taken = [("Martinsville,_Indiana","IN_37 for 19 miles"),
    #                ("Jct_I-465_&_IN_37_S,_Indiana","IN_37 for 25 miles"),
    #                ("Indianapolis,_Indiana","IN_37 for 7 miles")]
    
    # return {"total-segments" : len(route_taken),
    #         "total-miles" : 51.,
    #         "total-hours" : 1.07949,
    #         "total-delivery-hours" : 1.1364,
    #         "route-taken" : route_taken}


# Please don't modify anything below this line
#
if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise(Exception("Error: expected 3 arguments"))

    (_, start_city, end_city, cost_function) = sys.argv
    if cost_function not in ("segments", "distance", "time", "delivery"):
        raise(Exception("Error: invalid cost function"))

    result = get_route(start_city, end_city, cost_function)

    # Pretty print the route
    print("Start in %s" % start_city)
    for step in result["route-taken"]:
        print("   Then go to %s via %s" % step)

    print("\n          Total segments: %4d" % result["total-segments"])
    print("             Total miles: %8.3f" % result["total-miles"])
    print("             Total hours: %8.3f" % result["total-hours"])
    print("Total hours for delivery: %8.3f" % result["total-delivery-hours"])
