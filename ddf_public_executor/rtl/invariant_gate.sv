module invariant_gate #(
  parameter int DATA_W = 128
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
  logic sticky_fault;
  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      sticky_fault <= 1'b0;
      valid_o <= 1'b0;
      data_o <= '0;
    end else begin
      if (valid_i && !invariant_ok_i)
        sticky_fault <= 1'b1;
      valid_o <= valid_i && invariant_ok_i && !sticky_fault;
      data_o <= (valid_i && invariant_ok_i && !sticky_fault) ? data_i : '0;
    end
  end
  assign fault_o = sticky_fault;
endmodule
