from gtts import gTTS

def languages():
    """Sorted pretty printed string of supported languages"""
    return ", ".join(sorted("{}: '{}'".format(gTTS.LANGUAGES[k], k) for k in gTTS.LANGUAGES))

languages()