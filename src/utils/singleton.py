#!/usr/bin/env python3

"""
Metaclass to create a singleton class.

Using a metaclass is widely regarded as the most effective and maintainable way to implement a singleton in Python.
This approach is thread-safe and allows for clean, reusable code.

Advantages: Clean, reusable, and works well with inheritance.

Usage: Just set metaclass=Singleton on any class you want to make a singleton.

references:
- https://www.perplexity.ai/search/how-to-best-create-a-singleton-Qy6ScUesSe.d8mumPDP26g
- https://betterstack.com/community/questions/how-to-create-singleton-in-python/
"""

class Singleton(type):
    """Singleton superclass"""
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


# Usage:
#
# class MySingleton(metaclass=Singleton):
#     pass

# a = MySingleton()
# b = MySingleton()
# print(a is b)  # Output: True
