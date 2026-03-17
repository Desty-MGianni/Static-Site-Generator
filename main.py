import os
import shutil

from src.helpers_main import generate_page_recursive, move_file


def main() -> None:
    script_dir_path: str = os.path.dirname(os.path.abspath(__file__))
    static_path: str = os.path.join(script_dir_path, "static")
    public_path: str = os.path.join(script_dir_path, "public")

    if os.path.exists(public_path):
        shutil.rmtree(public_path)
    os.mkdir(public_path)

    move_file(static_path, public_path)

    markdown_file_path: str = os.path.join(script_dir_path, "content/")
    template_file_path: str = os.path.join(script_dir_path, "template.html")
    full_page_path: str = os.path.join(script_dir_path, "public/")
    generate_page_recursive(markdown_file_path, template_file_path, full_page_path)


if __name__ == "__main__":
    main()
