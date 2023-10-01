#include <dlfcn.h>
#include "my_application.h"

#define OABRemoteDesk_LIB_PATH "libOABRemoteDesk.so"
// #define OABRemoteDesk_LIB_PATH "/usr/lib/OABRemoteDesk/libOABRemoteDesk.so"
typedef bool (*OABRemoteDeskCoreMain)();
bool gIsConnectionManager = false;

bool flutter_OABRemoteDesk_core_main() {
   void* libOABRemoteDesk = dlopen(OABRemoteDesk_LIB_PATH, RTLD_LAZY);
   if (!libOABRemoteDesk) {
     fprintf(stderr,"load libOABRemoteDesk.so failed\n");
     return true;
   }
   auto core_main = (OABRemoteDeskCoreMain) dlsym(libOABRemoteDesk,"OABRemoteDesk_core_main");
   char* error;
   if ((error = dlerror()) != nullptr) {
       fprintf(stderr, "error finding OABRemoteDesk_core_main: %s", error);
       return true;
   }
   return core_main();
}

int main(int argc, char** argv) {
  if (!flutter_OABRemoteDesk_core_main()) {
      return 0;
  }
  for (int i = 0; i < argc; i++) {
    if (strcmp(argv[i], "--cm") == 0) {
      gIsConnectionManager = true;
    }
  }
  g_autoptr(MyApplication) app = my_application_new();
  return g_application_run(G_APPLICATION(app), argc, argv);
}
