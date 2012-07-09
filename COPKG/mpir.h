// Stub include header to auto-include the correct version 
//  of opensslconf.h for the target architecture.

#if defined(_MSC_VER) 
#  if defined(_M_IA64) || defined(_M_X64) || defined(_WIN64)
#include <mpir_x64.h>
#  else 
#include <mpir_x86.h>
#  endif 
#elif defined(__GNUG__) 
#  if defined(__x86_64__) || defined(__ia64__) 
#include <mpir_x64.h>
#  else 
#include <mpir_x86.h>
#  endif 
#elif defined(_x64) || defined(x64)
#include <mpir_x64.h>
#else
#include <mpir_x86.h>
#endif 
