class Calculator:
    """A simple calculator class for testing PR reviews."""
    
    def add(self, a: int, b: int) -> int:
        """Add two numbers together."""
        return a + b
    
    def subtract(self, a: int, b: int) -> int:
        """Subtract b from a."""
        return a - b
    
    def multiply(self, a: int, b: int) -> int:
        """Multiply two numbers."""
        return a * b
    
    def divide(self, a: int, b: int) -> float:
        """Divide a by b."""
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b

# TODO: Add more complex operations like:
# - Square root
# - Power
# - Absolute value
# - Factorial

def main():
    calc = Calculator()
    # Example usage
    print(calc.add(5, 3))      # Should print: 8
    print(calc.subtract(5, 3))  # Should print: 2
    print(calc.multiply(5, 3))  # Should print: 15
    print(calc.divide(6, 2))    # Should print: 3.0

if __name__ == "__main__":
    main() 