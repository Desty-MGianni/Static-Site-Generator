import os
import shutil
import sys

from src.helpers_main import generate_page_recursive, move_file


def main() -> None:

    basepath: str = sys.argv[1] if len(sys.argv) > 1 else "/"
    root: str = os.path.dirname(os.path.abspath(__file__))

    path_dict: dict[str, str] = {}
    path_dict["src"] = os.path.join(root, "static")
    path_dict["dest"] = os.path.join(root, "docs/")
    path_dict["content"] = os.path.join(root, "content/")
    path_dict["template"] = os.path.join(root, "template.html")

    if os.path.exists(path_dict["dest"]):
        shutil.rmtree(path_dict["dest"])
    os.makedirs(path_dict["dest"], exist_ok=True)

    print(f"Transfering static file to {path_dict["dest"]}...")
    move_file(path_dict["src"], path_dict["dest"])

    print(f"Generating site with basepath: {basepath}")
    generate_page_recursive(
        path_dict["content"], path_dict["template"], path_dict["dest"], basepath
    )


if __name__ == "__main__":
    main()
