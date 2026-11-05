# SPDX-FileCopyrightText: © 2026 Zachary Johnson
# SPDX-License-Identifier: Apache-2.0

import random

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, FallingEdge, RisingEdge

DEPTH = 32


async def reset(dut):
    cocotb.start_soon(Clock(dut.clk, 10, unit="us").start())
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 5)
    dut.rst_n.value = 1
    await FallingEdge(dut.clk)


async def write(dut, address, value):
    dut.ui_in.value = value
    dut.uio_in.value = (1 << 5) | address
    await RisingEdge(dut.clk)
    await FallingEdge(dut.clk)
    dut.uio_in.value = address


async def read(dut, address):
    dut.uio_in.value = address
    await RisingEdge(dut.clk)
    await FallingEdge(dut.clk)
    return int(dut.uo_out.value)


@cocotb.test()
async def test_fill_and_read_back(dut):
    await reset(dut)
    assert int(dut.uio_oe.value) == 0
    assert int(dut.uo_out.value) == 0, "read data should reset to 0"
    pattern = [(a * 37 + 11) & 0xFF for a in range(DEPTH)]
    for address, value in enumerate(pattern):
        await write(dut, address, value)
    for address, value in enumerate(pattern):
        got = await read(dut, address)
        assert got == value, f"addr {address}: got {got:#x}, want {value:#x}"


@cocotb.test()
async def test_walking_bits(dut):
    await reset(dut)
    for bit in range(8):
        for address in range(DEPTH):
            await write(dut, address, (1 << bit) if address % 2 == 0 else (0xFF ^ (1 << bit)))
        for address in range(DEPTH):
            want = (1 << bit) if address % 2 == 0 else (0xFF ^ (1 << bit))
            assert await read(dut, address) == want


@cocotb.test()
async def test_read_returns_old_data_during_write(dut):
    await reset(dut)
    await write(dut, 7, 0x42)
    dut.ui_in.value = 0x99
    dut.uio_in.value = (1 << 5) | 7
    await RisingEdge(dut.clk)
    await FallingEdge(dut.clk)
    assert int(dut.uo_out.value) == 0x42, "a read during a write returns the old value"
    dut.uio_in.value = 7
    await RisingEdge(dut.clk)
    await FallingEdge(dut.clk)
    assert int(dut.uo_out.value) == 0x99


@cocotb.test()
async def test_random(dut):
    await reset(dut)
    rng = random.Random(2026)
    model = {}
    for address in range(DEPTH):
        model[address] = rng.randrange(256)
        await write(dut, address, model[address])
    for _ in range(400):
        address = rng.randrange(DEPTH)
        if rng.randrange(2):
            model[address] = rng.randrange(256)
            await write(dut, address, model[address])
        else:
            assert await read(dut, address) == model[address]
