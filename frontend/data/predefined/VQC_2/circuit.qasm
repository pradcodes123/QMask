OPENQASM 2.0;
include "qelib1.inc";
qreg q[2];
creg c[1];

// change the angle percentages here to modify the alignminet of qubits towards y axis
ry(0*pi) q[0]; 
ry(1*pi) q[1];

cz q[1], q[0];
rz(0.12) q[0];
ry(-0.45) q[0];
rz(0.88) q[0];
rz(0.55) q[1];
ry(0.10) q[1];
rz(-0.33) q[1];
measure q[0] -> c[0];
