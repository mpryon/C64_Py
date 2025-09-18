#!/usr/bin/env python3
"""
Test script for C64 BASIC interpreter
"""

import subprocess
import sys
import tempfile
import os

def test_basic_commands():
    """Test basic commands"""
    print("Testing C64 BASIC interpreter...")
    
    # Test commands
    test_commands = [
        'PRINT "HELLO, WORLD!"',
        'A = 5',
        'PRINT A',
        'B = 10',
        'PRINT "A + B = "; A + B',
        'C$ = "HELLO"',
        'D$ = "WORLD"',
        'PRINT C$ + " " + D$',
        'PRINT "LENGTH: "; LEN(C$)',
        'PRINT "RANDOM: "; INT(RND(1) * 100)',
        'PRINT "SQUARE ROOT OF 16: "; SQR(16)',
        'PRINT "ABS(-5): "; ABS(-5)',
        'BYE'
    ]
    
    # Create temporary input file
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        for cmd in test_commands:
            f.write(cmd + '\n')
        input_file = f.name
    
    try:
        # Run the interpreter with test input
        result = subprocess.run(
            [sys.executable, 'c64_basic.py'],
            input=open(input_file, 'r').read(),
            capture_output=True,
            text=True
        )
        
        print("Output:")
        print(result.stdout)
        
        if result.stderr:
            print("Errors:")
            print(result.stderr)
            
        return True
        
    except Exception as e:
        print(f"Error running test: {e}")
        return False
    finally:
        os.unlink(input_file)

def test_program_mode():
    """Test program mode with sample program"""
    print("\nTesting program mode...")
    
    # Sample program
    program_lines = [
        '10 PRINT "PROGRAM MODE TEST"',
        '20 A = 10',
        '30 B = 20',
        '40 PRINT "A = "; A',
        '50 PRINT "B = "; B',
        '60 PRINT "SUM = "; A + B',
        '70 FOR I = 1 TO 3',
        '80 PRINT I',
        '90 NEXT I',
        '100 END',
        'RUN',
        'BYE'
    ]
    
    # Create temporary input file
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        for line in program_lines:
            f.write(line + '\n')
        input_file = f.name
    
    try:
        # Run the interpreter with test input
        result = subprocess.run(
            [sys.executable, 'c64_basic.py'],
            input=open(input_file, 'r').read(),
            capture_output=True,
            text=True
        )
        
        print("Program mode output:")
        print(result.stdout)
        
        if result.stderr:
            print("Errors:")
            print(result.stderr)
            
        return True
        
    except Exception as e:
        print(f"Error running program mode test: {e}")
        return False
    finally:
        os.unlink(input_file)

if __name__ == "__main__":
    print("C64 BASIC Interpreter Test Suite")
    print("=" * 40)
    
    # Test basic commands
    if test_basic_commands():
        print("✓ Basic commands test passed")
    else:
        print("✗ Basic commands test failed")
    
    # Test program mode
    if test_program_mode():
        print("✓ Program mode test passed")
    else:
        print("✗ Program mode test failed")
    
    print("\nTest complete!")
    print("\nTo run the interpreter manually:")
    print("python3 c64_basic.py") 