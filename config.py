import sys, copy
from distutils.extension import Extension
from distutils.util import get_platform


def get_openmoc_object_name():
  """Returns the name of the main openmoc shared library object"""

  # For Python 2.X.X
  if (sys.version_info[0] == 2):
    filename = '_openmoc.so'

  # For Python 3.X.X
  # NOTE: Python 3 distributions are not yet working with SWIG, but this
  # is a stub for the futuresmo
  elif (sys.version_info[0] == 3):
#    filename = '_openmoc.so'
    filename = '_openmoc.cpython-{version[0]}{version[1]}mu.so'
    filename = filename.format(version=sys.version_info)

  return filename


def get_shared_object_path():
  """Returns the name of the distutils build directory"""

  # For Python 2.X.X
  if (sys.version_info[0] == 2):
    directory = 'build/lib.{platform}-{version[0]}.{version[1]}'
    directory = directory.format(platform=get_platform(),
                                     version=sys.version_info)

    

  # For Python 3.X.X
  # NOTE: Python 3 distributions are not yet working with SWIG, but this is
  # a stub for the future
  elif (sys.version_info[0] == 3):
    directory = 'build/lib'

  return directory


def get_openmoc():
  """Returns the path and name of the main shared library object"""

  return get_shared_object_path() + '/' + get_openmoc_object_name()



