"""CLDF dataset metadata."""

from pathlib import Path
import cldfbench


class Dataset(cldfbench.Dataset):
    """CLDF dataset derived from Nawsawu (2016) Descriptive Phonology of Makyam Naga"""

    dir = Path(__file__).parent
    id = "nawsawu2016makyam"

    def cldf_specs(self):
        """Return CLDF dataset specification."""
        return cldfbench.CLDFSpec(
            dir=self.cldf_dir,
            module="Wordlist",
            data_fnames={
                "FormTable": "forms.csv",
                "LanguageTable": "languages.csv",
                "ParameterTable": "parameters.csv",
            },
        )

    def cmd_download(self, args):
        """Download raw data."""
        pass

    def cmd_makecldf(self, args):
        """Create CLDF dataset from raw data."""
        from run import convert_tsv_to_cldf

        tsv_file = self.raw_dir / "data.tsv"
        bibtex_file = self.raw_dir / "sources.bib"

        if not tsv_file.exists():
            raise ValueError(f"Raw data file not found: {tsv_file}")

        convert_tsv_to_cldf(
            str(tsv_file),
            str(bibtex_file) if bibtex_file.exists() else None,
            str(self.cldf_dir),
        )
