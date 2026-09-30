module ddf_node #(
  parameter int DATA_W = 128,
  parameter logic [DATA_W-1:0] XOR_MASK = '0
)(
  input logic clk,
  input logic rst_n,
  input logic valid_i,
  input logic [DATA_W-1:0] data_i,
  output logic valid_o,
  output logic [DATA_W-1:0] data_o
);
  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      valid_o <= 1'b0;
      data_o <= '0;
    end else begin
      valid_o <= valid_i;
      data_o <= data_i ^ XOR_MASK;
    end
  end
endmodule
