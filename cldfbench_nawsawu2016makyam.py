import pathlib
from clldutils.misc import slug
from pylexibank import Dataset as BaseDataset
from pylexibank import progressbar as pb
from cldfbench import CLDFSpec


class Dataset(BaseDataset):
    dir = pathlib.Path(__file__).parent
    id = "nawsawu2016makyam"

    writer_options = dict(keep_languages=True, keep_parameters=True)

    def validate(self, args):
        self.cldf_reader().validate(log=args.log)

    def cldf_specs(self):
        return CLDFSpec(
            module="Wordlist", dir=self.cldf_dir, metadata_fname="cldf-metadata.json"
        )

    def cmd_makecldf(self, args):
        args.writer.add_sources()
        args.log.info("Added sources")

        language_sources = {}
        for language in self.languages:
            args.writer.add_language(
                ID=language["ID"],
                Name=language["Name"],
                Glottocode=language.get("Glottocode"),
            )
            language_sources[language["ID"]] = language.get("Sources", "")

        concept_lookup = {}
        for concept in self.concepts:
            c_id = f"{concept['NUMBER']}-{slug(concept['ENGLISH'])}"

            args.writer.objects["ParameterTable"].append(
                {
                    "ID": c_id,
                    "Name": concept["ENGLISH"],
                    "Concepticon_ID": concept.get("CONCEPTICON_ID"),
                    "Concepticon_Gloss": concept.get("CONCEPTICON_GLOSS"),
                }
            )
            concept_lookup[concept["ENGLISH"]] = c_id

        args.log.info("Added concepts")

        data = self.raw_dir.read_csv("data.tsv", delimiter="\t", dicts=True)

        if "FormTable" not in args.writer.objects:
            args.writer.objects["FormTable"] = []

        added_count = 0
        for i, entry in enumerate(pb(data, desc="Processing forms")):
            concept_name = entry.get("SOURCE_CONCEPT")
            lang_id = entry.get("DOCULECT")

            if concept_name in concept_lookup:
                segments = entry.get("TOKENS", "").split()
                src_string = language_sources.get(lang_id, "")
                src_list = [s.strip() for s in src_string.split(";") if s.strip()]

                args.writer.objects["FormTable"].append(
                    {
                        "ID": f"{lang_id}-{concept_lookup[concept_name]}-{i}",
                        "Language_ID": lang_id,
                        "Parameter_ID": concept_lookup[concept_name],
                        "Value": entry.get("FORM"),
                        "Form": entry.get("FORM"),
                        "Segments": segments,
                        "Source": src_list,
                    }
                )
                added_count += 1

        args.log.info(f"Complete! Added {added_count} forms.")
