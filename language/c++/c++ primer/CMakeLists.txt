cmake_minimum_required(VERSION 3.0)
project(learncpp)

set(TARGET learncpp)
file(GLOB_RECURSE SRC src/*.cpp)

set(INCLUDE_LIST)
foreach(src_file IN LISTS SRC)
        if (${src_file} MATCHES "main.cpp$")
                continue()
        endif()
        string(REGEX REPLACE "/[^/]+.cpp" "" FILE_DIR ${src_file})
        message(STATUS ${FILE_DIR}/include)
        list(APPEND INCLUDE_LIST ${FILE_DIR}/include)
endforeach()
list(REMOVE_DUPLICATES INCLUDE_LIST)

message(STATUS "SRC: " ${SRC})
message(STATUS "INCLUDE_LIST: " ${INCLUDE_LIST})

add_executable(${TARGET} ${SRC})
# add_library(${TARGET}
#         SHARED
#         ${SRC})
target_include_directories(${TARGET}
                            PUBLIC
                            ${INCLUDE_LIST})
