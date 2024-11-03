`default_nettype none

module cell_mux (
    input [3:0] page,
    input [5:0] in,
    output [7:0] out
);

wire [72:0] cc_out;

combined_cells cc_inst (
    .in(in),
    .out(cc_out)
);

assign out = cc_out[8*page +: 8];

endmodule

