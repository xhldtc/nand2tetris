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
    @paint
    M=0

    @SCREEN
    D=A
    @base
    M=D

    @8192
    D=A
    @n
    M=D

    @base
    D=M
    @n
    D=D+M
    @last
    M=D

(LOOP)
    @KBD
    D=M
    @paint
    D=D&M
    @LOOP
    D;JNE

    @KBD
    D=M
    @paint
    D=D|M
    @LOOP
    D;JEQ

    @paint
    D=!M
    @paint
    M=D

    @base
    D=M
    @curr
    M=D
(DRAW)
    @last
    D=M
    @curr
    D=D-M
    @LOOP
    D;JEQ

    @paint
    D=M
    @curr
    A=M
    M=D

    @curr
    M=M+1
    @DRAW
    0;JMP
