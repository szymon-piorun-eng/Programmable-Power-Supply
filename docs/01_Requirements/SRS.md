# System requirements specification

Requirements specified include:

1. **Use Cases** potential use cases for the product as a standalone device.

2. **Input Power Source Profile** definition of input voltage range and characteristics of input source.

3. **Output Power** definition on output power characteristics.

4. **User interface** definition of power setting by user.

5. **Safety & Protection Matrix** definition of possible faults, their level of danger, and implemented protection protocols.

## 1. Use cases

This versatile High-Performance Low-Voltage Power Controller manages a wide range of applications, including:

- **Precision Resistive Load Driver**
    Acts as a high-fidelity driver for various heating elements. The implemented Constant Power Mode ensures stable thermal output regardless of the element's resistance drift due to temperature coefficient (TCR). Applications include:
    - Portable **Hot Wire Cutter**
    - **High-Current Micro-Soldering Station**
    - Control system for **Thermal Actuators**
- **Diagnostic and Validation Tool**
    - Functions as **an Automated laboratory power supply**
    - Testing equipment for embedded systems and FPGA boards
    - Li-Ion battery simulator
    - Low-frequency power waveform generator
- **General Power Delivery**
    - Powering high-current LED arrays and lighting modules
    - Driving small DC motors or actuators under controlled current/voltage limits

## 2. Input power source profile

Input source of this device is **12V barrel jack power supply**.

{{ render_req_table('input_power') }}

## 3. Output power 

{{ render_req_table('output_power') }}

## 4. User interface

{{ render_req_table('user_interface') }}
