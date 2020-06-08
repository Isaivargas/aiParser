import sys
import parser

tkn_EOI, tkn_Mul, tkn_Div, tkn_Mod, tkn_Add, tkn_Sub, tkn_Negate, tkn_Not, tkn_Lss, tkn_Leq, tkn_Gtr, \
tkn_Geq, tkn_Eq, tkn_Neq, tkn_Assign, tkn_And, tkn_Or, tkn_If, tkn_Else, tkn_While, tkn_Print, \
tkn_Putc, tkn_Lparen, tkn_Rparen, tkn_Lbrace, tkn_Rbrace, tkn_Semi, tkn_Comma, tkn_Ident, \
tkn_Integer, tkn_String,tkn_programa,tkn_questionMark,tkn_switch,tkn_case,tkn_break = range(36)

tokens = ["End_of_input", "Op_multiply", "Op_divide", "Op_mod", "Op_add", "Op_subtract",
            "Op_negate", "Op_not", "Op_less", "Op_lessequal", "Op_greater", "Op_greaterequal",
            "Op_equal", "Op_notequal", "Op_assign", "Op_and", "Op_or", "Keyword_if",
            "Keyword_else", "Keyword_while", "Keyword_print", "Keyword_putc", "LeftParen",
            "RightParen", "LeftBrace", "RightBrace", "Semicolon", "Comma", "Identifier",
            "Integer", "String","Keyword_programa","questionMark,","keyword_switch","keyword_case","keyword_break"]


simbolos =  {'{': tkn_Lbrace, '}': tkn_Rbrace, '(': tkn_Lparen, ')': tkn_Rparen, '+': tkn_Add, '-': tkn_Sub,
           '*': tkn_Mul, '%': tkn_Mod, ';': tkn_Semi, ',': tkn_Comma,'?':tkn_questionMark}

palabrasReservadas = {'if': tkn_If, 'else': tkn_Else, 'print': tkn_Print, 'putc': tkn_Putc
    , 'while': tkn_While,'programa':tkn_programa,'switch':tkn_switch,'case':tkn_case,'break':tkn_break}

the_ch           = " "
the_col          = 0
the_linea        = 1
input_file       = None
prediction_file  = None
input = ""
scannerProduction = []
parserPrediction  = []
scann = 0
scannerTokenList = []
aiScannerTokenList = []
tokenAccepted = []

def error(linea, col, msg):
    print(linea, col, msg)
    exit(1)



def next_ch(scann):
    global the_ch, the_col, the_linea

    if (scann == 0):
       the_ch = input_file.read(1)
       the_col += 1

    if (scann == 1):
        the_ch = prediction_file.read(1)
        the_col += 1

    if the_ch == '\n':
        the_linea += 1
        the_col = 0

    return the_ch


# Character constants
def char_lit(err_linea, err_col,scann):
    n = ord(next_ch(scann))  # skip opening quote

    if the_ch == '\'':
        error(err_linea, err_col, "empty character constant")
    elif the_ch == '\\':
        next_ch(scann)
        if the_ch == 'n':
            n = 10
        elif the_ch == '\\':
            n = ord('\\')
        else:
            error(err_linea, err_col, "unknown escape sequence \\%c" % (the_ch))
    if next_ch(scann) != '\'':
        error(err_linea, err_col, "multi-character constant")
    next_ch(scann)
    return tkn_Integer, err_linea, err_col, n


#  process divide or comments
def div_or_cmt(err_linea, err_col,scann):
    if next_ch(scann) != '*':
        return tkn_Div, err_linea, err_col

    # comment found cause the character is recognized as *
    next_ch(scann)
    while True:
        if the_ch == '*':
            if next_ch(scann) == '/':
                next_ch(scann)
                return gettok()
        elif len(the_ch) == 0:
            error(err_linea, err_col, "EOF in comment")
        else:
            next_ch(scann)


# "string"
def string_lit(start, err_linea, err_col):
    text = ""

    while next_ch(scann) != start:
        if len(the_ch) == 0:
            error(err_linea, err_col, "EOF while scanning string literal")
        if the_ch == '\n':
            error(err_linea, err_col, "EOL while scanning string literal")
        text += the_ch

    next_ch(scann)
    return tkn_String, err_linea, err_col, text


# handle identifiers and integers
def ident_or_int(err_linea, err_col,scann):

    is_number = True
    text = ""

    while the_ch.isalnum() or the_ch == '_':
        text += the_ch

        if not the_ch.isdigit():
            is_number = False
        next_ch(scann)

    if len(text) == 0:
        error(err_linea, err_col, "ident_or_int: unrecognized character: (%d) '%c'" % (ord(the_ch), the_ch))

    if text[0].isdigit():
        if not is_number:
            error(err_linea, err_col, "invalid number: %s" % (text))
        n = int(text)
        # Append the inputCode to scannerProduction
        scannerProduction.append(text)
        return tkn_Integer, err_linea, err_col, n

    if text in palabrasReservadas:

        #Append the inputCode to scannerProduction
        scannerProduction.append(text)
        #parser.coder(scannerProduction[0])
        return palabrasReservadas[text], err_linea, err_col

    return tkn_Ident, err_linea, err_col, text



def follow(expect, ifyes, ifno, err_linea, err_col,scann):

    if next_ch(scann) == expect:
        next_ch(scann)
        # Append the inputCode to scannerProduction
        scannerProduction.append(next_ch(scann))

        return ifyes, err_linea, err_col


    if ifno == tkn_EOI:
        error(err_linea, err_col, " unrecognized character: (%d) '%c'" % (ord(the_ch), the_ch))

    return ifno, err_linea, err_col


