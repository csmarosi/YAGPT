#include <iostream>
#include <string>
#include "Timer.h"

int funner(int i) {
    return ++i;
}

int wathcme() {
    int w = 0; //Life sucks, break here
    w = funner(42);
    return w;
}

//Note: struct is a public class
struct Base {
    Base(): i(0)
    {}
    virtual ~Base()
    {}
    void inc() {
        i++;
        std::cout << "i=" << i << std::endl;
    }
    int i;
};

struct Derived1: Base {
    static Derived1* getInstance() {
        if (!instance)
            instance = new Derived1();
        return instance;
    }
    static Derived1* instance;
};
Derived1* Derived1::instance = NULL;

struct Derived2: Base {
    static Derived2* getInstance() {
        delete instance;
        instance = new Derived2();
        return instance;
    }
    static Derived2* instance;
};
Derived2* Derived2::instance = NULL;

void fun() {
    int j = 0;
    for(int i = 0; i<45123; ++i) {
        j = funner(j);
    }
    std::cout << "j=" << j << std::endl;
}

void doAction(const std::string& choiche) {
    if ("" == choiche) {
        std::cout << "What, you did not choose anything!" << std::endl;
        return;
    }
    Timer t("You choose: '" + choiche + "'.");
    if ("d1" == choiche)
        Derived1::getInstance()->inc();
    else if ("d2" == choiche)
        Derived2::getInstance()->inc();
    else if ("fun" == choiche)
        fun();
    else if ("w" == choiche)
        wathcme();
}


extern "C" void mainLoop() {
    std::string choiche, read;
    bool retval;
    do {
        retval = getline(std::cin, read);
        if (read.size() > 0)
            choiche = read;
        doAction(choiche);
    } while (retval);
}
