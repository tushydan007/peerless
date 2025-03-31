from functools import wraps

def call_counter(func):
    """Decorator that counts the number of times a function is called."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.call_count += 1
        print(f"Function '{func.__name__}' called {wrapper.call_count} times")
        return func(*args, **kwargs)
    
    wrapper.call_count = 0  # Initialize call count
    return wrapper

# Example usage
@call_counter
def say_hello():
    print("Hello!")

@call_counter
def add(a, b):
    return a + b

# Test the decorator
say_hello()
say_hello()
print(add(3, 5))
print(add(10, 20))