def gettok(scann):

  if(scann==0):
    while (the_ch.isspace()):
           next_ch(scann)
    err_linea = the_linea
    err_col = the_col

    if len(the_ch) == 0:
        return tkn_EOI, err_linea, err_col
    elif the_ch == '/':
        return div_or_cmt(err_linea, err_col,scann)
    elif the_ch == '\'':
        return char_lit(err_linea, err_col,scann)
    elif the_ch == '<':
        return follow('=', tkn_Leq, tkn_Lss, err_linea, err_col,scann)
    elif the_ch == '>':
        return follow('=', tkn_Geq, tkn_Gtr, err_linea, err_col,scann)
    elif the_ch == '=':
        return follow('=', tkn_Eq, tkn_Assign, err_linea, err_col,scann)
    elif the_ch == '!':
        return follow('=', tkn_Neq, tkn_Not, err_linea, err_col,scann)
    elif the_ch == '&':
        return follow('&', tkn_And, tkn_EOI, err_linea, err_col,scann)
    elif the_ch == '|':
        return follow('|', tkn_Or, tkn_EOI, err_linea, err_col,scann)
    elif the_ch == ' " ':
        return string_lit(the_ch, err_linea, err_col,scann)
    elif the_ch in simbolos:
        # Append the inputCode to scannerProduction
        scannerProduction.append(the_ch)

        sym = simbolos[the_ch]
        next_ch(scann)
        return sym, err_linea, err_col
    else:
        return ident_or_int(err_linea, err_col,scann)

  else:

      next_ch(scann)
      while (the_ch.isspace()):
             next_ch(scann)

      err_linea = the_linea
      err_col   = the_col

      if len(the_ch) == 0:
          return tkn_EOI, err_linea, err_col
      elif the_ch == '/':
          return div_or_cmt(err_linea, err_col, scann)
      elif the_ch == '\'':
          return char_lit(err_linea, err_col, scann)
      elif the_ch == '<':
          return follow('=', tkn_Leq, tkn_Lss, err_linea, err_col, scann)
      elif the_ch == '>':
          return follow('=', tkn_Geq, tkn_Gtr, err_linea, err_col, scann)
      elif the_ch == '=':
          return follow('=', tkn_Eq, tkn_Assign, err_linea, err_col, scann)
      elif the_ch == '!':
          return follow('=', tkn_Neq, tkn_Not, err_linea, err_col, scann)
      elif the_ch == '&':
          return follow('&', tkn_And, tkn_EOI, err_linea, err_col, scann)
      elif the_ch == '|':
          return follow('|', tkn_Or, tkn_EOI, err_linea, err_col, scann)
      elif the_ch == ' ':
          return follow(' ', tkn_Or, tkn_EOI, err_linea, err_col, scann)
      elif the_ch == ' " ':
          return string_lit(the_ch, err_linea, err_col, scann)
      elif the_ch in simbolos:
          sym = simbolos[the_ch]
          next_ch(scann)
          return sym, err_linea, err_col
      else:
          return ident_or_int(err_linea, err_col, scann)


# save tokens to file, one dialog per line
def save_doc(lines, filename):
    data = '\n'.join(lines)
    file = open(filename, 'w')
    file.write(data)
    file.close()



def accepted():

    for i in range(len(scannerTokenList)):

        if (scannerTokenList[i] == aiScannerTokenList[i]):

            tokenAccepted.append(scannerTokenList[i])

            print("Token Accepted:",tokenAccepted)

        elif(scannerTokenList[i] == aiScannerTokenList[i+1]):

            tokenAccepted.append(scannerTokenList[i])

            print("Token Accepted:", tokenAccepted)

        elif (scannerTokenList[i] == aiScannerTokenList[i + 2]):

            tokenAccepted.append(scannerTokenList[i])

            print("Token Accepted:", tokenAccepted)

        elif (scannerTokenList[i] == aiScannerTokenList[i + 3]):

            tokenAccepted.append(scannerTokenList[i])

            print("Token Accepted:", tokenAccepted)

        else:

            print("Token Rejected",scannerTokenList[i])




def coder():

    for i in range(len(scannerProduction)):
        parserPrediction.append(parser.predict(scannerProduction[i]))

    # save sequences to file
    out_filename = 'parserPrediction.txt'
    save_doc(parserPrediction, out_filename)


    return parserPrediction



input_file = sys.stdin
predictionFile = sys.stdin

if 'fuente.txt':
    print()
    input_file = open('fuente.txt')
    prediction_file = open('parserPrediction.txt')


else:

    len(sys.argv) > 1
    try:
        input_file = open(sys.argv[1], "r", 4096)
    except IOError as e:
        error(0, 0, "Can't open %s" % sys.argv[1])

print("\n ----------------------------------------Scanner analisis of Input Code:----------------------------------------")

while True:
    t = gettok(scann)
    tok = t[0]
    linea = t[1]
    col = t[2]
    i = 0

    print("%d %s" % (col, tokens[tok]), end='')
    scannerTokenList.append(tokens[tok])

    if tok == tkn_Ident:
        print("  %s" % (t[3]))
    elif tok == tkn_String:
        print('  "%s"' % t[3])
    else:
       print("")

    if tok == tkn_EOI:
       break


parserPrediction = coder()


print("\n ----------------------------------------AI Parser predictions of the Input Code:----------------------------------------")

while True:

    scann   = 1

    t       = gettok(scann)
    tok     = t[0]
    aiLinea = t[1]
    aiCol   = t[2]

    print("%s \n " % ( tokens[tok]), end='')
    aiScannerTokenList.append(tokens[tok])

    if tok == tkn_EOI:
       break


print("\n------------------------------------------------------------AI parser-----------------------------------------------------")

accepted()