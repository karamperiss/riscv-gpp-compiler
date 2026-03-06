.data
str_nl: .asciz "\n"
.text
j Lmain
Lmain:
addi sp,sp,-44
addi gp,sp,0
L_2:
li t1,1
sw t1,-12(sp)
L_3:
lw t1,-12(sp)
li t2,10
blt t1,t2,L_5
L_4:
j L_8
L_5:
lw t1,-12(sp)
li t2,1
add t1,t1,t2
sw t1,-20(sp)
L_6:
lw t1,-20(sp)
sw t1,-12(sp)
L_7:
j L_3
L_8:
li a7,1
lw t0,-12(sp)
addi a0,t0,0
ecall
la a0,str_nl
li a7,4
ecall
L_9:
lw t1,-12(sp)
sw t1,-16(sp)
L_10:
lw t1,-16(sp)
li t2,1
add t1,t1,t2
sw t1,-28(sp)
L_11:
lw t1,-28(sp)
sw t1,-16(sp)
L_12:
lw t1,-16(sp)
li t2,2
sub t1,t1,t2
sw t1,-32(sp)
L_13:
lw t1,-32(sp)
sw t1,-16(sp)
L_14:
lw t1,-16(sp)
li t2,0
beq t1,t2,L_16
L_15:
j L_10
L_16:
li a7,1
lw t0,-16(sp)
addi a0,t0,0
ecall
la a0,str_nl
li a7,4
ecall
L_17:
li t1,0
li t2,1
sub t1,t1,t2
sw t1,-36(sp)
L_18:
lw t1,-16(sp)
lw t2,-36(sp)
ble t1,t2,L_20
L_19:
j L_23
L_20:
li t1,0
li t2,1
sub t1,t1,t2
sw t1,-40(sp)
L_21:
lw t1,-40(sp)
sw t1,-12(sp)
L_22:
j L_25
L_23:
li t1,0
li t2,2
sub t1,t1,t2
sw t1,-44(sp)
L_24:
lw t1,-44(sp)
sw t1,-12(sp)
L_25:
li a7,1
lw t0,-12(sp)
addi a0,t0,0
ecall
la a0,str_nl
li a7,4
ecall
L_26:
lw t1,-12(sp)
lw t2,-16(sp)
blt t1,t2,L_28
L_27:
j L_30
L_28:
li t1,1
sw t1,-12(sp)
L_29:
j L_31
L_30:
li t1,2
sw t1,-12(sp)
L_31:
li a7,1
lw t0,-12(sp)
addi a0,t0,0
ecall
la a0,str_nl
li a7,4
ecall
L_32:
li a7,10
ecall
la a0,str_nl
li a7,4
ecall
L_33:
lw ra,(sp)
jr ra
