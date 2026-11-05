/*
 * Copyright (c) 2026 Zachary Johnson
 * SPDX-License-Identifier: Apache-2.0
 *
 * DFF RAM: 32 words x 8 bits built entirely from flip-flops, with one
 * synchronous read/write port that behaves like a small SRAM macro.
 */

`default_nettype none

module tt_um_zjohnson2005_dffram (
    input  wire [7:0] ui_in,    // write data
    output wire [7:0] uo_out,   // registered read data
    input  wire [7:0] uio_in,   // [4:0] address, [5] write enable
    output wire [7:0] uio_out,
    output wire [7:0] uio_oe,
    input  wire       ena,
    input  wire       clk,
    input  wire       rst_n
);

    localparam DEPTH = 32;

    wire [7:0] write_data   = ui_in;
    wire [4:0] address      = uio_in[4:0];
    wire       write_enable = uio_in[5];

    reg [7:0] memory [0:DEPTH-1];
    reg [7:0] read_data;

    always @(posedge clk) begin
        if (write_enable) begin
            memory[address] <= write_data;
        end
    end

    always @(posedge clk) begin
        if (!rst_n) begin
            read_data <= 8'd0;
        end else begin
            read_data <= memory[address];
        end
    end

    assign uo_out  = read_data;
    assign uio_out = 8'd0;
    assign uio_oe  = 8'd0;

    wire _unused = &{ena, uio_in[7:6], 1'b0};

endmodule
