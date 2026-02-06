import pathlib
from clldutils.misc import slug
from pylexibank import Dataset as BaseDataset

PHONETIC_MAPPER = {}

CONCEPT_MAPPER = {}


class Dataset(BaseDataset):
    dir = pathlib.Path(__file__).parent
    id = "nawsawu1650"

    def cmd_makecldf(self, args):
        args.writer.add_sources()

        data = self.raw_dir.read_csv("data.tsv", delimiter="\t", dicts=True)

        added_concepts = set()
        added_languages = set()

        for entry in data:
            lang_name = entry["DOCULECT"]
            lang_id = slug(lang_name)
            if lang_id not in added_languages:
                args.writer.objects["LanguageTable"].append(
                    {
                        "ID": lang_id,
                        "Name": lang_name,
                        "Glottocode": entry.get("GLOTTOCODE"),
                    }
                )
                added_languages.add(lang_id)

            raw_concept = entry["SOURCE_CONCEPT"]
            concept_name = CONCEPT_MAPPER.get(raw_concept, raw_concept)
            concept_id = slug(concept_name)

            if concept_id not in added_concepts:
                args.writer.objects["ParameterTable"].append(
                    {
                        "ID": concept_id,
                        "Name": concept_name,
                        "Concepticon_ID": entry.get("CONCEPTICON_ID"),
                        "Concepticon_Gloss": entry.get("CONCEPTICON_NAME"),
                    }
                )
                added_concepts.add(concept_id)

            raw_tokens = (entry.get("SEGMENTS") or entry.get("TOKENS") or "").split()
            final_segments = []
            for s in raw_tokens:
                final_segments += PHONETIC_MAPPER.get(s, s).split(" ")

            args.writer.objects["FormTable"].append(
                {
                    "ID": f"{lang_id}-{concept_id}-{entry.get('ID', entry.get('SLNO'))}",
                    "Language_ID": lang_id,
                    "Parameter_ID": concept_id,
                    "Value": entry["FORM"],
                    "Form": entry["FORM"],
                    "Segments": final_segments,
                    "Source": [entry.get("SOURCE", "nawsawu2016makyam")],
                    "Comment": entry.get("NOTES"),
                }
            )

        print(f"Successfully processed {len(data)} rows.")
