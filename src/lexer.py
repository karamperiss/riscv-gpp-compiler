import sys
import state

class Token:
    def __init__(self, tokenType, token, line_counter):
        self.tokenType = tokenType
        self.token = token
        self.line_counter = line_counter

    def __str__(self):
        return f"{self.tokenType}: {self.token} (Line {self.line_counter})"

def lexical_analyzer(infile):
    tokens = []
    line_counter = 1
    char = infile.read(1)

    while char != "":  # EOF
        if char.isspace():
            if char == "\n":
                line_counter += 1
            char = infile.read(1)
            continue

        token = []

        if char.isdigit():
            while char.isdigit():
                token.append(char)
                char = infile.read(1)
            if char.isalpha():
                print(f"Error in line {line_counter}: unexpected letter '{char}' after number {''.join(token)}")
                sys.exit(1)
            num = int("".join(token))
            if num > 100000:
                print(f"Error: Number is too big")
                sys.exit(1)
            tokens.append(Token("number", ''.join(token), line_counter))
            continue

        if char.isalpha():
            letter_counter = 1
            while char.isdigit() or char.isalpha() or char == "_":
                token.append(char)
                char = infile.read(1)
                letter_counter += 1

            token_string = "".join(token)
            if letter_counter > 30:
                print(f"Error in line {line_counter}: Identifier '{token_string}' exceeds the 30-character limit.")
                sys.exit(1)
            if token_string in state.reserved_words:
                tokens.append(Token("keyword", token_string, line_counter))
            else:
                tokens.append(Token("identifier", token_string, line_counter))
            continue

        if char in "+-*/":
            tokens.append(Token("mathOp", char, line_counter))
            char = infile.read(1)
            continue

        if char == "=":
            tokens.append(Token("relationalOp", "=", line_counter))
            char = infile.read(1)
            continue

        if char == "<":
            next_char = infile.read(1)
            if next_char == "=":
                tokens.append(Token("relationalOp", "<=", line_counter))
                char = infile.read(1)
            elif next_char == ">":
                tokens.append(Token("relationalOp", "<>", line_counter))
                char = infile.read(1)
            else:
                tokens.append(Token("relationalOp", "<", line_counter))
                char = next_char
            continue

        if char == ">":
            next_char = infile.read(1)
            if next_char == "=":
                tokens.append(Token("relationalOp", ">=", line_counter))
                char = infile.read(1)
            else:
                tokens.append(Token("relationalOp", ">", line_counter))
                char = next_char
            continue

        if char == ":":
            next_char = infile.read(1)
            if next_char == "=":
                tokens.append(Token("assignOperator", ":=", line_counter))
            else:
                print(f"Error in line {line_counter}: expected '=' after ':'")
                sys.exit(1)
            char = infile.read(1)
            continue

        if char in "()[]":
            tokens.append(Token("groupSymbol", char, line_counter))
            char = infile.read(1)
            continue

        if char in ",;":
            tokens.append(Token("delimiter", char, line_counter))
            char = infile.read(1)
            continue

        if char == "%":
            tokens.append(Token("referenceOp", char, line_counter))
            char = infile.read(1)
            continue

        if char == "{":
            while True:
                char = infile.read(1)
                if char == "}":
                    tokens.append(Token("comment", "{}", line_counter))
                    break
                if char == "":
                    print(f"Error in line {line_counter}: unclosed comment")
                    sys.exit(1)
            char = infile.read(1)
            continue

        print(f"Error in line {line_counter}: unknown character '{char}'")
        sys.exit(1)
    return tokens