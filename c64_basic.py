#!/usr/bin/env python3
"""
Commodore 64 BASIC Interpreter
A Python implementation that mimics the classic C64 BASIC environment
"""

import re
import math
import random
import time
import os
import sys
from typing import Dict, List, Any, Optional, Union

# ANSI color codes for C64-style colors
class C64Colors:
    # C64 color palette (approximated with ANSI colors)
    BLACK = '\033[30m'
    WHITE = '\033[37m'
    RED = '\033[31m'
    CYAN = '\033[36m'
    PURPLE = '\033[35m'
    GREEN = '\033[32m'
    BLUE = '\033[34m'
    YELLOW = '\033[33m'
    ORANGE = '\033[33m'  # Using yellow as approximation
    BROWN = '\033[33m'   # Using yellow as approximation
    LIGHT_RED = '\033[91m'
    DARK_GREY = '\033[90m'
    GREY = '\033[37m'
    LIGHT_GREEN = '\033[92m'
    LIGHT_BLUE = '\033[94m'
    LIGHT_GREY = '\033[97m'
    
    # Background colors
    BG_BLACK = '\033[40m'
    BG_WHITE = '\033[47m'
    BG_RED = '\033[41m'
    BG_CYAN = '\033[46m'
    BG_PURPLE = '\033[45m'
    BG_GREEN = '\033[42m'
    BG_BLUE = '\033[44m'
    BG_YELLOW = '\033[43m'
    BG_LIGHT_BLUE = '\033[104m'
    
    # Special formatting
    BOLD = '\033[1m'
    RESET = '\033[0m'
    CLEAR_SCREEN = '\033[2J'
    CLEAR_LINE = '\033[K'
    CURSOR_HOME = '\033[H'

