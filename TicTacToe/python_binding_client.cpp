#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "Server_client.h"


namespace py = pybind11;


PYBIND11_MODULE(gameServerClient, m) {
   py::class_<Client>(m, "Client")
        .def(py::init())
        .def(py::init<int>())
        .def("loop", &Client::loop)
        .def("init", &Client::init)
        .def("getHistory",&Client::getHistory)
        .def("sendMessageStr", &Client::sendMessageStr); 
}


// create module by running  
// g++ -O3 -Wall -shared -std=c++11 -fPIC `python3 -m pybind11 --includes` python_binding_client.cpp  Server_client.cpp -o gameServerClient`python3-config --extension-suffix`
