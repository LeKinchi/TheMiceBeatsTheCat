#include <iostream>

#include "Server.h"

int main() {
    Server temp;
    temp.init();
    temp.loop();
    temp.loop();
    return 0;
}
