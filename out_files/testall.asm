.data
str_nl: .asciz "\n"
.text
j Lmain
syn:
sw ra,(sp)
L_2:
lw t1,-12(s0)
lw t0,-16(sp)
sw t1,(t0)
L_3:
lw t1,-16(s0)
lw t0,-8(sp)
sw t1,(t0)
L_4:
lw ra,(sp)
jr ra
Lmain:
addi sp,sp,-20
addi gp,sp,0
L_6:
li t1,2
sw t1,-12(sp)
L_7:
addi fp, sp,0
lw t1,-12(s0)
sw t1,-12(fp)
L_8:
addi t1,sp,-16
sw t1,-16(fp)
L_9:
addi t1,sp,-20
sw t1,-8(fp)
L_10:
sw sp,-4(fp)
addi sp,sp,0
jal syn
addi sp,sp,-0
L_11:
li a7,1
lw t0,-20(sp)
addi a0,t0,0
ecall
la a0,str_nl
li a7,4
ecall
L_12:
li a7,1
lw t0,-16(s0)
addi a0,t0,0
ecall
la a0,str_nl
li a7,4
ecall
L_13:
li a7,10
ecall
la a0,str_nl
li a7,4
ecall
L_14:
lw ra,(sp)
jr ra