class configuration:
  """User-defined build configuration options for OpenMOC

  Configuration options may be set using compile time flags. To view a
  list of these options, run 'python setup.py install --help' in the
  console. The default configuration options are shown below and should
  only be revised by developers familiar with the code and its configuration
  management system.
  """

  #############################################################################
  #                               User Options
  #############################################################################

  # Only supports GCC as the default compiler right now ??????
  # Default C++ compiler for the main openmoc module is GCC
  cc = 'gcc'

  # Default floating point for the main openmoc module is single precision
  fp = 'double'

  # Supported C++ compilers: 'gcc', 'icpc', 'bgxlc', 'nvcc', 'all'
  cpp_compilers = []

  # Supported floating point precision levels: 'single', 'double', 'all'
  fp_precision = []

  # Compile using ccache (for developers needing fast recompilation)
  with_ccache = False

  # Compile code with debug symbols (ie, -g)
  debug_mode = False

  # Build the openmoc.cuda and/or openmoc.cuda/single and/or openmoc.cuda.double
  # modules (depending on what precision levels are set for fp_precision)
  with_cuda = False

  # Compile with PAPI instrumentation
  with_papi = False

  # Compile with NumPy typemaps and the C API to allow users to pass NumPy
  # arrays to/from the C++ source code
  with_numpy = True

  # The vector length used for the VectorizedSolver class. This will used
  # as a hint for the Intel compiler to issue SIMD (ie, SSE, AVX, etc) vector
  # instructions. This is accomplished by adding "dummy" energy groups such
  # that the number of energy groups is be fit too a multiple of this
  # vector_length, and restructuring the innermost loops in the solver to
  # loop from 0 to the vector length
  vector_length = 8

  # The vector alignment used in the VectorizedSolver class when allocating
  # aligned data structures using MM_MALLOC and MM_FREE
  vector_alignment = 16

  # List of C/C++/CUDA distutils.extension objects which are created based
  # on which flags are specified at compile time.
  extensions = []

  # List of the packages to install - only openmoc is guaranteed to be built
  # while the others will be built based on which flags are specified
  # at compile time
  packages = ['openmoc', 'openmoc.compatible', 'openmoc.intel', 'openmoc.gnu',
              'openmoc.bgq', 'openmoc.cuda', 'openmoc.intel.double',
              'openmoc.intel.single', 'openmoc.gnu.double',
              'openmoc.gnu.single', 'openmoc.bgq.single',
              'openmoc.bgq.double', 'openmoc.cuda.double',
              'openmoc.cuda.single']


  #############################################################################
  #                                 Source Code
  #############################################################################

  # Dictionary of source code files to compile for each extension module
  sources = {}

  sources['gcc'] = ['openmoc/openmoc_wrap.cpp',
                    'src/Cell.cpp',
                    'src/Geometry.cpp',
                    'src/LocalCoords.cpp',
                    'src/log.cpp',
                    'src/Material.cpp',
                    'src/Point.cpp',
                    'src/Quadrature.cpp',
                    'src/Solver.cpp',
                    'src/CPUSolver.cpp',
                    'src/ThreadPrivateSolver.cpp',
                    'src/Surface.cpp',
                    'src/Timer.cpp',
                    'src/Track.cpp',
                    'src/TrackGenerator.cpp',
                    'src/Universe.cpp',
                    'src/Cmfd.cpp',
                    'src/Mesh.cpp']

  sources['icpc'] = ['openmoc/openmoc_wrap.cpp',
                     'src/Cell.cpp',
                     'src/Geometry.cpp',
                     'src/LocalCoords.cpp',
                     'src/log.cpp',
                     'src/Material.cpp',
                     'src/Point.cpp',
                     'src/Quadrature.cpp',
                     'src/Solver.cpp',
                     'src/CPUSolver.cpp',
                     'src/ThreadPrivateSolver.cpp',
                     'src/VectorizedSolver.cpp',
                     'src/VectorizedPrivateSolver.cpp',
                     'src/Surface.cpp',
                     'src/Timer.cpp',
                     'src/Track.cpp',
                     'src/TrackGenerator.cpp',
                     'src/Universe.cpp',
                     'src/Cmfd.cpp',
                     'src/Mesh.cpp']

  sources['bgxlc'] = ['openmoc/openmoc_wrap.cpp',
                      'src/Cell.cpp',
                      'src/Geometry.cpp',
                      'src/LocalCoords.cpp',
                      'src/log.cpp',
                      'src/Material.cpp',
                      'src/Point.cpp',
                      'src/Quadrature.cpp',
                      'src/Solver.cpp',
                      'src/CPUSolver.cpp',
                      'src/ThreadPrivateSolver.cpp',
                      'src/Surface.cpp',
                      'src/Timer.cpp',
                      'src/Track.cpp',
                      'src/TrackGenerator.cpp',
                      'src/Universe.cpp',
                      'src/Cmfd.cpp',
                      'src/Mesh.cpp']

  sources['nvcc'] = ['openmoc/cuda/openmoc_cuda_wrap.cpp',
                     'src/accel/cuda/GPUQuery.cu',
                     'src/accel/cuda/clone.cu',
                     'src/accel/cuda/GPUSolver.cu']


  #############################################################################
  #                                Compiler Flags
  #############################################################################

  # A dictionary of the compiler flags to use for each compiler type
  compiler_flags = {}

  compiler_flags['gcc'] = ['-c', '-O3', '-ffast-math', '-fopenmp',
                           '-std=c++0x', '-fpic']
  compiler_flags['icpc'] =['-c', '-O3', '-fast', '--ccache-skip', '-openmp',
                           '-xhost', '-std=c++0x', '-fpic', '--ccache-skip',
                             '-openmp-report', '-vec-report']
  compiler_flags['bgxlc'] = ['-c', '-O2', '-qarch=qp', '-qreport',
                             '-qsimd=auto', '-qtune=qp', '-qunroll=auto',
                             '-qsmp=omp', '-qpic']
  compiler_flags['nvcc'] =  ['-c', '-O3', '--compiler-options', '-fpic',
                             '-gencode=arch=compute_20,code=sm_20',
                             '-gencode=arch=compute_30,code=sm_30']


  #############################################################################
  #                                 Linker Flags
  #############################################################################

  # A dictionary of the linker flags to use for each compiler type
  linker_flags = {}

  if (get_platform()[:6] == 'macosx'):
    linker_flags['gcc'] = ['-fopenmp', '-dynamiclib', '-lpython2.7',
                           '-Wl,-install_name,' + get_openmoc_object_name()]
  else:
    linker_flags['gcc'] = ['-fopenmp', '-shared',
                           '-Wl,-soname,' + get_openmoc_object_name()]

  linker_flags['icpc'] = [ '-openmp', '-shared',
                           '-Xlinker', '-soname=' + get_openmoc_object_name()]
  linker_flags['bgxlc'] = ['-qmkshrobj', '-shared',
                           '-R/soft/compilers/ibmcmp-may2013/lib64/bg/bglib64',
                           '-Wl,-soname,' + get_openmoc_object_name()]
  linker_flags['nvcc'] = ['-shared', get_openmoc()]


  #############################################################################
  #                               Shared Libraries
  #############################################################################

  # A dictionary of the shared libraries to use for each compiler type
  shared_libraries = {}

  shared_libraries['gcc'] = ['stdc++', 'gomp', 'dl','pthread', 'm']
  shared_libraries['icpc'] = ['stdc++', 'iomp5', 'pthread', 'irc',
                              'imf','rt', 'mkl_rt','m',]
  shared_libraries['nvcc'] = ['cudart']
  shared_libraries['bgxlc'] = ['stdc++', 'pthread', 'm', 'xlsmp', 'rt']


  #############################################################################
  #                              Library Directories
  #############################################################################

  # A dictionary of the library directories to use for each compiler type
  # if not set in the LD_LIBRARY_PATH environment variable
  library_directories = {}

  if (get_platform()[:6] == 'macosx'):
    library_directories['gcc'] = [sys.exec_prefix + '/lib']
  else:
    library_directories['gcc'] = []

  library_directories['icpc'] = []
  library_directories['bgxlc'] = []
  library_directories['nvcc'] = ['/usr/local/cuda/lib64']


  #############################################################################
  #                              Include Directories
  #############################################################################

  # A dictionary of the include directories to use for each compiler type
  # for header files not found from paths set in the user's environment
  include_directories = {}

  if (get_platform()[:6] == 'macosx' and with_numpy):
    include_directories['gcc'] = [sys.exec_prefix + '/lib/python' + \
                                  str(sys.version_info[0]) + '.' + \
                                  str(sys.version_info[1]) + \
                                  '/site-packages/numpy/core/include']
  else:
    include_directories['gcc'] = []

  include_directories['icpc'] =[]
  include_directories['bgxlc'] = \
      ['/usr/lib64/python2.6/site-packages/numpy/core/include']
  include_directories['nvcc'] = ['/usr/local/cuda/include']


  ###########################################################################
  #                                 SWIG Flags
  ###########################################################################

  # A list of the flags for SWIG
  swig_flags = ['-c++', '-keyword', '-py3']


  #############################################################################
  #                                  Macros
  #############################################################################

  # A dictionary of the macros to set at compile time for each compiler type
  # and floating point precisin level
  macros = {}

  macros['gcc'] = {}
  macros['icpc'] = {}
  macros['bgxlc'] = {}
  macros['nvcc'] = {}

  macros['gcc']['single']= [('FP_PRECISION', 'float'),
                            ('SINGLE', None),
                            ('GNU', None),
                            ('VEC_LENGTH', vector_length),
                            ('VEC_ALIGNMENT', vector_alignment)]

  macros['icpc']['single']= [('FP_PRECISION', 'float'), 
                             ('SINGLE', None),
                             ('INTEL', None),
                             ('MKL_ILP64', None),
                             ('VEC_LENGTH', vector_length),
                             ('VEC_ALIGNMENT', vector_alignment)]
  
  macros['bgxlc']['single'] = [('FP_PRECISION', 'float'),
                               ('SINGLE', None),
                               ('BGXLC', None),
                               ('VEC_LENGTH', vector_length),
                               ('VEC_ALIGNMENT', vector_alignment),
                               ('CCACHE_CC', 'bgxlc++_r')]

  macros['nvcc']['single'] = [('FP_PRECISION', 'float'),
                              ('SINGLE', None),
                              ('CUDA', None),
                              ('CCACHE_CC', 'nvcc')]

  macros['gcc']['double'] = [('FP_PRECISION', 'double'),
                             ('DOUBLE', None),
                             ('GNU', None),
                             ('VEC_LENGTH', vector_length),
                             ('VEC_ALIGNMENT', vector_alignment)]

  macros['icpc']['double'] = [('FP_PRECISION', 'double'),
                              ('DOUBLE', None),
                              ('INTEL', None),
                              ('MKL_ILP64', None),
                              ('VEC_LENGTH', vector_length),
                              ('VEC_ALIGNMENT', vector_alignment)]

  macros['bgxlc']['double'] = [('FP_PRECISION', 'double'),
                               ('DOUBLE', None),
                               ('BGXLC', None),
                               ('VEC_LENGTH', vector_length),
                               ('VEC_ALIGNMENT', vector_alignment),
                               ('CCACHE_CC', 'bgxlc++_r')]

  macros['nvcc']['double'] = [('FP_PRECISION', 'double'),
                              ('DOUBLE', None),
                              ('CUDA', None),
                              ('CCACHE_CC', 'nvcc')]



  def setup_extension_modules(self):
    """Sets up the C/C++/CUDA extension modules for this distribution.

    Create list of extensions for Python modules within the openmoc
    Python package based on the user-defined flags defined at compile time.
    """

    # If the user selected 'all' compilers, enumerate them
    if self.cpp_compilers == ['all']:
      self.cpp_compilers = ['gcc', 'icpc', 'nvcc']

    # If the user selected 'all' FP precision levels, enumerate them
    if self.fp_precision == ['all']:
      self.fp_precision = ['double', 'single']

    # If the user wishes to compile using debug mode, append the debugging
    # flag to all lists of compiler flags for all distribution types
    if self.debug_mode:
      for k in self.compiler_flags:
        self.compiler_flags[k].append('-g')

    # If the user passed in the --no-numpy flag, tell SWIG not to embed
    # NumPy typemaps in the source code
    if not self.with_numpy:
      self.swig_flags += ['-DNO_NUMPY']

    # The main openmoc extension (defaults are gcc and single precision)
    self.extensions.append(
      Extension(name = '_openmoc',
                sources = copy.deepcopy(self.sources[self.cc]),
                library_dirs = self.library_directories[self.cc],
                libraries = self.shared_libraries[self.cc],
                extra_link_args = self.linker_flags[self.cc],
                include_dirs = self.include_directories[self.cc],
                define_macros = self.macros[self.cc][self.fp],
                swig_opts = self.swig_flags + ['-D' + self.cc.upper()]))

    # The openmoc.cuda extension if requested by the user at compile
    # time (--with-cuda)
    if self.with_cuda:

      self.cpp_compilers.append('nvcc')

      self.extensions.append(
        Extension(name = '_openmoc_cuda',
                  sources = copy.deepcopy(self.sources['nvcc']),
                  library_dirs = self.library_directories['nvcc'],
                  libraries = self.shared_libraries['nvcc'],
                  extra_link_args = self.linker_flags['nvcc'],
                  include_dirs = self.include_directories['nvcc'],
                  define_macros = self.macros['nvcc'][self.fp],
                  swig_opts = self.swig_flags  + ['-DNVCC'],
                  export_symbols = ['init_openmoc']))

      # Remove the main SWIG configuration file for builds of other
      # extensions (ie, openmoc.cuda.single, openmoc.cuda.double)
      self.sources['nvcc'].remove('openmoc/cuda/openmoc_cuda_wrap.cpp')

    # Loop over the compilers and floating point precision levels to create
    # extension modules for each (ie, openmoc.intel.double,
    # openmoc.cuda.single, etc)
    for fp in self.fp_precision:
      for cc in self.cpp_compilers:

        # Build the filename for the SWIG configuration file and the
        # extension name depending on the compiler and floating
        # point precision

        # For openmoc.cuda.* modules
        if cc == 'nvcc':
          ext_name = '_openmoc_cuda_' + fp
          swig_wrap_file = 'openmoc/cuda/' + fp
          swig_wrap_file += '/openmoc_cuda_' + fp + '_wrap.cpp'
          self.sources['nvcc'].append(swig_wrap_file)

        # For openmoc.gnu.* modules
        elif cc == 'gcc':
          ext_name = '_openmoc_gnu_' + fp
          swig_wrap_file = 'openmoc/gnu/' + fp
          swig_wrap_file += '/openmoc_gnu_' + fp + '_wrap.cpp'
          self.sources['gcc'].append(swig_wrap_file)

      # For openmoc.intel.* modules
        elif cc == 'icpc':
          ext_name = '_openmoc_intel_' + fp
          swig_wrap_file = 'openmoc/intel/' + fp
          swig_wrap_file += '/openmoc_intel_' + fp + '_wrap.cpp'
          self.sources['icpc'].append(swig_wrap_file)

        # For openmoc.intel.* modules
        elif cc == 'bgxlc':
          ext_name = '_openmoc_bgq_' + fp
          swig_wrap_file = 'openmoc/bgq/' + fp
          swig_wrap_file += '/openmoc_bgq_' + fp + '_wrap.cpp'
          self.sources['bgxlc'].append(swig_wrap_file)

        # If an unsupported compiler, throw error
        else:
          raise NameError('Compiler ' + str(cc) + ' is not supported')

        # Create the extension module and append it to the list of all
        # extension modules
        self.extensions.append(
          Extension(name = ext_name,
                    sources = copy.deepcopy(self.sources[cc]),
                    library_dirs = self.library_directories[cc],
                    libraries = self.shared_libraries[cc],
                    extra_link_args = self.linker_flags[cc],
                    include_dirs = self.include_directories[cc],
                    define_macros = self.macros[cc][fp],
                    swig_opts = self.swig_flags + ['-D' + cc.upper()]))

        # Clean up - remove the SWIG-generated wrap file from this
        # extension for the next extension
        self.sources[cc].remove(swig_wrap_file)
