# treesitter_example
Example of playing with TreeSitter for Java parsing

## Notes
* Using https://pypi.org/project/tree-sitter-languages/ instead of building the languages myself

## Example to run

### Example 1
```
$ python3 java_scope_finder.py ./data/Example.java 5
/Users/jmatthews/git/jwmatthews/treesitter_example/env/lib/python3.12/site-packages/tree_sitter/__init__.py:36: FutureWarning: Language(path, name) is deprecated. Use Language(ptr, name) instead.
  warn("{} is deprecated. Use {} instead.".format(old, new), FutureWarning)
Scope Type: class_declaration
Start Line: 1
End Line: 12

Code Snippet:
public class Example {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }

    public void methodOne() {
        // Some code here
        if (condition) {
            // More code
        }
    }
}
```
### Example 2
```
$ python3 java_scope_finder.py ./data/Example.java 10
/Users/jmatthews/git/jwmatthews/treesitter_example/env/lib/python3.12/site-packages/tree_sitter/__init__.py:36: FutureWarning: Language(path, name) is deprecated. Use Language(ptr, name) instead.
  warn("{} is deprecated. Use {} instead.".format(old, new), FutureWarning)
Scope Type: expression_statement
Start Line: 10
End Line: 10

Code Snippet:
            System.out.println("Inside of if #1");

```
