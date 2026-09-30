module ddf_pipeline #(
  parameter int DATA_W = 128,
  parameter int STAGES = 6,
  parameter int STATE_BANKS = 4,
  parameter int INVARIANT_GATES = 2,
  parameter int MODE = 0
)(
  input logic clk,
  input logic rst_n,
  input logic valid_i,
  input logic [DATA_W-1:0] data_i,
  input logic invariant_ok_i,
  output logic valid_o,
  output logic [DATA_W-1:0] data_o,
  output logic fault_o
);
  logic [STAGES:0] v;
  logic [DATA_W-1:0] d [0:STAGES];
  assign v[0]=valid_i;
  assign d[0]=data_i;
  genvar i;
  generate
    for (i=0;i<STAGES;i=i+1) begin : g
      localparam logic [DATA_W-1:0] MASK =
        ({{(DATA_W-1){1'b0}},1'b1} << ((i+MODE) % DATA_W));
      ddf_node #(.DATA_W(DATA_W),.XOR_MASK(MASK)) n(
        .clk(clk),.rst_n(rst_n),.valid_i(v[i]),.data_i(d[i]),
        .valid_o(v[i+1]),.data_o(d[i+1])
      );
    end
  endgenerate
  invariant_gate #(.DATA_W(DATA_W)) gate(
    .clk(clk),.rst_n(rst_n),.valid_i(v[STAGES]),.data_i(d[STAGES]),
    .invariant_ok_i(invariant_ok_i),
    .valid_o(valid_o),.data_o(data_o),.fault_o(fault_o)
  );
endmodule
