import os
import importlib

def define_env(env):
    macros_dir = os.path.join(os.path.dirname(__file__), 'macros')
    
    for filename in os.listdir(macros_dir):
        if filename.endswith('.py') and filename != '__init__.py':
            module_name = filename[:-3]
            
            full_module_path = f"scripts.macros.{module_name}"
            module = importlib.import_module(full_module_path)
            
            if hasattr(module, module_name):
                func = getattr(module, module_name)
                env.macro(
                    lambda *args, f=func, **kwargs: f(env, *args, **kwargs), 
                    name=module_name
                )