import os
import pathlib
import subprocess

REPOSITORY = pathlib.Path(__file__).parent.absolute()
PDBSTR = r"C:\Program Files (x86)\Windows Kits\10\Debuggers\x64\srcsrv\pdbstr.exe"
SRCTOOL = r"C:\Program Files (x86)\Windows Kits\10\Debuggers\x64\srcsrv\srctool.exe"
MAIN_CPP = os.path.join(REPOSITORY, "WinDbgSrcSrvRepro", "main.cpp")
SRCSRV_TXT = os.path.join(REPOSITORY, "srcsrv.txt")
RELEASE_PDB = os.path.join(REPOSITORY, "x64", "Release", "WinDbgSrcSrvRepro.pdb")
DEBUG_PDB = os.path.join(REPOSITORY, "x64", "Debug", "WinDbgSrcSrvRepro.pdb")

# --- 1: Generate srcsrv.txt ---

stream = fr"""
SRCSRV: ini ------------------------------------------------
VERSION=2
INDEXVERSION=2
VERCTRL=http
SRCSRV: variables ------------------------------------------
SRCSRVVERCTRL=http
GITHUB_TARGET=https://github.com/yjugl/WinDbgSrcSrvRepro/raw/%var4%/%var3%
SRCSRVTRG=%fnvar%(%var2%)
SRCSRV: source files ---------------------------------------
{MAIN_CPP}*GITHUB_TARGET*WinDbgSrcSrvRepro/main.cpp*ce0040bf20f6d8344ceaba4c57288ef22b63bf90
SRCSRV: end ------------------------------------------------
"""

if not os.path.exists(SRCSRV_TXT):
    with open(SRCSRV_TXT, "wb") as h:
        for line in stream.strip().split("\n"):
            h.write(line.encode("ascii") + b"\r\n")

# --- 2: Add srcsrv stream to .pdb files ---

def add_srcsrv_stream(pdb_path):
    if os.path.exists(pdb_path):
        print(subprocess.run([
            PDBSTR,
            "-w",
            f"-p:{pdb_path}",
            "-s:srcsrv",
            f"-i:{SRCSRV_TXT}"
        ], capture_output=True).stdout.decode())
    else:
        print(f"Skipping non-existing file {pdb_path}")
        print()

print("Adding srcsrv stream...")
add_srcsrv_stream(RELEASE_PDB)
add_srcsrv_stream(DEBUG_PDB)

# -- 3: Check .pdb files ---

def check_indexed_files(pdb_path):
    if os.path.exists(pdb_path):
        print(subprocess.run([
            SRCTOOL,
            f"{pdb_path}"
        ], capture_output=True).stdout.decode())
    else:
        print(f"Skipping non-existing file {pdb_path}")

print("Checking indexed files...")
check_indexed_files(RELEASE_PDB)
check_indexed_files(DEBUG_PDB)
