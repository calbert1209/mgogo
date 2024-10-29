from serializeWord import SerializeShortWord, SerializeWord, SerializeLongWord


class Serialize:
    _sWord = SerializeShortWord()
    _word = SerializeWord()
    _lWord = SerializeLongWord()

    def sWord(**kwargs):
        return Serialize._sWord.word(kwargs)

    def word(**kwargs):
        return Serialize._word.word(kwargs)

    def lWord(**kwargs):
        return Serialize._lWord.word(kwargs)