class C64Basic:
    def __init__(self):
        self.variables: Dict[str, Union[int, float, str]] = {}
        self.lines: Dict[int, str] = {}
        self.current_line = 0
        self.program_counter = 0
        self.running = False
        self.for_loops: Dict[str, Dict] = {}
        self.gosub_stack: List[int] = []
        self.colors_enabled = self.check_color_support()
        
        # Built-in functions
        self.functions = {
            'ABS': abs,
            'SQR': math.sqrt,
            'SIN': math.sin,
            'COS': math.cos,
            'TAN': math.tan,
            'LOG': math.log,
            'EXP': math.exp,
            'INT': int,
            'RND': lambda: random.random(),
            'LEN': len,
            'CHR$': chr,
            'ASC': ord,
            'STR$': str,
            'VAL': float,
        }
        
        # System variables
        self.variables['TI'] = 0  # Timer
        self.variables['TI$'] = "000000"  # Timer as string
        
        # Color variables (C64-style)
        self.variables['CO'] = 0  # Color (foreground)
        self.variables['BG'] = 6  # Background color (blue)
        
    def check_color_support(self):
        """Check if terminal supports colors"""
        return (
            hasattr(sys.stdout, 'isatty') and 
            sys.stdout.isatty() and 
            'TERM' in os.environ and 
            os.environ['TERM'] != 'dumb'
        )
    
    def color_print(self, text: str, fg_color: str = C64Colors.WHITE, bg_color: str = C64Colors.BG_BLUE, bold: bool = False):
        """Print text with C64-style colors"""
        if self.colors_enabled:
            color_code = ""
            if bold:
                color_code += C64Colors.BOLD
            color_code += fg_color + bg_color + text + C64Colors.RESET
            print(color_code, end="")
        else:
            print(text, end="")
    
    def set_color(self, fg: int = 1, bg: int = 6):
        """Set C64-style colors (1=white, 6=blue, etc.)"""
        if not self.colors_enabled:
            return
            
        color_map = {
            0: (C64Colors.BLACK, C64Colors.BG_BLACK),
            1: (C64Colors.WHITE, C64Colors.BG_BLACK),
            2: (C64Colors.RED, C64Colors.BG_BLACK),
            3: (C64Colors.CYAN, C64Colors.BG_BLACK),
            4: (C64Colors.PURPLE, C64Colors.BG_BLACK),
            5: (C64Colors.GREEN, C64Colors.BG_BLACK),
            6: (C64Colors.BLUE, C64Colors.BG_BLACK),
            7: (C64Colors.YELLOW, C64Colors.BG_BLACK),
            8: (C64Colors.ORANGE, C64Colors.BG_BLACK),
            9: (C64Colors.BROWN, C64Colors.BG_BLACK),
            10: (C64Colors.LIGHT_RED, C64Colors.BG_BLACK),
            11: (C64Colors.DARK_GREY, C64Colors.BG_BLACK),
            12: (C64Colors.GREY, C64Colors.BG_BLACK),
            13: (C64Colors.LIGHT_GREEN, C64Colors.BG_BLACK),
            14: (C64Colors.LIGHT_BLUE, C64Colors.BG_BLACK),
            15: (C64Colors.LIGHT_GREY, C64Colors.BG_BLACK),
        }
        
        bg_map = {
            0: C64Colors.BG_BLACK,
            1: C64Colors.BG_WHITE,
            2: C64Colors.BG_RED,
            3: C64Colors.BG_CYAN,
            4: C64Colors.BG_PURPLE,
            5: C64Colors.BG_GREEN,
            6: C64Colors.BG_BLUE,
            7: C64Colors.BG_YELLOW,
            8: C64Colors.BG_YELLOW,
            9: C64Colors.BG_YELLOW,
            10: C64Colors.BG_RED,
            11: C64Colors.BG_BLACK,
            12: C64Colors.BG_WHITE,
            13: C64Colors.BG_GREEN,
            14: C64Colors.BG_LIGHT_BLUE,
            15: C64Colors.BG_WHITE,
        }
        
        fg_color, _ = color_map.get(fg, (C64Colors.WHITE, C64Colors.BG_BLACK))
        bg_color = bg_map.get(bg, C64Colors.BG_BLUE)
        
        # Set terminal colors
        sys.stdout.write(fg_color + bg_color)
        sys.stdout.flush()
        
    def print_banner(self):
        """Display the classic C64 startup banner with colors"""
        if self.colors_enabled:
            # Clear screen and set C64 colors
            print(C64Colors.CLEAR_SCREEN, end="")
            self.set_color(1, 6)  # White text on blue background
            print(C64Colors.CURSOR_HOME, end="")
        
        self.color_print("    **** COMMODORE 64 BASIC V2 ****\n", C64Colors.WHITE, C64Colors.BG_BLUE, True)
        self.color_print(" 64K RAM SYSTEM  38911 BASIC BYTES FREE\n", C64Colors.WHITE, C64Colors.BG_BLUE)
        self.color_print("\n", C64Colors.WHITE, C64Colors.BG_BLUE)
        self.color_print("READY.\n", C64Colors.WHITE, C64Colors.BG_BLUE, True)
        self.color_print("\n", C64Colors.WHITE, C64Colors.BG_BLUE)
        
        if self.colors_enabled:
            # Reset colors for input
            print(C64Colors.RESET, end="")
    
    def print_ready(self):
        """Print READY prompt with C64 colors"""
        self.color_print("READY.\n", C64Colors.WHITE, C64Colors.BG_BLUE, True)
    
    def print_error(self, message: str):
        """Print error message in C64 style"""
        self.color_print(f"?{message}\n", C64Colors.RED, C64Colors.BG_BLUE, True)
    
    def print_break(self, line_num: int):
        """Print BREAK message in C64 style"""
        self.color_print(f"\nBREAK IN LINE {line_num}\n", C64Colors.RED, C64Colors.BG_BLUE, True)
        self.print_ready()
    
    def clear_screen(self):
        """Clear screen with C64 colors"""
        if self.colors_enabled:
            print(C64Colors.CLEAR_SCREEN, end="")
            self.set_color(1, 6)  # White text on blue background
            print(C64Colors.CURSOR_HOME, end="")
        else:
            print("\n" * 50)
    
    def handle_color(self, args: str):
        """Handle COLOR command (C64-style)"""
        try:
            if ',' in args:
                # COLOR fg,bg
                parts = args.split(',')
                fg_color = int(self.evaluate_expression(parts[0].strip()))
                bg_color = int(self.evaluate_expression(parts[1].strip()))
                self.variables['CO'] = fg_color
                self.variables['BG'] = bg_color
            else:
                # COLOR fg
                fg_color = int(self.evaluate_expression(args))
                self.variables['CO'] = fg_color
                bg_color = self.variables.get('BG', 6)
            
            self.set_color(fg_color, bg_color)
        except:
            self.print_error("SYNTAX ERROR")
    
    def handle_load(self, args: str):
        """Handle LOAD command"""
        try:
            # Remove quotes if present
            filename = args.strip().strip('"')
            if not filename:
                self.print_error("MISSING FILENAME")
                return
            
            # Add .bas extension if not present
            if not filename.lower().endswith('.bas'):
                filename += '.bas'
            
            try:
                with open(filename, 'r') as f:
                    # Clear current program
                    self.lines.clear()
                    
                    # Load program lines
                    for line in f:
                        line = line.strip()
                        if line:
                            line_num, command = self.parse_line(line)
                            if line_num is not None and command:
                                self.lines[line_num] = command
                    
                    self.color_print(f"LOADING \"{filename}\"\n", C64Colors.WHITE, C64Colors.BG_BLUE)
                    self.color_print("READY.\n", C64Colors.WHITE, C64Colors.BG_BLUE, True)
                    
            except FileNotFoundError:
                self.print_error(f"FILE NOT FOUND: {filename}")
            except Exception as e:
                self.print_error(f"LOAD ERROR: {str(e)}")
                
        except Exception as e:
            self.print_error(f"SYNTAX ERROR: {str(e)}")
    
    def handle_save(self, args: str):
        """Handle SAVE command"""
        try:
            # Remove quotes if present
            filename = args.strip().strip('"')
            if not filename:
                self.print_error("MISSING FILENAME")
                return
            
            # Add .bas extension if not present
            if not filename.lower().endswith('.bas'):
                filename += '.bas'
            
            try:
                with open(filename, 'w') as f:
                    # Save program lines in order
                    for line_num in sorted(self.lines.keys()):
                        f.write(f"{line_num} {self.lines[line_num]}\n")
                    
                    self.color_print(f"SAVING \"{filename}\"\n", C64Colors.WHITE, C64Colors.BG_BLUE)
                    self.color_print("READY.\n", C64Colors.WHITE, C64Colors.BG_BLUE, True)
                    
            except Exception as e:
                self.print_error(f"SAVE ERROR: {str(e)}")
                
        except Exception as e:
            self.print_error(f"SYNTAX ERROR: {str(e)}")
    
    def evaluate_expression(self, expr: str) -> Union[int, float, str]:
        """Evaluate a mathematical or string expression"""
        expr = expr.strip()
        
        # Handle string literals
        if expr.startswith('"') and expr.endswith('"'):
            return expr[1:-1]
        
        # Handle variables
        if expr.isalpha() or (expr[0].isalpha() and all(c.isalnum() or c == '$' for c in expr[1:])):
            if expr in self.variables:
                return self.variables[expr]
            else:
                # Return 0 for numeric variables, "" for string variables
                return 0 if not expr.endswith('$') else ""
        
        # Handle function calls
        func_match = re.match(r'(\w+)\s*\((.*)\)', expr)
        if func_match:
            func_name = func_match.group(1).upper()
            args_str = func_match.group(2)
            
            if func_name in self.functions:
                # Parse arguments
                args = []
                paren_count = 0
                current_arg = ""
                
                for char in args_str:
                    if char == '(':
                        paren_count += 1
                    elif char == ')':
                        paren_count -= 1
                    elif char == ',' and paren_count == 0:
                        args.append(current_arg.strip())
                        current_arg = ""
                        continue
                    current_arg += char
                
                if current_arg:
                    args.append(current_arg.strip())
                
                # Evaluate arguments
                evaluated_args = []
                for arg in args:
                    if arg:
                        evaluated_args.append(self.evaluate_expression(arg))
                
                # Call function
                if func_name == 'RND':
                    return self.functions[func_name]()
                elif func_name in ['CHR$', 'STR$']:
                    return self.functions[func_name](evaluated_args[0])
                elif func_name == 'ASC':
                    return self.functions[func_name](evaluated_args[0])
                elif func_name == 'LEN':
                    return self.functions[func_name](str(evaluated_args[0]))
                else:
                    return self.functions[func_name](*evaluated_args)
        
        # Handle basic arithmetic
        try:
            # Replace variables with their values
            for var_name, var_value in self.variables.items():
                if isinstance(var_value, str):
                    expr = expr.replace(var_name, f'"{var_value}"')
                else:
                    expr = expr.replace(var_name, str(var_value))
            
            # Handle string concatenation
            if '+' in expr and '"' in expr:
                parts = expr.split('+')
                result = ""
                for part in parts:
                    part = part.strip()
                    if part.startswith('"') and part.endswith('"'):
                        result += part[1:-1]
                    else:
                        result += str(self.evaluate_expression(part))
                return result
            
            # Evaluate numeric expression
            result = eval(expr)
            return int(result) if result == int(result) else result
            
        except:
            return 0
    
    def parse_line(self, line: str) -> tuple:
        """Parse a BASIC line into line number and command"""
        line = line.strip()
        if not line:
            return None, ""
        
        # Check for line number
        parts = line.split(' ', 1)
        if parts[0].isdigit():
            line_num = int(parts[0])
            command = parts[1] if len(parts) > 1 else ""
            return line_num, command
        else:
            return None, line
    
    def execute_command(self, command: str):
        """Execute a BASIC command"""
        original_command = command.strip()
        command = original_command.upper()
        
        if not command:
            return
        
        # PRINT command
        if command.startswith('PRINT'):
            self.handle_print(original_command[5:].strip())
        
        # INPUT command
        elif command.startswith('INPUT'):
            self.handle_input(original_command[5:].strip())
        
        # LET command (variable assignment)
        elif '=' in command:
            self.handle_assignment(original_command)
        
        # IF-THEN command
        elif command.startswith('IF'):
            self.handle_if_then(original_command)
        
        # FOR command
        elif command.startswith('FOR'):
            self.handle_for(original_command)
        
        # NEXT command
        elif command.startswith('NEXT'):
            self.handle_next(original_command[4:].strip())
        
        # GOTO command
        elif command.startswith('GOTO'):
            target = int(self.evaluate_expression(original_command[4:].strip()))
            self.program_counter = target
            return
        
        # GOSUB command
        elif command.startswith('GOSUB'):
            target = int(self.evaluate_expression(original_command[5:].strip()))
            self.gosub_stack.append(self.program_counter)
            self.program_counter = target
            return
        
        # RETURN command
        elif command == 'RETURN':
            if self.gosub_stack:
                self.program_counter = self.gosub_stack.pop()
            return
        
        # REM command (comment)
        elif command.startswith('REM'):
            return
        
        # CLS command (clear screen)
        elif command == 'CLS':
            self.clear_screen()
        
        # LIST command
        elif command.startswith('LIST'):
            self.list_program()
        
        # RUN command
        elif command == 'RUN':
            self.run_program()
        
        # NEW command
        elif command == 'NEW':
            self.lines.clear()
            self.variables.clear()
            self.program_counter = 0
            self.print_ready()
        
        # END command
        elif command == 'END':
            self.running = False
        
        # WAIT command (simple delay)
        elif command.startswith('WAIT'):
            try:
                delay = float(self.evaluate_expression(original_command[4:].strip()))
                time.sleep(delay)
            except:
                pass
        
        # POKE command (simulated)
        elif command.startswith('POKE'):
            self.color_print("POKE: Memory location simulated\n", C64Colors.RED, C64Colors.BG_BLUE, True)
        
        # PEEK command (simulated)
        elif command.startswith('PEEK'):
            self.color_print("PEEK: Memory location simulated\n", C64Colors.RED, C64Colors.BG_BLUE, True)
        
        # SYS command (simulated)
        elif command.startswith('SYS'):
            self.color_print("SYS: Machine language call simulated\n", C64Colors.RED, C64Colors.BG_BLUE, True)
        
        # LOAD command
        elif command.startswith('LOAD'):
            self.handle_load(original_command[4:].strip())
        
        # SAVE command
        elif command.startswith('SAVE'):
            self.handle_save(original_command[4:].strip())
        
        # COLOR command (C64-style)
        elif command.startswith('COLOR'):
            self.handle_color(original_command[5:].strip())
        
        # SCREEN command (set background color)
        elif command.startswith('SCREEN'):
            try:
                bg_color = int(self.evaluate_expression(original_command[6:].strip()))
                self.variables['BG'] = bg_color
                self.set_color(self.variables.get('CO', 1), bg_color)
            except:
                self.print_error("SYNTAX ERROR")
        
        else:
            self.print_error(f"SYNTAX ERROR IN {self.current_line}")
    
    def handle_print(self, args: str):
        """Handle PRINT command"""
        if not args:
            self.color_print("\n", C64Colors.WHITE, C64Colors.BG_BLUE)
            return
        
        # Check if the PRINT statement ends with a semicolon
        ends_with_semicolon = args.strip().endswith(';')
        
        # Handle multiple expressions separated by semicolons or commas
        parts = []
        current_part = ""
        in_string = False
        paren_count = 0
        
        for char in args:
            if char == '"':
                in_string = not in_string
                current_part += char
            elif char == '(':
                paren_count += 1
                current_part += char
            elif char == ')':
                paren_count -= 1
                current_part += char
            elif char in [';', ','] and not in_string and paren_count == 0:
                parts.append(current_part.strip())
                parts.append(char)
                current_part = ""
            else:
                current_part += char
        
        if current_part:
            parts.append(current_part.strip())
        
        # Process parts
        output = ""
        for part in parts:
            if part == ';':
                # No separator
                pass
            elif part == ',':
                # Tab separator
                output += " " * (16 - (len(output) % 16))
            else:
                result = self.evaluate_expression(part)
                output += str(result)
        
        # Add newline unless the statement ends with a semicolon
        if not ends_with_semicolon:
            output += "\n"
        
        self.color_print(output, C64Colors.WHITE, C64Colors.BG_BLUE)
    
    def handle_input(self, args: str):
        """Handle INPUT command"""
        prompt = ""
        if args.startswith('"'):
            end_quote = args.find('"', 1)
            if end_quote != -1:
                prompt = args[1:end_quote]
                args = args[end_quote + 1:].strip()
        
        if prompt:
            print(prompt, end="")
        else:
            print("? ", end="")
        
        try:
            user_input = input()
            
            # Parse variable names
            var_names = [name.strip() for name in args.split(',')]
            
            if len(var_names) == 1:
                # Single variable
                var_name = var_names[0]
                if var_name.endswith('$'):
                    self.variables[var_name] = user_input
                else:
                    try:
                        self.variables[var_name] = float(user_input)
                    except:
                        self.variables[var_name] = 0
            else:
                # Multiple variables
                inputs = user_input.split(',')
                for i, var_name in enumerate(var_names):
                    if i < len(inputs):
                        if var_name.endswith('$'):
                            self.variables[var_name] = inputs[i].strip()
                        else:
                            try:
                                self.variables[var_name] = float(inputs[i].strip())
                            except:
                                self.variables[var_name] = 0
        except:
            self.print_error("REDO FROM START")
    
    def handle_assignment(self, command: str):
        """Handle variable assignment (LET command)"""
        if command.startswith('LET '):
            command = command[4:]
        
        if '=' in command:
            var_part, expr_part = command.split('=', 1)
            var_name = var_part.strip()
            expr = expr_part.strip()
            
            result = self.evaluate_expression(expr)
            self.variables[var_name] = result
    
    def handle_if_then(self, command: str):
        """Handle IF-THEN command"""
        # Extract condition and action
        if_part = command[2:].strip()
        
        # Find THEN
        then_index = if_part.find('THEN')
        if then_index == -1:
            self.print_error("SYNTAX ERROR")
            return
        
        condition = if_part[:then_index].strip()
        action = if_part[then_index + 4:].strip()
        
        # Evaluate condition
        try:
            # Replace operators with Python equivalents
            condition = condition.replace('=', '==')
            condition = condition.replace('<>', '!=')
            
            # Evaluate variables in condition
            for var_name, var_value in self.variables.items():
                if isinstance(var_value, str):
                    condition = condition.replace(var_name, f'"{var_value}"')
                else:
                    condition = condition.replace(var_name, str(var_value))
            
            if eval(condition):
                self.execute_command(action)
        except:
            self.print_error("SYNTAX ERROR")
    
    def handle_for(self, command: str):
        """Handle FOR command"""
        # FOR I=1 TO 10 STEP 1
        for_part = command[3:].strip()
        
        # Parse variable assignment
        if '=' not in for_part:
            self.print_error("SYNTAX ERROR")
            return
        
        var_part, rest = for_part.split('=', 1)
        var_name = var_part.strip()
        
        # Parse TO and STEP
        if ' TO ' not in rest:
            self.print_error("SYNTAX ERROR")
            return
        
        to_part, step_part = rest.split(' TO ', 1)
        start_value = self.evaluate_expression(to_part.strip())
        
        if ' STEP ' in step_part:
            step_expr, step_value = step_part.split(' STEP ', 1)
            end_value = self.evaluate_expression(step_expr.strip())
            step = self.evaluate_expression(step_value.strip())
        else:
            end_value = self.evaluate_expression(step_part.strip())
            step = 1
        
        # Store FOR loop info
        self.for_loops[var_name] = {
            'start': start_value,
            'end': end_value,
            'step': step,
            'current': start_value,
            'return_line': self.program_counter
        }
        
        # Set initial value
        self.variables[var_name] = start_value
    
    def handle_next(self, var_name: str):
        """Handle NEXT command"""
        if var_name not in self.for_loops:
            self.print_error(f"NEXT WITHOUT FOR ERROR")
            return
        
        loop = self.for_loops[var_name]
        loop['current'] += loop['step']
        self.variables[var_name] = loop['current']
        
        # Check if loop should continue
        if loop['step'] > 0:
            if loop['current'] <= loop['end']:
                self.program_counter = loop['return_line']
        else:
            if loop['current'] >= loop['end']:
                self.program_counter = loop['return_line']
        
        # Remove loop if finished
        if (loop['step'] > 0 and loop['current'] > loop['end']) or \
           (loop['step'] < 0 and loop['current'] < loop['end']):
            del self.for_loops[var_name]
    
    def list_program(self):
        """List the current program"""
        if not self.lines:
            self.print_ready()
            return
        
        for line_num in sorted(self.lines.keys()):
            self.color_print(f"{line_num} {self.lines[line_num]}\n", C64Colors.WHITE, C64Colors.BG_BLUE)
    
    def run_program(self):
        """Run the current program"""
        if not self.lines:
            self.print_ready()
            return
        
        self.running = True
        self.program_counter = min(self.lines.keys())
        
        while self.running and self.program_counter in self.lines:
            line_num = self.program_counter
            command = self.lines[line_num]
            
            # Find next line
            line_numbers = sorted(self.lines.keys())
            current_index = line_numbers.index(line_num)
            if current_index + 1 < len(line_numbers):
                self.program_counter = line_numbers[current_index + 1]
            else:
                self.program_counter = None
            
            self.execute_command(command)
            
            if self.program_counter is None:
                break
        
        self.print_ready()
    
    def add_line(self, line: str):
        """Add a line to the program"""
        line_num, command = self.parse_line(line)
        
        if line_num is not None:
            if command:
                self.lines[line_num] = command
            else:
                # Empty line - delete it
                if line_num in self.lines:
                    del self.lines[line_num]
        else:
            # Immediate mode
            self.execute_command(command)
    
    def run(self):
        """Main interpreter loop"""
        self.print_banner()
        
        while True:
            try:
                line = input()
                if line.upper() == 'BYE':
                    self.color_print("GOODBYE!\n", C64Colors.WHITE, C64Colors.BG_BLUE, True)
                    break
                
                self.add_line(line)
                
            except KeyboardInterrupt:
                self.print_break(self.program_counter or 0)
                self.print_ready()
            except EOFError:
                break
            except Exception as e:
                self.print_error(f"SYNTAX ERROR")

def main():
    """Main function to run the C64 BASIC interpreter"""
    interpreter = C64Basic()
    interpreter.run()

if __name__ == "__main__":
    main() 