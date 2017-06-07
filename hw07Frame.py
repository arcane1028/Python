# -*- coding: utf-8 -*-
from string import letters, digits, whitespace

v_table = {}
lambda_table = {}
stack = []
depth = 0

class CuteType:
    INT = 1
    ID = 4

    MINUS = 2
    PLUS = 3

    L_PAREN = 5
    R_PAREN = 6

    TRUE = 8
    FALSE = 9

    TIMES = 10
    DIV = 11

    LT = 12
    GT = 13
    EQ = 14
    APOSTROPHE = 15

    DEFINE = 20
    LAMBDA = 21
    COND = 22
    QUOTE = 23
    NOT = 24
    CAR = 25
    CDR = 26
    CONS = 27
    ATOM_Q = 28
    NULL_Q = 29
    EQ_Q = 30
    SEE = 31
    KEYWORD_LIST = ('define', 'lambda', 'cond', 'quote', 'not', 'car', 'cdr', 'cons',
                    'atom?', 'null?', 'eq?', 'see')

    BINARYOP_LIST = (DIV, TIMES, MINUS, PLUS, LT, GT, EQ)
    BOOLEAN_LIST = (TRUE, FALSE)


def check_keyword(token):
    """
    :type token:str
    :param token:
    :return:
    """
    if token.lower() in CuteType.KEYWORD_LIST:
        return True
    return False


def _get_keyword_type(token):
    return {
        'define': CuteType.DEFINE,
        'lambda': CuteType.LAMBDA,
        'cond': CuteType.COND,
        'quote': CuteType.QUOTE,
        'not': CuteType.NOT,
        'car': CuteType.CAR,
        'cdr': CuteType.CDR,
        'cons': CuteType.CONS,
        'atom?': CuteType.ATOM_Q,
        'null?': CuteType.NULL_Q,
        'eq?': CuteType.EQ_Q,
        'see': CuteType.SEE
    }[token]


CUTETYPE_NAMES = dict((eval(attr, globals(), CuteType.__dict__), attr) for attr in dir(
    CuteType()) if not callable(attr) and not attr.startswith('__'))


class Token(object):
    def __init__(self, type, lexeme):
        """
        :type type:CuteType
        :type lexeme: str
        :param type:
        :param lexeme:
        :return:
        """
        if check_keyword(lexeme):
            self.type = _get_keyword_type(lexeme)
            self.lexeme = lexeme
        else:
            self.type = type
            self.lexeme = lexeme
            # print type

    def __str__(self):
        # return self.lexeme
        return '[' + CUTETYPE_NAMES[self.type] + ': ' + self.lexeme + ']'

    def __repr__(self):
        return str(self)


class Scanner:

    def __init__(self, source_string=None):
        """
        :type self.__source_string: str
        :param source_string:
        """
        self.__source_string = source_string
        self.__pos = 0
        self.__length = len(source_string)
        self.__token_list = []

    def __make_token(self, transition_matrix, build_token_func=None):
        old_state = 0
        self.__skip_whitespace()
        temp_char = ''
        return_token = ''
        while not self.eos():
            temp_char = self.get()
            if old_state == 0 and temp_char in (')', '('):
                return_token = temp_char
                old_state = transition_matrix[(old_state, temp_char)]
                break

            return_token += temp_char
            old_state = transition_matrix[(old_state, temp_char)]
            next_char = self.peek()
            if next_char in whitespace or next_char in ('(', ')'):
                break

        return build_token_func(old_state, return_token)

    def scan(self, transition_matrix, build_token_func):
        while not self.eos():
            self.__token_list.append(self.__make_token(
                transition_matrix, build_token_func))
        return self.__token_list

    def pos(self):
        return self.__pos

    def eos(self):
        return self.__pos >= self.__length

    def skip(self, pattern):
        while not self.eos():
            temp_char = self.peek()
            if temp_char in pattern:
                temp_char = self.get()
            else:
                break

    def __skip_whitespace(self):
        self.skip(whitespace)

    def peek(self, length=1):
        return self.__source_string[self.__pos: self.__pos + length]

    def get(self, length=1):
        return_get_string = self.peek(length)
        self.__pos += len(return_get_string)
        return return_get_string


