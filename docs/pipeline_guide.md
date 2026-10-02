# Pipeline Guide

The Week 2 pipeline performs the following flow:
1. Discover datasets in datasets/raw.
2. Validate schema, missing values, duplicates, labels, and ranges.
3. Engineer derived features for intrusion and phishing datasets.
4. Preprocess and optionally balance the data.
5. Split into train, validation, and test sets.
6. Save metadata and reports under datasets/metadata and reports/.
