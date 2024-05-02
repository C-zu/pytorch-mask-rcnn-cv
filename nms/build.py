import os
from setuptools import setup
from torch.utils.cpp_extension import BuildExtension, CUDAExtension

sources = ['src/nms.c']
headers = ['src/nms.h']
defines = []
with_cuda = False

if torch.cuda.is_available():
    print('Including CUDA code.')
    sources += ['src/nms_cuda.c']
    headers += ['src/nms_cuda.h']
    defines += [('WITH_CUDA', None)]
    with_cuda = True

this_file = os.path.dirname(os.path.realpath(__file__))
print(this_file)
extra_objects = ['src/cuda/nms_kernel.cu.o']
extra_objects = [os.path.join(this_file, fname) for fname in extra_objects]

# Define the CUDA extension module
extension = CUDAExtension(
    name='_ext.nms',
    sources=sources,
    include_dirs=[os.path.join(this_file, 'src')],
    define_macros=defines,
    extra_objects=extra_objects
)

# Setup the extension module
setup(
    name='nms',
    ext_modules=[extension],
    cmdclass={'build_ext': BuildExtension}
)