class CuteScanner(object):

    transM = {}

    def __init__(self, source):
        """
        :type source:str
        :param source:
        :return:
        """
        self.source = source
        self._init_TM()

    def _init_TM(self):
        for alpha in letters:
            self.transM[(0, alpha)] = 4
            self.transM[(4, alpha)] = 4

        for digit in digits:
            self.transM[(0, digit)] = 1
            self.transM[(1, digit)] = 1
            self.transM[(2, digit)] = 1
            self.transM[(4, digit)] = 4

        self.transM[(4, '?')] = 16
        self.transM[(0, '-')] = 2
        self.transM[(0, '+')] = 3
        self.transM[(0, '(')] = 5
        self.transM[(0, ')')] = 6

        self.transM[(0, '#')] = 7
        self.transM[(7, 'T')] = 8
        self.transM[(7, 'F')] = 9

        self.transM[(0, '/')] = 11
        self.transM[(0, '*')] = 10

        self.transM[(0, '<')] = 12
        self.transM[(0, '>')] = 13
        self.transM[(0, '=')] = 14
        self.transM[(0, "'")] = 15

    def tokenize(self):

        def build_token(type, lexeme): return Token(type, lexeme)
        cute_scanner = Scanner(self.source)
        return cute_scanner.scan(self.transM, build_token)


class TokenType():
    INT = 1
    ID = 4
    MINUS = 2
    PLUS = 3
    LIST = 5
    TRUE = 8
    FALSE = 9
    TIMES = 10
    DIV = 11
    LT = 12
    GT = 13
    EQ = 14
    APOSTROPHE = 15
    DEFINE = 20
    LAMBDA = 21
    COND = 22
    QUOTE = 23
    NOT = 24
    CAR = 25
    CDR = 26
    CONS = 27
    ATOM_Q = 28
    NULL_Q = 29
    EQ_Q = 30
    SEE = 31

NODETYPE_NAMES = dict((eval(attr, globals(), TokenType.__dict__), attr) for attr in dir(
    TokenType()) if not callable(attr) and not attr.startswith('__'))

class Node (object):

    def __init__(self, type, value=None):
        self.next = None
        self.value = value
        self.type = type

    def set_last_next(self, next_node):
        if self.next is not None:
            self.next.set_last_next(next_node)

        else:
            self.next = next_node

    def __str__(self):
        result = ''

        if self.type is TokenType.ID:
            result = '[' + NODETYPE_NAMES[self.type] + ':' + self.value + ']'
        elif self.type is TokenType.INT:
            result = '['+NODETYPE_NAMES[self.type]+':' + self.value + ']'
        elif self.type is TokenType.LIST:
            if self.value is not None:
                if self.value.type is TokenType.QUOTE:
                    result = str(self.value)
                else:
                    result = '(' + str(self.value) + ')'
            else:
                result = '(' + str(self.value) + ')'
        elif self.type is TokenType.QUOTE:
            result = "\'"
        else:
            result = '['+NODETYPE_NAMES[self.type]+']'

        # fill out
        if self.next is not None:
            return result + ' ' + str(self.next)
        else:
            return result


class BasicPaser(object):

    def __init__(self, token_list):
        """
        :type token_list:list
        :param token_list:
        :return:
        """
        self.token_iter = iter(token_list)

    def _get_next_token(self):
        """
        :rtype: Token
        :return:
        """
        next_token = next(self.token_iter, None)
        if next_token is None:
            return None
        return next_token

    def parse_expr(self):
        """
        :rtype : Node
        :return:
        """
        token = self._get_next_token()

        '"":type :Token""'
        if token is None:
            return None
        result = self._create_node(token)
        return result

    def _create_node(self, token):
        if token is None:
            return None
        elif token.type is CuteType.INT:
            return Node(TokenType.INT,  token.lexeme)
        elif token.type is CuteType.ID:
            return Node(TokenType.ID,   token.lexeme)
        elif token.type is CuteType.L_PAREN:
            return Node(TokenType.LIST, self._parse_expr_list())
        elif token.type is CuteType.R_PAREN:
            return None
        elif token.type in CuteType.BOOLEAN_LIST:
            return Node(token.type)
        elif token.type in CuteType.BINARYOP_LIST:
            return Node(token.type, token.lexeme)
        elif token.type is CuteType.QUOTE:
            return Node(TokenType.QUOTE, token.lexeme)
        elif token.type is CuteType.APOSTROPHE:
            node = Node(TokenType.LIST, Node(TokenType.QUOTE, token.lexeme))
            node.value.next = self.parse_expr()
            return node
        elif check_keyword(token.lexeme):
            return Node(token.type, token.lexeme)

    def _parse_expr_list(self):
        head = self.parse_expr()
        '"":type :Node""'
        if head is not None:
            head.next = self._parse_expr_list()
        return head


