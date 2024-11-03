`default_nettype none

module combined_cells (
    input [5:0] in,
    output [72:0] out
);

// constants
/////////////
(* keep *) sg13g2_tielo tielo_inst_notouch_(.L_LO(out[0]));
(* keep *) sg13g2_tiehi tiehi_inst_notouch_(.L_HI(out[1]));

// buffers & inverters
///////////////////////
(* keep *) sg13g2_buf_1 buf_1_inst_notouch_(.A(in[0]), .X(out[2]));
(* keep *) sg13g2_buf_2 buf_2_inst_notouch_(.A(in[0]), .X(out[3]));
(* keep *) sg13g2_buf_4 buf_4_inst_notouch_(.A(in[0]), .X(out[4]));
(* keep *) sg13g2_buf_8 buf_8_inst_notouch_(.A(in[0]), .X(out[5]));
(* keep *) sg13g2_buf_16 buf_16_inst_notouch_(.A(in[0]), .X(out[6]));
(* keep *) sg13g2_inv_1 inv_1_inst_notouch_(.A(in[0]), .Y(out[7]));
(* keep *) sg13g2_inv_2 inv_2_inst_notouch_(.A(in[0]), .Y(out[8]));
(* keep *) sg13g2_inv_4 inv_4_inst_notouch_(.A(in[0]), .Y(out[9]));
(* keep *) sg13g2_inv_8 inv_8_inst_notouch_(.A(in[0]), .Y(out[10]));
(* keep *) sg13g2_inv_16 inv_16_inst_notouch_(.A(in[0]), .Y(out[11]));

// and & nand variants
///////////////////////
(* keep *) sg13g2_and2_1 and2_1_inst_notouch_(.A(in[0]), .B(in[1]), .X(out[12]));
(* keep *) sg13g2_and2_2 and2_2_inst_notouch_(.A(in[0]), .B(in[1]), .X(out[13]));
(* keep *) sg13g2_and3_1 and3_1_inst_notouch_(.A(in[0]), .B(in[1]), .C(in[2]), .X(out[14]));
(* keep *) sg13g2_and3_2 and3_2_inst_notouch_(.A(in[0]), .B(in[1]), .C(in[2]), .X(out[15]));
(* keep *) sg13g2_and4_1 and4_1_inst_notouch_(.A(in[0]), .B(in[1]), .C(in[2]), .D(in[3]), .X(out[16]));
(* keep *) sg13g2_and4_2 and4_2_inst_notouch_(.A(in[0]), .B(in[1]), .C(in[2]), .D(in[3]), .X(out[17]));
(* keep *) sg13g2_nand2_1 nand2_1_inst_notouch_(.A(in[0]), .B(in[1]), .Y(out[18]));
(* keep *) sg13g2_nand2_2 nand2_2_inst_notouch_(.A(in[0]), .B(in[1]), .Y(out[19]));
(* keep *) sg13g2_nand2b_1 nand2b_1_inst_notouch_(.A_N(in[0]), .B(in[1]), .Y(out[20]));
(* keep *) sg13g2_nand2b_2 nand2b_2_inst_notouch_(.A_N(in[0]), .B(in[1]), .Y(out[21]));
(* keep *) sg13g2_nand3_1 nand3_1_inst_notouch_(.A(in[0]), .B(in[1]), .C(in[2]), .Y(out[22]));
(* keep *) sg13g2_nand3b_1 nand3b_1_inst_notouch_(.A_N(in[0]), .B(in[1]), .C(in[2]), .Y(out[23]));
(* keep *) sg13g2_nand4_1 nand4_1_inst_notouch_(.A(in[0]), .B(in[1]), .C(in[2]), .D(in[3]), .Y(out[24]));

// or & nor variants
/////////////////////
(* keep *) sg13g2_or2_1 or2_1_inst_notouch_(.A(in[0]), .B(in[1]), .X(out[25]));
(* keep *) sg13g2_or2_2 or2_2_inst_notouch_(.A(in[0]), .B(in[1]), .X(out[26]));
(* keep *) sg13g2_or3_1 or3_1_inst_notouch_(.A(in[0]), .B(in[1]), .C(in[2]), .X(out[27]));
(* keep *) sg13g2_or3_2 or3_2_inst_notouch_(.A(in[0]), .B(in[1]), .C(in[2]), .X(out[28]));
(* keep *) sg13g2_or4_1 or4_1_inst_notouch_(.A(in[0]), .B(in[1]), .C(in[2]), .D(in[3]), .X(out[29]));
(* keep *) sg13g2_or4_2 or4_2_inst_notouch_(.A(in[0]), .B(in[1]), .C(in[2]), .D(in[3]), .X(out[30]));
(* keep *) sg13g2_nor2_1 nor2_1_inst_notouch_(.A(in[0]), .B(in[1]), .Y(out[31]));
(* keep *) sg13g2_nor2_2 nor2_2_inst_notouch_(.A(in[0]), .B(in[1]), .Y(out[32]));
(* keep *) sg13g2_nor2b_1 nor2b_1_inst_notouch_(.A(in[0]), .B_N(in[1]), .Y(out[33]));
(* keep *) sg13g2_nor2b_2 nor2b_2_inst_notouch_(.A(in[0]), .B_N(in[1]), .Y(out[34]));
(* keep *) sg13g2_nor3_1 nor3_1_inst_notouch_(.A(in[0]), .B(in[1]), .C(in[2]), .Y(out[35]));
(* keep *) sg13g2_nor3_2 nor3_2_inst_notouch_(.A(in[0]), .B(in[1]), .C(in[2]), .Y(out[36]));
(* keep *) sg13g2_nor4_1 nor4_1_inst_notouch_(.A(in[0]), .B(in[1]), .C(in[2]), .D(in[3]), .Y(out[37]));
(* keep *) sg13g2_nor4_2 nor4_2_inst_notouch_(.A(in[0]), .B(in[1]), .C(in[2]), .D(in[3]), .Y(out[38]));

// xor & xnor variants
///////////////////////
(* keep *) sg13g2_xor2_1 xor2_1_inst_notouch_(.A(in[0]), .B(in[1]), .X(out[39]));
(* keep *) sg13g2_xnor2_1 xnor2_1_inst_notouch_(.A(in[0]), .B(in[1]), .Y(out[40]));

// and-into-or variants
////////////////////////
(* keep *) sg13g2_a21o_1 a21o_1_inst_notouch_(.A1(in[0]), .A2(in[1]), .B1(in[2]), .X(out[41]));
(* keep *) sg13g2_a21o_2 a21o_2_inst_notouch_(.A1(in[0]), .A2(in[1]), .B1(in[2]), .X(out[42]));
(* keep *) sg13g2_a21oi_1 a21oi_1_inst_notouch_(.A1(in[0]), .A2(in[1]), .B1(in[2]), .Y(out[43]));
(* keep *) sg13g2_a21oi_2 a21oi_2_inst_notouch_(.A1(in[0]), .A2(in[1]), .B1(in[2]), .Y(out[44]));
(* keep *) sg13g2_a22oi_1 a22oi_1_inst_notouch_(.A1(in[0]), .A2(in[1]), .B1(in[2]), .B2(in[3]), .Y(out[45]));
(* keep *) sg13g2_a221oi_1 a221oi_1_inst_notouch_(.A1(in[0]), .A2(in[1]), .B1(in[2]), .B2(in[3]), .C1(in[4]), .Y(out[46]));

// or-into-and variants
////////////////////////
(* keep *) sg13g2_o21ai_1 o21ai_1_inst_notouch_(.A1(in[0]), .A2(in[1]), .B1(in[2]), .Y(out[47]));

// other combinational cells (maj, mux, adder)
///////////////////////////////////////////////
(* keep *) sg13g2_mux2_1 mux2_1_inst_notouch_(.A0(in[0]), .A1(in[1]), .S(in[2]), .X(out[48]));
(* keep *) sg13g2_mux2_2 mux2_2_inst_notouch_(.A0(in[0]), .A1(in[1]), .S(in[2]), .X(out[49]));
(* keep *) sg13g2_mux4_1 mux4_1_inst_notouch_(.A0(in[0]), .A1(in[1]), .A2(in[2]), .A3(in[3]), .S0(in[4]), .S1(in[5]), .X(out[50]));

// latches
///////////
(* keep *) sg13g2_dlhq_1 dlhq_1_inst_notouch_(.D(in[0]), .GATE(in[1]), .Q(out[51]));
(* keep *) sg13g2_dlhrq_1 dlhrq_1_inst_notouch_(.D(in[0]), .GATE(in[1]), .RESET_B(in[2]), .Q(out[52]));
(* keep *) sg13g2_dlhr_1 dlhr_1_inst_notouch_(.D(in[0]), .GATE(in[1]), .RESET_B(in[2]), .Q(out[53]), .Q_N(out[54]));
(* keep *) sg13g2_dllrq_1 dllrq_1_inst_notouch_(.D(in[0]), .GATE_N(in[1]), .RESET_B(in[2]), .Q(out[55]));
(* keep *) sg13g2_dllr_1 dllr_1_inst_notouch_(.D(in[0]), .GATE_N(in[1]), .RESET_B(in[2]), .Q(out[56]), .Q_N(out[57]));

// flops
/////////
(* keep *) sg13g2_dfrbp_1 dfrbp_1_inst_notouch_(.CLK(in[0]), .D(in[1]), .RESET_B(in[2]), .Q(out[58]), .Q_N(out[59]));
(* keep *) sg13g2_dfrbp_2 dfrbp_2_inst_notouch_(.CLK(in[0]), .D(in[1]), .RESET_B(in[2]), .Q(out[60]), .Q_N(out[61]));

// flops with scan chain
/////////////////////////
(* keep *) sg13g2_sdfbbp_1 sdfbbp_1_inst_notouch_(.CLK(in[0]), .D(in[1]), .RESET_B(in[2]), .SET_B(in[3]), .SCD(in[4]), .SCE(in[5]), .Q(out[62]), .Q_N(out[63]));

// tri-state buffers
/////////////////////
tri [3:0] tri_;
(* keep *) sg13g2_ebufn_2 ebufn_2_inst1_notouch_(.A(in[0]), .TE_B(in[4:3]!=2'b00), .Z(tri_[0]));
(* keep *) sg13g2_ebufn_4 ebufn_4_inst1_notouch_(.A(in[1]), .TE_B(in[4:3]!=2'b01), .Z(tri_[0]));
(* keep *) sg13g2_ebufn_8 ebufn_8_inst1_notouch_(.A(in[2]), .TE_B(in[4:3]!=2'b10), .Z(tri_[0]));
(* keep *) sg13g2_einvn_2 einvn_2_inst1_notouch_(.A(in[0]), .TE_B(in[4:3]!=2'b00), .Z(tri_[1]));
(* keep *) sg13g2_einvn_4 einvn_4_inst1_notouch_(.A(in[1]), .TE_B(in[4:3]!=2'b01), .Z(tri_[1]));
(* keep *) sg13g2_einvn_8 einvn_8_inst1_notouch_(.A(in[2]), .TE_B(in[4:3]!=2'b10), .Z(tri_[1]));
(* keep *) sg13g2_ebufn_2 ebufn_2_inst2_notouch_(.A(in[0]), .TE_B(in[4:3]!=2'b00), .Z(tri_[2]));
(* keep *) sg13g2_ebufn_4 ebufn_4_inst2_notouch_(.A(in[1]), .TE_B(in[4:3]!=2'b01), .Z(tri_[2]));
(* keep *) sg13g2_ebufn_8 ebufn_8_inst2_notouch_(.A(in[2]), .TE_B(in[4:3]!=2'b10), .Z(tri_[2]));
(* keep *) sg13g2_sighold sighold_inst1_notouch_(.SH(tri_[2]));
(* keep *) sg13g2_einvn_2 einvn_2_inst2_notouch_(.A(in[0]), .TE_B(in[4:3]!=2'b00), .Z(tri_[3]));
(* keep *) sg13g2_einvn_4 einvn_4_inst2_notouch_(.A(in[1]), .TE_B(in[4:3]!=2'b01), .Z(tri_[3]));
(* keep *) sg13g2_einvn_8 einvn_8_inst2_notouch_(.A(in[2]), .TE_B(in[4:3]!=2'b10), .Z(tri_[3]));
(* keep *) sg13g2_sighold sighold_inst2_notouch_(.SH(tri_[3]));
assign out[64] = tri_[0];
assign out[65] = tri_[1];
assign out[66] = tri_[2];
assign out[67] = tri_[3];

// delay buffers
/////////////////
(* keep *) sg13g2_dlygate4sd1_1 dlygate4sd1_1_inst_notouch_(.A(in[0]), .X(out[68]));
(* keep *) sg13g2_dlygate4sd2_1 dlygate4sd2_1_inst_notouch_(.A(in[0]), .X(out[69]));
(* keep *) sg13g2_dlygate4sd3_1 dlygate4sd3_1_inst_notouch_(.A(in[0]), .X(out[70]));

// clock gating (latches for the clock tree)
/////////////////////////////////////////////
(* keep *) sg13g2_lgcp_1 lgcp_1_inst_notouch_(.CLK(in[0]), .GATE(in[1]), .GCLK(out[71]));
(* keep *) sg13g2_slgcp_1 slgcp_1_inst_notouch_(.CLK(in[0]), .GATE(in[1]), .SCE(in[2]), .GCLK(out[72]));

// fill cells
//////////////
//sg13g2_fill_1 fill_1_inst_notouch_();
//sg13g2_fill_2 fill_2_inst_notouch_();
//sg13g2_fill_4 fill_4_inst_notouch_();
//sg13g2_fill_8 fill_8_inst_notouch_();

// fill cells with decoupling capacitors
/////////////////////////////////////////
//sg13g2_decap_4 decap_4_inst_notouch_();
//sg13g2_decap_8 decap_8_inst_notouch_();

// antenna tie-down diode
//////////////////////////
//sg13g2_antennanp antennap_inst_notouch_(.A(in[0]));

endmodule

