# Hack Assembler (Nand2Tetris Project 6)

這是一個為 **Nand2Tetris** 課程中的 Hack 電腦架構所開發的組譯器（Assembler）。它的核心任務是將人類可讀的 **Hack 組合語言 (`.asm`)** 轉換為電腦硬體能直接執行的 **16-bit 二進位機器碼 (`.hack`)**。

---

## 📖 什麼是組譯器（Assembler）？

在電腦科學中，CPU 硬體只能看懂由 `0` 與 `1` 組成的二進位訊號（機器語言）。然而，直接用二進位編寫程式既困難又極易出錯，因此人們發明了**組合語言（Assembly Language）**，用簡單的英文助記符（如 `D=D+A`、`@LOOP`）來代表底層指令。

**組譯器（Assembler）** 就是位於「組合語言」與「機器語言」之間的翻譯官：
1. **指令轉譯**：將文字符號（如 `D+1`、`JMP`）查表轉換為對應的二進位位元組合。
2. **符號解析（Symbol Resolution）**：將程式中的變數名稱與跳躍標籤（Labels），自動對應並分配到正確的記憶體位址（RAM 與 ROM）。

---

## ⚙️ Hack 組譯器運作原理（兩階段掃描 Two-Pass）

為了能夠正確處理「先跳躍、後定義」的標籤（Forward Reference），本組譯器採用標準的**兩階段掃描（Two-Pass）**架構：

### 第一階段（Pass 1）：建立標籤符號表
* 逐行掃描 `.asm` 檔案，清除所有註解（`//`）與空白字元。
* 計算每條真實指令（A-Instruction 與 C-Instruction）所佔用的 **ROM 位址**（從 `0` 開始遞增）。
* 遇到標籤宣告（如 `(LOOP)`）時，不佔用 ROM 空間，直接將標籤名稱與當下的 ROM 位址存入**符號表（Symbol Table）**。

### 第二階段（Pass 2）：二進位機器碼翻譯
重新掃描所有指令，並根據指令類型進行翻譯：
* **A-Instruction (`@value` 或 `@symbol`)**：
  * 若為數字，直接轉為 16-bit 二進位碼（最高位為 `0`，後接 15-bit 數值）。
  * 若為符號，查詢符號表取得位址；若為首次出現的自訂變數，則從 **`RAM[16]`** 開始依序分配記憶體位址。
* **C-Instruction (`dest=comp;jump`)**：
  * 固定以 `111` 開頭，拆解 `comp`（7-bit）、`dest`（3-bit）、`jump`（3-bit）並查表組合為 16-bit 機器碼。

---

## 📂 專案檔案結構

```text
├── HackAssembler.py   # 組譯器主程式（包含 Parser、Code、SymbolTable 模組）
├── README.md          # 專案說明文件
└── test_files/        # 測試用組合語言檔案
    ├── Add.asm        # 基礎加法測試（無符號）
    ├── MaxL.asm       # 最大值運算（無符號版本）
    ├── Max.asm        # 最大值運算（含標籤與預設符號）
    ├── Rect.asm       # 螢幕繪製長方形（含自訂變數）
    └── Pong.asm       # 完整打磚塊遊戲（超過 20,000 行指令的大型測試）