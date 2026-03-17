import os
import shutil

from src.helpers_block import markdown_to_html_node


def move_file(src: str, dest: str) -> None:

    files_path: list[str] = os.listdir(src)
    for file_path in files_path:

        full_path: str = os.path.join(src, file_path)
        if os.path.isfile(full_path):
            print(f"Copying file from {full_path}")
            shutil.copy(full_path, dest)
        else:
            new_path: str = os.path.join(dest, file_path)
            os.mkdir(new_path)
            move_file(full_path, new_path)


def extract_title(markdown: str) -> str:
    first_line: str = markdown.split("\n", 1)[0]
    if not first_line.startswith("# "):
        raise Exception("No title found!")
    title: str = first_line.strip("# ")
    return title


def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    from_content: str = ""
    templ_content: str = ""

    with open(from_path, encoding="UTF-8") as md:
        from_content = md.read()

    with open(template_path, encoding="UTF-8") as templ:
        templ_content = templ.read()

    html: str = markdown_to_html_node(from_content).to_html()
    html_title: str = extract_title(from_content)

    templ_content: str = templ_content.replace("{{ Title }}", html_title)
    full_page: str = templ_content.replace("{{ Content }}", html)

    dest_dir: str = os.path.dirname(dest_path)
    os.makedirs(dest_dir, exist_ok=True)
    with open(dest_path, mode="w", encoding="UTF-8") as fd:
        fd.write(full_page)


def generate_page_recursive(from_path: str, template_path: str, dest_path: str) -> None:
    elements: list[str] = os.listdir(from_path)
    for element in elements:
        full_src_path = os.path.join(from_path, element)
        full_dest_path = os.path.join(dest_path, element)
        if os.path.isfile(full_src_path) and full_src_path.endswith(".md"):
            base_path: str = os.path.splitext(full_dest_path)[0]
            final_path: str = base_path + ".html"
            generate_page(full_src_path, template_path, final_path)
        elif os.path.isdir(full_src_path):
            generate_page_recursive(full_src_path, template_path, full_dest_path)
