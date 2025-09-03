<p align="center">
  English |
  <a href="README_CN.md">简体中文</a>
</p>

# Project Description

This project automatically generates Python APIs based on the CTP C++ API, making it easier for CTP Python developers to maintain the latest CTP interfaces and quickly upgrade CTP versions.

## 1. Compilation Environment

This project is compiled using the following environment. If you use other tool versions, please make appropriate adjustments.

- **Windows 11 + MSVC 2022**

- **Python 3.13.6** virtual environment, installed by uv.

- **CTP v6.7.11**: Official download address: https://www.simnow.com.cn/static/apiDownload.action

- **Meson + Ninja**: A modern C++ extension build system.

Meson: Similar to Make and CMake, its main task is to configure the compilation environment, generate compilation instructions (for example, for Ninja), and manage the entire compilation process. It does not directly compile code, but rather drives tools like Ninja to do so.

- **Pybind11**: Python C++ bindings

Pybind11: A lightweight C++ library for exposing (binding) C++ code to the Python interpreter. It allows Python code to seamlessly call C++ functions and classes, just like calling regular Python modules. Its core goal is to provide an extremely simple, nearly boilerplate-free interface that easily combines the high-performance computing capabilities of C++ with the ease of use and vast Python ecosystem.

- **uv**: A modern Python package manager with faster installation and smarter dependency resolution.

## 2. Install the Basic Environment (skip if already installed)

1. Install uv

On Windows

**Method 1: Global Installation (Recommended, choose one)**

```bash
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Method 2: Install in a Single Python Environment (Choose one)**

```bash
pip install uv
```

On Linux

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Install Python (Perform this step with Method 1, skip this with Method 2). I use 3.13.6; you can install your preferred version.

```bash
uv python install 3.13
```

## 3. Usage

1. Install a Python virtual environment and dependencies (execute from the root directory)

```bash
# Use uv to create a Python virtual environment with a specified version in the current project.

uv venv --python 3.13 .venv

```

```bash
# Install dependent libraries

uv add meson-python

uv add pybind11

uv add pybind11-stubgen

```

2. Execute the one-click build script in the `generator` directory (to generate Python bindings for the CTP C++ API)

```bash
# Activate the Python virtual environment and enter the generator.

.venv\Scripts\activate

cd ctp\api\generator
```

```bash
# Generate binding files with one click.

python generate_onekey.py
```

3. Execute the following build script in the root directory to generate the CTP C++ API and encapsulate it into a Python-callable interface.

```bash
# Compile the CTP Python API with one click.

python build.py
```

## 4. Script Function Details

The generator script is located in `ctp/api/generator/`

### 1. `generator_function_const.py`

- **Purpose**: **Generates basic function constant files**
- **Function**:
- Reads the CTP header files `ThostFtdcMdApi.h` and `ThostFtdcTraderApi.h.h`
- Parses the functions therein and generates `ctp_function_const.py` (function constant definitions)

### 2. `generate_data_type.py`

- **Purpose**: **Generates data type definition files**
- **Function**:
- Reads the CTP header file `ThostFtdcUserApiDataType.h`
- Parses the `#define` constant definitions and `typedef` type definitions therein
- Generates `ctp_function_const.py`

### 3. `generate_struct.py`

- **Purpose**: **Generates structure definition files**
- **Function**:
- Reads the CTP header file `ThostFtdcUserApiStruct.h`
- Relies on the type mappings in `ctp_typedef.py`
- Parses the C++ structure definition and generates the Python dictionary-formatted structure definition file `ctp_struct.py`

### 4. `generate_api_functions.py`

- **Purpose**: **Generates API function binding code**
- **Function**:
- Reads the CTP API header files (such as `ThostFtdcTraderApi.h` and `ThostFtdcMdApi.h`)
- Relies on the structure definitions in `ctp_struct.py`
- Generates a large number of C++ source code files for Python bindings

### 5. `generate_dll_entry.py`

