#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "reslik/reslik_unit.hpp"

namespace py = pybind11;

PYBIND11_MODULE(_core, m) {
    m.doc() = "ResLik C++ Core";

    py::class_<reslik::ResLikUnit>(m, "ResLikUnit")
        .def(py::init<int>())
        .def("forward", &reslik::ResLikUnit::forward)
        .def("update_stats", &reslik::ResLikUnit::update_stats);
}
