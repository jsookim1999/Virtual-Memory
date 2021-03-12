# Virtual-Memory

Coursework project from CS 143B (Project in OS) with Lubomir Bic.

## Project Overview (from uci.grlcontent.com)
This project implements a virtual memory (VM) system using segmentation and paging. The system manages the necessary segment and page tables (PTs) in a simulated main memory. It accepts virtual addresses (VAs) and translates them into physical addresses (PAs) according to the current contents of the segment and PTs. Two versions of the VM manager can be implemented: The simpler version assumes that the entire VA space is resident in physical memory (PM). The second supports demand paging.

 

The system is optionally extended with a translation look-aside buffer (TLB) to make the translation process more efficient.