import Tokens
from Error import SyntaxError, raise_
from Tokens import *

class Lexer:
    @staticmethod
    def generate_tokens(code: str):
        # ---------------- Variables---------------------
        tokens = []
        count = 0
        code = code.replace('    ', '\t')
        basic_characters = {'\n':NEWLINE, '\t': TAB,
                            '=': EQUAL, '+': PLUS, '-': MINUS, '*': MUL, '^':'CARAT',
                            '/': DIV, '#':HASH, '%':MOD, '&':AND, '|': OR, '!': NOT,
                            '(': LEFT_PAREN, ')': RIGHT_PAREN, '[': LEFT_BRACE, ']': RIGHT_BRACE,
                            '{': LEFT_SET, '}': RIGHT_SET, ':': COLON, ';': END, '$':VARIABLE,'@':LABEL,
                            '>': GREATER, '<': LESSER
                            }
        alpha = 'abcdefghijklmnopqrstuvwxyz' + 'abcdefghijklmnopqrstuvwxyz'.upper()
        numeric = '0123456789'
        alpha_numeric = alpha + numeric + '_'

        while count < len(code):
            if code[count] in basic_characters:
                tokens.append(Token(basic_characters.get(code[count])))

            elif code[count] == '"' or code[count] == "'":
                check = '"' if code[count] == '"' else code[count]
                string = ''
                run = True
                count += 1
                while run:
                    if count >= len(code):
                        raise_(SyntaxError('Console','1',f'Missing quotation({check}) mark', code))
                    if code[count] == check:
                        break
                    string += code[count]
                    count += 1
                tokens.append(Token(STRING,string))
                count += 1
                continue

            elif code[count] in alpha:
                string = code[count]
                count = count + 1
                while count < len(code) and code[count] in alpha_numeric :
                    string += code[count]
                    count += 1
                tokens.append(Token(DTYPE if string in DTYPES else KEYWORD if string in KEYWORDS else IDENTIFIER, string))
                continue

            elif code[count] in numeric:
                string = code[count]
                count = count + 1
                while count < len(code) and (code[count] in numeric or code[count] == '.') :
                    string += code[count]
                    count += 1
                if string.find('.') != -1:
                    tokens.append(Token(FLOAT, string))
                    continue
                tokens.append(Token(INTEGER,string))
                continue

            count += 1

        return Lexer.compress(tokens)

    @staticmethod
    def compress(tokens:list[Token]):
        pop_tok = []
        for index, token in enumerate(tokens):
            if token.type == Tokens.EQUAL and index > 0:
                match tokens[index - 1].type:
                    case Tokens.EQUAL:
                        pop_tok.append(index)
                        tokens[index-1].type = Tokens.DEQUAL
                    case Tokens.GREATER:
                        pop_tok.append(index)
                        tokens[index-1].type = Tokens.GEQUAL
                    case Tokens.LESSER:
                        pop_tok.append(index)
                        tokens[index-1].type = Tokens.LEQUAL
                    case Tokens.PLUS:
                        pop_tok.append(index)
                        tokens[index-1].type = Tokens.PEQUAL
                    case Tokens.MINUS:
                        pop_tok.append(index)
                        tokens[index-1].type = Tokens.MEQUAL
                    case Tokens.MUL:
                        pop_tok.append(index)
                        tokens[index-1].type = Tokens.MULEQUAL
                    case Tokens.COLON:
                        pop_tok.append(index)
                        tokens[index-1].type = Tokens.REASSIGN
                    case Tokens.MOD:
                        pop_tok.append(index)
                        tokens[index-1].type = Tokens.MODEQUAL
                    case Tokens.DIV:
                        pop_tok.append(index)
                        tokens[index-1].type = Tokens.DIVEQUAL
                    case Tokens.NOT:
                        pop_tok.append(index)
                        tokens[index-1].type = Tokens.NEQUAL
            if token.type == Tokens.PLUS and index > 0:
                match tokens[index - 1].type:
                    case Tokens.PLUS:
                        pop_tok.append(index)
                        tokens[index - 1].type = Tokens.INCREMENT
        for p in pop_tok:
            tokens.pop(p)
        return tokens