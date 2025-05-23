#include <iostream>
#include <exception>
#include <boost/json.hpp>
#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/json_parser.hpp>

#include "template.h"

Config::Config(const std::string json_text) {
    try {
        boost::json::value json_value = boost::json::parse(json_text);
        boost::json::object root_object = json_value.get_object();

// JsonStruct
    }
    catch (std::exception const& e)
    {
        std::cerr << e.what() << std::endl;
    }
}


int main() {
    std::ifstream file("example.json");
    std::string str;
    std::string file_contents;
    while (std::getline(file, str)) {
        file_contents += str;
        file_contents.push_back('\n');
    }

    Config cfg(file_contents);
    std::cout << "string " << cfg.string_key << std::endl;
    std::cout << "int " << cfg.int_key << std::endl;
    std::cout << "double " << cfg.double_key << std::endl;
    std::cout << "bool " << cfg.bool_key << std::endl;

    std::cout << "string " << cfg.inner.string_key << std::endl;
    std::cout << "int " << cfg.inner.int_key << std::endl;
    std::cout << "double " << cfg.inner.double_key << std::endl;
    std::cout << "bool " << cfg.inner.bool_key << std::endl;

    std::cout << "string " << cfg.inner.really_inner.string_key << std::endl;
    std::cout << "int " << cfg.inner.really_inner.int_key << std::endl;
    std::cout << "double " << cfg.inner.really_inner.double_key << std::endl;
    std::cout << "bool " << cfg.inner.really_inner.bool_key << std::endl;

    std::cout << "string " << cfg.inner.really_inner.really_innermost.string_key << std::endl;
    std::cout << "int " << cfg.inner.really_inner.really_innermost.int_key << std::endl;
    std::cout << "double " << cfg.inner.really_inner.really_innermost.double_key << std::endl;
    std::cout << "bool " << cfg.inner.really_inner.really_innermost.bool_key << std::endl;
}
