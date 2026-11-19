# Nand2Tetris Project 07: VM Translator (Part I)

本專案為 **Nand2Tetris (From Nand to Tetris)** 第七章作業的實作，旨在打造一個虛擬機翻譯器（VM Translator）的第一階段版本，負責將 Hack 虛擬機語言（`.vm`）轉換為 Hack 組合語言（`.asm`）。

---

## 📋 實作範圍與功能

本階段的 `VMTranslator.py` 支援以下兩大類 VM 指令：

### 1. 堆疊算術與邏輯運算 (Stack Arithmetic)
* **二元運算**：`add`、`sub`、`and`、`or`
* **一元運算**：`neg`、`not`
* **比較運算**：`eq`、`gt`、`lt`（自動生成遞增流水號標籤，避免多重跳躍衝突）

### 2. 記憶體存取指令 (Memory Access)
支援 `push` 與 `pop` 操作於以下 8 種記憶體區段（Memory Segments）：
* `constant`（常數推入）
* `local`、`argument`、`this`、`that`（動態基底指標區段）
* `temp`（固定對應 `RAM[5]` ~ `RAM[12]`）
* `pointer`（直接存取 `THIS` / `THAT` 指標本身）
* `static`（轉換為 `@FileName.i` 符號變數，配置於 `RAM[16]` 之後）

---

## 🏗️ 程式架構

`VMTranslator.py` 採用模組化設計，主要分為三個部分：
* **`Parser`**：讀取 `.vm` 檔案，過濾空白與註解（`//`），並拆解指令類型（`C_ARITHMETIC`、`C_PUSH`、`C_POP`）與參數（`arg1`、`arg2`）。
* **`CodeWriter`**：將解析後的 VM 指令翻譯為對應的 Hack 組合語言，並寫入目標 `.asm` 檔案中。
* **`main`**：處理命令列輸入路徑，串接 `Parser` 與 `CodeWriter` 完成檔案轉換。

---

## 🚀 執行方式

### 環境需求
* Python 3.x
* Nand2Tetris 官方軟體套件（`CPUEmulator`）

### 轉換指令
在 `07` 目錄下開啟終端機，執行以下指令即可將 `.vm` 轉換為同名的 `.asm` 檔案：

```bash
# StackArithmetic 測試題
python VMTranslator.py StackArithmetic/SimpleAdd/SimpleAdd.vm
python VMTranslator.py StackArithmetic/StackTest/StackTest.vm

# MemoryAccess 測試題
python VMTranslator.py MemoryAccess/BasicTest/BasicTest.vm
python VMTranslator.py MemoryAccess/PointerTest/PointerTest.vm
python VMTranslator.py MemoryAccess/StaticTest/StaticTest.vm
```

---

## ✅ 測試與驗證

1. 執行上述 Python 指令，確認各測試資料夾內皆已生成對應的 `.asm` 檔案。
2. 開啟 Nand2Tetris 官方工具 **`CPUEmulator`**。
3. 點選 `File -> Load Script`，依序載入以下測試腳本（**不帶 `VME` 後綴**）：
   * `StackArithmetic/SimpleAdd/SimpleAdd.tst`
   * `StackArithmetic/StackTest/StackTest.tst`
   * `MemoryAccess/BasicTest/BasicTest.tst`
   * `MemoryAccess/PointerTest/PointerTest.tst`
   * `MemoryAccess/StaticTest/StaticTest.tst`
4. 點擊執行按鈕（`>>`），確認視窗底部狀態列皆顯示 **`End of script - Comparison ended successfully`**，即代表驗證通過。