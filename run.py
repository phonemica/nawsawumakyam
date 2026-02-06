import pathlib
from pylexibank import Dataset as BaseDataset

# from pylexibank import Forms
from clldutils.misc import slug


class Dataset(BaseDataset):
    dir = pathlib.Path(__file__).parent
    id = "nawsawu1650"

    def cmd_makecldf(self, args):
        args.writer.add_sources()

        concepts = {}
        raw_data = self.raw_dir.read_csv("data.tsv", delimiter="\t", dicts=True)

        glosses = [c for c in raw_data[0].keys() if c not in skip_cols]

        for gloss in glosses:
            concepts[gloss] = args.writer.add_concept(ID=slug(gloss), Name=gloss)

        # 3. Process each row (Language variety)
        for row in raw_data:
            lang_id = row["glottolog"] or slug(row["local"])

            # Add the language to the LanguageTable
            args.writer.add_language(
                ID=lang_id,
                Name=row["local"],
                Glottocode=row["glottolog"] if len(row["glottolog"]) == 8 else None,
            )

            # 4. Extract forms for each concept
            for gloss in glosses:
                value = row.get(gloss)
                if value and value.strip():
                    # Handle multiple forms separated by commas if necessary
                    for form in value.split(","):
                        args.writer.add_form(
                            Language_ID=lang_id,
                            Parameter_ID=concepts[gloss],
                            Value=form.strip(),
                            Form=form.strip(),
                            Source=["nawsawu1650makyam"],  # Reference to your bib file
                        )
