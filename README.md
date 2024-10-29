# Mgogo

A library to convert [Adafruit Macropad RP4020](https://learn.adafruit.com/adafruit-macropad-rp2040/overview) settings to and from binary for read and write to micro-controller non-volatile memory.

Inspired by the [Redis serialization protocol specification (RESP)](https://redis.io/docs/latest/develop/reference/protocol-spec/)

## Basic types

| type | length | prefix | notes |
| --- | --- | --- | --- |
| SWORD | 3 bytes | `#` | short word |
| WORD | 7 bytes | `_` | |
| LWORD | 15 bytes | `$` | long word |
| PCODE | 1 byte | `+` | push code |
| RCODE | 1 byte | `-` | release code |
| (END) | 1 byte | `\n` | signals end of binary array in NVM. |

## Complex types

| type | prefix | notes |
| --- | --- | --- |
| ARRAY | `*n` | of length n; may only hold a single type |
| KCODE | `+-` | union of PCODE \| RCODE |
| COMM | `<` | WORD (label) + SWORD (LED color) + ARRAY\<KCODE\> |
| PAGE | `[` | LWORD (label) + ARRAY\<COMM\> |

## Intended limitations

Strings beyond 15 characters in length are not supported. In actuality the display UI cannot handle more strings longer than this anyway.

Unicode is not supported by the default Circuit Python font, so one byte per character should be sufficient.

## About the name

_Mgogo_ is Swahili for woodpecker, a bird with a sense of rhythm.

