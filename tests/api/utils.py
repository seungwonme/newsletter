import os


def create_unique_filename(folder_name: str, file_name: str) -> str:
    """
    Generates a unique file name by appending _num if the file already exists.

    Args:
        folder_name (str): The name of the folder.
        file_name (str): The name of the file.

    Returns:
        str: The unique file path.
    """
    current_dir = os.getcwd()
    output_dir = os.path.join(current_dir, folder_name)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_file = os.path.join(output_dir, file_name)
    base_name, ext = os.path.splitext(output_file)
    num = 1

    while os.path.exists(output_file):
        output_file = f"{base_name}_{num}{ext}"
        num += 1

    return output_file


def save_docs_to_unique_file(
    docs: list, folder_name: str = "output", file_name: str = "docs_output.md"
):
    """
    Saves documents to a uniquely named file in the specified folder.

    Args:
        docs (list): The list of documents to save.
        folder_name (str, optional): The name of the folder. Defaults to "output".
        file_name (str, optional): The name of the file. Defaults to "docs_output.md".
    """
    output_file = create_unique_filename(folder_name, file_name)

    with open(output_file, "w", encoding="utf-8") as f:
        for doc in docs:
            f.write(f"{doc}\n")

    print(f"Documents saved to {output_file}")


def save_text_to_unique_file(
    text: str, folder_name: str = "output", file_name: str = "text_output.md"
):
    """
    Saves text to a uniquely named file in the specified folder.

    Args:
        text (str): The text to save.
        folder_name (str, optional): The name of the folder. Defaults to "output".
        file_name (str, optional): The name of the file. Defaults to "docs_output.md".
    """
    output_file = create_unique_filename(folder_name, file_name)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(text)

    print(f"Text saved to {output_file}")
