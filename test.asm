start:
    lui x1, 0xff
    beq x0, x0, check1
    xori x2, x0, 0x1001
check1:
    addi x0, x0, 5
