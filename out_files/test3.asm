.data
str_nl: .asciz "\n"
.text
j Lmain
Lmain:
addi sp,sp,-76
addi gp,sp,0
L_2:
li a7,5
ecall
addi t0,a0,0
sw t0,-12(sp)
L_3:
lw t1,-12(sp)
li t2,10000
ble t1,t2,L_5
L_4:
j L_7
L_5:
li t1,0
sw t1,-16(sp)
L_6:
j L_31
L_7:
lw t1,-12(sp)
li t2,30000
ble t1,t2,L_9
L_8:
j L_13
L_9:
lw t1,-12(sp)
li t2,10000
sub t1,t1,t2
sw t1,-20(sp)
L_10:
lw t1,-20(sp)
li t2,10
div t1,t1,t2
sw t1,-24(sp)
L_11:
lw t1,-24(sp)
sw t1,-16(sp)
L_12:
j L_31
L_13:
lw t1,-12(sp)
li t2,70000
ble t1,t2,L_15
L_14:
j L_22
L_15:
li t1,30000
li t2,10000
sub t1,t1,t2
sw t1,-28(sp)
L_16:
lw t1,-28(sp)
li t2,10
div t1,t1,t2
sw t1,-32(sp)
L_17:
lw t1,-12(sp)
li t2,30000
sub t1,t1,t2
sw t1,-36(sp)
L_18:
lw t1,-36(sp)
li t2,5
div t1,t1,t2
sw t1,-40(sp)
L_19:
lw t1,-32(sp)
lw t2,-40(sp)
add t1,t1,t2
sw t1,-44(sp)
L_20:
lw t1,-44(sp)
sw t1,-16(sp)
L_21:
j L_31
L_22:
li t1,30000
li t2,10000
sub t1,t1,t2
sw t1,-48(sp)
L_23:
lw t1,-48(sp)
li t2,10
div t1,t1,t2
sw t1,-52(sp)
L_24:
li t1,70000
li t2,30000
sub t1,t1,t2
sw t1,-56(sp)
L_25:
lw t1,-56(sp)
li t2,5
div t1,t1,t2
sw t1,-60(sp)
L_26:
lw t1,-52(sp)
lw t2,-60(sp)
add t1,t1,t2
sw t1,-64(sp)
L_27:
lw t1,-12(sp)
li t2,70000
sub t1,t1,t2
sw t1,-68(sp)
L_28:
lw t1,-68(sp)
li t2,2
div t1,t1,t2
sw t1,-72(sp)
L_29:
lw t1,-64(sp)
lw t2,-72(sp)
add t1,t1,t2
sw t1,-76(sp)
L_30:
lw t1,-76(sp)
sw t1,-16(sp)
L_31:
li a7,1
lw t0,-16(sp)
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
