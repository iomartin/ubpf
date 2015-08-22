#!/usr/bin/env python
import unittest
import struct
import disassembler

class DisassemblerTests(unittest.TestCase):
    def check(self, inst, expected):
        data = struct.pack("L", inst)
        self.assertEquals(expected, disassembler.disassemble_one(data, 0))

    def test_alu(self):
        self.check(0x0000000200000104, "ADD r1, $2")
        self.check(0xffffffff00000904, "ADD r9, $ffffffff")
        self.check(0x000000000000210c, "ADD r1, r2")
        self.check(0x000000000000211c, "SUB r1, r2")
        self.check(0x000000000000212c, "MUL r1, r2")
        self.check(0x000000000000213c, "DIV r1, r2")
        self.check(0x000000000000214c, "OR r1, r2")
        self.check(0x000000000000215c, "AND r1, r2")
        self.check(0x000000000000216c, "LSH r1, r2")
        self.check(0x000000000000217c, "RSH r1, r2")
        self.check(0x000000000000218c, "NEG r1, r2")
        self.check(0x000000000000219c, "MOD r1, r2")
        self.check(0x00000000000021ac, "XOR r1, r2")
        self.check(0x00000000000021bc, "MOV r1, r2")
        self.check(0x00000000000021cc, "ARSH r1, r2")
        self.check(0x00000010000001dc, "END16 r1")
        self.check(0x00000020000001dc, "END32 r1")
        self.check(0x00000040000001dc, "END64 r1")

    def test_alu64(self):
        self.check(0x0000000200000107, "ADD64 r1, $2")
        self.check(0xffffffff00000907, "ADD64 r9, $ffffffff")
        self.check(0x000000000000210f, "ADD64 r1, r2")
        self.check(0x000000000000211f, "SUB64 r1, r2")
        self.check(0x000000000000212f, "MUL64 r1, r2")
        self.check(0x000000000000213f, "DIV64 r1, r2")
        self.check(0x000000000000214f, "OR64 r1, r2")
        self.check(0x000000000000215f, "AND64 r1, r2")
        self.check(0x000000000000216f, "LSH64 r1, r2")
        self.check(0x000000000000217f, "RSH64 r1, r2")
        self.check(0x000000000000218f, "NEG64 r1, r2")
        self.check(0x000000000000219f, "MOD64 r1, r2")
        self.check(0x00000000000021af, "XOR64 r1, r2")
        self.check(0x00000000000021bf, "MOV64 r1, r2")
        self.check(0x00000000000021cf, "ARSH64 r1, r2")
        self.check(0x00000010000001df, "END6416 r1") # XXX
        self.check(0x00000020000001df, "END6432 r1") # XXX
        self.check(0x00000040000001df, "END6464 r1") # XXX

    def test_jmp(self):
        self.check(0x0000000000010005, "JA +1")
        self.check(0x000000007fff0005, "JA +32767")
        self.check(0x00000000ffff0005, "JA -1")
        self.check(0x0000000080000005, "JA -32768")
        self.check(0x0000003300010115, "JEQ r1, $33, +1")
        self.check(0x000000000001211d, "JEQ r1, r2, +1")
        self.check(0x000000000001212d, "JGT r1, r2, +1")
        self.check(0x000000000001213d, "JGE r1, r2, +1")
        self.check(0x000000000001214d, "JSET r1, r2, +1")
        self.check(0x000000000001215d, "JNE r1, r2, +1")
        self.check(0x000000000001216d, "JSGT r1, r2, +1")
        self.check(0x000000000001217d, "JSGE r1, r2, +1")
        self.check(0x0000000100000085, "CALL $1")
        self.check(0x0000000000000095, "EXIT")

    # TODO test ld

    def test_ldx(self):
        self.check(0x0000000000002161, "LDXW MEM r1, [r2]")
        self.check(0x0000000000002169, "LDXH MEM r1, [r2]")
        self.check(0x0000000000002171, "LDXB MEM r1, [r2]")
        self.check(0x0000000000002179, "LDXDW MEM r1, [r2]")
        self.check(0x0000000000012161, "LDXW MEM r1, [r2+1]")
        self.check(0x000000007fff2161, "LDXW MEM r1, [r2+32767]")
        self.check(0x00000000ffff2161, "LDXW MEM r1, [r2-1]")
        self.check(0x0000000080002161, "LDXW MEM r1, [r2-32768]")

    def test_st(self):
        self.check(0x0000003300000162, "STW MEM [r1], $33")
        self.check(0x0000003300010162, "STW MEM [r1+1], $33")
        self.check(0x000000337fff0162, "STW MEM [r1+32767], $33")
        self.check(0x00000033ffff0162, "STW MEM [r1-1], $33")
        self.check(0x0000003380000162, "STW MEM [r1-32768], $33")

    def test_stx(self):
        self.check(0x0000000000002163, "STXW MEM [r1], r2")
        self.check(0x0000000000012163, "STXW MEM [r1+1], r2")
        self.check(0x000000007fff2163, "STXW MEM [r1+32767], r2")
        self.check(0x00000000ffff2163, "STXW MEM [r1-1], r2")
        self.check(0x0000000080002163, "STXW MEM [r1-32768], r2")
