#!/usr/bin/env python
"""
Java Code Scope Finder

This application identifies the smallest code block (such as a method, class, if-statement, etc.)
in a Java source file that contains a specified line number.

Dependencies:
- Python 3.6 or higher
- tree_sitter Python Package
- tree-sitter-languages Python Packageto get the Java grammar

"""

import sys
import os
import argparse
from tree_sitter import Language, Parser
from tree_sitter_languages import get_language, get_parser

def parse_code(code, parser):
    """
    Parses the Java source code using Tree-sitter.

    Parameters:
    - code (bytes): The Java source code in bytes.
    - parser (Parser): The Tree-sitter parser object.

    Returns:
    - Tree: The parsed syntax tree.
    """
    try:
        tree = parser.parse(code)
        return tree
    except Exception as e:
        print(f"Error parsing code: {e}")
        sys.exit(1)

def read_file(file_path):
    """
    Reads the contents of a file.

    Parameters:
    - file_path (str): Path to the file.

    Returns:
    - bytes: The file contents in bytes.
    - list: List of lines in the file.
    """
    try:
        with open(file_path, 'rb') as f:
            code = f.read()
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        return code, lines
    except FileNotFoundError:
        print(f"Error: File '{file_path}' does not exist.")
        sys.exit(1)
    except IOError:
        print(f"Error: Cannot read file '{file_path}'.")
        sys.exit(1)

def node_contains_line(node, line_number):
    """
    Checks if a Tree-sitter node contains the given line number.

    Parameters:
    - node: A Tree-sitter node.
    - line_number (int): The line number to check.

    Returns:
    - bool: True if the node contains the line number, False otherwise.
    """
    return node.start_point[0] <= line_number - 1 <= node.end_point[0]

def find_smallest_enclosing_scope(node, line_number, smallest_scope):
    """
    Recursively traverses the AST to find the smallest scope containing the line number.

    Parameters:
    - node: Current Tree-sitter node.
    - line_number (int): The line number to find.
    - smallest_scope (dict): Dictionary holding the smallest scope found so far.

    Returns:
    - dict: Updated smallest_scope with the smallest enclosing scope.
    """
    if node_contains_line(node, line_number):
        # Update smallest_scope if current node is smaller
        current_scope = {
            'type': node.type,
            'start_line': node.start_point[0] + 1,
            'end_line': node.end_point[0] + 1
        }
        if (smallest_scope['start_line'] is None or
            (current_scope['end_line'] - current_scope['start_line'] <
             smallest_scope['end_line'] - smallest_scope['start_line'])):
            smallest_scope = current_scope

        # Traverse children to find a smaller scope
        for child in node.children:
            smallest_scope = find_smallest_enclosing_scope(child, line_number, smallest_scope)

    return smallest_scope

def find_scope(tree, line_number):
    """
    Finds the smallest code scope in the AST that contains the given line number.

    Parameters:
    - tree: The parsed syntax tree.
    - line_number (int): The line number to find.

    Returns:
    - dict: Information about the smallest enclosing scope.
    """
    root_node = tree.root_node
    smallest_scope = {
        'type': None,
        'start_line': None,
        'end_line': None
    }
    smallest_scope = find_smallest_enclosing_scope(root_node, line_number, smallest_scope)
    return smallest_scope

def display_result(scope, lines):
    """
    Displays the scope information and code snippet.

    Parameters:
    - scope (dict): The scope information.
    - lines (list): List of lines from the source file.
    """
    if scope['type'] is None:
        print("No relevant code scope found for the given line number.")
    else:
        print(f"Scope Type: {scope['type']}")
        print(f"Start Line: {scope['start_line']}")
        print(f"End Line: {scope['end_line']}\n")
        print("Code Snippet:")
        # Adjust for 0-based indexing
        snippet = ''.join(lines[scope['start_line']-1 : scope['end_line']])
        print(snippet)

def validate_line_number(line_number, total_lines):
    """
    Validates the provided line number.

    Parameters:
    - line_number (int): The line number to validate.
    - total_lines (int): Total number of lines in the file.

    Returns:
    - bool: True if valid, False otherwise.
    """
    if line_number <= 0:
        print("Error: Line number must be a positive integer.")
        return False
    if line_number > total_lines:
        print(f"Error: Line number {line_number} exceeds total number of lines ({total_lines}).")
        return False
    return True

def parse_arguments():
    """
    Parses command-line arguments.

    Returns:
    - argparse.Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Find the smallest Java code scope containing a specific line number.")
    parser.add_argument('file_path', type=str, help='Path to the Java source file.')
    parser.add_argument('line_number', type=int, help='Line number to analyze.')
    parser.add_argument('--lang-path', type=str, default=None,
                        help='Path to the compiled Tree-sitter Java language library.')
    return parser.parse_args()

def main():
    # Parse command-line arguments
    args = parse_arguments()
    file_path = args.file_path
    line_number = args.line_number
    lang_path = args.lang_path

    # Read the Java source file
    code, lines = read_file(file_path)
    total_lines = len(lines)

    # Validate the line number
    if not validate_line_number(line_number, total_lines):
        sys.exit(1)

    language = get_language("java")
    parser = get_parser('java')

    # Parse the code
    tree = parse_code(code, parser)

    # Find the smallest enclosing scope
    scope = find_scope(tree, line_number)

    # Display the result
    display_result(scope, lines)

if __name__ == "__main__":
    main()
