import argparse
import json
from enum import Enum

PLACE_HOLDER = '// JsonStruct'
HEADER_PLUG = 'template.h'

class Type(Enum):
    STRING = 0
    INT = 1
    DOUBLE = 2
    BOOL = 3
    NONE = 4

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('json', help='the json file to parse')
    parser.add_argument('struct_name', help='the name of the cpp and h files to generate')
    args = parser.parse_args()
    return (args.json, args.struct_name)

def get_type(value):
    if type(value) == str:
        return Type.STRING
    # Must come before int because subclass of int
    elif type(value) == bool:
        return Type.BOOL
    elif type(value) == int:
        return Type.INT
    elif type(value) == float:
        return Type.DOUBLE
    

    return Type.NONE

def get_header_line(key, value):
    t = get_type(value)

    if type(value) == bool:
        return f"\tbool {key} = {str(value).lower()};\n"
    elif type(value) == str:
        return f"\tstd::string {key} = \"{value}\";\n"
    elif type(value) == int:
        return f"\tint {key} = {value};\n"
    elif type(value) == float:
        return f"\tdouble {key} = {value};\n"

def generate_header(output_filename, configuration):
    # Read template file
    text = ''
    with open('template.h', 'r') as file:
        text = file.read()

    # Generate text to plug in template file
    plug_text = ''
    for key, value in configuration:    
        if isinstance(value, dict) or isinstance(value, list):
            continue
        else:
            plug_text += get_header_line(key, value)

    # Insert plug text into text and generate header file
    if PLACE_HOLDER in text:
        text = text.replace(PLACE_HOLDER, plug_text)
        with open(output_filename + '.h', 'w') as file:
            file.write(text)

def get_read_value(key, value):
    t = get_type(value)

    if type(value) == bool:
        return f"\t\t{key} = boost::json::value_to<bool>(root.at(\"{key}\"));\n"
    elif type(value) == str:
        return f"\t\t{key} = boost::json::value_to<std::string>(root.at(\"{key}\"));\n"
    elif type(value) == int:
        return f"\t\t{key} = boost::json::value_to<int>(root.at(\"{key}\"));\n"
    elif type(value) == float:
        return f"\t\t{key} = boost::json::value_to<double>(root.at(\"{key}\"));\n"
    
def generate_cpp_file(output_filename, configuration):
    # Read template file
    text = ''
    with open('template.cpp', 'r') as file:
        text = file.read()

    # Modify include statement
    if HEADER_PLUG in text:
        text = text.replace(HEADER_PLUG, output_filename + '.h')

    # Generate text to plug in template file
    plug_text = ''
    for key, value in configuration:
        if isinstance(value, dict) or isinstance(value, list):
            continue
        else:
            plug_text += get_read_value(key, value)

    # Insert plug text into text and generate header file
    if PLACE_HOLDER in text:
        text = text.replace(PLACE_HOLDER, plug_text)

        with open(output_filename + '.cpp', 'w') as file:
            file.write(text)

    


if __name__ == "__main__":
    json_filename, output_filename = parse_arguments()
    
    configuration = []
    with open(json_filename) as json_file:
        map = json.load(json_file)
        configuration = map.items()
    
    if len(configuration) > 0:
        generate_header(output_filename, configuration)
        generate_cpp_file(output_filename, configuration)