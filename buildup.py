from cx_Freeze import setup, Executable
 
buildOptions = dict(packages=['numpy','numpy.core.multiarray','numpy.lib.format' ,'cv2', 'pynput','time',
  'math', 'd3dshot', 'threading', 'tkinter'])

exe = [Executable('main.py', base = "Win32GUI")]
 
setup(
    name='testingName',
    version='0.0.1',
    author='me',
    description = 'description',
    options = dict(build_exe = buildOptions),
    executables = exe
)


# python buildup.py. build