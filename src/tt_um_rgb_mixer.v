`default_nettype none

module tt_um_rgb_mixer (
    input  wire [7:0] ui_in,    // Dedicated inputs - connected to the input switches
    output wire [7:0] uo_out,   // Dedicated outputs - connected to the 7 segment display
    input  wire [7:0] uio_in,   // IOs: Bidirectional Input path
    output wire [7:0] uio_out,  // IOs: Bidirectional Output path
    output wire [7:0] uio_oe,   // IOs: Bidirectional Enable path (active high: 0=input, 1=output)
    input  wire       ena,      // will go high when the design is enabled
    input  wire       clk,      // clock
    input  wire       rst_n     // reset_n - low to reset
);

    wire reset = ! rst_n;
    assign uio_oe = 8'b0;
    assign uio_out = 8'b0;
    assign uo_out[7:3] = 5'b0;

    rgb_mixer rgb_mixer(
    .clk        (clk),
    .reset      (reset),
    .enc0_a     (ui_in[0]),
    .enc0_b     (ui_in[1]),
    .enc1_a     (ui_in[2]),
    .enc1_b     (ui_in[3]),
    .enc2_a     (ui_in[4]),
    .enc2_b     (ui_in[5]),
    .pwm0_out   (uo_out[0]),
    .pwm1_out   (uo_out[1]),
    .pwm2_out   (uo_out[2])
);

endmodule
