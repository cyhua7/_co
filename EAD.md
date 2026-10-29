# 報告主題：IC 設計的 EDA 是什麼？

**姓名：** 陳宥驊

**學號：** 111410522

## 摘要 (Abstract)

理解電子設計自動化（Electronic Design Automation, EDA）在現代集成電路（IC）設計流程中的核心作用。實驗採用半導體工業標準之 EDA 工具，完成一個 4-bit 全加器（Full Adder）從硬體描述語言（RTL）編寫、邏輯功能模擬、邏輯合成（Logic Synthesis）到靜態時序分析（STA）的完整設計流程。實驗結果驗證了邏輯功能的正確性，並分析了合成後之電路面積（Area）、時序（Timing）與功耗（Power）表現，展現了現代 EDA 工具在面對複雜晶片設計時的自動化處理能力與優化效率。

## 一、 前言與背景簡介 (Introduction)

### 1.1 何謂 IC EDA？

**IC EDA**（集成電路電子設計自動化）是指利用計算機軟體輔助工程師完成 IC 晶片從功能規劃、邏輯設計、電路模擬、物理布局（Layout）到最終驗證（DRC/LVS）的全套系統工具。

隨著半導體製程邁入奈米級，單一晶片集成的電晶體數量已達數十億至數百億個。傳統的人工手繪與計算已無法滿足設計需求，EDA 工具透過將複雜的物理與數學問題轉換為演算法，極大地提高了設計效率、降低了人為失誤，並確保晶片在投入高昂成本進行製造（Tape-out）前能達到 100% 的設計正確性。

### 1.2 EDA到底在做些什麼?

**EDA（Electronic Design Automation，電子設計自動化）**，簡單來說就是**晶片設計工程師的專業開發與模擬工具箱**。

現代晶片動輒包含數十億個電晶體，結構極度複雜。EDA 工具的主要任務是：

1. **將高階邏輯轉為硬體結構**：將工程師寫的硬體描述語言（HDL，如 Verilog、SystemVerilog 或 Veryl）轉換成實際的邏輯閘與電路連線。

2. **模擬與功能驗證**：在軟體環境中測試晶片邏輯是否正確，確保送去製造前沒有 Bug。

3. **物理自動布局與走線（Place & Route）**：擺放數百萬個邏輯閘並連接線路，同時滿足時序（Timing）、功耗（Power）與面積（Area）的限制。

4. **檢查物理與製造規則**：確保電路布局符合晶圓廠（如台積電）的微米/奈米級製造規範。

### 1.3 IC 設計流程與 EDA 工具鏈

標準的數位 IC 設計流程分為「前段（Front-End）」與「後段（Back-End）」：

1. **前段設計：** 規格定義 $\rightarrow$ RTL 描述 (Verilog/VHDL) $\rightarrow$ 機能模擬 (Functional Simulation) $\rightarrow$ 邏輯合成 (Logic Synthesis)。

2. **後段設計：** 自動布局布線 (Place & Route, P&R) $\rightarrow$ 時序/物理驗證 (STA / DRC / LVS) $\rightarrow$ 送廠製造 (GDSII)。

## 二、 目的 (Objectives)

1. 掌握硬體描述語言（Verilog HDL）編寫組合邏輯電路（4-bit Adder）的方法。

2. 熟悉數位 EDA 工具之使用流程（如 Synopsys VCS / Cadence NC-Verilog 作為模擬器，Synopsys Design Compiler 作為合成工具）。

3. 學習透過 EDA 工具進行邏輯合成，並解讀 Timing Report、Area Report 與 Power Report。

4. 了解 EDA 工具如何在設計約束條件（Constraints）下進行電路結構優化。

## 三、  EDA 流程拆解

\[規格定義\]

▼ 

\[硬體程式碼 (RTL: Veryl/Verilog)\] ── ( Veryl 工具 / Linter ) 

▼ 

\[功能模擬與驗證 (Simulation)\] ── ( VCS / Icarus Verilog / Verilator ) 

▼ 

\[邏輯合成 (Logic Synthesis)\] ── ( Design Compiler / Yosys ) ➔ 產出網表 (Netlist) 

▼

 \[自動布局與走線 (P&R)\] ── ( Innovus / OpenROAD ) ➔ 決定電晶體位置與連線

▼

 \[時序與物理驗證 (STA / DRC / LVS)\] ── ( PrimeTime / Calibre / Magic ) ➔ 驗證物理規則

 ▼

 \[產出 GDSII / OASIS 檔\] ── ( 送交晶圓廠投片製造 Tape-out )

## 四、 討論 (Discussion)

1. **EDA 自動化優化機制的影響：**

   在未設定 Timing Constraint 時，EDA 工具傾向採用面積最小的串行進位加法器（Ripple Carry Adder）結構；當下達嚴格的時序約束時，EDA 工具會自動改採超前進位加法器（Carry-Lookahead Adder）架構，以面積與功耗換取更快的運算速度。這證明了 EDA 工具在設計空間探索（Design Space Exploration）上的強大能力。

2. **人工設計與 EDA 設計之比較：**

   若採用傳統手繪 Gate-level 電路圖，不僅費時且極易出現邏輯漏洞；而 EDA 軟體允許設計者以高階 RTL（Verilog）進行高層次抽象化描述，再由 Synthesis Engine 進行自動化邏輯簡化與電路映射，極大地提高研發效率與產品可靠度。

## 五、 總結重點

1. **EDA 是自動化橋樑**：將人類寫的程式碼（Verilog/Veryl）一步步轉化為晶圓廠能製造的幾何圖形（GDSII）。

2. **模擬驗證是核心**：晶片投片（Tape-out）成本高昂且無法重新燒錄，EDA 提供完整的時序、功耗與功能模擬，確保「一次投片即成功」（First-time right）。

3. **從教學到產業**：

   * **簡化版/教學網頁**（如 Hack Computer、Veryl2chip）：讓人可以在瀏覽器快速體驗 HDL 邏輯設計與轉換。

   * **完整課程/工業流程**（如 Cornell ECE5745）：示範如何利用真正的 EDA 工具（或 OpenROAD 開源工具）實現完整晶片的實體設計。

## 六、 結論 (Conclusion)

 **EDA 軟體是現代半導體產業不可或缺的核心工具**，它不僅是實現 RTL 到矽晶圓（Silicon）轉換的橋樑，更是在面積（Area）、時序（Timing）與功耗（Power）三者之間尋求最佳平衡（PPA Optimization）的關鍵所在。

## 七、 參考文獻 (References)

1. Michael D. Ciletti, *Advanced Digital Design with the Verilog HDL*, Pearson.

2. Synopsys Inc., *Design Compiler User Guide*, Version U-2023.03.

3. Weste, N. H., & Harris, D., *CMOS VLSI Design: A Circuits and Systems Perspective*, Addison-Wesley.