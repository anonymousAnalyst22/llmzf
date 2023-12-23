# LLMIF

LLMIF is an IoT protocol fuzzer guided by the specifciation-augmented large language model. Currently it supports fuzzing the Zigbee protocol. It is composed of two modules: Fuzzing controller and stack controller.

To use LLMIF, one should
* download IAR toolchains (for 8051 or for ARM) to compile the stack controller. Logics of the stack controller is in the file of ZMain.c.
* Load the compiled stack firmware on CC2530/CC2538 to build a Zigbee coordinator node for Zigbee communiaiton channel.
* Conenct your CC2530/CC2538 module to your PC/Raspberry Pi with USB. A USB-to-serial conveter may be needed.
* Run the fuzzing controller with python. The main.py is a good start to investigate.