def run_list(root_node):
    """
    :type root_node: Node
    """
    op_code_node = root_node.value
    if op_code_node.type is TokenType.LIST:
        if op_code_node.value.type is TokenType.LAMBDA:
            return run_func(op_code_node.value)(root_node, True)

    if op_code_node.type is TokenType.ID:
        l_node = run_expr(op_code_node)
        l_node.next = op_code_node.next
        newNode = Node(TokenType.LIST, l_node)
        return run_func(l_node.value)(newNode, True)

    return run_func(op_code_node)(root_node)

def run_func(op_code_node):
    """
    :type op_code_node:Node/
    """
    def quote(node):
        return node

    def strip_quote(node):
        """
        :type node: Node
        """
        if node.type is TokenType.LIST:
            if node.value is TokenType.QUOTE or TokenType.APOSTROPHE:
                return node.value.next
        if node.type is TokenType.QUOTE:
            return node.next
        return node

    def cons(node):
        """
        :type node: Node
        """
        l_node = node.value.next
        r_node = l_node.next
        r_node = run_expr(r_node)
        l_node = run_expr(l_node)
        new_r_node = r_node
        new_l_node = l_node
        new_r_node = strip_quote(new_r_node)
        new_l_node = strip_quote(new_l_node)
        new_l_node.next = new_r_node.value

        return create_new_quote_list(new_l_node, True)

    def car(node):
        l_node = run_expr(node.value.next)
        result = strip_quote(l_node).value
        if result.type is not TokenType.LIST:
            return result
        return create_new_quote_list(result)

    def cdr(node):
        """
        :type node: Node
        """
        l_node = node.value.next
        l_node = run_expr(l_node)
        new_r_node = strip_quote(l_node)
        return create_new_quote_list(new_r_node.value.next, True)

    def null_q(node):
        l_node = run_expr(node.value.next)
        new_l_node = strip_quote(l_node).value
        if new_l_node is None:
            return Node(TokenType.TRUE)
        else:
            return Node(TokenType.FALSE)

    def atom_q(node):
        l_node = run_expr(node.value.next)
        new_l_node = strip_quote(l_node)

        if new_l_node.type is TokenType.LIST:
            if new_l_node.value is None:
                return Node(TokenType.TRUE)
            return Node(TokenType.FALSE)
        else:
            return Node(TokenType.TRUE)

    def eq_q(node):
        l_node = node.value.next
        r_node = l_node.next
        new_l_node = strip_quote(run_expr(l_node))
        new_r_node = strip_quote(run_expr(r_node))

        if (new_l_node.type or new_r_node.type) is not TokenType.INT:
            return Node(TokenType.FALSE)
        if new_l_node.value == new_r_node.value:
            return Node(TokenType.TRUE)
        return Node(TokenType.FALSE)

    # Fill Out
    # table을 보고 함수를 작성하시오
    def not_op(node):
        l_node = node.value.next
        l_node = run_expr(l_node)
        if l_node.type is TokenType.TRUE:
            return Node(TokenType.FALSE)
        elif l_node.type is TokenType.FALSE:
            return Node(TokenType.TRUE)
        return Node(TokenType.ID, "is not boolean")

    def plus(node):
        l_node = node.value.next
        r_node = l_node.next
        l_node = run_expr(l_node)
        r_node = run_expr(r_node)

        if (l_node.type or r_node.type) is not TokenType.INT:
            return Node(TokenType.ID, "is not int")
        result = int(l_node.value) + int(r_node.value)
        return Node(TokenType.INT, str(result))

    def minus(node):
        l_node = node.value.next
        r_node = l_node.next
        l_node = run_expr(l_node)
        r_node = run_expr(r_node)

        if (l_node.type or r_node.type) is not TokenType.INT:
            return Node(TokenType.ID, "is not int")
        result = int(l_node.value) - int(r_node.value)
        return Node(TokenType.INT, str(result))

    def multiple(node):
        l_node = node.value.next
        r_node = l_node.next
        l_node = run_expr(l_node)
        r_node = run_expr(r_node)

        if (l_node.type or r_node.type) is not TokenType.INT:
            return Node(TokenType.ID, "is not int")

        result = int(l_node.value) * int(r_node.value)
        return Node(TokenType.INT, str(result))

    def divide(node):
        l_node = node.value.next
        r_node = l_node.next
        l_node = run_expr(l_node)
        r_node = run_expr(r_node)

        if (l_node.type or r_node.type) is not TokenType.INT:
            return Node(TokenType.ID, "is not int")
        if int(r_node.value) is 0:
            return Node(TokenType.ID, "division by 0")
        result = int(l_node.value) / int(r_node.value)
        return Node(TokenType.INT, str(result))

    def lt(node):
        l_node = node.value.next
        r_node = l_node.next
        l_node = run_expr(l_node)
        r_node = run_expr(r_node)

        if (l_node.type or r_node.type) is not TokenType.INT:
            return Node(TokenType.ID, "is not int")

        if(int(l_node.value) < int(r_node.value)) is True:
            return Node(TokenType.TRUE)
        else:
            return Node(TokenType.FALSE)

    def gt(node):
        l_node = node.value.next
        r_node = l_node.next
        l_node = run_expr(l_node)
        r_node = run_expr(r_node)

        if (l_node.type or r_node.type) is not TokenType.INT:
            return Node(TokenType.ID, "is not int")

        if (int(l_node.value) > int(r_node.value)) is True:
            return Node(TokenType.TRUE)
        else:
            return Node(TokenType.FALSE)

    def eq(node):
        l_node = node.value.next
        r_node = l_node.next
        l_node = run_expr(l_node)
        r_node = run_expr(r_node)

        if (l_node.type or r_node.type) is not TokenType.INT:
            return Node(TokenType.ID, "is not int")

        if (int(l_node.value) == int(r_node.value)) is True:
            return Node(TokenType.TRUE)
        else:
            return Node(TokenType.FALSE)

    def cond(node):
        l_node = node.value.next

        if l_node is not None:
            return run_cond(l_node)
        else:
            print('cond null error!')

    def run_cond(node):
        """
        :type node: Node
        """
        condition = node.value
        result = node.value.next

        condition = run_expr(condition)

        if condition.type is TokenType.TRUE:
            return run_expr(result)
        elif condition.type is TokenType.FALSE:
            if node.next is not None:
                return run_cond(node.next)
        return Node(TokenType.ID, "error")

    def define(node):
        l_node = node.value.next
        var_name = l_node.value
        if (depth >= len(stack)) is True:
            a = {var_name: run_expr(l_node.next)}
            stack.append(dict(a))
        else:
            stack[depth][var_name] = run_expr(l_node.next)
        return Node(TokenType.ID, var_name + " = " + stack[depth][var_name].__str__())

    def see(node):
        for c in v_table:
            print (c + ":"),; print(v_table[c])
        return node

    def lambdas(node, con=False):
        if con is True:
            #ex) ( ( lambda (x y z) ( + x ( - y z ) ) 2 3 4 )
            global depth
            depth += 1
            local_table={}
            stack.append(local_table)
            param = node.value.next # 2 3 4
            if param is None:
                return node
            formal = node.value.value.next # (x y z)( + x ( - y z) )
            statement = formal.next # ( + x ( - y z ) )

            iterator = formal.value # x -> y -> z
            param_iterator(iterator, param)

            temp = statement
            temp = body_iterator(temp)
            return_value = run_expr(temp)

            stack.pop()
            depth-=1
            return return_value
        else:
            return node

    def param_iterator(iter, param):
        stack[depth][iter.value] = run_expr(Node(param.type, param.value))
        if iter.next is not None:
            # v_table[ x -> y -> z ] = run_expr(Node(TokenType.INT, 2 -> 3-> 4))
            return param_iterator(iter.next, param.next)
        else:
            return
    def body_iterator(body):
        if body.next is not None:
            run_expr(body)
            return body_iterator(body.next)
        else:
            return body

    def create_new_quote_list(value_node, list_flag=False):
        """
        :type value_node: Node
        """
        quote_list = Node(TokenType.QUOTE, 'quote')
        wrapper_new_list = Node(TokenType.LIST, quote_list)
        if value_node is None:
            pass
        elif value_node.type is TokenType.LIST:
            if list_flag:
                inner_l_node = Node(TokenType.LIST, value_node)
                quote_list.next = inner_l_node
            else:
                quote_list.next = value_node
            return wrapper_new_list
        new_value_list = Node(TokenType.LIST, value_node)
        quote_list.next = new_value_list
        return wrapper_new_list

    table={}

    table['cons'] = cons
    table["'"] = quote
    table['quote'] = quote
    table['cdr'] = cdr
    table['car'] = car
    table['eq?'] = eq_q
    table['null?'] = null_q
    table['atom?'] = atom_q
    table['not'] = not_op
    table['+'] = plus
    table['-'] = minus
    table['*'] = multiple
    table['/'] = divide
    table['<'] = lt
    table['>'] = gt
    table['='] = eq
    table['cond'] = cond
    table['define'] = define
    table['lambda'] = lambdas
    table['see'] = see

    return table[op_code_node.value]

