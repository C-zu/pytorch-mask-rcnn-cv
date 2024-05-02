import os
import torch
from setuptools import setup
from torch.utils.cpp_extension import BuildExtension, CUDAExtension

sources = ['src/crop_and_resize.c']
headers = ['src/crop_and_resize.h']
defines = []
with_cuda = False

extra_objects = []
extra_compile_args = ['-fopenmp', '-std=c99']

if torch.cuda.is_available():
    print('Including CUDA code.')
    sources += ['src/crop_and_resize_gpu.c']
    headers += ['src/crop_and_resize_gpu.h']
    defines += [('WITH_CUDA', None)]
    extra_objects += ['src/cuda/crop_and_resize_kernel.cu.o']
    with_cuda = True

this_file = os.path.dirname(os.path.realpath(__file__))
print(this_file)
sources = [os.path.join(this_file, fname) for fname in sources]
headers = [os.path.join(this_file, fname) for fname in headers]
extra_objects = [os.path.join(this_file, fname) for fname in extra_objects]

# Define the extension module
extension = CUDAExtension(
    name='_ext.crop_and_resize',
    sources=sources,
    include_dirs=[os.path.join(this_file, 'src')],
    define_macros=defines,
    extra_objects=extra_objects,
    extra_compile_args=extra_compile_args
)

# Setup the extension module using setup function
if __name__ == '__main__':
    setup(
        name='crop_and_resize',
        ext_modules=[extension],
        cmdclass={'build_ext': BuildExtension}
    )
