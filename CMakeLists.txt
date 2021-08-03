project(clang-format-wheel)
cmake_minimum_required(VERSION 3.16)

# Define a build rule clang-format
include(ExternalProject)
ExternalProject_add(build-clang-format
  SOURCE_DIR ${CMAKE_SOURCE_DIR}/llvm-project/llvm
  BINARY_DIR ${CMAKE_BINARY_DIR}/llvm
  DOWNLOAD_COMMAND ""
  UPDATE_COMMAND ""
  INSTALL_COMMAND ""
  USES_TERMINAL_CONFIGURE 1
  USES_TERMINAL_BUILD 1
  CMAKE_ARGS -DBUILD_SHARED_LIBS=OFF -DLLVM_ENABLE_PROJECTS=clang
  BUILD_COMMAND ${CMAKE_COMMAND} --build . --target clang-format
)
set(clang-format-executable ${CMAKE_BINARY_DIR}/llvm/bin/clang-format)

# Reduce the size of the executable by executing strip if it is present on the system
find_program(STRIP_EXECUTABLE strip)
if(STRIP_EXECUTABLE)
  add_custom_target(
    strip-clang-format
    ALL
    COMMAND ${STRIP_EXECUTABLE} ${clang-format-executable}
    COMMENT "Stripping clang-format executable for size reduction"
  )
  add_dependencies(strip-clang-format build-clang-format)
endif()

# Define an installation rule that copies the executable to our Python package
install(
    PROGRAMS ${clang-format-executable}
    DESTINATION clang-format/data/bin
)
