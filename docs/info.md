<!---

This file is used to generate your project datasheet. Please fill in the information below and delete any unused
sections.

You can also include images in this folder and reference them in the markdown. Each image must be less than
512 kb in size, and the combined size of all images must be less than 1 MB.
-->

## How it works

This is a 32-word by 8-bit RAM (256 bits) built entirely from flip-flops instead of an SRAM macro. It has a single port that can either read or write each clock, and it behaves like a small synchronous SRAM.

The input pins (data, address and write enable) are captured into registers on every clock edge first. On the following edge the RAM reads the word at the registered address into an output register, and if write enable was high it also replaces that word with the registered data. Read data therefore appears on `uo_out` two clocks after you set the address, and a write takes effect one clock after you present it.

Registering the inputs keeps the slow part of the design, the 5-bit address decode and the 32-to-1 read multiplexer, between flip-flops. That makes timing independent of how long signals take to arrive from the chip's pins.

A read and a write to the same address on the same clock returns the old value (read-before-write). The new value shows up on the next clock.

The memory contents are not reset, to save area. Only the output register resets to 0, so write a location before you read it.

| Pin | Function |
|---|---|
| `ui_in[7:0]` | write data |
| `uio_in[4:0]` | address (0 to 31) |
| `uio_in[5]` | write enable |
| `uo_out[7:0]` | read data |

## How to test

1. Hold `rst_n` low for a few clocks, then release it.
2. To write: put the data on `ui_in`, the address on `uio[4:0]`, and set `uio[5] = 1` for one clock.
3. To read: set `uio[5] = 0` and put the address on `uio[4:0]`. Two clock edges later the stored value appears on `uo_out`.
4. A simple check is to write each address with its own number (address 5 gets 5), then read them all back.

## External hardware

No extra parts are needed beyond the Tiny Tapeout demo board, but the board's DIP switches only reach `ui_in`. The control signals on the `uio` pins have to be driven another way:

- **Recommended:** drive and read every pin from the demo board's RP2040 using the Tiny Tapeout MicroPython SDK. A short script makes timing exact and repeatable.
- **By hand:** wire the `uio` pins to switches through the PMOD headers.

Read results from the RP2040 rather than the 7-segment display, since `uo_out` also drives the display segments and binary values light up as odd segment patterns.

Set up the data and address first, wait one clock, and only then assert the command or write enable. The board's signals are not synchronized to the chip's clock, so changing everything at once can let a clock edge capture a mix of old and new values.
