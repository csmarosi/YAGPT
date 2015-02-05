#include <string>
#include <chrono>
#include <iostream>

using namespace std::chrono;

class Timer {
    const std::string s;
    system_clock::time_point start, finish;

    public:
    Timer(const std::string& s)
        : s(s)
        , start(system_clock::now())
    {}

    ~Timer() {
        finish = system_clock::now();
        nanoseconds ns = finish - start;
        std::cout << "Total time: "
            << ns.count() << " nanoseconds for " << s << std::endl;
    }
};

