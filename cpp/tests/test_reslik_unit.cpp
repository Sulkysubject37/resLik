#include "reslik/reslik_unit.hpp"
#include <iostream>
#include <cassert>

int main() {
    std::cout << "Running basic C++ connectivity test..." << std::endl;
    
    // Test instantiation
    reslik::ResLikUnit unit(128);
    
    // Test forward pass (stub)
    std::vector<float> input(128, 1.0f);
    auto output = unit.forward(input);
    
    assert(output.size() == 128);
    
    std::cout << "C++ connectivity test passed." << std::endl;
    return 0;
}
