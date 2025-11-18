# Wealth Builder Pro

**Wealth Builder Pro** is a desktop GUI investment projection tool written in Python (Tkinter + Matplotlib + NumPy).  
It helps users estimate long-term portfolio growth, passive income at a safe withdrawal rate, milestones, and shows visual projections.

> This repository contains the UI app `investment_calc.py`. Run it locally to launch the GUI.

---

## Features

- Configure monthly contributions, annual increases, initial lump sum and investment period.
- Pick from several strategy types (Index funds, Roth IRA, Crypto, etc.) and set allocations.
- Weighted average return calculation and projection of portfolio growth.
- Text-based action plan and milestone detection.
- Interactive Matplotlib charts embedded in Tkinter.

---

## Requirements

- Python 3.9+ (3.10/3.11 recommended)
- `matplotlib`
- `numpy`
- `tkinter` (usually included with system Python — on Linux you may need to install `python3-tk`)

You can install required packages via:

```bash
python -m venv venv
source venv/bin/activate   # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