def lookupTable(node):
    if node.value in stack[depth]:
        return run_expr(stack[depth][node.value])
    else:
        return lookupTable2(node, depth-1)

def lookupTable2(node, index):
    if index is -1:
        return node
    if node.value in stack[index]:
        return run_expr(stack[index][node.value])
    else:
        return lookupTable2(node, index-1)

def run_expr(root_node):
    """
    :type root_node : Node
    """
    if root_node is None:
        return None

    if root_node.type is TokenType.ID:
        node = lookupTable(root_node)
        return node
    elif root_node.type is TokenType.INT:
        return root_node
    elif root_node.type is TokenType.TRUE:
        return root_node
    elif root_node.type is TokenType.FALSE:
        return root_node
    elif root_node.type is TokenType.LIST:
        return run_list(root_node)
    else:
        print 'Run Expr Error'
    return None


def print_node(node):
    """
    "Evaluation 후 결과를 출력하기 위한 함수"
    "입력은 List Node 또는 atom"
    :type node: Node
    """
    def print_list(node):
        """
        "List노드의 value에 대해서 출력"
        "( 2 3 )이 입력이면 2와 3에 대해서 모두 출력함"
        :type node: Node
        """
        def print_list_val(node):
            if node.next is not None:
                return print_node(node)+' '+print_list_val(node.next)
            return print_node(node)

        if node.type is TokenType.LIST:
            if node.value is None:
                return '( )'
            if node.value.type is TokenType.QUOTE:
                return print_node(node.value)
            return '('+print_list_val(node.value)+')'

    if node is None:
        return ''
    if node.type in [TokenType.ID, TokenType.INT]:
        return node.value
    if node.type is TokenType.TRUE:
        return '#T'
    if node.type is TokenType.FALSE:
        return '#F'
    if node.type is TokenType.PLUS:
        return '+'
    if node.type is TokenType.MINUS:
        return '-'
    if node.type is TokenType.TIMES:
        return '*'
    if node.type is TokenType.DIV:
        return '/'
    if node.type is TokenType.GT:
        return '>'
    if node.type is TokenType.LT:
        return '<'
    if node.type is TokenType.EQ:
        return '='
    if node.type is TokenType.LIST:
        return print_list(node)
    if node.type is TokenType.ATOM_Q:
        return 'atom?'
    if node.type is TokenType.CAR:
        return 'car'
    if node.type is TokenType.CDR:
        return 'cdr'
    if node.type is TokenType.COND:
        return 'cond'
    if node.type is TokenType.CONS:
        return 'cons'
    if node.type is TokenType.LAMBDA:
        return 'lambda'
    if node.type is TokenType.NULL_Q:
        return 'null?'
    if node.type is TokenType.EQ_Q:
        return 'eq?'
    if node.type is TokenType.NOT:
        return 'not'
    if node.type is TokenType.QUOTE:
        return "'"+print_node(node.next)
    if node.type is TokenType.DEFINE:
        return "define"
    if node.type is TokenType.SEE:
        return "see"

