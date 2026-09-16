"""Unit tests for OwnSynsetWrapper, the adapter around a raw `wn` synset object."""
import wn

from passivlingo_dictionary.wrappers.OwnSynsetWrapper import OwnSynsetWrapper
from passivlingo_dictionary.wrappers.OwnWordNetWrapper import OwnWordNetWrapper


def _house_noun_synset():
    return next(s for s in wn.synsets('house', lang='en') if s.pos == 'n')


class TestOwnSynsetWrapperProperties:
    def test_id_delegates_to_underlying_synset(self):
        raw = _house_noun_synset()
        wrapped = OwnSynsetWrapper('en', raw)
        assert wrapped.id == raw.id

    def test_pos_delegates_to_underlying_synset(self):
        raw = _house_noun_synset()
        wrapped = OwnSynsetWrapper('en', raw)
        assert wrapped.pos == 'n'

    def test_lang_returns_constructor_argument(self):
        raw = _house_noun_synset()
        wrapped = OwnSynsetWrapper('de', raw)
        assert wrapped.lang == 'de'

    def test_ili_returns_the_ili_id_string(self):
        raw = _house_noun_synset()
        wrapped = OwnSynsetWrapper('en', raw)
        assert wrapped.ili == raw.ili.id

    def test_ili_returns_empty_string_when_absent(self):
        class _FakeSynsetNoIli:
            ili = None

        wrapped = OwnSynsetWrapper('en', _FakeSynsetNoIli())
        assert wrapped.ili == ''

    def test_ili_swallows_exceptions_and_returns_empty_string(self):
        class _FakeSynsetRaisesOnIli:
            @property
            def ili(self):
                raise RuntimeError('boom')

        wrapped = OwnSynsetWrapper('en', _FakeSynsetRaisesOnIli())
        assert wrapped.ili == ''


class TestOwnSynsetWrapperDelegatedMethods:
    def test_senses_and_lemmas_delegate(self):
        raw = _house_noun_synset()
        wrapped = OwnSynsetWrapper('en', raw)
        assert wrapped.lemmas() == raw.lemmas()
        assert len(wrapped.senses()) == len(raw.senses())

    def test_definition_delegates(self):
        raw = _house_noun_synset()
        wrapped = OwnSynsetWrapper('en', raw)
        assert wrapped.definition() == raw.definition()

    def test_examples_combines_synset_and_sense_examples(self):
        raw = _house_noun_synset()
        wrapped = OwnSynsetWrapper('en', raw)
        expected = list(raw.examples())
        for sense in raw.senses():
            expected.extend(sense.examples())
        assert wrapped.examples() == expected

    def test_hypernyms_returns_wrapped_synsets_with_same_lang(self):
        raw = _house_noun_synset()
        wrapped = OwnSynsetWrapper('de', raw)
        hypernyms = wrapped.hypernyms()
        assert len(hypernyms) == len(raw.hypernyms())
        assert all(isinstance(h, OwnSynsetWrapper) for h in hypernyms)
        assert all(h.lang == 'de' for h in hypernyms)
        assert [h.id for h in hypernyms] == [s.id for s in raw.hypernyms()]

    def test_hyponyms_returns_wrapped_synsets(self):
        w = OwnWordNetWrapper('de')
        raw = next(s for s in w.translate('vehicle', 'en') if s.pos == 'n' and len(s.hyponyms()) > 0)
        hyponyms = raw.hyponyms()
        assert len(hyponyms) > 0
        assert all(isinstance(h, OwnSynsetWrapper) for h in hyponyms)

    def test_meronyms_returns_wrapped_synsets(self):
        w = OwnWordNetWrapper('de')
        raw = next(s for s in w.translate('house', 'en') if s.pos == 'n' and len(s.meronyms()) > 0)
        meronyms = raw.meronyms()
        assert len(meronyms) > 0
        assert all(isinstance(m, OwnSynsetWrapper) for m in meronyms)

    def test_get_related_entails_returns_wrapped_synsets(self):
        w = OwnWordNetWrapper('de')
        raw = next(s for s in w.translate('snore', 'en') if s.pos == 'v')
        related = raw.get_related('entails')
        assert len(related) > 0
        assert all(isinstance(r, OwnSynsetWrapper) for r in related)


class TestOwnSynsetWrapperRepr:
    def test_repr_includes_id(self):
        raw = _house_noun_synset()
        wrapped = OwnSynsetWrapper('en', raw)
        assert repr(wrapped) == f'OwnSynsetWrapper({raw.id})'
        assert str(wrapped) == repr(wrapped)
