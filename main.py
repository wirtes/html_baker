
import os
import json


def load_configs():
    config_file = open('config/config.json')
    config = json.load(config_file)
    return config


def get_html_files(directory):
    html_templates = []
    for this_file in os.listdir(directory):
        if this_file.endswith(".html"):
            html_templates.append(this_file)
    return(html_templates)


def write_html(file_path, output):
    print("+++ Writing: ", file_path)
    file = open(file_path, 'w')
    file.write(output)
    file.close()
    return


def load_file_to_list(data_file):
    text_file = open(data_file, 'r')
    file_content = []
    while True:
        line = text_file.readline()
        if len(line) > 3:
            file_content.append(line.strip())
        if not line:
            break
    return file_content


def insert_includes(includes_path, include_file, special_includes, template_file):
    include_html = ""
    # Check if we gotta do something special
    if include_file in special_includes:
        print("=== Processing: "+include_file+" for "+template_file)
        if include_file == "nav.html":
            with open(includes_path + include_file, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    # Find the <li> for the page we're building and mark it as the active one
                    include_html += line.replace('<li><a href="'+template_file+'">', '<li class="active"><a href="'+template_file+'">')
    else:
        with open(includes_path + include_file) as f:
            include_html = f.read()

    return include_html


def process_template(file_to_open):
    # NEED TO MOVE THESE TO A CONFIG!
    return


if __name__ == '__main__':
    config = load_configs()
    working_directory = config["working_directory"]
    output_path = working_directory
    src_path = working_directory + config["src_path"]
    includes_path = src_path + config["includes_path"]
    templates_to_process = get_html_files(src_path)
    print(templates_to_process)

    for template in templates_to_process:
        file_to_open = src_path + template
        file_to_write = output_path + template
        print("=== Processing: " + file_to_open)
        with open(file_to_open) as file:
            output_html = ''
            for line in file:
                if line.startswith("<!--PREPROCESS_INCLUDE-->"):
                    # Split the preprocess comment & grab the filename of the include (after the colon)
                    include_file = line.split(":")[1].rstrip()
                    print("Including: " + includes_path + include_file)
                    output_html += insert_includes(includes_path, include_file, config["special_includes"], template)
                else:
                    output_html += line
            write_html(file_to_write, output_html)




