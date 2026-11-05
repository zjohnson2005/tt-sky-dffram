<!---

This file is used to generate your project datasheet. Please fill in the information below and delete any unused
sections.

You can also include images in this folder and reference them in the markdown. Each image must be less than
512 kb in size, and the combined size of all images must be less than 1 MB.
-->

## How it works

This is a 32-word by 8-bit RAM (256 bits) built entirely from flip-flops instead of an SRAM macro. It has a single port that can either read or write each clock, and it behaves like a small synchronous SRAM.

On every rising clock edge the RAM reads the word at the current address into an output register, so read data appears on `uo_out` one clock after you set the address. If write enable is high, the word at that address is also replaced with `ui_in` on the same edge.

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
3. To read: set `uio[5] = 0` and put the address on `uio[4:0]`. After the next clock edge the stored value appears on `uo_out`.
4. A simple check is to write each address with its own number (address 5 gets 5), then read them all back.

## External hardware

None required. Switches on the inputs and LEDs on the outputs are enough to try it by hand.
