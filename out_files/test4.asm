.data
str_nl: .asciz "\n"
.text
j Lmain
Lmain:
addi sp,sp,-20
addi gp,sp,0
L_2:
li a7,5
ecall
addi t0,a0,0
sw t0,-12(sp)
L_3:
li a7,5
ecall
addi t0,a0,0
sw t0,-16(sp)
L_4:
li a7,5
ecall
addi t0,a0,0
sw t0,-20(sp)
L_5:
lw t1,-12(sp)
li t2,18
bge t1,t2,L_7
L_6:
j L_21
L_7:
lw t1,-12(sp)
li t2,65
ble t1,t2,L_9
L_8:
j L_21
L_9:
lw t1,-20(sp)
li t2,20000
bge t1,t2,L_11
L_10:
j L_13
L_11:
lw t1,-16(sp)
li t2,650
bge t1,t2,L_19
L_12:
j L_13
L_13:
lw t1,-20(sp)
li t2,50000
bge t1,t2,L_19
L_14:
j L_15
L_15:
lw t1,-16(sp)
li t2,700
bge t1,t2,L_17
L_16:
j L_21
L_17:
lw t1,-20(sp)
li t2,15000
bge t1,t2,L_19
L_18:
j L_21
L_19:
li a7,1
li t0,1
addi a0,t0,0
ecall
la a0,str_nl
li a7,4
ecall
L_20:
j L_22
L_21:
li a7,1
li t0,0
addi a0,t0,0
ecall
la a0,str_nl
li a7,4
ecall
L_22:
li a7,10
ecall
la a0,str_nl
li a7,4
ecall
L_23:
lw ra,(sp)
jr ra
