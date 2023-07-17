# A Compiler in Python3
This compiler translates a Minimal++ program to MIPS-assembly machine code.
## Usage

To run the compiler on Linux, open a terminal and execute it with python3:

` python3 compiler.py source_program asm_output `

- The `source_program` sould be a valid Minimal++ program. Otherwise, the Compiler will return an Error.
- If no `asm_output` file is specified, the final assembly code can be found in the file `out.asm`.
- If the `source_program` does not contain functions, the Compiler can produce an equivelant executable program in C language, named `intermediate_code.c`.
## Arguments


|Argument        |Explanation                                      |
|----------------|-------------------------------------------------|
|`-h` or `--help`|Display a help message                           |
|`--changelog`   |Display the changelog of the latest version      |

## Test code
In the Tests folder you can find Minimal++ scripts to test and play with the compiler.
