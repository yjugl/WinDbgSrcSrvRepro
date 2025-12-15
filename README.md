Reproducing the issue with the provided EXE/PDB files
=====================================================

- Copy `WinDbgSrcSrvRepro.pdb` to your symbol cache, e.g. `C:\ProgramData\Dbg\sym\WinDbgSrcSrvRepro.pdb\EBA25382142C48B68B05BF320F6CEC501\WinDbgSrcSrvRepro.pdb`.
- Uninstall the current version of WinDbg: `winget uninstall Microsoft.WinDbg`.
- Install the WinDbg version to test, e.g. `winget install Microsoft.WinDbg --version 1.2402.24001.0`.
- Run `WinDbgSrcSrvRepro.exe` under WinDbg with SRCSRV support enabled, e.g. `windbgx -c ".srcfix; !sym noisy; .srcnoisy 3; g; k" WinDbgSrcSrvRepro.exe`.
- On GOOD versions: when the breakpoint triggers, the source code is shown.
- On BAD versions: when the breakpoint triggers, WinDbg shows an error page.

Steps to craft your own reproducer PDB file
===========================================

- Build the Release and/or Debug project using Visual Studio.
- Make sure the `.pdb` file is generated.
- Close Visual Studio.
- Run `add_srcsrv_stream.py`.

A correct output looks like below, showing that `main.cpp` now gets resolved to a github URL:

```
Adding srcsrv stream...

Skipping non-existing file C:\Users\yjugl\source\repos\WinDbgSrcSrvRepro\x64\Debug\WinDbgSrcSrvRepro.pdb

Checking indexed files...
[C:\Users\yjugl\source\repos\WinDbgSrcSrvRepro\WinDbgSrcSrvRepro\main.cpp] trg: https://github.com/yjugl/WinDbgSrcSrvRepro/raw/ce0040bf20f6d8344ceaba4c57288ef22b63bf90/WinDbgSrcSrvRepro/main.cpp
C:\Users\yjugl\source\repos\WinDbgSrcSrvRepro\x64\Release\WinDbgSrcSrvRepro.pdb: 1 source file is indexed - 187 are not.

Skipping non-existing file C:\Users\yjugl\source\repos\WinDbgSrcSrvRepro\x64\Debug\WinDbgSrcSrvRepro.pdb
```

Steps to reproduce the issue with your crafted PDB file
=======================================================

- Make sure your symbol cache is empty so that it holds no previous copy of the .pdb file.
- Open `WinDbgSrcSrvRepro.exe` once under `WinDbg` so that the PDB file gets copied to the symbol cache.
- Double-check that `lm` shows `private symbols` for that binary with a path to the symbol cache.
- Close WinDbg.
- Now rename the repository folder e.g. to `WinDbgSrcRepro_NOCHEATING`, so that the debugger won't find the files on disk and will have to look for them online!

Now for each version of WinDbg you want to test:

- Uninstall the current version of WinDbg: `winget uninstall Microsoft.WinDbg`.
- Install the WinDbg version to test, e.g. `winget install Microsoft.WinDbg --version 1.2402.24001.0`.
- Run `WinDbgSrcSrvRepro.exe` under WinDbg with SRCSRV support enabled, e.g. `windbgx -c ".srcfix; !sym noisy; .srcnoisy 3; g; k" WinDbgSrcSrvRepro.exe`.
- On GOOD versions: when the breakpoint triggers, the source code is shown.
- On BAD versions: when the breakpoint triggers, WinDbg shows an error page.
