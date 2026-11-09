# Attribution and data provenance

- Dataset: **Vehicle dataset** (vehicle-dataset-from-cardekho).
- Author / publisher: **Nehal Birla** on Kaggle.
- Source: https://www.kaggle.com/datasets/nehalbirla/vehicle-dataset-from-cardekho
- Dataset version: **4**, published 2023-01-14.
- File selected: **Car details v3.csv**, 8,128 rows before filtering.
- Public download: https://www.kaggle.com/api/v1/datasets/download/nehalbirla/vehicle-dataset-from-cardekho?datasetVersionNumber=4
- Source listing license: **Database: Open Database, Contents: Database Contents**.
- Database license: https://opendatacommons.org/licenses/odbl/1.0/
- Contents license: https://opendatacommons.org/licenses/dbcl/1.0/

The included `artifacts/reference.csv` and `artifacts/holdout_predictions.csv` contain subsets and transformations of the original database. These derived database contents are provided under the source database/contents licenses, including attribution and the applicable ODbL share-alike requirements. These terms concern the data, not a new blanket license for all application source code. Preserve this attribution with any redistribution. See the linked license texts for the full terms.

Modifications: normalize categorical text, retain recognized passenger-car makers and seat configurations, remove commercial/unverified profiles and duplicate records, parse engine/power, engineer log km, split grouped vehicle profiles, and append model predictions for evaluation. Original author does not endorse this project. The uploaded Excel file was not used in training.

The CSV SHA-256, exact cleaning counts, exclusions, library versions and model metrics are recorded in `artifacts/evaluation.json`. The historical source is not a live feed of current asking prices. Original source has no individual observation dates. Numeric v3 selling prices are handled as INR without lakh multiplication; this processing convention is explicitly stated because the general Kaggle metadata does not include a column-level unit definition.
