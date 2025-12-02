#!/usr/bin/env python3
"""
Manual config creation script as fallback if spacy init config fails.
This creates config files directly without using the CLI.
"""

import sys
from pathlib import Path
import json


def create_ner_config(output_path: Path, train_path: Path, dev_path: Path):
    """Create NER config manually."""
    config_content = f"""[paths]
train = "{train_path}"
dev = "{dev_path}"
vectors = null
init_tok2vec = null

[system]
gpu_allocator = null
seed = 0

[nlp]
lang = "en"
pipeline = ["tok2vec","ner"]
batch_size = 1000
disabled = []
before_creation = null
after_creation = null
after_pipeline_creation = null
tokenizer = {{"@tokenizers":"spacy.Tokenizer.v1"}}

[components]

[components.ner]
factory = "ner"
moves = null
update_with_oracle_cut_size = 100
incorrect_spans_key = "incorrect_spans"

[components.ner.model]
@architectures = "spacy.TransitionBasedParser.v2"
state_type = "ner"
extra_state_tokens = false
hidden_width = 64
maxout_pieces = 2
use_upper = true
nO = null

[components.ner.model.tok2vec]
@architectures = "spacy.HashEmbedCNN.v2"
pretrained_vectors = null
width = 96
depth = 4
embed_size = 2000
window_size = 1
maxout_pieces = 3
subword_features = true

[components.tok2vec]
factory = "tok2vec"

[components.tok2vec.model]
@architectures = "spacy.HashEmbedCNN.v2"
pretrained_vectors = null
width = 96
depth = 4
embed_size = 2000
window_size = 1
maxout_pieces = 3
subword_features = true

[corpora]

[corpora.train]
@readers = "spacy.Corpus.v1"
path = "{train_path}"
max_length = 0
gold_preproc = false
limit = 0
augmenter = null

[corpora.dev]
@readers = "spacy.Corpus.v1"
path = "{dev_path}"
max_length = 0
gold_preproc = false
limit = 0
augmenter = null

[training]
dev_corpus = "corpora.dev"
train_corpus = "corpora.train"
seed = 0
gpu_allocator = null
dropout = 0.1
accumulate_gradient = 3
patience = 1600
max_epochs = 0
max_steps = 20000
eval_frequency = 200
frozen_components = []
annotating_components = []
before_to_disk = null
before_update = null

[training.batcher]
@batchers = "spacy.batch_by_words.v1"
discard_oversize = false
tolerance = 0.2
get_length = null

[training.batcher.size]
@schedules = "compounding.v1"
start = 100
stop = 1000
compound = 1.001
t = 0.0

[training.logger]
@loggers = "spacy.ConsoleLogger.v1"
progress_bar = false

[training.optimizer]
@optimizers = "Adam.v1"
beta1 = 0.9
beta2 = 0.999
L2_is_weight_decay = true
L2 = 0.01
grad_clip = 1.0
use_averages = false
eps = 0.00000001
learn_rate = 0.001

[training.score_weights]
ents_f = 1.0
ents_p = 0.0
ents_r = 0.0
"""
    
    with open(output_path, 'w') as f:
        f.write(config_content)
    
    print(f"✅ Created NER config: {output_path}")


def create_intent_config(output_path: Path, train_path: Path, dev_path: Path):
    """Create Intent Classification config manually."""
    config_content = f"""[paths]
train = "{train_path}"
dev = "{dev_path}"
vectors = null
init_tok2vec = null

[system]
gpu_allocator = null
seed = 0

[nlp]
lang = "en"
pipeline = ["tok2vec","textcat_multilabel"]
batch_size = 1000
disabled = []
before_creation = null
after_creation = null
after_pipeline_creation = null
tokenizer = {{"@tokenizers":"spacy.Tokenizer.v1"}}

[components]

[components.textcat_multilabel]
factory = "textcat_multilabel"
scorer = {{"@scorers":"spacy.textcat_multilabel_scorer.v1"}}
threshold = 0.5

[components.textcat_multilabel.model]
@architectures = "spacy.TextCatEnsemble.v2"
nO = null

[components.textcat_multilabel.model.tok2vec]
@architectures = "spacy.HashEmbedCNN.v2"
pretrained_vectors = null
width = 96
depth = 4
embed_size = 2000
window_size = 1
maxout_pieces = 3
subword_features = true

[components.textcat_multilabel.model.linear_model]
@architectures = "spacy.TextCatBOW.v2"
exclusive_classes = false
ngram_size = 1
no_output_layer = false
nO = null

[components.tok2vec]
factory = "tok2vec"

[components.tok2vec.model]
@architectures = "spacy.HashEmbedCNN.v2"
pretrained_vectors = null
width = 96
depth = 4
embed_size = 2000
window_size = 1
maxout_pieces = 3
subword_features = true

[corpora]

[corpora.train]
@readers = "spacy.Corpus.v1"
path = "{train_path}"
max_length = 0
gold_preproc = false
limit = 0
augmenter = null

[corpora.dev]
@readers = "spacy.Corpus.v1"
path = "{dev_path}"
max_length = 0
gold_preproc = false
limit = 0
augmenter = null

[training]
dev_corpus = "corpora.dev"
train_corpus = "corpora.train"
seed = 0
gpu_allocator = null
dropout = 0.1
accumulate_gradient = 3
patience = 1600
max_epochs = 0
max_steps = 20000
eval_frequency = 200
frozen_components = []
annotating_components = []
before_to_disk = null
before_update = null

[training.batcher]
@batchers = "spacy.batch_by_words.v1"
discard_oversize = false
tolerance = 0.2
get_length = null

[training.batcher.size]
@schedules = "compounding.v1"
start = 100
stop = 1000
compound = 1.001
t = 0.0

[training.logger]
@loggers = "spacy.ConsoleLogger.v1"
progress_bar = false

[training.optimizer]
@optimizers = "Adam.v1"
beta1 = 0.9
beta2 = 0.999
L2_is_weight_decay = true
L2 = 0.01
grad_clip = 1.0
use_averages = false
eps = 0.00000001
learn_rate = 0.001

[training.score_weights]
cats_score = 1.0
cats_micro_p = null
cats_micro_r = null
cats_micro_f = null
cats_macro_p = null
cats_macro_r = null
cats_macro_f = null
cats_macro_auc = null
cats_f_per_type = null
"""
    
    with open(output_path, 'w') as f:
        f.write(config_content)
    
    print(f"✅ Created Intent config: {output_path}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Manually create spaCy config files")
    parser.add_argument("--type", choices=["ner", "intent", "both"], default="both")
    parser.add_argument("--data-dir", default="cyber-train/spacy-training")
    parser.add_argument("--output-dir", default="cyber-train/models/configs")
    
    args = parser.parse_args()
    
    data_dir = Path(args.data_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    if args.type in ["ner", "both"]:
        train_path = data_dir / "entities_train.spacy"
        dev_path = data_dir / "entities_dev.spacy"
        if train_path.exists() and dev_path.exists():
            create_ner_config(
                output_dir / "config_ner.cfg",
                train_path.absolute(),
                dev_path.absolute()
            )
        else:
            print(f"❌ Training files not found: {train_path}, {dev_path}")
    
    if args.type in ["intent", "both"]:
        train_path = data_dir / "intents_train.spacy"
        dev_path = data_dir / "intents_dev.spacy"
        if train_path.exists() and dev_path.exists():
            create_intent_config(
                output_dir / "config_intent.cfg",
                train_path.absolute(),
                dev_path.absolute()
            )
        else:
            print(f"❌ Training files not found: {train_path}, {dev_path}")


