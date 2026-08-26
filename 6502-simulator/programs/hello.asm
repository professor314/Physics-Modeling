; Hello World for 6502 simulator
; Writes "Hello" to the LCD display at $6000
;
; The LCD data register is at $6000.
; Writing a byte places the ASCII character at the cursor
; and advances the cursor automatically.

    .org $8000

start:
    LDA #$48        ; 'H'
    STA $6000
    LDA #$65        ; 'e'
    STA $6000
    LDA #$6C        ; 'l'
    STA $6000
    LDA #$6C        ; 'l'
    STA $6000
    LDA #$6F        ; 'o'
    STA $6000
    BRK             ; stop

    ; Reset vector — CPU starts execution here after reset
    .org $FFFC
    .word $8000     ; reset vector points to start
    .word $0000     ; IRQ vector (unused)
