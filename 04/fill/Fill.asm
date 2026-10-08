// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

(LOOP)
    // 1. Read keyboard input state
    @KBD
    D=M

    // 2. Branch: if D == 0 (no key), go to CLEAR; otherwise set BLACK
    @CLEAR
    D;JEQ

    // 3. Set color to black (-1 / 0xFFFF)
    @color
    M=-1
    @DRAW
    0;JMP

(CLEAR)
    // 4. Set color to white (0 / 0x0000)
    @color
    M=0

(DRAW)
    // 5. Initialize screen pointer (ptr) to SCREEN base address (16384)
    @SCREEN
    D=A
    @ptr
    M=D

(DRAW_LOOP)
    // 6. Write color to the memory address stored in ptr
    @color
    D=M
    @ptr
    A=M
    M=D

    // 7. Advance pointer to the next word (+1)
    @ptr
    M=M+1

    // 8. Check if whole screen is filled (SCREEN 16384 + 8192 words = KBD address 24576)
    // D = ptr - KBD; if D < 0, continue loop
    @ptr
    D=M
    @KBD
    D=D-A
    @DRAW_LOOP
    D;JLT

    // 9. Screen redraw complete; return to main loop to continuously listen to keyboard
    @LOOP
    0;JMP