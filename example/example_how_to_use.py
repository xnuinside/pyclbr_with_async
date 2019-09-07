import pyclbr_with_async as pyclbr

# (c) Iuliia Volkova (xnunside@gmail.com)

# Example read module and generate test file with plot for this module

# path - adding path to sys.paths, so you can import python module from any folder - just add it to paths
# some_module - python module name
# tested with python 3.7

# you can change module to any yours, just to be sure, that it showed in python p
module_name = "some_module"
parsed_module = pyclbr.readmodule_ex(module_name, path=[""])

SP_4 = "    "
async_method_signature = "async def test_{method}(self):\n{SP_4}pass\n"
method_signature = "def test_{method}(self):\n{SP_4}pass\n"
class_method_signature = "\n{SP_4}def test_{method}(self):\n{SP_4}{SP_4}pass\n"
class_async_method_signature = "\n{SP_4}async def test_{method}(self):\n{SP_4}{SP_4}pass\n"
class_signature = "class Test{cls_name}:{SP_4}\n"

file_output = "import pytest\n"

async_in = False


def generate_tests(c):
    test_case = None
    if isinstance(c, pyclbr.Class):
        methods = c.methods.items()
        async_methods = c.async_methods.items()
        test_case = class_signature.format(SP_4=SP_4, cls_name=c.name)
        for method, lineno in methods:
            if method != '__init__':
                test_case += class_method_signature.format(SP_4=SP_4, method=method)
        for method, lineno in async_methods:
            if method != '__init__':
                test_case += class_async_method_signature.format(SP_4=SP_4, method=method)
    elif isinstance(c, pyclbr.Function):
        test_case = method_signature.format(SP_4=SP_4, method=c.name)
    elif isinstance(c, pyclbr.AsyncFunction):
        test_case = async_method_signature.format(SP_4=SP_4, method=c.name)
    return test_case


for k, v in parsed_module.items():
    file_output += "\n\n"
    file_output += generate_tests(v)
print(file_output)
