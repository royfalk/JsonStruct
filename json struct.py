import argparse
import json
from enum import Enum

PLACE_HOLDER = '// JsonStruct'
HEADER_PLUG = 'template.h'

INNER_STRUCT = [
    '\tstruct {\n',
    'INNER_STRUCT_PLUG\n',
    '\t} INNER_STRUCT_NAME;\n'
]



INNER_STRUCT_NAME = "INNER_STRUCT_NAME"
INNER_STRUCT_PLUG = "INNER_STRUCT_PLUG"

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

def recursive_generate_header_content(configuration, tabs):
    # Generate text to plug in template file
    plug_text = ''
    for key, value in configuration:    
        if isinstance(value, dict) or isinstance(value, list):
            inner_text = '\n' + tabs + INNER_STRUCT[0]
            inner_text += INNER_STRUCT[1].replace(INNER_STRUCT_PLUG, recursive_generate_header_content(value.items(), tabs+"\t"))
            inner_text += tabs + INNER_STRUCT[2].replace(INNER_STRUCT_NAME, key)
            plug_text += inner_text
        else:
            plug_text += tabs + get_header_line(key, value)
    return plug_text[:-1] # Remove last newline

def generate_header(output_filename, configuration):
    # Read template file
    text = ''
    with open('template.h', 'r') as file:
        text = file.read()

    # Generate text to plug in template file
    plug_text = recursive_generate_header_content(configuration, '')
    
    # Insert plug text into text and generate header file
    if PLACE_HOLDER in text:
        text = text.replace(PLACE_HOLDER, plug_text)
        with open(output_filename + '.h', 'w') as file:
            file.write(text)

def get_read_value(root, key, value, chain):
    chain = chain if len(chain) == 0 else f"{chain}."
    t = get_type(value)

    if type(value) == bool:
        return f"\t\t{chain}{key} = boost::json::value_to<bool>({root}_object.at(\"{key}\"));\n"
    elif type(value) == str:
        return f"\t\t{chain}{key} = boost::json::value_to<std::string>({root}_object.at(\"{key}\"));\n"
    elif type(value) == int:
        return f"\t\t{chain}{key} = boost::json::value_to<int>({root}_object.at(\"{key}\"));\n"
    elif type(value) == float:
        return f"\t\t{chain}{key} = boost::json::value_to<double>({root}_object.at(\"{key}\"));\n"

def recursive_generate_cpp_content(root, configuration, chain = ''):
    plug_text = ''
    for key, value in configuration:
        if isinstance(value, dict) or isinstance(value, list):
            chain = key if len(chain) == 0 else f"{chain}.{key}"

            plug_text += f"\n\t\tboost::json::object {key}_object = {root}_object.at(\"{key}\").get_object();\n"
            plug_text += recursive_generate_cpp_content(key, value.items(), chain)
            pass
        else:
            plug_text += get_read_value(root, key, value, chain)
    
    return plug_text

def generate_cpp_file(output_filename, configuration):
    # Read template file
    text = ''
    with open('template.cpp', 'r') as file:
        text = file.read()

    # Modify include statement
    if HEADER_PLUG in text:
        text = text.replace(HEADER_PLUG, output_filename + '.h')

    # Generate text to plug in template file
    plug_text = recursive_generate_cpp_content("root", configuration)
    
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