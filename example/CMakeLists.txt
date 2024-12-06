cmake_minimum_required (VERSION 3.5)
project (TestJsonStruct)

find_package( 
    Boost 1.83 REQUIRED 
    COMPONENTS  json 
)

add_executable(TestJsonStruct config.cpp)

target_link_libraries(${PROJECT_NAME}
    Boost::boost
    Boost::json
)