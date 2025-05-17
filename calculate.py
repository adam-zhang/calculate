#!/bin/python
import re
import sys

#def tokenize(expr):
#    expr = expr.replace(' ', '')
#    tokens = re.findall(r'(\d+\.?\d*|$|$|\+|\-|\*|/)', expr)
#    new_tokens = []
#    for i in range(len(tokens)):
#        token = tokens[i]
#        if token == '-':
#            if i == 0 or tokens[i-1] in '+-*/(':
#                new_tokens.append('u-')
#            else:
#                new_tokens.append('-')
#        else:
#            new_tokens.append(token)
#    return new_tokens

def tokenize(expr):
    expr = expr.replace(' ', '')  # 移除所有空格
    tokens = []
    current_num = ''  # 正在构建的数值字符串
    prev_type = None  # 记录上一个Token的类型 ('number', 'operator', '(', ')')

    for i, char in enumerate(expr):
        # 当前字符是数字或小数点时，继续构建数值
        if char.isdigit() or char == '.':
            current_num += char
        else:
            # 遇到非数字字符，先将之前的数值存入Token
            if current_num:
                tokens.append(current_num)
                current_num = ''
                prev_type = 'number'
            
            # 处理运算符或括号
            if char in ('+', '-', '*', '/', '(', ')'):
                # 判断是否为一元负号 ('u-')
                if char == '-':
                    # 位于起始位置 或 前一个字符为运算符或左括号 => 一元负号
                    if (i == 0) or (prev_type in ('operator', '(')):
                        tokens.append('u-')
                        prev_type = 'operator'  # 一元负号视为运算符
                    else:
                        tokens.append('-')
                        prev_type = 'operator'
                # 处理其他运算符或括号
                elif char in ('+', '*', '/'):
                    tokens.append(char)
                    prev_type = 'operator'
                elif char == '(':
                    tokens.append('(')
                    prev_type = '('
                elif char == ')':
                    tokens.append(')')
                    prev_type = ')'
            else:
                # 非法字符异常处理
                raise ValueError(f"无效字符 '{char}'")

    # 遍历结束后，处理最后的数值
    if current_num:
        tokens.append(current_num)

    return tokens

def shunting_yard(tokens):
    output = []
    stack = []
    operators = {
        '+': {'priority': 1, 'assoc': 'left'},
        '-': {'priority': 1, 'assoc': 'left'},
        '*': {'priority': 2, 'assoc': 'left'},
        '/': {'priority': 2, 'assoc': 'left'},
        'u-': {'priority': 3, 'assoc': 'right'}
    }
    for token in tokens:
        if token.replace('.', '', 1).isdigit():
            output.append(token)
        elif token == '(':
            stack.append(token)
        elif token == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            if not stack:
                raise ValueError("Mismatched parentheses")
            stack.pop()
        else:
            while stack and stack[-1] != '(':
                top = stack[-1]
                if top not in operators:
                    break
                current_op = operators[token]
                top_op = operators[top]
                if ( (current_op['assoc'] == 'left' and current_op['priority'] <= top_op['priority']) or
                     (current_op['assoc'] == 'right' and current_op['priority'] < top_op['priority']) ):
                    output.append(stack.pop())
                else:
                    break
            stack.append(token)
    while stack:
        if stack[-1] == '(':
            raise ValueError("Mismatched parentheses")
        output.append(stack.pop())
    return output

def evaluate_postfix(postfix):
    stack = []
    for token in postfix:
        if token.replace('.', '', 1).isdigit():
            num = float(token) if '.' in token else int(token)
            stack.append(num)
        elif token == 'u-':
            stack.append(-stack.pop())
        else:
            b = stack.pop()
            a = stack.pop()
            if token == '+':
                stack.append(a + b)
            elif token == '-':
                stack.append(a - b)
            elif token == '*':
                stack.append(a * b)
            elif token == '/':
                stack.append(a / b)
            else:
                raise ValueError(f"Unknown operator: {token}")
    if len(stack) != 1:
        raise ValueError("Invalid expression")
    return stack[0]

def calculate(expr):
    tokens = tokenize(expr)
    print(tokens)
    postfix = shunting_yard(tokens)
    return evaluate_postfix(postfix)

def main():
    # 合并所有参数为一个表达式（例如：将 "3" "+" "2" 合并为 "3+2"）
    expr = ' '.join(sys.argv[1:]) if len(sys.argv) > 1 else ''
    if not expr:
        print("请提供表达式参数！")
        return
    
    #result = calculate(expr)
    #print(f"结果: {result}")
    print(calculate(sys.argv[1]))

if __name__ == "__main__":
    main()
