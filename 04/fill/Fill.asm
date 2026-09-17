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

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen.
// When no key is pressed, the program clears the screen.

(LOOP)
    // 1. 讀取鍵盤輸入狀態
    @KBD
    D=M

    // 2. 判斷按鍵狀態：若 D == 0 (沒按鍵) 則跳轉到 CLEAR，否則填黑
    @CLEAR
    D;JEQ

    // 3. 設定填色數值為黑色 (-1 / 1111111111111111)
    @color
    M=-1
    @DRAW
    0;JMP

(CLEAR)
    // 4. 設定填色數值為白色 (0)
    @color
    M=0

(DRAW)
    // 5. 初始化螢幕指標 (screen pointer) 指向 SCREEN 起始位址 (16384)
    @SCREEN
    D=A
    @ptr
    M=D

(DRAW_LOOP)
    // 6. 將目前顏色的值寫入指標所指向的螢幕記憶體
    @color
    D=M
    @ptr
    A=M
    M=D

    // 7. 指標前進下一個 WORD (+1)
    @ptr
    M=M+1

    // 8. 檢查是否已塗滿整個螢幕 (SCREEN 起始 16384 + 8192 個 WORD = KBD 位址 24576)
    // 計算 ptr - KBD，若小於 0 代表尚未塗滿，繼續迴圈
    @ptr
    D=M
    @KBD
    D=D-A
    @DRAW_LOOP
    D;JLT

    // 9. 畫面刷洗完畢，跳回主迴圈繼續監聽鍵盤
    @LOOP
    0;JMP