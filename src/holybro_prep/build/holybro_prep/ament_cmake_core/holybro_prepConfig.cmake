# generated from ament/cmake/core/templates/nameConfig.cmake.in

# prevent multiple inclusion
if(_holybro_prep_CONFIG_INCLUDED)
  # ensure to keep the found flag the same
  if(NOT DEFINED holybro_prep_FOUND)
    # explicitly set it to FALSE, otherwise CMake will set it to TRUE
    set(holybro_prep_FOUND FALSE)
  elseif(NOT holybro_prep_FOUND)
    # use separate condition to avoid uninitialized variable warning
    set(holybro_prep_FOUND FALSE)
  endif()
  return()
endif()
set(_holybro_prep_CONFIG_INCLUDED TRUE)

# output package information
if(NOT holybro_prep_FIND_QUIETLY)
  message(STATUS "Found holybro_prep: 0.0.0 (${holybro_prep_DIR})")
endif()

# warn when using a deprecated package
if(NOT "" STREQUAL "")
  set(_msg "Package 'holybro_prep' is deprecated")
  # append custom deprecation text if available
  if(NOT "" STREQUAL "TRUE")
    set(_msg "${_msg} ()")
  endif()
  # optionally quiet the deprecation message
  if(NOT ${holybro_prep_DEPRECATED_QUIET})
    message(DEPRECATION "${_msg}")
  endif()
endif()

# flag package as ament-based to distinguish it after being find_package()-ed
set(holybro_prep_FOUND_AMENT_PACKAGE TRUE)

# include all config extra files
set(_extras "")
foreach(_extra ${_extras})
  include("${holybro_prep_DIR}/${_extra}")
endforeach()
