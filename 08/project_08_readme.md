# Nand2Tetris Project 08: VM Translator (Part II)

本專案為 **Nand2Tetris (From Nand to Tetris)** 第八章作業的實作，在 Project 07 的基礎上擴充完成完整的虛擬機翻譯器（VM Translator），支援**程式流程控制**、**函式呼叫與遞迴機制**，以及**多檔案目錄編譯**。

## 📋 實作範圍與新增功能

除了完整保留 Project 07 的堆疊算術與 8 種記憶體區段操作外，本階段新增以下核心功能：

### 1. 程式流程控制 (Program Flow)

* **`label labelName`**：產生函式作用域內的唯一標籤 `(currentFunc$labelName)`。

* **`goto labelName`**：無條件跳躍至指定標籤。

* **`if-goto labelName`**：彈出堆疊頂端數值，若不為 `0`（True）則跳躍至指定標籤。

### 2. 函式呼叫與返回機制 (Function Calling)

* **`function f nVars`**：宣告函式進入點標籤 `(f)`，並自動將 `nVars` 個區域變數（`local`）初始化為 `0`。

* **`call f nArgs`**：保存呼叫端狀態（推入返回位址、`LCL`、`ARG`、`THIS`、`THAT`），重新配置被呼叫端的 `ARG` 與 `LCL` 指標，並跳躍至目標函式。

* **`return`**：將回傳值寫入呼叫端的 `*ARG`，恢復呼叫端的記憶體區段指標與 `SP`，並跳回返回位址繼續執行。

### 3. Bootstrap 啟動碼與多檔案支援

* **資料夾編譯**：支援傳入整個資料夾路徑，自動掃描並合併目錄下所有 `.vm` 檔案，輸出為同名的單一 `.asm` 檔案。

* **Static 變數隔離**：切換翻譯不同 `.vm` 檔案時自動更新檔名前綴（`@FileName.i`），確保跨檔案的靜態變數互不干擾。

* **智慧啟動碼判斷**：當輸入為「資料夾」時，自動在組語開頭寫入 Bootstrap 啟動碼（設定 `SP = 256` 並執行 `call Sys.init 0`）；若輸入為「單一 `.vm` 檔」則不加入啟動碼，以完美相容不具 `Sys.vm` 的基礎測試腳本。

## 🏗️ 程式架構

`VMTranslator.py` 擴充後的模組職責如下：

* **`Parser`**：解析 `.vm` 原始碼，新增辨識 `C_LABEL`、`C_GOTO`、`C_IF`、`C_FUNCTION`、`C_CALL` 與 `C_RETURN` 指令類型。

* **`CodeWriter`**：新增 `write_init`、`write_label`、`write_goto`、`write_if`、`write_function`、`write_call`、`write_return` 與 `set_file_name` 方法，精確控制堆疊框架（Stack Frame）與指標位移。

* **`main`**：自動判斷輸入參數為單一檔案或目錄，統籌檔案巡覽、啟動碼寫入與組語輸出。

## 🚀 執行方式

### 環境需求

* Python 3.x

* Nand2Tetris 官方軟體套件（`CPUEmulator`）

### 轉換指令

在 `08` 目錄下開啟終端機，依照測資類型傳入單一檔案或整個資料夾路徑：

```
# 1~3 題：單一檔案測試（不寫入 Bootstrap 啟動碼）
python VMTranslator.py ProgramFlow/BasicLoop/BasicLoop.vm
python VMTranslator.py ProgramFlow/FibonacciSeries/FibonacciSeries.vm
python VMTranslator.py FunctionCalls/SimpleFunction/SimpleFunction.vm

# 4~6 題：多檔案資料夾測試（自動合併所有 .vm 並加入 Bootstrap 啟動碼）
python VMTranslator.py FunctionCalls/FibonacciElement
python VMTranslator.py FunctionCalls/NestedCall
python VMTranslator.py FunctionCalls/StaticsTest

```

## ✅ 測試與驗證

1. 執行上述 6 道 Python 指令，確認各測試目錄下皆已生成對應的 `.asm` 檔案。

2. 開啟 Nand2Tetris 官方工具 **`CPUEmulator`**（建議將上方 `Animate` 設為 **`No animation`** 以加速執行遞迴測資）。

3. 點選 `File -> Load Script`，依序載入以下測試腳本（**不帶 `VME` 後綴**）：

   * `ProgramFlow/BasicLoop/BasicLoop.tst`

   * `ProgramFlow/FibonacciSeries/FibonacciSeries.tst`

   * `FunctionCalls/SimpleFunction/SimpleFunction.tst`

   * `FunctionCalls/FibonacciElement/FibonacciElement.tst`

   * `FunctionCalls/NestedCall/NestedCall.tst`

   * `FunctionCalls/StaticsTest/StaticsTest.tst`

4. 點擊執行按鈕（`>>`），確認視窗底部狀態列皆顯示 **`End of script - Comparison ended successfully`**，即代表全數通過驗證。