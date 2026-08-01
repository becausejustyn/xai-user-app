# Local image setup

The repository does not include the research images. The images are not part of the code
license.

## Get the source images

1. Open the [Diverse Human Faces Dataset](https://synthesis.ai/diverse-human-faces-dataset/) page.
2. Read and accept the Synthesis AI terms for the dataset.
3. Get the dataset from Synthesis AI through its current access process.
4. Keep the downloaded files outside this repository.

The download places all 70,001 files in the active directory, so create a directory for
the dataset first. The source dataset supplies the prediction images. It does not supply
the two XAI explanation images. Generate those explanation images with your model and
XAI methods.

## Prepare local trial files

Create one folder for each trial. Use this structure:

```text
trials/
├── README.md
├── trial_001/
│   ├── prediction.png
│   ├── explanation_a.png
│   └── explanation_b.png
└── trial_002/
    ├── prediction.png
    ├── explanation_a.png
    └── explanation_b.png
```

The app loads folders whose names start with `trial_`. Each folder must contain all three
PNG files. The app ignores incomplete folders.

The root `.gitignore` file excludes local trial folders. Do not override this rule unless
you have permission to redistribute every image.
