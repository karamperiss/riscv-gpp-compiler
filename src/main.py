import sys
import os
import traceback
import state
import lexer
from parser import Parser
from intermediate import intermediateCodeGenerator
from symbol_table import symbolTableGenerator
from codegen import test_quadToFinalCode_and_write_output

def main(args):
    if len(sys.argv) != 2:
        print("Use: python3 main.py <filename>")
        sys.exit(1)

    input_filename = sys.argv[1]
    base_name, _ = os.path.splitext(os.path.basename(input_filename))
    intermediate_code_filename = f"{base_name}.int"
    symbol_table_filename = f"{base_name}.sym"
    final_code_filename = f"{base_name}.asm"

    try:
        with open(input_filename, "r", encoding="utf-8") as infile:
            tokens = lexer.lexical_analyzer(infile)
            print("The program passed the lexical analysis successfully.")

            try:
                parser = Parser(tokens)
                parser.program()
                print("The program passed the syntax analysis successfully.")

                intermediateCodeGenerator(intermediate_code_filename)
                print(f"Intermediate code written to {intermediate_code_filename}")

                symbolTableGenerator(symbol_table_filename)
                print(f"Symbol table written to {symbol_table_filename}")

                test_quadToFinalCode_and_write_output(final_code_filename)
                print(f"Final code written to {final_code_filename}")

            except SyntaxError as e:
                print(f"Syntax Error: {e}")

    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main(sys.argv)