- **Purpose**: **Generates the C++ DLL entry point code file**
- **Function**:
- Generates three files: `dllmain.cpp`, `stdafx.cpp`, and `stdafx.h`.

- **dllmain.cpp**: Contains the standard DLL entry point function, handling process and thread loading/unloading.
- **stdafx.cpp**: A simple precompiled header include file.
- **stdafx.h**: Contains the Windows API header files and common definitions.

### 6. `generate_cpp.py`

- **Purpose**: **Generates `cpp` and `h` files**
- **Function**: **Generates `ctpmd.cpp`, `ctpmd.h`, and `ctptd.cpp`, `ctptd.h`, for `ctp.api.src.ctpmd` and `ctp.api.src.ctptd`, respectively.
- The header file contains complete class declarations and function prototypes.
- The `cpp` file contains all implementation and bindings.

### 7. `generate_onekey.py`

- **Purpose**: **One-click assembles all md and td header, source, and other files to generate cpp and h files**
- **Function**:
- One-click assembles the files generated by the above files, as well as header, source, and other files, to generate four files: `ctpmd.cpp`, `ctpmd.h`, and `ctptd.cpp`, `ctptd.h`.

### 8. `build.py`

- **Purpose**: **One-click compiles the CTP C++ API into a Python API**
- **Function**:
- One-click compiles the Python-callable CTP API files, located in `ctp/api/`. These files include:
- `ctpmd.cp313-win_amd64.pyd`
- `ctptd.cp313-win_amd64.pyd`
- `ctpmd.pyi`
- `ctptd.pyi`

File Dependencies:

1. **`generator_function_const.py`** → Generate `ctp_function_const.py`
2. **`generate_data_type.py`** → Generate `ctp_typedef.py` and `ctp_constant.py`
3. **`generate_struct.py`** (depends on `ctp_typedef.py`) → Generate `ctp_struct.py`
4. **`generate_api_functions.py`** (depends on `ctp_struct.py` and `ctp_function_const.py`) → Generate multiple API header and source binding files for `md` and `td`
5. **`generate_dll_entry.py`** → Generate `dllmain.cpp`, `stdafx.cpp`, and `stdafx.h`
6. **`generate_cpp.py`** (depends on all the above files, as well as the generated header and source files) → Generates `ctpmd.cpp`, `ctpmd.h`, and `ctptd.cpp` and `ctptd.h`
7. **`generate_onekey.py`** → Assembles `ctpmd.cpp`, `ctpmd.h`, and `ctptd.cpp` and `ctptd.h` files with one click (equivalent to executing the above process with one click)
8. **`build.py`** (depends on the `ctpmd` and `ctptd` modules in `ctp/api/src/`) → Compiles `ctpmd.cp313-win_amd64.pyd`, `ctptd.cp313-win_amd64.pyd`, `ctpmd.pyi`, and `ctptd.pyi` with one click

## 5. Script Usage

The code generated by these scripts is used to:

- Encapsulate the CTP C++ API into a Python-callable interface
- Automatically handle data type conversion
- Generate Python bindings for callback functions
- Generate Python bindings for request functions

## 6. Advantages

- Use pybind to bind C++ to the Python CTP API, offering superior performance compared to SWIG conversion.
- Automatic synchronization: When the CTP official header files are updated, the latest h, dll, so, and lib files are replaced. After executing the generated script, the script will automatically reflect the latest virtual functions.
- Easy maintenance: No need to manually update a large number of hard-coded function declarations.
- Reduced errors: Avoid omissions or errors that may result from manual maintenance.
- Improved efficiency: Developers only need to focus on business logic, without worrying about changes to the underlying interfaces.

Summary: This is a complete code generation toolchain that automatically generates Python bindings for the CTP API, eliminating the need to manually write repetitive binding code and improving maintainability and robustness.

## 7. Community Support

- **Technical Exchange (QQ Group)**: `446042777`

## 8. Disclaimer

**[Disclaimer content](doc/Disclaimer.md)**