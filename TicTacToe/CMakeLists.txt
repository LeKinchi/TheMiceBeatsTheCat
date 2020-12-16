cmake_minimum_required(VERSION 3.17)
project(Game_Server)

set(CMAKE_CXX_STANDARD 17)

add_executable(Game_Server main.cpp TCP_Packet.h Server.cpp Server.h)