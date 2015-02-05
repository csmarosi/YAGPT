#include <chrono>
#include <thread>

#include <dlfcn.h>

void lateMain() {
    std::this_thread::sleep_for(std::chrono::milliseconds(100));

    void *handle;
    handle = dlopen("./mainLoop.so", RTLD_NOW);

    typedef void (*mainLoop_t)();
    mainLoop_t mainLoop = (mainLoop_t) dlsym(handle, "mainLoop");
    mainLoop();

    dlclose(handle);
}

int main() {
    std::this_thread::sleep_for(std::chrono::milliseconds(1));
    lateMain();
    return 0;
}
