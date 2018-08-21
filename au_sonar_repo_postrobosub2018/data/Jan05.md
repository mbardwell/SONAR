# Jan05 Pool Test

## Initial Setup

* ULB-364 Pinger factory set to 27 kHz
* 2 x TC4013 hydrophones.
The two hydrophones are mounted on a rod x mm apart.
* BBB with PRUDaq configured to sample 2 simultaneous 10-bit ADCs at 500 kHz
* Custom programmable gain amplifier (Gain is R_var/1000). R_var (MCP4561) has 257 steps with each step 420 ohm and total resistance of 108000 (found experimentally)

The hydrophones and pinger are attached to a rope. The hydrophones are in series | O O | perpendicular to the rope. The distance from the pinger is changed and data is recorded. 

## Data
**Location: [ARVP Google Drive](https://drive.google.com/drive/u/1/folders/1-VW_4AqCC_KSoZ4bMbO5TKs7oXSrocZF)**

**Futher Information: [Spreadsheet](https://docs.google.com/spreadsheets/d/1lHz33_HVPFC0HvN3P8ELJCpuJP21mUrJQsu77IJILTM/edit) | [Google Doc](https://docs.google.com/document/u/1/d/1E-jKqNbrPnj-20fqM8clOE0pb3awmEkB_oU8lpvN5qM/edit?usp=drive_web)**

| Test No.  | File name  | Pinger Power  | Gain  |
| ---  | ---  | ---  | ---  |
| 1 | Jan05_test1_xf | 1/8W | 65.6x |
| 2 | Jan05_test2_xf | 1/2W | 27.8x |
| 3 | Jan05_test3_xf | 2W | 21x |
| 4 | Jan05_test4_xf | 2W | Variable |
| 5 | Jan05_test5 | 2W | 25x |

*Test 1-3*: the distance of pinger from the hydrophones is changed while keeping the angle at 0. The pinger power is changed at each test and a constant gain is used.

*Test 4*: the distance of pinger from the hydrophones is changed while keeping the angle at 0. The pinger power is kept constant and a variable gain is used.

*Test 5*: the two hyrdophones are kept at a constant distance of 6 ft rotated at 45 degrees.
