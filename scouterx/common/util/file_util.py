def read_file(file_path):
    """Returns the contents of a file as a string. Returns an empty string on error."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Failed to read file: {e}")
        return ""


if __name__ == '__main__':
    file_contents = read_file('example.txt')
    print(file_contents)
