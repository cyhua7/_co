// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

    // Initialize R2 = 0
    @R2
    M=0

    // Copy R0 into i (counter)
    @R0
    D=M
    @i
    M=D

(LOOP)
    // If i <= 0, jump to END
    @i
    D=M
    @END
    D;JLE  

    // R2 = R2 + R1
    @R1
    D=M
    @R2
    M=M+D

    // i = i - 1
    @i
    M=M-1

    // Repeat loop
    @LOOP
    0;JMP

(END)
    // Infinite loop to terminate execution cleanly
    @END
    0;JMP