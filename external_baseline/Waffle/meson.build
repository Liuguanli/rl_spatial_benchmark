project('Waffle', 'cpp', default_options: ['cpp_std=c++17', 'buildtype=debugoptimized'])

incdir = include_directories('include')
src = [
  'src/main.cpp',
  'src/Directory.cpp',
  'src/Node.cpp',
  'src/Page.cpp',
  'src/Waffle.cpp',
]

executable('Index', sources: src, include_directories: incdir)
