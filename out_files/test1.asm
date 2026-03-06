.data
str_nl: .asciz "\n"
.text
j Lmain
Lmain:
addi sp,sp,-52
addi gp,sp,0
L_2:
li t1,0
sw t1,-12(sp)
L_3:
li t1,1
sw t1,-16(sp)
L_4:
li t1,0
sw t1,-20(sp)
L_5:
lw t1,-20(sp)
li t2,10
ble t1,t2,L_7
L_6:
j L_15
L_7:
li a7,1
lw t0,-12(sp)
addi a0,t0,0
ecall
la a0,str_nl
li a7,4
ecall
L_8:
lw t1,-12(sp)
lw t2,-16(sp)
add t1,t1,t2
sw t1,-32(sp)
L_9:
lw t1,-32(sp)
sw t1,-24(sp)
L_10:
lw t1,-16(sp)
sw t1,-12(sp)
L_11:
lw t1,-24(sp)
sw t1,-16(sp)
L_12:
lw t1,-20(sp)
li t2,1
add t1,t1,t2
sw t1,-44(sp)
L_13:
lw t1,-44(sp)
sw t1,-20(sp)
L_14:
j L_5
L_15:
li t1,1
sw t1,-28(sp)
L_16:
li t1,1
sw t1,-20(sp)
L_17:
li a7,1
lw t0,-28(sp)
addi a0,t0,0
ecall
la a0,str_nl
li a7,4
ecall
L_18:
lw t1,-28(sp)
lw t2,-20(sp)
mul t1,t1,t2
sw t1,-48(sp)
L_19:
lw t1,-48(sp)
sw t1,-28(sp)
L_20:
lw t1,-20(sp)
li t2,1
add t1,t1,t2
sw t1,-52(sp)
L_21:
lw t1,-52(sp)
sw t1,-20(sp)
L_22:
lw t1,-20(sp)
li t2,7
bgt t1,t2,L_24
L_23:
j L_17
L_24:
li a7,10
ecall
la a0,str_nl
li a7,4
ecall
L_25:
lw ra,(sp)
jr ra