def Test_method(input):
    test_cute = CuteScanner(input)
    test_tokens = test_cute.tokenize()
    test_basic_paser = BasicPaser(test_tokens)
    node = test_basic_paser.parse_expr()
    cute_inter = run_expr(node)
    print print_node(cute_inter)


def interpreter():
    while True:
        prompt = raw_input(" > ")

        if prompt == "exit":
            print "exit"
            break
        print " ...",
        Test_method(prompt)

def Test_All():

    """Test_method("(+ 1 2 )")
    Test_method("(- ( + 1 2 ) 4 )")
    Test_method("(* 3 2 )")
    Test_method("(/ 10 2 )")
    Test_method("(< 1 5 )")
    Test_method("(= 3 ( + 1 2 ) )")
    Test_method("(> 1 5 )")
    Test_method("(not #F )")
    Test_method("(null? '( 1 2 3) )")
    Test_method("(cond (#F 1) ( #T 2 ) )")
    Test_method("(cond ( ( null? ' ( 1 2 3 ) ) 1 ) ( ( > 100 10 ) 2 ) ( #T 3 ) )")

    Test_method("( car '( a b c d ) )")

    Test_method("( define a '(2 3 4))")
    Test_method("( define b ( - 5 2) )")

    Test_method("(define b ( + b 3 ))")
    Test_method("(define plus1 (lambda (x) (+ x 1) ) )")
    Test_method("( (lambda (x) ( - x x )) 9 )")
    Test_method("(define plus2 (lambda (x) (+ (plus1 x) 1 ) ) )")
    Test_method("(plus1 3)")
    Test_method("(plus2 3)")

    Test_method("( define cube (lambda (n) (define sqrt ( lambda (n) (* n n) ) )(* (sqrt n) n))  )")
    Test_method("( cube 3 )")
    Test_method("( define lastitem (lambda (ls) (cond ((null? (cdr ls)) (car ls) )( #T (lastitem (cdr ls))))))")
    Test_method("( lastitem '(a b c d))")
    Test_method("(define square (lambda (x) (* x x)))")
    Test_method("(define yourfunc (lambda (x func) (func x)))")
    Test_method("(yourfunc 3 square)")
    interpreter()"""

    Test_method("(define a 1)")
    Test_method("(define b '(1 2 3))")
    Test_method("(define c (- 5 2))")
    Test_method("(define d '(+ 2 3))")
    Test_method("(define test b)")
    Test_method("(+ a 3)")
    Test_method("(define a 2)")
    Test_method("(* a 4)")

    Test_method("((lambda (x) (* x -2)) 3)")
    Test_method("((lambda (x) (/ x 2)) a)")
    Test_method("((lambda (x y) ( * x y)) 3 5)")
    Test_method("((lambda (x y) ( * x y)) a 5)")
    Test_method("(define plus1 (lambda (x) (+ x 1)))")
    Test_method("(plus1 3)")
    Test_method("(define mul1 (lambda (x) (* x a)))")
    Test_method("(mul1 a)")
    Test_method("(define plus2 (lambda (x) (+ (plus1 x) 1 )))")
    Test_method("(plus2 4)")
    Test_method("(define plus3 (lambda (x) (+ (plus1 x) a )))")
    Test_method("(plus3 a")
    Test_method("(define mul2 (lambda (x) (* (plus1 x) -2 )))")
    Test_method("(mul2 7")
    Test_method("(define lastitem (lambda (ls) (cond ((null? (cdr ls)) (car ls)) (#T (lastitem (cdr ls))))))")
    Test_method("(lastitem '(1 2 3 4 5 6))")
    Test_method("(define square (lambda (x) (* x x)))")
    Test_method("(define yourfunc (lambda (x func) (func x))")
    Test_method("(yourfunc 3 square)")
    Test_method("(define square (lambda (x) (* x x)))")
    Test_method("(define multwo (lambda (x) (* 2 x)))")
    Test_method("(define newfun (lambda (fun1 fun2 x) (fun2 (fun1 x))))")
    Test_method("(newfun square multwo 10)")
    Test_method("(define cube (lambda (n) (define sqrt(lambda (n) (* n n))) (* (sqrt n) n)))")
    Test_method("(cube 3)")
    #Test_method("(sqrt 4)")

    interpreter()
Test_All()